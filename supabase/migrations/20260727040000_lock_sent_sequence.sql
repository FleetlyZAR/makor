-- Hard lock the order of any sequence email that has already gone out to
-- anyone. Its content stays editable and regenerable, but its position cannot
-- change, so every reader moves through the same order even though the content
-- they receive may differ by when they reach that step. A move is refused if
-- either the email being moved or the neighbour it would swap with has sends.
-- Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept here for
-- version control.

drop function if exists public.admin_sequence_move(int, int);

create or replace function public.admin_sequence_move(p_step int, p_dir int)
returns json
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v_other int; v_key text; v_other_key text;
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  select key into v_key from comms.sequence_emails where step = p_step;
  if v_key is null then return json_build_object('ok', false, 'error', 'not found'); end if;
  if p_dir < 0 then
    select max(step) into v_other from comms.sequence_emails where step < p_step;
  else
    select min(step) into v_other from comms.sequence_emails where step > p_step;
  end if;
  if v_other is null then return json_build_object('ok', false, 'error', 'no neighbour'); end if;
  select key into v_other_key from comms.sequence_emails where step = v_other;
  if exists (select 1 from comms.sends s where s.email_key in (v_key, v_other_key)) then
    return json_build_object('ok', false, 'error', 'This position is locked, because an email here has already gone out to readers.');
  end if;
  update comms.sequence_emails set step = -999999 where step = p_step;
  update comms.sequence_emails set step = p_step   where step = v_other;
  update comms.sequence_emails set step = v_other  where step = -999999;
  return json_build_object('ok', true);
end;
$$;

grant execute on function public.admin_sequence_move(int, int) to authenticated;
