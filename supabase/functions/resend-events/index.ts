// Makor: resend-events
//
// Receives Resend email webhooks (delivered, opened, clicked, bounced,
// complained) and records them in public.events for the admin dashboard.
// Authenticated by a shared token in the query string (?k=...), checked against
// app_config.resend_webhook_key. Deploy with verify_jwt=false.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

const KEEP: Record<string, string> = {
  "email.delivered": "email_delivered",
  "email.opened": "email_opened",
  "email.clicked": "email_clicked",
  "email.bounced": "email_bounced",
  "email.complained": "email_complained",
};

Deno.serve(async (req: Request) => {
  try {
    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });

    // Token check.
    const url = new URL(req.url);
    const given = url.searchParams.get("k") ?? "";
    const { data: crow } = await admin.from("app_config").select("value").eq("key", "resend_webhook_key").maybeSingle();
    const expected = crow?.value ?? "";
    if (!expected || given !== expected) return new Response("forbidden", { status: 403 });

    const ev = await req.json().catch(() => ({}));
    const type = KEEP[ev?.type];
    if (!type) return new Response(JSON.stringify({ skipped: ev?.type }), { headers: { "Content-Type": "application/json" } });

    const d = ev.data ?? {};
    const recipient = Array.isArray(d.to) ? d.to[0] : (typeof d.to === "string" ? d.to : null);
    const link = d.click?.link ?? null;
    const campaign = d.broadcast_id ?? "transactional";
    const label = d.subject ?? null;

    await admin.from("events").insert({
      type,
      campaign,
      label,
      email_id: d.email_id ?? null,
      recipient,
      link,
      created_at: ev.created_at ?? new Date().toISOString(),
    });

    return new Response(JSON.stringify({ ok: true, type }), { headers: { "Content-Type": "application/json" } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 500, headers: { "Content-Type": "application/json" } });
  }
});
