# Makor Edge Functions: badge emails

Two functions power the "email me when I earn a badge" flow. Both are already
deployed to the makor Supabase project. This file records how they are wired so
the setup is not tribal knowledge.

## award-badges

Fired by a database webhook whenever a post-quiz is saved. It recomputes a
reader's badges and title from all their attempts, records new awards in
`public.user_badges` (one row per award, so nothing is emailed twice), and sends
one bundled email via Resend that names the movement just finished and links to
the next uncompleted, published movement (read from `/search-index.json`).

Deployed with `verify_jwt = false`; it authenticates the webhook itself with an
optional shared secret (`WEBHOOK_KEY`).

## badge-unsubscribe

The opt-out link in every email. Verifies a signed token and sets
`public.user_prefs.badge_emails = false`. Deployed with `verify_jwt = false`.

## One-time setup (do these once)

1. Set the secrets on the makor project:

   supabase secrets set RESEND_API_KEY=your_resend_key --project-ref oztgjzncxgobcszcwibp
   supabase secrets set WEBHOOK_KEY=some_long_random_string --project-ref oztgjzncxgobcszcwibp

   Optional overrides (defaults shown):
   supabase secrets set SITE_URL=https://makor.co.za MAIL_FROM="Makor <admin@makor.co.za>"

2. Create the database webhook in the Supabase dashboard:
   Database > Webhooks > Create a new hook
     Table:        public.attempts
     Events:       Insert
     Type:         Supabase Edge Function
     Function:     award-badges
     HTTP headers: add  x-makor-key: <the same WEBHOOK_KEY value>

That is all. New post-quizzes will trigger the email. The function skips sending
if a reader has opted out, and never double-sends an award.

## Analytics pipeline (admin dashboard)

Three more pieces power the admin dashboard's traffic, participation, email, and
attribution views. All are deployed and wired already.

- `public.events` table: first-party analytics store (page views + email events),
  RLS-locked so only the service role reads it.
- `track` function: receives the cookieless page-view beacon from the site
  (added in Base.astro) and writes page_view rows. verify_jwt=false.
- `resend-events` function: receives Resend email webhooks (delivered, opened,
  clicked, bounced, complained) and writes email rows. Authenticated by a token
  in the URL (`?k=`, checked against app_config.resend_webhook_key).
  verify_jwt=false.
- `admin_analytics(p_days)` RPC: admin-gated (same admins check as
  admin_overview), returns traffic, participation, email-by-campaign, and
  attribution as one JSON object. The admin page calls it via
  window.makorAnalytics(days).

Resend open and click tracking are enabled on makor.co.za, and a Resend webhook
points at the resend-events function. Opens and clicks are only captured from
sends made after tracking was turned on.

The only step that still needs a deploy is the site itself (the beacon in
Base.astro and the dashboard in admin.astro). Traffic and participation start
filling in once that ships.

## Redeploying after edits

supabase functions deploy award-badges --no-verify-jwt --project-ref oztgjzncxgobcszcwibp
supabase functions deploy badge-unsubscribe --no-verify-jwt --project-ref oztgjzncxgobcszcwibp
