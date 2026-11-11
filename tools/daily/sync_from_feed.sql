-- Pull the live feed into the email calendar, once. Used by DAILY-RUN.md step 7.
-- 1) select net.http_get(url := 'https://makor.co.za/daily/feed.json?t=' || extract(epoch from now())::bigint, timeout_milliseconds := 30000);
-- 2) put the returned id in place of __REQ__ below and run this block. It raises
--    (and changes nothing) if the response is missing, not 200, or fails validation.

do $$
declare
  v_req   bigint := __REQ__;  -- replace with the id from net.http_get
  v_code  int;
  v_body  text;
  v_feed  jsonb;
  v_today date := timezone('Africa/Johannesburg', now())::date;
  v_bad   text;
begin
  select status_code, content into v_code, v_body from net._http_response where id = v_req;
  if not found then raise exception 'pending: no response yet for %', v_req; end if;
  if v_code <> 200 then raise exception 'http %', v_code; end if;
  v_feed := v_body::jsonb;
  if (v_feed->>'version') is distinct from '1' then raise exception 'feed version'; end if;
  select string_agg(c.key, ', ') into v_bad from jsonb_each_text(v_feed->'calendar') c
   where c.key !~ '^\d{4}-\d{2}-\d{2}$' or not (v_feed->'verses') ? c.value;
  if v_bad is not null then raise exception 'calendar: %', v_bad; end if;
  select string_agg(v.key, ', ') into v_bad from jsonb_each(v_feed->'verses') v
   where coalesce(length(v.value->>'verse_text'),0) = 0 or coalesce(length(v.value->>'writeup_html'),0) = 0
      or coalesce(v.value->>'study_url','') not like 'https://makor.co.za/%'
      or coalesce(v.value->>'daily_page_url','') not like 'https://makor.co.za/daily/%';
  if v_bad is not null then raise exception 'verses: %', v_bad; end if;

  insert into comms.daily_pool (slug, ref, verse_text, writeup_html, writeup_txt, study_url, daily_page_url, image_path, og_image_path, active)
  select v.key, v.value->>'ref', v.value->>'verse_text', v.value->>'writeup_html', v.value->>'writeup_txt',
         v.value->>'study_url', v.value->>'daily_page_url', v.value->>'image_path', v.value->>'og_image_path', true
    from jsonb_each(v_feed->'verses') v
  on conflict (slug) do update set ref = excluded.ref, verse_text = excluded.verse_text, writeup_html = excluded.writeup_html,
    writeup_txt = excluded.writeup_txt, study_url = excluded.study_url, daily_page_url = excluded.daily_page_url,
    image_path = excluded.image_path, og_image_path = excluded.og_image_path;

  insert into comms.daily_schedule (on_date, slug)
  select c.key::date, c.value from jsonb_each_text(v_feed->'calendar') c where c.key::date <= v_today
  on conflict (on_date) do nothing;

  insert into comms.daily_schedule (on_date, slug)
  select c.key::date, c.value from jsonb_each_text(v_feed->'calendar') c where c.key::date > v_today
  on conflict (on_date) do update set slug = excluded.slug, updated_at = now();
end $$;
