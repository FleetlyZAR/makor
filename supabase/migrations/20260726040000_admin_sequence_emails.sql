-- Admin: read the weekly sequence emails that have gone out, with send counts,
-- so the Sunday email panel can list them and open each one to read. Admin
-- guarded, same pattern as the other admin RPCs. Applied to project
-- oztgjzncxgobcszcwibp via the Supabase MCP; kept here for version control.

create or replace function public.admin_sequence_emails()
returns table(
  step int, key text, cadence text, subject text, preview_text text,
  html text, txt text, active boolean, sent_count bigint, last_sent timestamptz)
language plpgsql security definer set search_path to 'comms','public'
as $$
begin
  if not public.is_admin() then return; end if;
  return query
    select se.step, se.key, se.cadence, se.subject, se.preview_text,
           se.html, se.txt, se.active,
           coalesce((select count(*) from comms.sends s where s.email_key = se.key), 0) as sent_count,
           (select max(s.sent_at) from comms.sends s where s.email_key = se.key) as last_sent
    from comms.sequence_emails se
    order by se.step asc;
end;
$$;

grant execute on function public.admin_sequence_emails() to authenticated;
