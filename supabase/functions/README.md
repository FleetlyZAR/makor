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

## Redeploying after edits

supabase functions deploy award-badges --no-verify-jwt --project-ref oztgjzncxgobcszcwibp
supabase functions deploy badge-unsubscribe --no-verify-jwt --project-ref oztgjzncxgobcszcwibp
