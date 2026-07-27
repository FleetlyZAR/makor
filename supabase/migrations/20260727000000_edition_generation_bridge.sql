-- Bridge for the generate-weekly-edition function to reach comms.weekly_editions.
--
-- Edge functions talk to the database through PostgREST, which only exposes the
-- public schema, so the function cannot touch comms directly. These two
-- SECURITY DEFINER helpers live in public and are callable by the service role
-- only (the key the function uses), keeping comms unexposed to the browser.
-- Applied to project oztgjzncxgobcszcwibp via the Supabase MCP; kept here for
-- version control.

create or replace function public.gen_edition_read(p_id bigint)
returns json
language plpgsql security definer set search_path to 'comms','public'
as $$
declare v json;
begin
  select to_json(t) into v from (
    select id, story_slug, story_ref, story_title, feature_key, feature_label, instruction, status
    from comms.weekly_editions where id = p_id
  ) t;
  return v;
end;
$$;

create or replace function public.gen_edition_write(
  p_id bigint, p_subject text, p_preview text, p_thinking text, p_html text, p_txt text,
  p_model text, p_status text, p_error text)
returns void
language plpgsql security definer set search_path to 'comms','public'
as $$
begin
  update comms.weekly_editions set
    subject      = coalesce(p_subject, subject),
    preview_text = coalesce(p_preview, preview_text),
    thinking     = coalesce(p_thinking, thinking),
    html         = coalesce(p_html, html),
    txt          = coalesce(p_txt, txt),
    model        = coalesce(p_model, model),
    status       = coalesce(p_status, status),
    error        = p_error,
    generated_at = case when p_status = 'generated' then now() else generated_at end,
    updated_at   = now()
  where id = p_id;
end;
$$;

revoke all on function public.gen_edition_read(bigint) from public;
revoke all on function public.gen_edition_write(bigint,text,text,text,text,text,text,text,text) from public;
grant execute on function public.gen_edition_read(bigint) to service_role;
grant execute on function public.gen_edition_write(bigint,text,text,text,text,text,text,text,text) to service_role;
