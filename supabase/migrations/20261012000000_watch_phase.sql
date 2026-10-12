-- Film watch-throughs: a new attempt phase 'watch'.
--
-- Recorded when someone watches a study's Makor film to the end (the locked
-- player in src/components/StudyFilm.astro). Like 'listen' it is an unscored
-- completion (score 0), so it counts as a study done everywhere 'listen' does:
-- the friend activity feed (which says "watched" for it) and the studies_done
-- tally in the admin People and Users views. Pre and post score averages are
-- untouched. Applied to project oztgjzncxgobcszcwibp via the Supabase MCP on
-- 12 October 2026; kept here for version control.

alter table public.attempts drop constraint if exists attempts_phase_check;
alter table public.attempts add constraint attempts_phase_check
  check (phase = any (array['pre'::text, 'post'::text, 'listen'::text, 'watch'::text]));

create or replace function public.friend_activity()
returns table(user_id uuid, display_name text, avatar_url text, book text, title text, study_slug text, phase text, created_at timestamptz)
language sql security definer set search_path to 'public'
as $$
  select t.user_id, t.display_name, t.avatar_url, t.book, t.title, t.study_slug, t.phase, t.created_at
  from (
    select distinct on (a.user_id, a.study_slug)
      a.user_id, p.display_name, p.avatar_url, a.book, a.title, a.study_slug, a.phase, a.created_at
    from attempts a
    join profiles p on p.id = a.user_id
    where auth.uid() is not null
      and a.phase in ('post', 'listen', 'watch')
      and (
        a.user_id = auth.uid()
        or exists (
          select 1 from friendships f
          where f.status = 'accepted'
            and ((f.requester = auth.uid() and f.addressee = a.user_id)
              or (f.addressee = auth.uid() and f.requester = a.user_id))
        )
      )
    order by a.user_id, a.study_slug, (a.phase = 'post') desc, a.created_at desc
  ) t
  order by t.created_at desc
  limit 100
$$;

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
      coalesce(count(distinct at.study_slug) filter (where at.phase in ('post','listen','watch')), 0)::int as studies_done,
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
      coalesce((select count(distinct at.study_slug) from attempts at where at.user_id = u.id and at.phase in ('post','listen','watch')), 0)::int,
      coalesce((select count(*) from events e where e.type = 'share' and e.user_id = u.id), 0),
      coalesce((select count(*) from friendships f where f.requester = u.id), 0),
      coalesce((select count(*) from plan_members m where m.invited_by = u.id), 0),
      (select max(at.created_at) from attempts at where at.user_id = u.id)
    from auth.users u
    left join profiles pr on pr.id = u.id
    order by 6 desc, 5 desc, u.created_at desc;
end;
$$;
