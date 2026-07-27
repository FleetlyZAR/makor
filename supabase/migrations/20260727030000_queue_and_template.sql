-- Approving a generated edition should queue it into the weekly sequence as the
-- next step, not blast it to subscribers immediately. And the generator should
-- match the house email design, so expose one existing email as a template.
-- Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept here for
-- version control.

-- Promote a generated edition into comms.sequence_emails at the next step.
create or replace function public.admin_queue_edition(p_id bigint)
returns json
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v_e comms.weekly_editions; v_step int; v_key text; v_base text;
begin
  if not public.is_admin() then raise exception 'not authorized'; end if;
  select * into v_e from comms.weekly_editions where id = p_id;
  if v_e.id is null then return json_build_object('ok', false, 'error', 'not found'); end if;
  if v_e.html is null or v_e.status not in ('generated', 'approved') then
    return json_build_object('ok', false, 'error', 'generate the edition first');
  end if;
  select coalesce(max(step), 0) + 1 into v_step from comms.sequence_emails;
  v_base := trim(both '-' from coalesce(nullif(regexp_replace(lower(coalesce(v_e.story_title, v_e.subject, 'edition')), '[^a-z0-9]+', '-', 'g'), ''), 'edition'));
  v_key := v_base;
  if exists (select 1 from comms.sequence_emails where key = v_key) then v_key := v_base || '-' || p_id; end if;
  insert into comms.sequence_emails(step, key, cadence, subject, preview_text, html, txt, active)
  values (v_step, v_key, 'weekly', v_e.subject, v_e.preview_text, v_e.html, v_e.txt, true);
  update comms.weekly_editions set status = 'scheduled', updated_at = now() where id = p_id;
  return json_build_object('ok', true, 'step', v_step, 'key', v_key);
end;
$$;

-- One existing email's html, for the generator to match the house design.
create or replace function public.gen_email_template()
returns text
language sql security definer set search_path to 'comms','public'
as $$
  select html from comms.sequence_emails
  where key in ('how-it-works', 'welcome')
  order by (key = 'how-it-works') desc
  limit 1;
$$;

grant execute on function public.admin_queue_edition(bigint) to authenticated;
revoke all on function public.gen_email_template() from public;
grant execute on function public.gen_email_template() to service_role;
