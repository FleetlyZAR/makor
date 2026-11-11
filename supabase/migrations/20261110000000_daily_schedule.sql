-- Dated scripture of the day calendar for the weekday email.
--
-- The repo keeps the calendar in tools/daily/calendar.json and the verses in
-- tools/daily/verses/. tools/daily/build.py writes the SQL that upserts each
-- scheduled verse into comms.daily_pool and each date into comms.daily_schedule,
-- so the email sends the same verse the app shows that day.
--
-- Fail safe: pick_today() uses the schedule first. If today has no schedule row,
-- or the scheduled verse is missing or inactive, it falls back to the original
-- least sent random pick, so an email always goes out.

create table if not exists comms.daily_schedule (
  on_date    date primary key,
  slug       text not null references comms.daily_pool (slug) on update cascade,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table comms.daily_schedule enable row level security;
-- No policies: only the service role and security definer functions read it,
-- the same as the rest of the comms schema.

create or replace function comms.pick_today()
 returns comms.daily_pool
 language plpgsql
 security definer
 set search_path to 'comms', 'public', 'pg_temp'
as $function$
declare
  v_today   date := timezone('Africa/Johannesburg', now())::date;
  v_pool_id bigint;
  v_row     comms.daily_pool;
begin
  if (select daily_enabled from comms.config where id = 1)
     and extract(isodow from v_today) between 1 and 5 then

    select pool_id into v_pool_id
      from comms.daily_log
     where sent_on = v_today
       and pool_id is not null;

    if v_pool_id is null then
      -- 1. The dated calendar.
      select p.id into v_pool_id
        from comms.daily_schedule s
        join comms.daily_pool p on p.slug = s.slug
       where s.on_date = v_today
         and p.active
         and p.study_url is not null;

      -- 2. Fallback: the original least sent random pick.
      if v_pool_id is null then
        select id into v_pool_id
          from comms.daily_pool
         where active
           and study_url is not null
           and id <> coalesce(
                 (select pool_id from comms.daily_log
                   where pool_id is not null
                   order by sent_on desc limit 1), -1)
         order by times_sent asc, random()
         limit 1;
      end if;

      if v_pool_id is not null then
        insert into comms.daily_log (sent_on, pool_id)
        values (v_today, v_pool_id)
        on conflict (sent_on) do nothing;

        select pool_id into v_pool_id
          from comms.daily_log
         where sent_on = v_today
           and pool_id is not null;
      end if;
    end if;
  end if;

  if v_pool_id is null then
    select pool_id into v_pool_id
      from comms.daily_log
     where pool_id is not null
     order by sent_on desc
     limit 1;
  end if;

  if v_pool_id is null then
    return null;
  end if;

  select * into v_row from comms.daily_pool where id = v_pool_id;
  return v_row;
end;
$function$;

-- How far ahead the email calendar reaches, for the admin view and the daily run.
create or replace function comms.daily_schedule_horizon()
 returns table (covered_days int, last_date date)
 language sql
 stable
 security definer
 set search_path to 'comms', 'public', 'pg_temp'
as $$
  with t as (select timezone('Africa/Johannesburg', now())::date as d),
  run as (
    select s.on_date, s.on_date - (row_number() over (order by s.on_date))::int as grp
      from comms.daily_schedule s, t
     where s.on_date >= t.d
  )
  select coalesce((select count(*)::int from run where grp = (select t.d - 1 from t)), 0),
         (select max(on_date) from comms.daily_schedule);
$$;

-- Same lockdown as comms.pick_today(): no execute for public, anon or authenticated.
revoke execute on function comms.daily_schedule_horizon() from public, anon, authenticated;
revoke all on table comms.daily_schedule from anon, authenticated;
