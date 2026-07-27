// Makor: generate-weekly-edition
//
// POST { edition_id }: called from the admin dashboard (Sunday email panel).
//   Reads the edition's instruction (the chosen story and the feature to
//   highlight), asks the model to write the Sunday email under Makor's study
//   discipline, and writes subject, preview text, the reasoning ("thinking"),
//   and the html and text bodies back onto the edition row. The dashboard then
//   shows a preview to approve and send.
//
// Auth: verify_jwt is on, and the caller must be an admin (public.admins by
// email). The model call uses ANTHROPIC_API_KEY from the function secrets;
// ANTHROPIC_MODEL is optional and overrides the default model id.
//
// Deploy: supabase functions deploy generate-weekly-edition
// Secrets:  ANTHROPIC_API_KEY (required), ANTHROPIC_MODEL (optional)

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ANTHROPIC_API_KEY = Deno.env.get("ANTHROPIC_API_KEY") ?? "";
const ANTHROPIC_MODEL = Deno.env.get("ANTHROPIC_MODEL") ?? "claude-sonnet-4-5";
const SITE_URL = (Deno.env.get("SITE_URL") ?? "https://makor.co.za").replace(/\/+$/, "");

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(o: unknown, status = 200) {
  return new Response(JSON.stringify(o), { status, headers: { ...cors, "Content-Type": "application/json" } });
}

// The study discipline, distilled for a single weekly email. Kept in step with
// the Makor pipeline: BSB spine, historically orthodox, Christ centred, plain
// accessible English for a young African audience, and no em or en dashes.
const SYSTEM_PROMPT = [
  "You are the writer for Makor, a free Christ centred Bible study platform (makor.co.za). You write one weekly email that goes out on a Sunday.",
  "",
  "Every email does two things: it opens up one story or passage of Scripture, and it warmly points readers to one feature of Makor.",
  "",
  "Editorial posture: lean into the strangeness. Many of these passages are genuinely odd, even unsettling. Do not sand off the weirdness or rush past it. Open by letting the reader feel how strange the text is, name the oddness plainly, and let it create real tension. Then deal with it reverently and carefully, drawing out the deep truth the strangeness is carrying. The weird surface is a door into depth, never a punchline and never mere shock. Hold the tension, then resolve it in Christ.",
  "",
  "Non negotiables:",
  "1. Historically orthodox theology, anchored in Scripture. Let the text drive every claim. Christ is the interpretive centre. Keep strict typology discipline; never force a fanciful reading.",
  "2. Scripture spine is the Berean Standard Bible (BSB, public domain). Quote verses accurately in the BSB. Do not use the NIV, ESV, or NLT.",
  "3. Plain, accessible English a working person or a first time reader can follow, warm and reverent, never talking down. This is discipleship, not display.",
  "4. Never use an em dash or an en dash anywhere, in prose or in html. Use commas, colons, semicolons, or clean sentence breaks.",
  "5. Do not invent quotes, URLs, or citations.",
  "",
  "Brand and format for the html body: you will be given the html of an existing Makor email as the house template. Reproduce its exact structure and inline styling, the header wordmark panel, the colours, the fonts, the teal rounded button, and the footer. Change only the body content to this week's email. Keep it email safe with inline styles only, single column, max width 560px.",
  "You may greet the reader with the literal token {{first_name}} exactly as the house template does; the sender fills it in. The main call to action link should point into makor.co.za (the study being featured, or the relevant feature page).",
  "",
  "Call the emit_edition tool exactly once with the finished email in these fields:",
  "subject: a compelling, honest subject line, no dashes.",
  "preview_text: one short preheader line.",
  "thinking: a few short paragraphs explaining the passage you chose to draw out, the redemptive and Christ centred thread, and why you framed the feature the way you did, so the editor can judge it before sending. Plain text, no dashes.",
  "html: the full email body as one self contained html string with inline styles.",
  "txt: a plain text version of the same email, no html.",
].join("\n");

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method" }, 405);

  const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });

  // Caller must be a signed in admin.
  const authHeader = req.headers.get("Authorization") ?? "";
  const token = authHeader.replace(/^Bearer\s+/i, "");
  if (!token) return json({ error: "not authorized" }, 401);
  const { data: udata, error: uerr } = await admin.auth.getUser(token);
  const email = udata?.user?.email;
  if (uerr || !email) return json({ error: "not authorized" }, 401);
  const { data: isAdmin } = await admin.from("admins").select("email").eq("email", email).maybeSingle();
  if (!isAdmin) return json({ error: "admins only" }, 403);

  let editionId: number | null = null;
  try {
    const body = await req.json();
    editionId = Number(body?.edition_id);
  } catch (_) { /* handled below */ }
  if (!editionId) return json({ error: "missing edition_id" }, 400);

  // comms is not exposed to PostgREST, so read and write it through the
  // service-role-only bridge functions in public.
  const write = (f: Record<string, string | null>) => admin.rpc("gen_edition_write", {
    p_id: editionId, p_subject: f.subject ?? null, p_preview: f.preview_text ?? null,
    p_thinking: f.thinking ?? null, p_html: f.html ?? null, p_txt: f.txt ?? null,
    p_model: f.model ?? null, p_status: f.status ?? null, p_error: f.error ?? null,
  });

  const { data: ed, error: edErr } = await admin.rpc("gen_edition_read", { p_id: editionId });
  if (edErr || !ed) return json({ error: "edition not found", detail: edErr?.message }, 404);

  // Key from the function env, or fall back to the vault (set in the database).
  let apiKey = ANTHROPIC_API_KEY;
  if (!apiKey) {
    const { data: vaultKey } = await admin.rpc("gen_get_anthropic_key");
    if (typeof vaultKey === "string" && vaultKey) apiKey = vaultKey;
  }
  if (!apiKey) {
    await write({ status: "error", error: "No Anthropic API key found in the function env or the vault" });
    return json({ ok: false, error: "no anthropic api key" }, 500);
  }

  await write({ status: "generating", error: null });

  const { data: template } = await admin.rpc("gen_email_template");

  const userMessage = [
    "Write this Sunday's Makor email.",
    "",
    "Featured story or passage:",
    `  Title: ${ed.story_title ?? "(choose a fitting title)"}`,
    `  Reference: ${ed.story_ref ?? "(none given, pick a fitting passage)"}`,
    `  Study link: ${ed.story_slug ? `${SITE_URL}/${ed.story_slug}/` : "(link to the most fitting page on makor.co.za)"}`,
    "",
    "Feature to highlight:",
    `  ${ed.feature_label || ed.feature_key || "(choose the most helpful Makor feature to point to)"}`,
    "",
    "Editor's instruction:",
    `  ${ed.instruction || "(no extra instruction; use your judgement within the discipline)"}`,
    "",
    "House template to match exactly. Reproduce its header, colours, fonts, button, and footer; change only the body to this week's email:",
    typeof template === "string" && template ? template : "(no template available; follow the brand description above)",
  ].join("\n");

  try {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: ANTHROPIC_MODEL,
        max_tokens: 12000,
        system: SYSTEM_PROMPT,
        tools: [{
          name: "emit_edition",
          description: "Return the finished Sunday email.",
          input_schema: {
            type: "object",
            properties: {
              subject: { type: "string" },
              preview_text: { type: "string" },
              thinking: { type: "string" },
              html: { type: "string" },
              txt: { type: "string" },
            },
            required: ["subject", "preview_text", "thinking", "html", "txt"],
          },
        }],
        tool_choice: { type: "tool", name: "emit_edition" },
        messages: [{ role: "user", content: userMessage }],
      }),
    });

    if (!res.ok) {
      const detail = await res.text();
      await write({ status: "error", error: `model error ${res.status}: ${detail.slice(0, 500)}` });
      return json({ ok: false, error: `model error ${res.status}`, detail: detail.slice(0, 500) }, 502);
    }

    // Structured tool output: the fields arrive as a real object, no parsing.
    const data = await res.json();
    const toolUse = (data?.content ?? []).find((b: { type: string }) => b.type === "tool_use");
    const parsed = (toolUse?.input ?? null) as { subject?: string; preview_text?: string; thinking?: string; html?: string; txt?: string } | null;
    if (!parsed || !parsed.html) {
      await write({ status: "error", error: "model returned no email content" });
      return json({ ok: false, error: "no content from model" }, 502);
    }

    const strip = (s: string | undefined) => String(s ?? "").replace(/[–—]/g, ", ");
    await write({
      subject: strip(parsed.subject),
      preview_text: strip(parsed.preview_text),
      thinking: strip(parsed.thinking),
      html: strip(parsed.html),
      txt: strip(parsed.txt),
      model: ANTHROPIC_MODEL,
      status: "generated",
      error: null,
    });

    return json({ ok: true, edition_id: editionId, status: "generated" });
  } catch (e) {
    await write({ status: "error", error: String(e).slice(0, 500) });
    return json({ ok: false, error: String(e) }, 500);
  }
});
