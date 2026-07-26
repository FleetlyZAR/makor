-- Friend activity: also surface listen-throughs, not just completed quizzes.
--
-- A listen-through is an attempt with phase 'listen' (recorded when someone
-- finishes listening to a study). The feed now includes these and returns the
-- phase so the page can say "listened to" instead of "completed". One row per
-- person and study, preferring the completed attempt, so a study that was both
-- listened to and finished shows once as completed rather than twice.
-- Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept here for
-- version control.

-- Return shape gains a phase column, so drop the old signature first.
drop function if exists public.friend_activity();

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
      and a.phase in ('post', 'listen')
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
