-- Close the comms schema to the public anon and authenticated roles.
--
-- These tables (including subscribers, which holds real email addresses) had
-- Row Level Security switched off, so anyone with the public anon key could
-- read or change every row. Every legitimate writer bypasses RLS: the tables
-- are owned by postgres, the send functions are SECURITY DEFINER owned by
-- postgres, the daily and weekly cron jobs run as postgres, and the edge
-- functions use the service role (which has BYPASSRLS). No site code reads
-- comms from the browser. So enabling RLS with no policies denies the client
-- and leaves the senders untouched.
--
-- weekly_editions already has RLS with an admin only policy from the admin
-- dashboard migration, so it is not repeated here. Applied to project
-- oztgjzncxgobcszcwibp via the Supabase MCP; kept here for version control.

alter table comms.daily_log       enable row level security;
alter table comms.daily_pool      enable row level security;
alter table comms.subscribers     enable row level security;
alter table comms.sends           enable row level security;
alter table comms.sequence_emails enable row level security;
alter table comms.daily_template  enable row level security;
alter table comms.config          enable row level security;
