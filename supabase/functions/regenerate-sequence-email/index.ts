// Makor: regenerate-sequence-email
//
// POST { step, instruction }: rewrites one email in the weekly onboarding
//   sequence (comms.sequence_emails) with the model, keeping its purpose and
//   place, applying the editor's instruction, under Makor's discipline. Reads
//   and writes through the service-role bridges (comms is not exposed to REST).
//
// Auth: verify_jwt on, caller must be an admin. Key from ANTHROPIC_API_KEY or
// the anthropic_api_key vault secret. ANTHROPIC_MODEL optional.

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

const SYSTEM_PROMPT = [
  "You are improving one email in Makor's welcome sequence (makor.co.za), a free Christ centred Bible study platform. The email keeps its purpose and its place in the sequence; you are rewriting it, not inventing a new one.",
  "",
  "Non negotiables:",
  "1. Historically orthodox theology, anchored in Scripture, Christ as the interpretive centre. Strict typology discipline.",
  "2. Scripture spine is the Berean Standard Bible (BSB, public domain). Do not use the NIV, ESV, or NLT.",
  "3. Plain, accessible English a working person can follow, warm and reverent, never talking down.",
  "4. Never use an em dash or an en dash anywhere, in prose or in html. Use commas, colons, semicolons, or clean sentence breaks.",
  "5. Do not invent quotes, URLs, or citations.",
  "",
  "Brand and format for the html body: Ink #0E2A2E, Water/teal #0F6C6C, Brass #B8862F, on vellum #F6F3EC. Inline styles only, single column max width 560px, a serif Makor wordmark and brass rule at the top, a teal rounded button for the main link, and a small footer linking to " + SITE_URL + "/email-preferences/.",
  "",
  "Call the emit_email tool exactly once with: subject (no dashes), preview_text (one short line), html (full self contained email), txt (plain text version).",
].join("\n");

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method" }, 405);

  const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });

  const authHeader = req.headers.get("Authorization") ?? "";
  const token = authHeader.replace(/^Bearer\s+/i, "");
  if (!token) return json({ error: "not authorized" }, 401);
  const { data: udata, error: uerr } = await admin.auth.getUser(token);
  const email = udata?.user?.email;
  if (uerr || !email) return json({ error: "not authorized" }, 401);
  const { data: isAdmin } = await admin.from("admins").select("email").eq("email", email).maybeSingle();
  if (!isAdmin) return json({ error: "admins only" }, 403);

  let step: number | null = null;
  let instruction = "";
  try {
    const body = await req.json();
    step = Number(body?.step);
    instruction = String(body?.instruction ?? "");
  } catch (_) { /* handled below */ }
  if (step === null || Number.isNaN(step)) return json({ error: "missing step" }, 400);

  const { data: se, error: seErr } = await admin.rpc("gen_sequence_read", { p_step: step });
  if (seErr || !se) return json({ error: "sequence email not found", detail: seErr?.message }, 404);

  let apiKey = ANTHROPIC_API_KEY;
  if (!apiKey) {
    const { data: vaultKey } = await admin.rpc("gen_get_anthropic_key");
    if (typeof vaultKey === "string" && vaultKey) apiKey = vaultKey;
  }
  if (!apiKey) return json({ ok: false, error: "no anthropic api key" }, 500);

  const userMessage = [
    "Rewrite this welcome sequence email, keeping its purpose and place.",
    "",
    `Current subject: ${se.subject ?? ""}`,
    `Current preview: ${se.preview_text ?? ""}`,
    "",
    "Current html:",
    se.html ?? "",
    "",
    "Editor's instruction:",
    instruction || "(no extra instruction; improve clarity and warmth within the discipline, keep the same intent)",
  ].join("\n");

  try {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": apiKey, "anthropic-version": "2023-06-01", "Content-Type": "application/json" },
      body: JSON.stringify({
        model: ANTHROPIC_MODEL,
        max_tokens: 12000,
        system: SYSTEM_PROMPT,
        tools: [{
          name: "emit_email",
          description: "Return the rewritten sequence email.",
          input_schema: {
            type: "object",
            properties: {
              subject: { type: "string" },
              preview_text: { type: "string" },
              html: { type: "string" },
              txt: { type: "string" },
            },
            required: ["subject", "preview_text", "html", "txt"],
          },
        }],
        tool_choice: { type: "tool", name: "emit_email" },
        messages: [{ role: "user", content: userMessage }],
      }),
    });
    if (!res.ok) {
      const detail = await res.text();
      return json({ ok: false, error: `model error ${res.status}`, detail: detail.slice(0, 500) }, 502);
    }
    const data = await res.json();
    const toolUse = (data?.content ?? []).find((b: { type: string }) => b.type === "tool_use");
    const p = (toolUse?.input ?? null) as { subject?: string; preview_text?: string; html?: string; txt?: string } | null;
    if (!p || !p.html) return json({ ok: false, error: "no content from model" }, 502);

    const strip = (s: string | undefined) => String(s ?? "").replace(/[–—]/g, ", ");
    await admin.rpc("gen_sequence_write", {
      p_step: step, p_subject: strip(p.subject), p_preview: strip(p.preview_text),
      p_html: strip(p.html), p_txt: strip(p.txt),
    });
    return json({ ok: true, step });
  } catch (e) {
    return json({ ok: false, error: String(e) }, 500);
  }
});
