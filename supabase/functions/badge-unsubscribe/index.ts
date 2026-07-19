// Makor: badge-unsubscribe
//
// Public opt-out link placed in badge emails. Verifies a signed token, then
// sets public.user_prefs.badge_emails = false for that reader. Deploy with
// verify_jwt=false (the link is clicked straight from an inbox).

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const SITE_URL = (Deno.env.get("SITE_URL") ?? "https://makor.co.za").replace(/\/+$/, "");

async function sign(userId: string): Promise<string> {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(SERVICE_ROLE), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(userId));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function page(title: string, body: string): Response {
  const html = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title></head>
  <body style="margin:0;background:#F6F3EC;font-family:Arial,Helvetica,sans-serif;color:#0E2A2E;">
    <div style="max-width:480px;margin:60px auto;padding:28px 24px;background:#fff;border:1px solid #E4DDCC;border-radius:14px;text-align:center;">
      <div style="font-family:Georgia,serif;font-size:24px;font-weight:bold;letter-spacing:.03em;">Makor</div>
      <div style="height:3px;width:52px;background:#B8862F;margin:8px auto 20px;"></div>
      <h1 style="font-family:Georgia,serif;font-size:22px;color:#0E2A2E;margin:0 0 10px;">${title}</h1>
      <p style="font-size:15px;color:#566a6a;margin:0 0 20px;">${body}</p>
      <a href="${SITE_URL}/" style="display:inline-block;background:#0F6C6C;color:#fff;text-decoration:none;font-weight:bold;font-size:15px;padding:11px 22px;border-radius:999px;">Back to Makor</a>
    </div>
  </body></html>`;
  return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8" } });
}

Deno.serve(async (req: Request) => {
  const url = new URL(req.url);
  const userId = url.searchParams.get("u") ?? "";
  const token = url.searchParams.get("t") ?? "";
  if (!userId || !token) return page("Link not valid", "This unsubscribe link is missing information. Please use the link from a recent Makor email.");

  const expected = await sign(userId);
  if (token !== expected) return page("Link not valid", "This unsubscribe link could not be verified. Please use the most recent Makor email.");

  const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });
  await admin.from("user_prefs").upsert({ user_id: userId, badge_emails: false, updated_at: new Date().toISOString() }, { onConflict: "user_id" });

  return page("You are unsubscribed", "You will no longer receive an email when you earn a badge. Your progress and badges are still safe on your progress page, and you can turn these emails back on there whenever you like.");
});
