// Makor: notify-group-invite
//
// POST: triggered by a database trigger on INSERT into public.group_members.
//   Emails the invited reader that a friend has asked them to join a reading
//   group, unless they have turned group invite emails off in user_prefs.
// GET ?u=<userId>&t=<hmac>: one-click opt out of group invite emails
//   (used by the List-Unsubscribe header and the email footer).
//
// Auth: shared secret in x-makor-key (app_config.webhook_key), same pattern
// as notify-friend-request, so deploy with verify_jwt=false.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const SITE_URL = (Deno.env.get("SITE_URL") ?? "https://makor.co.za").replace(/\/+$/, "");
const MAIL_FROM = Deno.env.get("MAIL_FROM") ?? "Makor <admin@makor.co.za>";
const FUNCTIONS_BASE = SUPABASE_URL.replace(".supabase.co", ".functions.supabase.co");

function esc(s: string): string {
  return String(s ?? "").replace(/[&<>\"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c] as string));
}
function json(o: unknown, status = 200) {
  return new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json" } });
}
async function sign(userId: string): Promise<string> {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(SERVICE_ROLE), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(userId));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

const ORDER_LABEL: Record<string, string> = { multitrack: "Multi-track", canonical: "Canonical", chronological: "Chronological" };

Deno.serve(async (req: Request) => {
  const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });

  // One-click opt out.
  if (req.method === "GET" || req.method === "POST" && new URL(req.url).searchParams.get("u")) {
    const url = new URL(req.url);
    const u = url.searchParams.get("u") ?? "";
    const t = url.searchParams.get("t") ?? "";
    if (u && t && t === (await sign(u))) {
      await admin.from("user_prefs").upsert({ user_id: u, group_invite_emails: false, updated_at: new Date().toISOString() });
      return new Response(
        `<!doctype html><html><body style=\"font-family:Georgia,serif;background:#F6F3EC;color:#0E2A2E;padding:40px 20px;text-align:center;\">` +
        `<h1 style=\"font-size:26px;\">You will no longer receive group invite emails.</h1>` +
        `<p style=\"color:#566a6a;\">You can turn them back on any time at <a href=\"${SITE_URL}/email-preferences/\" style=\"color:#0F6C6C;\">makor.co.za/email-preferences</a>.</p>` +
        `</body></html>`,
        { headers: { "Content-Type": "text/html; charset=utf-8" } },
      );
    }
    if (req.method === "GET") return new Response("invalid link", { status: 400 });
  }

  try {
    const body = await req.json().catch(() => ({}));
    const record = body.record ?? body;
    const groupId = record?.group_id;
    const invitee: string | undefined = record?.user_id;
    const inviter: string | undefined = record?.invited_by;
    if (!groupId || !invitee) return json({ skipped: "missing ids" });
    if (record?.status && record.status !== "invited") return json({ skipped: "not a pending invite" });

    // Secrets from app_config; env overrides.
    const cfg: Record<string, string> = {};
    try {
      const { data: crows } = await admin.from("app_config").select("key,value");
      for (const r of (crows ?? []) as { key: string; value: string }[]) cfg[r.key] = r.value;
    } catch (_) { /* optional */ }
    const resendKey = Deno.env.get("RESEND_API_KEY") || cfg["resend_api_key"] || "";
    const webhookKey = Deno.env.get("WEBHOOK_KEY") || cfg["webhook_key"] || "";

    if (webhookKey) {
      const given = req.headers.get("x-makor-key") ?? "";
      if (given !== webhookKey) return new Response("forbidden", { status: 403 });
    }

    // Respect the opt out.
    const { data: prefs } = await admin.from("user_prefs").select("group_invite_emails").eq("user_id", invitee).maybeSingle();
    if (prefs && prefs.group_invite_emails === false) return json({ ok: true, emailed: false, reason: "opted out" });

    // The group and its plan template.
    const { data: g } = await admin
      .from("groups")
      .select("id, start_date, meet_link, plan_templates(name, plan_order, years, cadence)")
      .eq("id", groupId)
      .maybeSingle();
    if (!g) return json({ ok: true, emailed: false, reason: "group gone" });
    const tpl = (g as { plan_templates?: { name?: string; plan_order?: string; years?: number; cadence?: string } }).plan_templates ?? {};
    const planName = (tpl.name || "a reading plan").trim();
    const pace = `${ORDER_LABEL[tpl.plan_order ?? ""] || tpl.plan_order || ""}, ${tpl.years ?? 1} year${(tpl.years ?? 1) > 1 ? "s" : ""}, ${tpl.cadence === "weekday" ? "weekdays" : "every day"}`;

    // Who is inviting, and who receives.
    const { data: rp } = inviter
      ? await admin.from("profiles").select("display_name").eq("id", inviter).maybeSingle()
      : { data: null };
    const inviterName = (rp?.display_name || "A fellow reader").trim();
    const { data: u } = await admin.auth.admin.getUserById(invitee);
    const to = u?.user?.email;
    if (!to) return json({ ok: true, emailed: false, reason: "no email" });
    const firstName = (u?.user?.user_metadata?.full_name || u?.user?.user_metadata?.name || "").split(" ")[0] || "";

    const token = await sign(invitee);
    const unsubUrl = `${FUNCTIONS_BASE}/notify-group-invite?u=${invitee}&t=${token}`;
    const prefsUrl = `${SITE_URL}/email-preferences/`;
    const respondUrl = `${SITE_URL}/groups/`;

    const greeting = firstName ? `Dear ${esc(firstName)},` : "Dear reader,";
    const subject = `${inviterName} invited you to read the Bible together on Makor`;

    const html = `<!doctype html><html><body style=\"margin:0;background:#F6F3EC;\">
  <div style=\"max-width:560px;margin:0 auto;padding:28px 22px;font-family:Arial,Helvetica,sans-serif;color:#0E2A2E;\">
    <div style=\"font-family:Georgia,serif;font-size:24px;font-weight:bold;letter-spacing:.03em;color:#0E2A2E;\">Makor</div>
    <div style=\"height:3px;width:52px;background:#B8862F;margin:8px 0 20px;\"></div>
    <p style=\"font-size:16px;margin:0 0 6px;\">${greeting}</p>
    <p style=\"font-size:16px;color:#566a6a;margin:0 0 18px;\">Grace to you. Though one may be overpowered, two can defend themselves. A cord of three strands is not quickly broken. (Ecclesiastes 4:12)</p>
    <div style=\"background:#ffffff;border:1px solid #E4DDCC;border-radius:12px;padding:20px 22px;margin:0 0 20px;\">
      <div style=\"font-family:Georgia,serif;font-size:20px;color:#0E2A2E;margin:0 0 6px;\"><strong>${esc(inviterName)}</strong> has invited you to a Makor reading group.</div>
      <div style=\"font-family:Georgia,serif;font-size:16px;color:#0F6C6C;margin:0 0 8px;\">${esc(planName)}</div>
      <div style=\"font-size:14px;color:#566a6a;\">${esc(pace)}, starting ${esc(String(g.start_date))}. You read the same passages at the same times${g.meet_link ? ", with a group video call to talk them through" : ""}, and each sitting lands on your calendar.</div>
    </div>
    <a href=\"${respondUrl}\" style=\"display:inline-block;background:#0F6C6C;color:#ffffff;text-decoration:none;font-family:Arial,sans-serif;font-weight:bold;font-size:15px;padding:12px 22px;border-radius:999px;\">See the invitation</a>
    <p style=\"font-size:13px;color:#566a6a;margin:14px 0 0;\">Joining is your choice. Accept on Makor and the plan is yours to add to your calendar.</p>
    <p style=\"font-family:Georgia,serif;font-style:italic;color:#0F6C6C;font-size:15px;margin:26px 0 0;\">In Your light we see light. (Psalm 36:9)</p>
    <hr style=\"border:none;border-top:1px solid #E4DDCC;margin:24px 0 12px;\">
    <p style=\"font-size:12px;color:#8a9a9a;margin:0;\">You are receiving this because someone invited you to a reading group on Makor. <a href=\"${unsubUrl}\" style=\"color:#0F6C6C;\">Turn these emails off</a>, or <a href=\"${prefsUrl}\" style=\"color:#0F6C6C;\">manage all your email preferences</a>.</p>
  </div></body></html>`;

    const text = [
      greeting, "",
      "Grace to you. Though one may be overpowered, two can defend themselves. A cord of three strands is not quickly broken. (Ecclesiastes 4:12)", "",
      `${inviterName} has invited you to a Makor reading group: ${planName} (${pace}), starting ${g.start_date}. You read the same passages at the same times${g.meet_link ? ", with a group video call" : ""}, and each sitting lands on your calendar.`, "",
      `See the invitation: ${respondUrl}`, "",
      "Joining is your choice. Accept on Makor and the plan is yours to add to your calendar.", "",
      "In Your light we see light. (Psalm 36:9)", "",
      `Turn these emails off: ${unsubUrl}`,
      `Manage all your email preferences: ${prefsUrl}`,
    ].join("\n");

    if (!resendKey) return json({ ok: true, emailed: false, reason: "no resend key" });
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${resendKey}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: MAIL_FROM, to, subject, html, text,
        headers: { "List-Unsubscribe": `<${unsubUrl}>`, "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" },
      }),
    });
    if (!res.ok) return json({ ok: true, emailed: false, resend_status: res.status, resend_body: await res.text() });
    return json({ ok: true, emailed: true });
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
