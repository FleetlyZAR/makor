# Group plans rework: handoff

## The corrected model (from Luyanda, 19 July 2026)

Luyanda authors a catalog of plan TEMPLATES; he is not a member of anyone's
group. A member picks a template, becomes the LEADER of their own group
instance, sets their own sittings (one to three per day, with times), start
date, and an optional Google Meet link, then INVITES friends. Invitees
accept before they are members (consent, same as friendships). Nobody but
the admin can author templates.

## Current state (v1, shipped but menu link hidden)

- public.group_plans conflates template and group: admin-created rows carry
  both the plan definition AND the fixed times/start/meet. Members join it
  directly. Seeded row: "The One Story: the whole Bible, chronologically, in
  a year" (chronological, 1 year, daily, 05:00).
- public.group_plan_members, RPC list_group_plans().
- /groups/ page lists plans with join/leave and an admin create form.
  Menu item is commented out in Base.astro; page reachable by URL.
- /plan/?group=<id> loads a group's config into the calendar machinery
  (Google Calendar + ICS), names the calendar "Makor: <group name>", and
  attaches the Meet link to every sitting (location + description).
  See loadGroupCtx() in plan.astro.

## Target schema

- plan_templates: id, name, description, plan_order, years, cadence,
  created_by (admin), created_at. Admin-only insert/update via admins table
  (copy the existing group_plans insert policy).
- groups: id, template_id -> plan_templates, leader uuid, slots jsonb
  ({1..3: {on, time}}), start_date, meet_link, created_at. Any authenticated
  user may create; leader manages.
- group_members: group_id, user_id, status ('invited','accepted'),
  invited_by, joined_at. Leader inserts invites for FRIENDS (reuse
  my_friendships to pick); invitee updates own row to accepted or deletes.
- Migrate: convert the seeded group_plans row into a plan_templates row;
  group_plan_members rows are only test data; keep or drop group_plans
  after migration.
- Invite notification: replicate the friendships trigger + edge function
  pattern (notify-friend-request) as notify-group-invite; respect a new
  user_prefs.group_invite_emails toggle, surfaced on /email-preferences/.
  Webhook auth via app_config.webhook_key, same as notify_friend_request().

## Pages

- /groups/: two layers. "Plans you can start" (templates catalog; Start
  this plan -> form: sessions 1-3 with times, start date, meet link ->
  creates group, then invite friends from my_friendships accepted list).
  "Your groups": groups you lead or belong to, invitations awaiting your
  acceptance, Add to my calendar (-> /plan/?group=<id>, update loadGroupCtx
  to read the new groups table), Join the Meet, leave.
- Admin template form stays admin-gated (email check client side, RLS
  server side).

## Facts you will need

- The repo has MOVED to ~/Documents/Developer/makor (was ~/Documents/makor).
- Supabase project: makor, ref oztgjzncxgobcszcwibp. Apply changes via MCP
  (precedent: analytics, comms, social, group v1 all deployed this way).
- Calendar machinery: plan.astro inline script; scheduleItems and
  scheduleEvents take arbitrary cfg {order, years, cadence, slots, start}.
  GROUP_MEET and CAL_SUMMARY are the group hooks.
- Email pattern: comms uses Vault (comms.send_email) but the social
  notifications use app_config.resend_api_key via edge function; follow
  notify-friend-request/index.ts as the template.
- IP note: first template deliberately named "The One Story..." and NOT
  "Eden to Eternity / Daily Grace" (their trademark and curated plan).
  Any Daily Grace branding requires their permission first.

## Separate open item (not groups)

iOS: calendar study links open the website because no app exists. The fix
is the Capacitor native shell + Universal Links (see the earlier
scaffolding conversation), not a website change.
