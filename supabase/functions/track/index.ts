// Makor: track
//
// Receives cookieless page-view beacons from the site and writes them to
// public.events via the service role. No secret required (public ingest), but
// it only ever writes a single, sanitized page_view row, so misuse is limited
// to noise. Deploy with verify_jwt=false.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function clip(s: unknown, n: number): string | null {
  if (typeof s !== "string" || !s) return null;
  return s.slice(0, n);
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return new Response("method", { status: 405, headers: cors });
  try {
    const b = await req.json().catch(() => ({}));
    const path = clip(b.p, 300);
    if (!path) return new Response(JSON.stringify({ skipped: "no path" }), { headers: { ...cors, "Content-Type": "application/json" } });

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });
    await admin.from("events").insert({
      type: "page_view",
      path,
      referrer: clip(b.r, 300),
      session_id: clip(b.s, 64),
      user_id: b.u && /^[0-9a-f-]{36}$/i.test(b.u) ? b.u : null,
      is_auth: !!b.a,
    });
    return new Response(JSON.stringify({ ok: true }), { headers: { ...cors, "Content-Type": "application/json" } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 500, headers: { ...cors, "Content-Type": "application/json" } });
  }
});
