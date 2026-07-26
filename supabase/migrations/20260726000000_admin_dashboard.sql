-- Admin dashboard: weekly Sunday editions, share tracking support, and the
-- admin RPCs behind the new accordions (Sunday email, Plans and groups, Users).
--
-- Additive and non-destructive. A new comms.weekly_editions table gets Row
-- Level Security enabled with an admin only policy from the start, and every
-- RPC is SECURITY DEFINER guarded by public.admins, matching admin_overview.
-- Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept here for
-- version control.

-- Shared admin check, by email on the JWT, same source as admin_overview.
create or replace function public.is_admin()
returns boolean
language sql stable security definer set search_path to 'public'
as $$
  select exists (select 1 from public.admins a where a.email = (auth.jwt() ->> 'email'));
$$;

-- 1. Weekly Sunday editions: an AI curated story plus a feature to highlight.
create table if not exists comms.weekly_editions (
  id             bigint generated always as identity primary key,
  position       integer not null default 0,
  target_send_on date,
  story_slug     text,
  story_ref      text,
  story_title    text,
  feature_key    text,
  feature_label  text,
  instruction    text,
  subject        text,
  preview_text   text,
  html           text,
  txt            text,
  thinking       text,
  model          text,
  status         text not null default 'draft'
                 check (status in ('draft','generating','generated','approved','scheduled','sent','error')),
  error          text,
  created_by     uuid,
  generated_at   timestamptz,
  sent_at        timestamptz,
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now()
);

alter table comms.weekly_editions enable row level security;
drop policy if exists "weekly editions admin all" on comms.weekly_editions;
create policy "weekly editions admin all"
  on comms.weekly_editions for all to authenticated
  using (public.is_admin())
  with check (public.is_admin());

-- 2. Editions read for the dashboard (position order).
create or replace function public.admin_weekly_editions()
returns table(
  id bigint, pos int, target_send_on date, story_slug text, story_ref text, story_title text,
  feature_key text, feature_label text, instruction text, subject text, preview_text text,
  html text, txt text, thinking text, model text, status text, error text,
  generated_at timestamptz, sent_at timestamptz, created_at timestamptz)
language plpgsql security definer set search_path to 'comms','public'
as $$
begin
  if not public.is_admin() then return; end if;
  return query
    select e.id, e.position, e.target_send_on, e.story_slug, e.story_ref, e.story_title,
           e.feature_key, e.feature_label, e.instruction, e.subject, e.preview_text,
           e.html, e.txt, e.thinking, e.model, e.status, e.error,
           e.generated_at, e.sent_at, e.created_at
    from comms.weekly_editions e
    order by e.position asc, e.id asc;
end;
$$;

-- 3. Create a draft edition; returns its id so the client can trigger generation.
create or replace function public.admin_create_edition(
  p_story_slug text, p_story_ref text, p_story_title text,
  p_feature_key text, p_feature_label text, p_instruction text, p_target_send_on date)
returns bigint
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v_id bigint; v_pos int;
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  select coalesce(max(position),0)+1 into v_pos from comms.weekly_editions;
  insert into comms.weekly_editions(position, target_send_on, story_slug, story_ref, story_title,
                                    feature_key, feature_label, instruction, created_by)
  values (v_pos, p_target_send_on, p_story_slug, p_story_ref, p_story_title,
          p_feature_key, p_feature_label, p_instruction, auth.uid())
  returning id into v_id;
  return v_id;
end;
$$;

-- 4. Status change (approve, reset to draft, schedule) with a guarded allow list.
create or replace function public.admin_set_edition_status(p_id bigint, p_status text)
returns void
language plpgsql security definer set search_path to 'comms','public'
as $$
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  if p_status not in ('draft','generating','generated','approved','scheduled','sent','error') then
    raise exception 'bad status';
  end if;
  update comms.weekly_editions set status = p_status, updated_at = now() where id = p_id;
end;
$$;

-- 5. Delete an edition.
create or replace function public.admin_delete_edition(p_id bigint)
returns void
language plpgsql security definer set search_path to 'comms','public'
as $$
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  delete from comms.weekly_editions where id = p_id;
end;
$$;

-- 6. Reorder by swapping position with the neighbour in the given direction.
create or replace function public.admin_move_edition(p_id bigint, p_dir int)
returns void
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v_pos int; v_other_id bigint; v_other_pos int;
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  select position into v_pos from comms.weekly_editions where id = p_id;
  if v_pos is null then return; end if;
  if p_dir < 0 then
    select id, position into v_other_id, v_other_pos from comms.weekly_editions
      where position < v_pos order by position desc limit 1;
  else
    select id, position into v_other_id, v_other_pos from comms.weekly_editions
      where position > v_pos order by position asc limit 1;
  end if;
  if v_other_id is null then return; end if;
  update comms.weekly_editions set position = v_other_pos, updated_at = now() where id = p_id;
  update comms.weekly_editions set position = v_pos, updated_at = now() where id = v_other_id;
end;
$$;

-- 7. Send an edition to all current subscribers via the batch endpoint.
create or replace function public.admin_send_edition(p_id bigint)
returns json
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v_e comms.weekly_editions; v_from text; v_payload jsonb; v_count int; v_req bigint;
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  select * into v_e from comms.weekly_editions where id = p_id;
  if v_e.id is null then return json_build_object('ok', false, 'error', 'not found'); end if;
  if v_e.html is null or v_e.status not in ('generated','approved','scheduled') then
    return json_build_object('ok', false, 'error', 'edition is not ready to send');
  end if;
  select from_email into v_from from comms.config where id = 1;
  select jsonb_agg(jsonb_build_object(
           'from', coalesce(v_from, 'Makor <admin@makor.co.za>'),
           'to', s.email,
           'subject', v_e.subject,
           'html', v_e.html,
           'text', v_e.txt)),
         count(*)
    into v_payload, v_count
    from comms.subscribers s
    where s.unsubscribed_at is null and s.email is not null;
  if coalesce(v_count,0) = 0 then return json_build_object('ok', false, 'error', 'no subscribers'); end if;
  v_req := comms.send_batch(v_payload);
  update comms.weekly_editions set status = 'sent', sent_at = now(), updated_at = now() where id = p_id;
  return json_build_object('ok', true, 'recipients', v_count, 'request', v_req);
end;
$$;

-- 8. Plans and groups overview, with the four error buckets.
create or replace function public.admin_plans_overview()
returns json
language plpgsql security definer set search_path to 'public','comms'
as $$
declare v json;
begin
  if not public.is_admin() then return json_build_object('error', 'not authorized'); end if;
  select json_build_object(
    'total_plans',      (select count(*) from plans),
    'group_plans',      (select count(*) from plans p where exists (select 1 from plan_members m where m.owner = p.owner)),
    'solo_plans',       (select count(*) from plans p where not exists (select 1 from plan_members m where m.owner = p.owner)),
    'total_members',    (select count(*) from plan_members),
    'accepted_members', (select count(*) from plan_members where status = 'accepted'),
    'pending_members',  (select count(*) from plan_members where status = 'invited'),
    'err_bounced', (select coalesce(json_agg(x), '[]'::json) from (
        select e.recipient, e.created_at
        from events e where e.type = 'email_bounced'
        order by e.created_at desc limit 25) x),
    'err_stuck_invites', (select coalesce(json_agg(x), '[]'::json) from (
        select coalesce(po.display_name, 'A reader') as owner_name,
               coalesce(pm.display_name, 'A reader') as member_name,
               m.joined_at
        from plan_members m
        left join profiles po on po.id = m.owner
        left join profiles pm on pm.id = m.member
        where m.status = 'invited' and m.joined_at < now() - interval '7 days'
        order by m.joined_at asc limit 50) x),
    'err_orphan_plans', (select coalesce(json_agg(x), '[]'::json) from (
        select coalesce(pr.display_name, 'A reader') as owner_name, p.updated_at
        from plans p left join profiles pr on pr.id = p.owner
        where not exists (select 1 from plan_members m where m.owner = p.owner and m.status = 'accepted')
        order by p.updated_at desc limit 50) x),
    'err_send_failures', (select coalesce(json_agg(x), '[]'::json) from (
        select s.email_key, s.step, s.status, s.sent_at
        from comms.sends s where s.status is distinct from 'sent'
        order by s.sent_at desc limit 50) x)
  ) into v;
  return v;
end;
$$;

-- 9. Users overview: per person, with shares, invites, and studies.
create or replace function public.admin_users_overview()
returns table(
  user_id uuid, name text, email text, joined timestamptz, studies_done int,
  shares bigint, friend_invites bigint, group_invites bigint, last_active timestamptz)
language plpgsql security definer set search_path to 'public'
as $$
begin
  if not public.is_admin() then return; end if;
  return query
    select u.id,
      coalesce(u.raw_user_meta_data->>'full_name', u.raw_user_meta_data->>'name', pr.display_name, '')::text,
      u.email::text,
      u.created_at,
      coalesce((select count(distinct at.study_slug) from attempts at where at.user_id = u.id and at.phase = 'post'), 0)::int,
      coalesce((select count(*) from events e where e.type = 'share' and e.user_id = u.id), 0),
      coalesce((select count(*) from friendships f where f.requester = u.id), 0),
      coalesce((select count(*) from plan_members m where m.invited_by = u.id), 0),
      (select max(at.created_at) from attempts at where at.user_id = u.id)
    from auth.users u
    left join profiles pr on pr.id = u.id
    order by 6 desc, 5 desc, u.created_at desc;
end;
$$;

grant execute on function public.is_admin() to authenticated;
grant execute on function public.admin_weekly_editions() to authenticated;
grant execute on function public.admin_create_edition(text,text,text,text,text,text,date) to authenticated;
grant execute on function public.admin_set_edition_status(bigint,text) to authenticated;
grant execute on function public.admin_delete_edition(bigint) to authenticated;
grant execute on function public.admin_move_edition(bigint,int) to authenticated;
grant execute on function public.admin_send_edition(bigint) to authenticated;
grant execute on function public.admin_plans_overview() to authenticated;
grant execute on function public.admin_users_overview() to authenticated;
