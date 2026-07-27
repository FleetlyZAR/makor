-- Manage the weekly onboarding sequence from the admin panel: edit, reorder,
-- turn off or delete, and AI regenerate. These touch comms.sequence_emails,
-- which the live run_weekly cron sends in step order, so reordering changes
-- what mid-sequence readers receive next. Admin RPCs are guarded by
-- public.admins; the gen_sequence_* bridges are for the generate function
-- (service role only). Applied to project oztgjzncxgobcszcwibp via the
-- Supabase MCP; kept here for version control.

-- Edit content and the on/off flag.
create or replace function public.admin_sequence_update(
  p_step int, p_subject text, p_preview text, p_html text, p_txt text, p_active boolean)
returns void
language plpgsql security definer set search_path to 'comms','public'
as $$
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  update comms.sequence_emails set
    subject      = coalesce(p_subject, subject),
    preview_text = coalesce(p_preview, preview_text),
    html         = coalesce(p_html, html),
    txt          = coalesce(p_txt, txt),
    active       = coalesce(p_active, active)
  where step = p_step;
end;
$$;

-- Delete, but refuse when the email has already been sent (send history FK).
create or replace function public.admin_sequence_delete(p_step int)
returns json
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v_key text;
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  select key into v_key from comms.sequence_emails where step = p_step;
  if v_key is null then return json_build_object('ok', false, 'error', 'not found'); end if;
  if exists (select 1 from comms.sends s where s.email_key = v_key) then
    return json_build_object('ok', false, 'error', 'This email has already been sent to readers, so it cannot be deleted. Turn it off instead.');
  end if;
  delete from comms.sequence_emails where step = p_step;
  return json_build_object('ok', true);
end;
$$;

-- Reorder by swapping step with the neighbour in the given direction.
create or replace function public.admin_sequence_move(p_step int, p_dir int)
returns void
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v_other int;
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  if p_dir < 0 then
    select max(step) into v_other from comms.sequence_emails where step < p_step;
  else
    select min(step) into v_other from comms.sequence_emails where step > p_step;
  end if;
  if v_other is null then return; end if;
  update comms.sequence_emails set step = -999999 where step = p_step;
  update comms.sequence_emails set step = p_step   where step = v_other;
  update comms.sequence_emails set step = v_other  where step = -999999;
end;
$$;

-- Bridges for the generate function (service role only), since comms is not
-- exposed to PostgREST.
create or replace function public.gen_sequence_read(p_step int)
returns json
language sql security definer set search_path to 'comms','public'
as $$
  select to_json(t) from (
    select step, key, cadence, subject, preview_text, html, txt
    from comms.sequence_emails where step = p_step
  ) t;
$$;

create or replace function public.gen_sequence_write(
  p_step int, p_subject text, p_preview text, p_html text, p_txt text)
returns void
language plpgsql security definer set search_path to 'comms','public'
as $$
begin
  update comms.sequence_emails set
    subject      = coalesce(p_subject, subject),
    preview_text = coalesce(p_preview, preview_text),
    html         = coalesce(p_html, html),
    txt          = coalesce(p_txt, txt)
  where step = p_step;
end;
$$;

grant execute on function public.admin_sequence_update(int,text,text,text,text,boolean) to authenticated;
grant execute on function public.admin_sequence_delete(int) to authenticated;
grant execute on function public.admin_sequence_move(int,int) to authenticated;
revoke all on function public.gen_sequence_read(int) from public;
revoke all on function public.gen_sequence_write(int,text,text,text,text) from public;
grant execute on function public.gen_sequence_read(int) to service_role;
grant execute on function public.gen_sequence_write(int,text,text,text,text) to service_role;
