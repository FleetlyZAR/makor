// Makor: award-badges
//
// Triggered by a Supabase database webhook on INSERT into public.attempts.
// When a reader submits a post-quiz, this recomputes their badges and title
// from all their attempts, records any newly earned ones in public.user_badges,
// and sends one bundled email (via Resend) that names the movement they just
// finished and points them to the next one.
//
// Idempotency: user_badges has a composite primary key (user_id, badge_key),
// so an award is only ever inserted, and therefore only ever emailed, once.
//
// Env required:
//   SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY  (injected by Supabase)
//   RESEND_API_KEY                           (set this as a secret)
//   SITE_URL      default https://makor.co.za
//   MAIL_FROM     default "Makor <admin@makor.co.za>"
//   WEBHOOK_KEY   optional shared secret the webhook must send as x-makor-key
//
// This function does its own auth (webhook secret), so deploy with verify_jwt=false.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") ?? "";
const SITE_URL = (Deno.env.get("SITE_URL") ?? "https://makor.co.za").replace(/\/+$/, "");
const MAIL_FROM = Deno.env.get("MAIL_FROM") ?? "Makor <admin@makor.co.za>";
const WEBHOOK_KEY = Deno.env.get("WEBHOOK_KEY") ?? "";
const FUNCTIONS_BASE = SUPABASE_URL.replace(".supabase.co", ".functions.supabase.co");

type Attempt = { study_slug: string; book: string | null; title: string | null; phase: string; score: number; created_at: string };
type IndexEntry = { book: string; bookSlug: string; title: string; ref: string; slug: string; order: number; url: string; available: boolean };

const TORAH = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"];
const GOSPELS = ["Matthew", "Mark", "Luke", "John"];
const GROWTH_THRESHOLD = 25;

// Display metadata. Keys without a book suffix are one-time; scroll-sealed and
// treasure-old-and-new are awarded per book (key ends with :bookSlug).
const BADGE_META: Record<string, { name: string; verse: string; line: string }> = {
  "first-light": { name: "First Light", verse: "Genesis 1:3", line: "You have taken the first step into the Word. Let there be light, and there was light." },
  "both-testaments": { name: "Both Testaments", verse: "One story, two testaments", line: "You have now walked in both the Old and the New. They tell one story, and it is His." },
  "foundations": { name: "Foundations", verse: "Genesis to Deuteronomy", line: "You have finished the five books of the Torah, the bedrock the rest of Scripture is built upon." },
  "fourfold-witness": { name: "The Fourfold Witness", verse: "The four Gospels", line: "Four witnesses, one Christ. You have read Matthew, Mark, Luke, and John to the end." },
  "whole-counsel": { name: "The Whole Counsel", verse: "Acts 20:27", line: "You have received the whole counsel of God, every movement of every book. Well done." },
  "daily-bread": { name: "Daily Bread", verse: "Matthew 6:11", line: "Seven days in a row in the Word. Give us this day our daily bread, and you have." },
  "morning-by-morning": { name: "Morning by Morning", verse: "Lamentations 3:23", line: "Thirty days unbroken. His mercies are new every morning, and so is your reading." },
  "faithful-in-little": { name: "Faithful in Little", verse: "Luke 16:10", line: "A hundred days in the Word. Faithful in little, and being made faithful in much." },
  "rightly-dividing": { name: "Rightly Dividing", verse: "2 Timothy 2:15", line: "Full marks on a knowledge check. A worker who has no need to be ashamed." },
  "growth-shown": { name: "Growth Shown", verse: "Before and after", line: "You scored far higher after the study than before it. This is the whole point: growth." },
};
function badgeName(key: string): { name: string; verse: string; line: string; book?: string } {
  if (key.startsWith("scroll-sealed:")) return { name: "Scroll Sealed", verse: "A finished book", line: "You have finished every movement of a whole book of the Bible.", book: key.split(":")[1] };
  if (key.startsWith("treasure-old-and-new:")) return { name: "Treasure Old and New", verse: "Matthew 13:52", line: "Full marks across an entire book. You bring out treasure new and old.", book: key.split(":")[1] };
  return BADGE_META[key] ?? { name: key, verse: "", line: "" };
}

const TIERS = [
  { key: "tier:1", name: "Berean", line: "You examine the Scriptures daily, like the noble Bereans who received the word with eagerness." },
  { key: "tier:2", name: "Disciple", line: "You have settled into the way of a learner and a follower." },
  { key: "tier:3", name: "Steward of the Word", line: "You have been entrusted with much, and you are handling it with care." },
  { key: "tier:4", name: "Workman", line: "You have a deep, tested familiarity with most of Scripture." },
  { key: "tier:5", name: "Discipled Scribe", line: "Every scribe trained for the kingdom brings out of his treasure what is new and old. You have finished the whole Bible." },
];

function esc(s: string): string {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c] as string));
}

async function sign(userId: string): Promise<string> {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(SERVICE_ROLE), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(userId));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

Deno.serve(async (req: Request) => {
  try {
    const body = await req.json().catch(() => ({}));
    const record = body.record ?? body;
    const userId: string | undefined = record?.user_id;
    if (!userId) return json({ skipped: "no user_id" });
    if (record?.phase && record.phase !== "post") return json({ skipped: "not a post attempt" });

    const admin = createClient(SUPABASE_URL, SERVICE_ROLE, { auth: { persistSession: false } });

    // Secrets live in the private app_config table; env vars override if present.
    const cfg: Record<string, string> = {};
    try {
      const { data: crows } = await admin.from("app_config").select("key,value");
      for (const r of (crows ?? []) as { key: string; value: string }[]) cfg[r.key] = r.value;
    } catch (_) { /* config table optional */ }
    const resendKey = RESEND_API_KEY || cfg["resend_api_key"] || "";
    const webhookKey = WEBHOOK_KEY || cfg["webhook_key"] || "";

    // Webhook auth: require the shared key if one is configured.
    if (webhookKey) {
      const given = req.headers.get("x-makor-key") ?? (req.headers.get("authorization") ?? "").replace(/^Bearer\s+/i, "");
      if (given !== webhookKey) return new Response("forbidden", { status: 403 });
    }

    // 1. All of this reader's attempts.
    const { data: attempts } = await admin.from("attempts").select("study_slug,book,title,phase,score,created_at").eq("user_id", userId);
    const rows: Attempt[] = attempts ?? [];

    // 2. The canon-ordered movement index (also tells us what is published).
    const idx: IndexEntry[] = await fetch(`${SITE_URL}/search-index.json`).then((r) => r.json()).catch(() => []);
    const total = idx.length || 1354;
    const bySlug: Record<string, IndexEntry[]> = {};
    const byKey: Record<string, IndexEntry> = {};
    const plannedByBook: Record<string, number> = {};
    for (const e of idx) {
      (bySlug[e.slug] ||= []).push(e);
      byKey[e.book + "||" + e.slug] = e;
      plannedByBook[e.book] = (plannedByBook[e.book] ?? 0) + 1;
    }
    const resolveBook = (a: Attempt): string | null => {
      if (a.book) return a.book;
      const hits = bySlug[a.study_slug];
      return hits && hits.length === 1 ? hits[0].book : null;
    };

    // 3. Compute state.
    const postByBook: Record<string, Set<string>> = {};
    const scores: Record<string, { pre?: number; post?: number }> = {};
    const dayset = new Set<string>();
    let firstPostDate = "";
    let hasPerfect = false;
    let bestLift = 0;
    let lastPost: { book: string; slug: string; at: string } | null = null;

    for (const a of rows) {
      const book = resolveBook(a);
      if (!book) continue;
      const key = book + "||" + a.study_slug;
      scores[key] ||= {};
      if (a.phase === "pre") scores[key].pre = a.score;
      if (a.phase === "post") {
        scores[key].post = a.score;
        (postByBook[book] ||= new Set()).add(a.study_slug);
        if (!firstPostDate || a.created_at < firstPostDate) firstPostDate = a.created_at;
        if (a.score >= 100) hasPerfect = true;
        const d = new Date(a.created_at);
        dayset.add(d.getUTCFullYear() + "-" + (d.getUTCMonth() + 1) + "-" + d.getUTCDate());
        if (!lastPost || a.created_at > lastPost.at) lastPost = { book, slug: a.study_slug, at: a.created_at };
      }
    }
    for (const key of Object.keys(scores)) {
      const s = scores[key];
      if (typeof s.pre === "number" && typeof s.post === "number") bestLift = Math.max(bestLift, s.post - s.pre);
    }

    let totalCompleted = 0;
    const completedBooks: string[] = [];
    for (const book of Object.keys(postByBook)) {
      const done = postByBook[book].size;
      totalCompleted += done;
      const planned = plannedByBook[book] ?? 0;
      if (planned && done >= planned) completedBooks.push(book);
    }

    const perfectBooks: string[] = [];
    for (const book of completedBooks) {
      const planned = plannedByBook[book] ?? 0;
      let perfect = 0;
      for (const e of idx) if (e.book === book) { const s = scores[book + "||" + e.slug]; if (s && (s.post ?? 0) >= 100) perfect++; }
      if (planned && perfect >= planned) perfectBooks.push(book);
    }

    // Streaks.
    const days = [...dayset].map((k) => { const [y, m, d] = k.split("-").map(Number); return Date.UTC(y, m - 1, d); }).sort((a, b) => a - b);
    const activeDays = days.length;
    let longestStreak = days.length ? 1 : 0, run = days.length ? 1 : 0;
    for (let i = 1; i < days.length; i++) {
      const diff = Math.round((days[i] - days[i - 1]) / 86400000);
      if (diff === 1) run++; else if (diff > 1) run = 1;
      if (run > longestStreak) longestStreak = run;
    }

    // Tier.
    const tierMins = [0, 1, Math.ceil(total * 0.15), Math.ceil(total * 0.40), Math.ceil(total * 0.70), total];
    let tierIndex = 0;
    for (let i = 0; i < tierMins.length; i++) if (totalCompleted >= tierMins[i]) tierIndex = i;

    // 4. Which badges are earned right now.
    const earned = new Set<string>();
    if (totalCompleted >= 1) earned.add("first-light");
    for (const b of completedBooks) earned.add("scroll-sealed:" + slugify(b));
    if (completedBooks.some((b) => testamentOf(b, idx) === "Old") && completedBooks.some((b) => testamentOf(b, idx) === "New")) earned.add("both-testaments");
    if (TORAH.every((b) => completedBooks.includes(b))) earned.add("foundations");
    if (GOSPELS.every((b) => completedBooks.includes(b))) earned.add("fourfold-witness");
    if (totalCompleted >= total) earned.add("whole-counsel");
    if (longestStreak >= 7) earned.add("daily-bread");
    if (longestStreak >= 30) earned.add("morning-by-morning");
    if (activeDays >= 100) earned.add("faithful-in-little");
    if (hasPerfect) earned.add("rightly-dividing");
    if (bestLift >= GROWTH_THRESHOLD) earned.add("growth-shown");
    for (const b of perfectBooks) earned.add("treasure-old-and-new:" + slugify(b));
    for (let i = 1; i <= tierIndex; i++) earned.add("tier:" + i);

    // 5. Diff against the ledger.
    const { data: existingRows } = await admin.from("user_badges").select("badge_key").eq("user_id", userId);
    const existing = new Set((existingRows ?? []).map((r: { badge_key: string }) => r.badge_key));
    const toAward = [...earned].filter((k) => !existing.has(k));
    if (toAward.length === 0) return json({ ok: true, new: 0 });

    await admin.from("user_badges").upsert(toAward.map((k) => ({ user_id: userId, badge_key: k })), { onConflict: "user_id,badge_key", ignoreDuplicates: true });

    // 6. Respect opt-out.
    const { data: prefs } = await admin.from("user_prefs").select("badge_emails").eq("user_id", userId).maybeSingle();
    if (prefs && prefs.badge_emails === false) return json({ ok: true, new: toAward.length, emailed: false, reason: "opted out" });

    // 7. Recipient.
    const { data: u } = await admin.auth.admin.getUserById(userId);
    const to = u?.user?.email;
    if (!to) return json({ ok: true, new: toAward.length, emailed: false, reason: "no email" });
    const firstName = (u?.user?.user_metadata?.full_name || u?.user?.user_metadata?.name || "").split(" ")[0] || "";

    // 8. What did they just finish, and what is next.
    let lastLine = "";
    if (lastPost) {
      const e = byKey[lastPost.book + "||" + lastPost.slug];
      lastLine = e ? `You have just finished ${e.title} in ${e.book}.` : "";
    }
    const postSet = new Set<string>();
    for (const book of Object.keys(postByBook)) for (const slug of postByBook[book]) postSet.add(book + "||" + slug);
    const next = pickNext(idx, postSet, lastPost ? lastPost.book + "||" + lastPost.slug : null);

    // 9. Build and send the bundled email.
    const newTierKeys = toAward.filter((k) => k.startsWith("tier:")).map((k) => parseInt(k.split(":")[1], 10)).sort((a, b) => b - a);
    const newTier = newTierKeys.length ? TIERS[newTierKeys[0] - 1] : null;
    const newBadges = toAward.filter((k) => !k.startsWith("tier:"));

    const token = await sign(userId);
    const unsubUrl = `${FUNCTIONS_BASE}/badge-unsubscribe?u=${userId}&t=${token}`;
    const email = buildEmail({ firstName, newBadges, newTier, lastLine, next, unsubUrl });

    if (resendKey) {
      const res = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: { Authorization: `Bearer ${resendKey}`, "Content-Type": "application/json" },
        body: JSON.stringify({ from: MAIL_FROM, to, subject: email.subject, html: email.html, text: email.text, headers: { "List-Unsubscribe": `<${unsubUrl}>`, "List-Unsubscribe-Post": "List-Unsubscribe=One-Click" } }),
      });
      if (!res.ok) return json({ ok: true, new: toAward.length, emailed: false, resend_status: res.status, resend_body: await res.text() });
    }

    return json({ ok: true, new: toAward.length, emailed: !!resendKey, subject: email.subject });
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});

function json(o: unknown, status = 200) {
  return new Response(JSON.stringify(o), { status, headers: { "Content-Type": "application/json" } });
}
function slugify(s: string) { return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""); }
function testamentOf(book: string, idx: IndexEntry[]): string {
  const e = idx.find((x) => x.book === book);
  // Fall back to canon position if needed.
  return e ? (GOSPELS.includes(book) || isNewTestament(book) ? "New" : "Old") : "Old";
}
function isNewTestament(book: string): boolean {
  const nt = ["Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"];
  return nt.includes(book);
}
function pickNext(idx: IndexEntry[], postSet: Set<string>, lastKey: string | null): IndexEntry | null {
  const pos = lastKey ? idx.findIndex((e) => e.book + "||" + e.slug === lastKey) : -1;
  for (let i = pos + 1; i < idx.length; i++) { const e = idx[i]; if (e.available && !postSet.has(e.book + "||" + e.slug)) return e; }
  for (let i = 0; i < idx.length; i++) { const e = idx[i]; if (e.available && !postSet.has(e.book + "||" + e.slug)) return e; }
  return null;
}

function buildEmail(o: { firstName: string; newBadges: string[]; newTier: { name: string; line: string } | null; lastLine: string; next: IndexEntry | null; unsubUrl: string }) {
  const greeting = o.firstName ? `Dear ${esc(o.firstName)},` : "Dear reader,";
  const subject = o.newTier
    ? `You are now a ${o.newTier.name}`
    : o.newBadges.length === 1
      ? `You earned ${badgeName(o.newBadges[0]).name}`
      : `You earned ${o.newBadges.length} new badges`;

  const badgeRows = o.newBadges.map((k) => {
    const b = badgeName(k);
    const title = b.book ? `${b.name}: ${b.book}` : b.name;
    return `<tr><td style="padding:10px 0;border-bottom:1px solid #E4DDCC;">
      <div style="font-family:Georgia,serif;font-size:18px;color:#0E2A2E;font-weight:bold;">${esc(title)}</div>
      <div style="font-size:12px;color:#B8862F;font-weight:bold;letter-spacing:.02em;">${esc(b.verse)}</div>
      <div style="font-size:14px;color:#566a6a;margin-top:3px;">${esc(b.line)}</div>
    </td></tr>`;
  }).join("");

  const tierBlock = o.newTier ? `
    <div style="background:#0E2A2E;border-radius:12px;padding:20px 22px;margin:0 0 20px;color:#eaf4f3;">
      <div style="font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8fc0bf;">A new title</div>
      <div style="font-family:Georgia,serif;font-size:26px;color:#e6c168;margin:4px 0 6px;">You are now a ${esc(o.newTier.name)}</div>
      <div style="font-size:14px;color:#bcd6d5;">${esc(o.newTier.line)}</div>
    </div>` : "";

  const nextBlock = o.next ? `
    <div style="margin:22px 0 6px;">
      ${o.lastLine ? `<p style="font-size:15px;color:#0E2A2E;margin:0 0 10px;">${esc(o.lastLine)} Keep the flame going.</p>` : ""}
      <p style="font-size:15px;color:#566a6a;margin:0 0 14px;">Your next step is <strong style="color:#0E2A2E;">${esc(o.next.title)}</strong> (${esc(o.next.ref)}).</p>
      <a href="${SITE_URL}${o.next.url}" style="display:inline-block;background:#0F6C6C;color:#ffffff;text-decoration:none;font-family:Arial,sans-serif;font-weight:bold;font-size:15px;padding:12px 22px;border-radius:999px;">Continue: ${esc(o.next.title)}</a>
    </div>` : `
    <div style="margin:22px 0 6px;">
      <a href="${SITE_URL}/" style="display:inline-block;background:#0F6C6C;color:#ffffff;text-decoration:none;font-family:Arial,sans-serif;font-weight:bold;font-size:15px;padding:12px 22px;border-radius:999px;">Continue on Makor</a>
    </div>`;

  const html = `<!doctype html><html><body style="margin:0;background:#F6F3EC;">
  <div style="max-width:560px;margin:0 auto;padding:28px 22px;font-family:Arial,Helvetica,sans-serif;color:#0E2A2E;">
    <div style="font-family:Georgia,serif;font-size:24px;font-weight:bold;letter-spacing:.03em;color:#0E2A2E;">Makor</div>
    <div style="height:3px;width:52px;background:#B8862F;margin:8px 0 20px;"></div>
    <p style="font-size:16px;margin:0 0 6px;">${greeting}</p>
    <p style="font-size:16px;color:#566a6a;margin:0 0 18px;">Grace to you. Your faithfulness in the Word has borne fruit worth marking.</p>
    ${tierBlock}
    ${o.newBadges.length ? `<div style="font-family:Georgia,serif;font-size:18px;color:#0E2A2E;margin:0 0 6px;">${o.newBadges.length === 1 ? "A new badge" : "New badges"}</div><table style="width:100%;border-collapse:collapse;">${badgeRows}</table>` : ""}
    ${nextBlock}
    <p style="font-family:Georgia,serif;font-style:italic;color:#0F6C6C;font-size:15px;margin:26px 0 0;">In Your light we see light. (Psalm 36:9)</p>
    <hr style="border:none;border-top:1px solid #E4DDCC;margin:24px 0 12px;">
    <p style="font-size:12px;color:#8a9a9a;margin:0;">You are receiving this because you are growing in the Word on Makor. If you would rather not be told when you earn a badge, <a href="${o.unsubUrl}" style="color:#0F6C6C;">turn these emails off</a>.</p>
  </div></body></html>`;

  const textLines: string[] = [greeting, "", "Grace to you. Your faithfulness in the Word has borne fruit worth marking.", ""];
  if (o.newTier) textLines.push(`New title: You are now a ${o.newTier.name}. ${o.newTier.line}`, "");
  for (const k of o.newBadges) { const b = badgeName(k); textLines.push(`Badge: ${b.book ? b.name + ": " + b.book : b.name} (${b.verse}). ${b.line}`); }
  if (o.newBadges.length) textLines.push("");
  if (o.lastLine) textLines.push(o.lastLine);
  if (o.next) textLines.push(`Your next step is ${o.next.title} (${o.next.ref}): ${SITE_URL}${o.next.url}`);
  else textLines.push(`Continue on Makor: ${SITE_URL}/`);
  textLines.push("", "In Your light we see light. (Psalm 36:9)", "", `Turn these emails off: ${o.unsubUrl}`);

  return { subject, html, text: textLines.join("\n") };
}
