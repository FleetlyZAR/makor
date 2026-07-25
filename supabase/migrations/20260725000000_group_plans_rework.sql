-- Group plans rework (GROUPS-HANDOFF.md).
--
-- The v1 model conflated a plan definition with a single fixed group: admins
-- created group_plans rows and members joined them directly. The corrected
-- model separates the two:
--   * plan_templates: an admin authored catalog of plan definitions.
--   * groups: a member's own instance of a template. The member is the leader
--     and sets their own sittings, start date, and optional Meet link.
--   * group_members: invitations that become memberships on acceptance, the
--     same consent pattern as friendships.
--
-- Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept here for
-- version control. Tables are created before any policy, because the groups
-- and group_members select policies reference each other.

-- 1. Tables ---------------------------------------------------------------
create table if not exists public.plan_templates (
  id          bigint generated always as identity primary key,
  name        text not null,
  description text,
  plan_order  text not null default 'chronological',
  years       integer not null default 1,
  cadence     text not null default 'daily',
  created_by  uuid references auth.users(id) on delete set null,
  created_at  timestamptz not null default now()
);

create table if not exists public.groups (
  id          bigint generated always as identity primary key,
  template_id bigint not null references public.plan_templates(id) on delete restrict,
  leader      uuid not null references auth.users(id) on delete cascade,
  slots       jsonb not null,
  start_date  date not null,
  meet_link   text,
  created_at  timestamptz not null default now()
);

create table if not exists public.group_members (
  group_id   bigint not null references public.groups(id) on delete cascade,
  user_id    uuid not null references auth.users(id) on delete cascade,
  status     text not null default 'invited' check (status in ('invited','accepted')),
  invited_by uuid references auth.users(id) on delete set null,
  joined_at  timestamptz not null default now(),
  primary key (group_id, user_id)
);

alter table public.plan_templates enable row level security;
alter table public.groups         enable row level security;
alter table public.group_members  enable row level security;

-- 2. Policies -------------------------------------------------------------
-- plan_templates: everyone signed in can read; only admins author.
create policy "plan templates readable when signed in"
  on public.plan_templates for select to authenticated using (true);

create policy "plan templates created by admins"
  on public.plan_templates for insert to authenticated
  with check (
    auth.uid() = created_by
    and exists (select 1 from public.admins a
                where lower(a.email) = lower(coalesce((auth.jwt() ->> 'email'), '')))
  );

create policy "plan templates updated by admins"
  on public.plan_templates for update to authenticated
  using (exists (select 1 from public.admins a
                 where lower(a.email) = lower(coalesce((auth.jwt() ->> 'email'), ''))))
  with check (exists (select 1 from public.admins a
                      where lower(a.email) = lower(coalesce((auth.jwt() ->> 'email'), ''))));

create policy "plan templates deleted by admins"
  on public.plan_templates for delete to authenticated
  using (exists (select 1 from public.admins a
                 where lower(a.email) = lower(coalesce((auth.jwt() ->> 'email'), ''))));

-- groups: leader and members read; any authenticated user starts one; leader manages.
create policy "groups readable by leader and members"
  on public.groups for select to authenticated
  using (
    auth.uid() = leader
    or exists (select 1 from public.group_members m where m.group_id = id and m.user_id = auth.uid())
  );

create policy "groups created by any member"
  on public.groups for insert to authenticated
  with check (auth.uid() = leader);

create policy "groups managed by leader"
  on public.groups for update to authenticated
  using (auth.uid() = leader) with check (auth.uid() = leader);

create policy "groups deleted by leader"
  on public.groups for delete to authenticated
  using (auth.uid() = leader);

-- group_members: invitee sees own row, leader sees invites they sent. This
-- policy deliberately does NOT reference public.groups, to avoid recursion
-- with the groups select policy above.
create policy "group members readable to leader and self"
  on public.group_members for select to authenticated
  using (auth.uid() = user_id or auth.uid() = invited_by);

create policy "group members invited by leader"
  on public.group_members for insert to authenticated
  with check (
    status = 'invited'
    and invited_by = auth.uid()
    and exists (select 1 from public.groups g where g.id = group_id and g.leader = auth.uid())
  );

create policy "group members accept own invite"
  on public.group_members for update to authenticated
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy "group members removed by self or leader"
  on public.group_members for delete to authenticated
  using (
    auth.uid() = user_id
    or exists (select 1 from public.groups g where g.id = group_id and g.leader = auth.uid())
  );

-- 3. RPCs ----------------------------------------------------------------
create or replace function public.list_plan_templates()
returns table(id bigint, name text, description text, plan_order text, years integer, cadence text)
language sql security definer set search_path to 'public'
as $$
  select t.id, t.name, t.description, t.plan_order, t.years, t.cadence
  from plan_templates t
  where auth.uid() is not null
  order by t.created_at asc
$$;

-- Groups the caller leads or is invited to, with the template joined in and a
-- role of 'leader', 'accepted', or 'invited'. member_count is the leader plus
-- accepted invitees.
create or replace function public.my_groups()
returns table(
  id bigint, template_id bigint, name text, description text,
  plan_order text, years integer, cadence text,
  slots jsonb, start_date date, meet_link text,
  leader uuid, leader_name text, role text, member_count bigint, created_at timestamptz
)
language sql security definer set search_path to 'public'
as $$
  select g.id, g.template_id, t.name, t.description,
    t.plan_order, t.years, t.cadence,
    g.slots, g.start_date, g.meet_link,
    g.leader,
    coalesce(lp.display_name, 'A reader'),
    case when g.leader = auth.uid() then 'leader'
         else coalesce((select m.status from group_members m
                        where m.group_id = g.id and m.user_id = auth.uid()), 'none') end,
    (1 + (select count(*) from group_members m where m.group_id = g.id and m.status = 'accepted')),
    g.created_at
  from groups g
  join plan_templates t on t.id = g.template_id
  left join profiles lp on lp.id = g.leader
  where g.leader = auth.uid()
     or exists (select 1 from group_members m where m.group_id = g.id and m.user_id = auth.uid())
  order by g.created_at desc
$$;

-- 4. Invite notifications: in-app + email, mirroring the friendship pattern
create or replace function public.inapp_group_invite()
returns trigger language plpgsql security definer set search_path to 'public'
as $$
declare nm text; tname text;
begin
  if (NEW.status is distinct from 'invited') then return NEW; end if;
  select coalesce(p.display_name, 'A reader') into nm from profiles p where p.id = NEW.invited_by;
  select t.name into tname from groups g join plan_templates t on t.id = g.template_id where g.id = NEW.group_id;
  insert into notifications (user_id, type, title, body, deep_link, data)
  values (NEW.user_id, 'group_invite',
          coalesce(nm, 'A reader') || ' invited you to a reading group',
          tname, '/groups/',
          jsonb_build_object('group_id', NEW.group_id, 'invited_by', NEW.invited_by));
  return NEW;
exception when others then return NEW;
end; $$;

create or replace function public.inapp_group_accepted()
returns trigger language plpgsql security definer set search_path to 'public'
as $$
declare nm text; ldr uuid;
begin
  if (NEW.status = 'accepted' and OLD.status is distinct from 'accepted') then
    select coalesce(p.display_name, 'A reader') into nm from profiles p where p.id = NEW.user_id;
    select g.leader into ldr from groups g where g.id = NEW.group_id;
    if ldr is not null then
      insert into notifications (user_id, type, title, body, deep_link, data)
      values (ldr, 'group_accepted',
              coalesce(nm, 'A reader') || ' joined your reading group',
              null, '/groups/',
              jsonb_build_object('group_id', NEW.group_id, 'member', NEW.user_id));
    end if;
  end if;
  return NEW;
exception when others then return NEW;
end; $$;

create or replace function public.notify_group_invite()
returns trigger language plpgsql security definer set search_path to 'public', 'net', 'extensions'
as $$
declare wkey text;
begin
  if (NEW.status is distinct from 'invited') then return NEW; end if;
  select value into wkey from public.app_config where key = 'webhook_key';
  perform net.http_post(
    url := 'https://oztgjzncxgobcszcwibp.supabase.co/functions/v1/notify-group-invite',
    body := jsonb_build_object('record', to_jsonb(NEW)),
    headers := jsonb_build_object(
      'Content-Type','application/json',
      'x-makor-key', coalesce(wkey,''),
      'Authorization','Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im96dGdqem5jeGdvYmNzemN3aWJwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQyMzIwOTgsImV4cCI6MjA5OTgwODA5OH0.23adT65vNiT9lCIUCcew5FNOqNknhpMSdtbhgawczvE'
    ),
    timeout_milliseconds := 5000
  );
  return NEW;
exception when others then
  return NEW;
end; $$;

create trigger trg_inapp_group_invite   after insert on public.group_members
  for each row execute function inapp_group_invite();
create trigger trg_inapp_group_accepted after update on public.group_members
  for each row execute function inapp_group_accepted();
create trigger trg_notify_group_invite  after insert on public.group_members
  for each row execute function notify_group_invite();

-- 5. Email preference: group invite emails --------------------------------
alter table public.user_prefs add column if not exists group_invite_emails boolean not null default true;

create or replace function public.get_email_prefs()
returns jsonb language plpgsql security definer set search_path to 'public', 'comms'
as $$
declare
  uid uuid := auth.uid();
  p record;
  seq boolean;
begin
  if uid is null then raise exception 'not signed in'; end if;
  select * into p from public.user_prefs where user_id = uid;
  select (s.unsubscribed_at is null) into seq from comms.subscribers s where s.user_id = uid;
  return jsonb_build_object(
    'badge_emails', coalesce(p.badge_emails, true),
    'friend_request_emails', coalesce(p.friend_request_emails, true),
    'group_invite_emails', coalesce(p.group_invite_emails, true),
    'daily_emails', coalesce(p.daily_emails, true),
    'sequence_emails', coalesce(seq, true)
  );
end $$;

create or replace function public.set_email_prefs(p jsonb)
returns void language plpgsql security definer set search_path to 'public', 'comms'
as $$
declare
  uid uuid := auth.uid();
  v_email text; v_name text;
begin
  if uid is null then raise exception 'not signed in'; end if;

  insert into public.user_prefs (user_id, badge_emails, friend_request_emails, group_invite_emails, daily_emails, updated_at)
  values (
    uid,
    coalesce((p->>'badge_emails')::boolean, true),
    coalesce((p->>'friend_request_emails')::boolean, true),
    coalesce((p->>'group_invite_emails')::boolean, true),
    coalesce((p->>'daily_emails')::boolean, true),
    now()
  )
  on conflict (user_id) do update set
    badge_emails = excluded.badge_emails,
    friend_request_emails = excluded.friend_request_emails,
    group_invite_emails = excluded.group_invite_emails,
    daily_emails = excluded.daily_emails,
    updated_at = now();

  if p ? 'sequence_emails' then
    if (p->>'sequence_emails')::boolean then
      update comms.subscribers set unsubscribed_at = null where user_id = uid;
      if not found then
        select u.email,
               coalesce(u.raw_user_meta_data->>'full_name', u.raw_user_meta_data->>'name', '')
          into v_email, v_name
          from auth.users u where u.id = uid;
        if v_email is not null then
          insert into comms.subscribers (user_id, email, first_name, last_name, enrolled_at)
          values (
            uid, v_email,
            nullif(initcap(split_part(v_name, ' ', 1)), ''),
            nullif(btrim(substring(v_name from position(' ' in v_name || ' '))), '')
          )
          on conflict (user_id) do update set unsubscribed_at = null;
        end if;
      end if;
    else
      update comms.subscribers set unsubscribed_at = now() where user_id = uid and unsubscribed_at is null;
    end if;
  end if;
end $$;

-- 6. Migrate the seeded plan and retire v1 --------------------------------
insert into public.plan_templates (name, description, plan_order, years, cadence, created_by, created_at)
select name, description, plan_order, years, cadence, creator, created_at
from public.group_plans
where id = 1
  and not exists (select 1 from public.plan_templates pt where pt.name = public.group_plans.name);

drop function if exists public.list_group_plans();
drop table if exists public.group_plan_members;
drop table if exists public.group_plans;
