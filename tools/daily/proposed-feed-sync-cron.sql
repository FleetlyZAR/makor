-- PROPOSED, NOT APPLIED. Needs Luyanda's approval: it adds recurring pg_cron jobs.
-- If approved, move it back to supabase/migrations/ and apply it.

-- The email calendar syncs itself from the deployed site.
--
-- tools/daily/build.py publishes https://makor.co.za/daily/feed.json with the
-- calendar and the email fields of every scheduled verse. Twice each morning,
-- before the 05:00 UTC email, and once in the evening, pg_cron asks pg_net to
-- fetch it, then applies it two minutes later:
--   comms.daily_sync_request()  queues the HTTP fetch
--   comms.daily_sync_apply()    validates the response and upserts
--                               comms.daily_pool and comms.daily_schedule
--
-- Fail safe: a failed fetch, a bad status, malformed JSON or a feed that fails
-- validation changes nothing (the reason is logged in comms.daily_sync). Dates
-- up to and including today are never rewritten, and an existing pool row keeps
-- its active flag. pick_today() still falls back to the random pick if a date
-- has no schedule row.

create table if not exists comms.daily_sync (
  id           bigserial primary key,
  request_id   bigint,
  requested_at timestamptz not null default now(),
  applied_at   timestamptz,
  status       text,
  detail       text
);
alter table comms.daily_sync enable row level security;
revoke all on table comms.daily_sync from anon, authenticated;

create or replace function comms.daily_sync_request()
 returns bigint
 language plpgsql
 security definer
 set search_path to 'comms', 'public', 'pg_temp'
as $function$
declare
  v_req bigint;
begin
  v_req := net.http_get(
    url := 'https://makor.co.za/daily/feed.json?t=' || extract(epoch from now())::bigint,
    timeout_milliseconds := 30000
  );
  insert into comms.daily_sync (request_id) values (v_req);
  return v_req;
end;
$function$;

create or replace function comms.daily_sync_apply()
 returns text
 language plpgsql
 security definer
 set search_path to 'comms', 'public', 'pg_temp'
as $function$
declare
  v_sync    comms.daily_sync;
  v_code    int;
  v_body    text;
  v_feed    jsonb;
  v_today   date := timezone('Africa/Johannesburg', now())::date;
  v_bad     text;
  v_verses  int;
  v_dates   int;
begin
  select * into v_sync from comms.daily_sync
   where applied_at is null and request_id is not null
   order by id desc limit 1;
  if v_sync.id is null then
    return 'nothing to apply';
  end if;

  select status_code, content into v_code, v_body
    from net._http_response where id = v_sync.request_id;
  if not found then
    return 'pending';
  end if;

  -- Older unapplied requests are superseded by this one.
  update comms.daily_sync set applied_at = now(), status = 'superseded'
   where applied_at is null and id < v_sync.id;

  if v_code is distinct from 200 then
    update comms.daily_sync set applied_at = now(), status = 'http error', detail = coalesce(v_code::text, 'no status')
     where id = v_sync.id;
    return 'http error ' || coalesce(v_code::text, 'none');
  end if;

  begin
    v_feed := v_body::jsonb;
  exception when others then
    update comms.daily_sync set applied_at = now(), status = 'bad json', detail = left(sqlerrm, 300)
     where id = v_sync.id;
    return 'bad json';
  end;

  -- Validate before touching anything.
  if (v_feed->>'version') is distinct from '1'
     or jsonb_typeof(v_feed->'calendar') is distinct from 'object'
     or jsonb_typeof(v_feed->'verses') is distinct from 'object'
     or (select count(*) from jsonb_object_keys(v_feed->'calendar')) = 0 then
    v_bad := 'feed shape';
  end if;

  if v_bad is null then
    select string_agg(c.key || ' -> ' || c.value, ', ') into v_bad
      from jsonb_each_text(v_feed->'calendar') c
     where c.key !~ '^\d{4}-\d{2}-\d{2}$'
        or not (v_feed->'verses') ? c.value;
    if v_bad is not null then v_bad := 'calendar: ' || left(v_bad, 200); end if;
  end if;

  if v_bad is null then
    select string_agg(v.key, ', ') into v_bad
      from jsonb_each(v_feed->'verses') v
     where v.key !~ '^[a-z0-9-]+$'
        or coalesce(length(v.value->>'ref'), 0) = 0
        or coalesce(length(v.value->>'verse_text'), 0) = 0
        or coalesce(length(v.value->>'writeup_html'), 0) = 0
        or coalesce(length(v.value->>'writeup_txt'), 0) = 0
        or coalesce(v.value->>'study_url', '') not like 'https://makor.co.za/%'
        or coalesce(v.value->>'daily_page_url', '') not like 'https://makor.co.za/daily/%'
        or (v.value->>'verse_text') ~ '[—–]'
        or (v.value->>'writeup_txt') ~ '[—–]';
    if v_bad is not null then v_bad := 'verses: ' || left(v_bad, 200); end if;
  end if;

  if v_bad is not null then
    update comms.daily_sync set applied_at = now(), status = 'invalid', detail = v_bad
     where id = v_sync.id;
    return 'invalid: ' || v_bad;
  end if;

  insert into comms.daily_pool (slug, ref, verse_text, writeup_html, writeup_txt, study_url, daily_page_url, image_path, og_image_path, active)
  select v.key, v.value->>'ref', v.value->>'verse_text', v.value->>'writeup_html', v.value->>'writeup_txt',
         v.value->>'study_url', v.value->>'daily_page_url', v.value->>'image_path', v.value->>'og_image_path', true
    from jsonb_each(v_feed->'verses') v
  on conflict (slug) do update set
    ref = excluded.ref, verse_text = excluded.verse_text, writeup_html = excluded.writeup_html,
    writeup_txt = excluded.writeup_txt, study_url = excluded.study_url, daily_page_url = excluded.daily_page_url,
    image_path = excluded.image_path, og_image_path = excluded.og_image_path
  where (comms.daily_pool.ref, comms.daily_pool.verse_text, comms.daily_pool.writeup_html, comms.daily_pool.writeup_txt,
         comms.daily_pool.study_url, comms.daily_pool.daily_page_url, comms.daily_pool.image_path, comms.daily_pool.og_image_path)
        is distinct from
        (excluded.ref, excluded.verse_text, excluded.writeup_html, excluded.writeup_txt,
         excluded.study_url, excluded.daily_page_url, excluded.image_path, excluded.og_image_path);
  get diagnostics v_verses = row_count;

  -- Today and earlier: insert if missing, never rewrite.
  insert into comms.daily_schedule (on_date, slug)
  select c.key::date, c.value from jsonb_each_text(v_feed->'calendar') c
   where c.key::date <= v_today
  on conflict (on_date) do nothing;

  -- The future follows the feed.
  insert into comms.daily_schedule (on_date, slug)
  select c.key::date, c.value from jsonb_each_text(v_feed->'calendar') c
   where c.key::date > v_today
  on conflict (on_date) do update set slug = excluded.slug, updated_at = now()
   where comms.daily_schedule.slug is distinct from excluded.slug;

  select count(*) into v_dates from jsonb_object_keys(v_feed->'calendar');

  update comms.daily_sync set applied_at = now(), status = 'ok',
         detail = v_dates || ' dates in feed, ' || v_verses || ' pool rows written'
   where id = v_sync.id;
  return 'ok: ' || v_dates || ' dates, ' || v_verses || ' pool rows written';
end;
$function$;

revoke execute on function comms.daily_sync_request() from public, anon, authenticated;
revoke execute on function comms.daily_sync_apply() from public, anon, authenticated;

-- 03:10 and 04:10 UTC (05:10 and 06:10 in South Africa), before the 05:00 UTC
-- email, plus 18:10 UTC so a change deployed during the day lands the same day.
select cron.schedule('makor-daily-sync-request', '10 3,4,18 * * *', 'select comms.daily_sync_request();');
select cron.schedule('makor-daily-sync-apply',   '13 3,4,18 * * *', 'select comms.daily_sync_apply();');
