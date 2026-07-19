-- Badge and tier award ledger, plus per-reader email preferences.
-- Applied to the makor project on 2026-07-19.

create table if not exists public.user_badges (
  user_id uuid not null references auth.users(id) on delete cascade,
  badge_key text not null,
  earned_at timestamptz not null default now(),
  primary key (user_id, badge_key)
);
alter table public.user_badges enable row level security;

drop policy if exists "read own badges" on public.user_badges;
create policy "read own badges" on public.user_badges
  for select using (auth.uid() = user_id);

create table if not exists public.user_prefs (
  user_id uuid primary key references auth.users(id) on delete cascade,
  badge_emails boolean not null default true,
  updated_at timestamptz not null default now()
);
alter table public.user_prefs enable row level security;

drop policy if exists "read own prefs" on public.user_prefs;
create policy "read own prefs" on public.user_prefs
  for select using (auth.uid() = user_id);

drop policy if exists "update own prefs" on public.user_prefs;
create policy "update own prefs" on public.user_prefs
  for update using (auth.uid() = user_id);

drop policy if exists "insert own prefs" on public.user_prefs;
create policy "insert own prefs" on public.user_prefs
  for insert with check (auth.uid() = user_id);
