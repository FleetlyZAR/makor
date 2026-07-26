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
  "Access-Control-Allow-Headers": "authorization, content-type",
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
  "Non negotiables:",
  "1. Historically orthodox theology, anchored in Scripture. Let the text drive every claim. Christ is the interpretive centre. Keep strict typology discipline; never force a fanciful reading.",
  "2. Scripture spine is the Berean Standard Bible (BSB, public domain). Quote verses accurately in the BSB. Do not use the NIV, ESV, or NLT.",
  "3. Plain, accessible English a working person or a first time reader can follow, warm and reverent, never talking down. This is discipleship, not display.",
  "4. Never use an em dash or an en dash anywhere, in prose or in html. Use commas, colons, semicolons, or clean sentence breaks.",
  "5. Do not invent quotes, URLs, or citations. Do not put the reader's name in unless it is provided.",
  "",
  "Brand and format for the html body:",
  "Colours: Ink #0E2A2E, Water/teal #0F6C6C, Brass #B8862F, on a vellum #F6F3EC background. Use inline styles only (email safe). Center a single column at max width 560px. Open with a serif Makor wordmark and a short brass rule, exactly like Makor's other emails. Use a teal rounded button for the main link. Close with a short italic teal line of Scripture and a small footer that links to " + SITE_URL + "/email-preferences/ so readers can manage their emails.",
  "The main call to action link should point into makor.co.za (the study being featured, or the relevant feature page).",
  "",
  "Return your answer as a single JSON object and nothing else, with exactly these string fields:",
  '{ "subject": "...", "preview_text": "...", "thinking": "...", "html": "...", "txt": "..." }',
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

  // Load the edition from the comms schema (service role, bypasses RLS).
  const { data: ed, error: edErr } = await admin.schema("comms").from("weekly_editions").select("*").eq("id", editionId).maybeSingle();
  if (edErr || !ed) return json({ error: "edition not found" }, 404);

  if (!ANTHROPIC_API_KEY) {
    await admin.schema("comms").from("weekly_editions").update({ status: "error", error: "ANTHROPIC_API_KEY is not set on the function", updated_at: new Date().toISOString() }).eq("id", editionId);
    return json({ ok: false, error: "ANTHROPIC_API_KEY is not set on the function" }, 500);
  }

  await admin.schema("comms").from("weekly_editions").update({ status: "generating", error: null, updated_at: new Date().toISOString() }).eq("id", editionId);

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
  ].join("\n");

  try {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: ANTHROPIC_MODEL,
        max_tokens: 4096,
        system: SYSTEM_PROMPT,
        messages: [{ role: "user", content: userMessage }],
      }),
    });

    if (!res.ok) {
      const detail = await res.text();
      await admin.schema("comms").from("weekly_editions").update({ status: "error", error: `model error ${res.status}: ${detail.slice(0, 500)}`, updated_at: new Date().toISOString() }).eq("id", editionId);
      return json({ ok: false, error: `model error ${res.status}`, detail: detail.slice(0, 500) }, 502);
    }

    const data = await res.json();
    const text: string = (data?.content ?? []).map((b: { type: string; text?: string }) => (b.type === "text" ? b.text ?? "" : "")).join("").trim();

    // The model is asked for a bare JSON object; tolerate stray prose around it.
    let parsed: { subject?: string; preview_text?: string; thinking?: string; html?: string; txt?: string } | null = null;
    try { parsed = JSON.parse(text); }
    catch (_) {
      const s = text.indexOf("{"), e = text.lastIndexOf("}");
      if (s >= 0 && e > s) { try { parsed = JSON.parse(text.slice(s, e + 1)); } catch (_2) { /* below */ } }
    }
    if (!parsed || !parsed.html) {
      await admin.schema("comms").from("weekly_editions").update({ status: "error", error: "could not parse model output as JSON", updated_at: new Date().toISOString() }).eq("id", editionId);
      return json({ ok: false, error: "could not parse model output" }, 502);
    }

    const strip = (s: string | undefined) => String(s ?? "").replace(/[–—]/g, ", ");
    await admin.schema("comms").from("weekly_editions").update({
      subject: strip(parsed.subject),
      preview_text: strip(parsed.preview_text),
      thinking: strip(parsed.thinking),
      html: strip(parsed.html),
      txt: strip(parsed.txt),
      model: ANTHROPIC_MODEL,
      status: "generated",
      error: null,
      generated_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }).eq("id", editionId);

    return json({ ok: true, edition_id: editionId, status: "generated" });
  } catch (e) {
    await admin.schema("comms").from("weekly_editions").update({ status: "error", error: String(e).slice(0, 500), updated_at: new Date().toISOString() }).eq("id", editionId);
    return json({ ok: false, error: String(e) }, 500);
  }
});
