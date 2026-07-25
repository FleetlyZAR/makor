-- Shared reading plans.
--
-- Simplified model (replaces the earlier templates/groups design): a reading
-- plan belongs to one owner. On the plan page the owner may invite friends to
-- read along; a friend must accept, and on accepting the owner's plan (order,
-- length, sittings, and optional Meet link) becomes theirs to add to their own
-- calendar. Consent works exactly like friendships. A person may own their own
-- plan and also be a member of friends' plans.
--
-- Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept here for
-- version control.

-- Retire the earlier groups/templates model if present.
drop table if exists public.group_members cascade;
drop table if exists public.groups cascade;
drop table if exists public.plan_templates cascade;
drop function if exists public.list_plan_templates();
drop function if exists public.my_groups();
drop function if exists public.inapp_group_invite() cascade;
drop function if exists public.inapp_group_accepted() cascade;
drop function if exists public.notify_group_invite() cascade;

-- A plan belongs to one owner; friends are invited to read along on it.
create table if not exists public.plans (
  owner      uuid primary key references auth.users(id) on delete cascade,
  cfg        jsonb not null,
  meet_link  text,
  updated_at timestamptz not null default now()
);

create table if not exists public.plan_members (
  owner      uuid not null references public.plans(owner) on delete cascade,
  member     uuid not null references auth.users(id) on delete cascade,
  status     text not null default 'invited' check (status in ('invited','accepted')),
  invited_by uuid references auth.users(id) on delete set null,
  joined_at  timestamptz not null default now(),
  primary key (owner, member)
);

alter table public.plans        enable row level security;
alter table public.plan_members enable row level security;

-- plans: owner manages; owner and invited/accepted members can read it.
create policy "plans readable by owner and members"
  on public.plans for select to authenticated
  using (
    auth.uid() = owner
    or exists (select 1 from public.plan_members m where m.owner = plans.owner and m.member = auth.uid())
  );
create policy "plans inserted by owner"
  on public.plans for insert to authenticated with check (auth.uid() = owner);
create policy "plans updated by owner"
  on public.plans for update to authenticated
  using (auth.uid() = owner) with check (auth.uid() = owner);
create policy "plans deleted by owner"
  on public.plans for delete to authenticated using (auth.uid() = owner);

-- plan_members: owner sees their roster, member sees their own row. Does not
-- reference plans, to avoid recursion with the plans select policy.
create policy "plan members readable by owner and self"
  on public.plan_members for select to authenticated
  using (auth.uid() = owner or auth.uid() = member);
create policy "plan members invited by owner"
  on public.plan_members for insert to authenticated
  with check (status = 'invited' and invited_by = auth.uid() and owner = auth.uid());
create policy "plan members accept own invite"
  on public.plan_members for update to authenticated
  using (auth.uid() = member) with check (auth.uid() = member);
create policy "plan members removed by self or owner"
  on public.plan_members for delete to authenticated
  using (auth.uid() = member or auth.uid() = owner);

-- Members of the caller's own plan.
create or replace function public.my_plan_members()
returns table(member uuid, name text, status text)
language sql security definer set search_path to 'public'
as $$
  select m.member, coalesce(p.display_name, 'A reader'), m.status
  from plan_members m
  left join profiles p on p.id = m.member
  where m.owner = auth.uid()
  order by (m.status = 'accepted') desc, m.joined_at asc
$$;

-- Plans the caller has been invited to or joined (as a member).
create or replace function public.my_plan_memberships()
returns table(owner uuid, owner_name text, status text)
language sql security definer set search_path to 'public'
as $$
  select m.owner, coalesce(p.display_name, 'A reader'), m.status
  from plan_members m
  left join profiles p on p.id = m.owner
  where m.member = auth.uid()
  order by (m.status = 'invited') desc, m.joined_at asc
$$;

-- Invitation notifications: in-app + email, mirroring the friendship pattern.
create or replace function public.inapp_plan_invite()
returns trigger language plpgsql security definer set search_path to 'public'
as $$
declare nm text;
begin
  if (NEW.status is distinct from 'invited') then return NEW; end if;
  select coalesce(p.display_name, 'A reader') into nm from profiles p where p.id = NEW.invited_by;
  insert into notifications (user_id, type, title, body, deep_link, data)
  values (NEW.member, 'plan_invite',
          coalesce(nm, 'A reader') || ' invited you to read the Bible together',
          null, '/plan/',
          jsonb_build_object('owner', NEW.owner, 'invited_by', NEW.invited_by));
  return NEW;
exception when others then return NEW;
end; $$;

create or replace function public.inapp_plan_accepted()
returns trigger language plpgsql security definer set search_path to 'public'
as $$
declare nm text;
begin
  if (NEW.status = 'accepted' and OLD.status is distinct from 'accepted') then
    select coalesce(p.display_name, 'A reader') into nm from profiles p where p.id = NEW.member;
    insert into notifications (user_id, type, title, body, deep_link, data)
    values (NEW.owner, 'plan_accepted',
            coalesce(nm, 'A reader') || ' is reading with you',
            null, '/plan/',
            jsonb_build_object('owner', NEW.owner, 'member', NEW.member));
  end if;
  return NEW;
exception when others then return NEW;
end; $$;

create or replace function public.notify_plan_invite()
returns trigger language plpgsql security definer set search_path to 'public', 'net', 'extensions'
as $$
declare wkey text;
begin
  if (NEW.status is distinct from 'invited') then return NEW; end if;
  select value into wkey from public.app_config where key = 'webhook_key';
  perform net.http_post(
    url := 'https://oztgjzncxgobcszcwibp.supabase.co/functions/v1/notify-plan-invite',
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

create trigger trg_inapp_plan_invite   after insert on public.plan_members
  for each row execute function inapp_plan_invite();
create trigger trg_inapp_plan_accepted after update on public.plan_members
  for each row execute function inapp_plan_accepted();
create trigger trg_notify_plan_invite  after insert on public.plan_members
  for each row execute function notify_plan_invite();
