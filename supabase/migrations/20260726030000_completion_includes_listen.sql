-- Count listen-throughs as completed studies in the admin People and Users
-- views, matching how the rest of the app counts completion (a quiz post or a
-- listen). Only the studies_done tally changes; pre and post score averages are
-- untouched. Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept
-- here for version control.

create or replace function public.admin_overview()
returns table(name text, email text, joined timestamptz, studies_done integer, pre_avg integer, post_avg integer, last_active timestamptz)
language plpgsql security definer set search_path to 'public'
as $$
begin
  if not exists (select 1 from public.admins a where a.email = (auth.jwt() ->> 'email')) then
    return;
  end if;
  return query
    select
      coalesce(u.raw_user_meta_data->>'full_name', u.raw_user_meta_data->>'name', '') as name,
      u.email::text as email,
      u.created_at as joined,
      coalesce(count(distinct at.study_slug) filter (where at.phase in ('post','listen')), 0)::int as studies_done,
      round(avg(at.score) filter (where at.phase = 'pre'))::int as pre_avg,
      round(avg(at.score) filter (where at.phase = 'post'))::int as post_avg,
      max(at.created_at) as last_active
    from auth.users u
    left join public.attempts at on at.user_id = u.id
    group by u.id, u.raw_user_meta_data, u.email, u.created_at
    order by studies_done desc, last_active desc nulls last;
end;
$$;

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
      coalesce((select count(distinct at.study_slug) from attempts at where at.user_id = u.id and at.phase in ('post','listen')), 0)::int,
      coalesce((select count(*) from events e where e.type = 'share' and e.user_id = u.id), 0),
      coalesce((select count(*) from friendships f where f.requester = u.id), 0),
      coalesce((select count(*) from plan_members m where m.invited_by = u.id), 0),
      (select max(at.created_at) from attempts at where at.user_id = u.id)
    from auth.users u
    left join profiles pr on pr.id = u.id
    order by 6 desc, 5 desc, u.created_at desc;
end;
$$;
