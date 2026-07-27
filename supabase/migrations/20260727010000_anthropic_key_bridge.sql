-- Let the generate-weekly-edition function read its model key from Supabase
-- Vault, the same encrypted store send_batch uses for the Resend key. The
-- secret itself is set directly in the vault (not in version control). This
-- helper is callable by the service role only. Applied to project
-- oztgjzncxgobcszcwibp via the Supabase MCP; kept here for version control.

create or replace function public.gen_get_anthropic_key()
returns text
language sql security definer set search_path to 'vault','public'
as $$
  select decrypted_secret from vault.decrypted_secrets where name = 'anthropic_api_key' limit 1;
$$;

revoke all on function public.gen_get_anthropic_key() from public;
grant execute on function public.gen_get_anthropic_key() to service_role;
