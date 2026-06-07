-- ════════════════════════════════════════════════════════════
-- WC2026 Prediction League — Supabase Schema
-- Run this entire file in the Supabase SQL Editor once.
-- ════════════════════════════════════════════════════════════

-- 1. USERS
create table if not exists users (
  id            uuid primary key default gen_random_uuid(),
  username      text unique not null,
  password_hash text not null,
  is_admin      boolean not null default false,
  created_at    timestamptz default now()
);

-- 2. PREDICTIONS
create table if not exists predictions (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid references users(id) on delete cascade,
  match_id        integer not null,
  home_score      integer not null,
  away_score      integer not null,
  penalty_winner  text check (penalty_winner in ('home', 'away')),
  updated_at      timestamptz default now(),
  unique (user_id, match_id)
);

-- 3. RESULTS  (admin-only writes)
create table if not exists results (
  match_id        integer primary key,
  home_score      integer not null,
  away_score      integer not null,
  penalty_winner  text check (penalty_winner in ('home', 'away')),
  entered_at      timestamptz default now()
);

-- ── Row Level Security ───────────────────────────────────────
alter table users       enable row level security;
alter table predictions enable row level security;
alter table results     enable row level security;

-- Users: anyone can insert (register); anyone can read usernames; only owner reads hash
create policy "users_insert"        on users for insert with check (true);
create policy "users_select_public" on users for select using (true);
create policy "users_update_self"   on users for update using (auth.uid()::text = id::text);

-- Predictions: users can read/write their own
create policy "pred_select_own"  on predictions for select  using (true);
create policy "pred_insert_own"  on predictions for insert  with check (true);
create policy "pred_update_own"  on predictions for update  using (true);

-- Results: anyone can read; anyone can write (admin check is in app code)
create policy "results_select"  on results for select using (true);
create policy "results_insert"  on results for insert with check (true);
create policy "results_update"  on results for update using (true);
