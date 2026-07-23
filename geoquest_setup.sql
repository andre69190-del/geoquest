-- ============================================================================
-- GeoQuest — Supabase Schema Setup (frische, selbst gehostete Instanz)
-- ----------------------------------------------------------------------------
-- Rekonstruiert aus dem tatsaechlichen App-Code (gen.py) + ARCHITECTURE.md §10.
-- Nur STRUKTUR, keine Daten-Migration.
--
-- Ausfuehren: Supabase Studio -> SQL Editor -> komplett einfuegen -> Run.
-- Idempotent: mehrfaches Ausfuehren ist gefahrlos (IF NOT EXISTS /
--             CREATE OR REPLACE / DROP POLICY IF EXISTS vor CREATE POLICY).
--
-- Quelle je Spalte/RPC = wie die App Supabase wirklich aufruft:
--   .rpc(name, {p_...})  -> RPC-Signaturen (Param-Namen MUESSEN exakt passen)
--   .from(tabelle)       -> Tabellen + benutzte Spalten
--   .auth.signUp(...)    -> user_metadata.username -> handle_new_user
-- ============================================================================


-- ────────────────────────────────────────────────────────────────────────────
-- 0. EXTENSIONS
-- ────────────────────────────────────────────────────────────────────────────
create extension if not exists pgcrypto;   -- gen_random_uuid()


-- ────────────────────────────────────────────────────────────────────────────
-- 1. TABELLE: profiles   (1 Zeile pro auth.users)
-- ----------------------------------------------------------------------------
-- Spalten aus ARCHITECTURE.md §10 + tatsaechlich in gen.py referenzierte:
--   plates_collected : TEXT (NICHT jsonb!) — gen.py behandelt es als JSON-STRING
--                      (typeof === "string", JSON.parse / JSON.stringify).
--   stats_history    : jsonb ARRAY (Array.isArray-Check) -> default '[]'.
--   stats_mastery    : jsonb OBJECT (Object.keys-Check)  -> default '{}'.
--   current_league / last_eval_week : TEXT — von evaluateWeeklyLeague() +
--                      RPC update_league benutzt (NICHT league_id/league_score;
--                      siehe Hinweis am Dateiende).
--   is_premium / premium_until : von processMockPayment() geschrieben.
-- ────────────────────────────────────────────────────────────────────────────
create table if not exists public.profiles (
  id                uuid primary key references auth.users(id) on delete cascade,
  username          text unique,
  total_score       int         not null default 0,
  games_played      int         not null default 0,
  geo_coins         int         not null default 0,
  current_title     text,
  joker_5050        int         not null default 0,
  joker_freeze      int         not null default 0,
  plates_collected  text                 default '[]',            -- JSON-String
  stats_mastery     jsonb       not null default '{}'::jsonb,     -- Objekt
  stats_history     jsonb       not null default '[]'::jsonb,     -- Array
  survival_best     int         not null default 0,
  last_daily_date   text,
  current_league    text        not null default 'Bronze',
  last_eval_week    text        not null default '',
  is_premium        boolean     not null default false,
  premium_until     timestamptz,
  created_at        timestamptz not null default now()
);

-- Falls die Tabelle bereits existierte: fehlende Spalten idempotent ergaenzen.
alter table public.profiles add column if not exists username         text;
alter table public.profiles add column if not exists total_score      int         not null default 0;
alter table public.profiles add column if not exists games_played     int         not null default 0;
alter table public.profiles add column if not exists geo_coins        int         not null default 0;
alter table public.profiles add column if not exists current_title    text;
alter table public.profiles add column if not exists joker_5050       int         not null default 0;
alter table public.profiles add column if not exists joker_freeze     int         not null default 0;
alter table public.profiles add column if not exists plates_collected text                 default '[]';
alter table public.profiles add column if not exists stats_mastery    jsonb       not null default '{}'::jsonb;
alter table public.profiles add column if not exists stats_history    jsonb       not null default '[]'::jsonb;
alter table public.profiles add column if not exists survival_best    int         not null default 0;
alter table public.profiles add column if not exists last_daily_date  text;
alter table public.profiles add column if not exists current_league   text        not null default 'Bronze';
alter table public.profiles add column if not exists last_eval_week   text        not null default '';
alter table public.profiles add column if not exists is_premium       boolean     not null default false;
alter table public.profiles add column if not exists premium_until    timestamptz;
alter table public.profiles add column if not exists created_at       timestamptz not null default now();

-- Unique auf username absichern (idempotent)
do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'profiles_username_key'
  ) then
    alter table public.profiles add constraint profiles_username_key unique (username);
  end if;
end $$;


-- ────────────────────────────────────────────────────────────────────────────
-- 2. TABELLE: game_sessions   (jede gespeicherte Runde)
-- ----------------------------------------------------------------------------
-- Insert aus gen.py: {user_id, mode, score, best_streak, rounds, accuracy,
--                     username, device_type}
-- Sortierung/Filter: .order("created_at") (gen.py) und get_prev_week_rank()
--                    filtern ueber created_at -> Zeitstempel-Spalte = created_at.
-- ────────────────────────────────────────────────────────────────────────────
create table if not exists public.game_sessions (
  id           bigint generated always as identity primary key,
  user_id      uuid references public.profiles(id) on delete set null,
  mode         text,
  score        int         not null default 0,
  best_streak  int         not null default 0,
  rounds       int         not null default 0,
  accuracy     int         not null default 0,
  username     text,
  device_type  text,
  created_at   timestamptz not null default now()
);

alter table public.game_sessions add column if not exists username    text;
alter table public.game_sessions add column if not exists device_type text;
alter table public.game_sessions add column if not exists created_at  timestamptz not null default now();

create index if not exists idx_sessions_user    on public.game_sessions(user_id);
create index if not exists idx_sessions_created on public.game_sessions(created_at desc);
create index if not exists idx_sessions_mode    on public.game_sessions(mode);


-- ────────────────────────────────────────────────────────────────────────────
-- 3. TABELLE: passport_stamps   (Ziel der RPC upsert_stamp)
-- ----------------------------------------------------------------------------
-- mastery_level: 0=besucht, 1=Bronze, 2=Silber, 3=Gold
-- ────────────────────────────────────────────────────────────────────────────
create table if not exists public.passport_stamps (
  id             uuid primary key default gen_random_uuid(),
  user_id        uuid not null references public.profiles(id) on delete cascade,
  country_code   text not null,
  visits         int  not null default 1,
  perfect_rounds int  not null default 0,
  mastery_level  smallint not null default 0,
  first_seen_at  timestamptz not null default now(),
  updated_at     timestamptz not null default now(),
  unique (user_id, country_code)
);

create index if not exists idx_stamps_user_cc on public.passport_stamps(user_id, country_code);


-- ────────────────────────────────────────────────────────────────────────────
-- 4. TABELLEN: stamps + user_stamps   (Lese-Pfad der Reisepass-Anzeige)
-- ----------------------------------------------------------------------------
-- gen.py liest beim Profil-Load:
--   sb.from("user_stamps").select("stamp_id,stamps(country_code)").eq("user_id",..)
-- PostgREST braucht dafuer beide Tabellen + FK user_stamps.stamp_id -> stamps.id,
-- sonst schlaegt der Embed-Join mit 400 fehl. (Siehe Hinweis am Dateiende:
-- diese Tabellen bleiben aktuell ungefuellt, weil upsert_stamp in
-- passport_stamps schreibt — Alt-Inkonsistenz der App.)
-- ────────────────────────────────────────────────────────────────────────────
create table if not exists public.stamps (
  id           uuid primary key default gen_random_uuid(),
  country_code text not null
);

create table if not exists public.user_stamps (
  id         uuid primary key default gen_random_uuid(),
  user_id    uuid not null references public.profiles(id) on delete cascade,
  stamp_id   uuid not null references public.stamps(id)   on delete cascade,
  created_at timestamptz not null default now(),
  unique (user_id, stamp_id)
);

create index if not exists idx_user_stamps_user on public.user_stamps(user_id);


-- ────────────────────────────────────────────────────────────────────────────
-- 5. TABELLE: feedback   (In-App Feedback / Bug / Crash)
-- ----------------------------------------------------------------------------
-- Insert aus gen.py: {category, message, mode, app_version, lang, username?}
-- ────────────────────────────────────────────────────────────────────────────
create table if not exists public.feedback (
  id           uuid        primary key default gen_random_uuid(),
  created_at   timestamptz not null default now(),
  category     text        not null,
  message      text        not null,
  mode         text,
  user_id      uuid        references auth.users(id) on delete set null,
  username     text,
  lang         text        default 'de',
  app_version  text
);

create index if not exists feedback_created_at_idx on public.feedback (created_at desc);
create index if not exists feedback_category_idx   on public.feedback (category);

-- Laengen-Constraints (Spam-/Missbrauchsschutz) — idempotent
do $$
begin
  if not exists (select 1 from pg_constraint where conname = 'feedback_message_len') then
    alter table public.feedback
      add constraint feedback_message_len check (char_length(message) <= 2000) not valid;
  end if;
  if not exists (select 1 from pg_constraint where conname = 'feedback_username_len') then
    alter table public.feedback
      add constraint feedback_username_len check (username is null or char_length(username) <= 20) not valid;
  end if;
end $$;


-- ════════════════════════════════════════════════════════════════════════════
-- 6. TRIGGER-FUNKTIONEN
-- ════════════════════════════════════════════════════════════════════════════

-- 6a. updated_at frisch halten (nur passport_stamps hat diese Spalte)
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists stamps_updated_at on public.passport_stamps;
create trigger stamps_updated_at
  before update on public.passport_stamps
  for each row execute procedure public.touch_updated_at();


-- 6b. Auto-Profil bei Registrierung (auth.users AFTER INSERT)
--     username aus raw_user_meta_data->>'username' sonst Local-Part der E-Mail.
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, username)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1))
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();


-- ════════════════════════════════════════════════════════════════════════════
-- 7. RPCs  (alle SECURITY DEFINER; Param-Namen exakt wie in gen.py)
-- ════════════════════════════════════════════════════════════════════════════

-- 7a. add_score({p_user_id, p_score, p_coins, p_rounds, p_duration_ms})
--     -> addiert Score + Coins atomar, zaehlt games_played hoch. returns void.
--     Sanfte Anti-Cheat-Schranken (nur bei p_rounds >= 1, damit die
--     Offline-Queue mit p_rounds:0 nicht faelschlich blockiert wird).
create or replace function public.add_score(
  p_user_id     uuid,
  p_score       int,
  p_coins       int    default 0,
  p_rounds      int    default 10,
  p_duration_ms bigint default 0
)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  -- sanfter Auth-Guard: falls eingeloggt, muss die eigene ID gemeint sein
  if auth.uid() is not null and auth.uid() <> p_user_id then
    raise exception 'Unauthorized: caller % <> user %', auth.uid(), p_user_id;
  end if;

  if p_score < 0 then p_score := 0; end if;
  if p_coins < 0 then p_coins := 0; end if;

  -- Anti-Cheat nur bei vollstaendiger Rundenangabe
  if p_rounds >= 1 then
    if p_duration_ms > 0 and p_duration_ms < p_rounds::bigint * 1500 then
      raise exception 'Cheat detected (zu schnell): % ms fuer % Runden', p_duration_ms, p_rounds;
    end if;
    if p_score > least(p_rounds, 100) * 1800 then
      raise exception 'Cheat detected (Score zu hoch): % > %', p_score, least(p_rounds,100)*1800;
    end if;
  end if;

  update public.profiles
     set total_score  = coalesce(total_score,  0) + p_score,
         games_played = coalesce(games_played, 0) + 1,
         geo_coins    = coalesce(geo_coins,    0) + p_coins
   where id = p_user_id;
end;
$$;


-- 7b. add_coins({p_user_id, p_amount}) -> gibt den NEUEN Coin-Stand zurueck (int).
create or replace function public.add_coins(
  p_user_id uuid,
  p_amount  int
)
returns int
language plpgsql
security definer
set search_path = public
as $$
declare
  v_new int;
begin
  if p_amount < 0 then p_amount := 0; end if;
  update public.profiles
     set geo_coins = coalesce(geo_coins, 0) + p_amount
   where id = p_user_id
   returning geo_coins into v_new;
  return coalesce(v_new, 0);
end;
$$;


-- 7c. spend_coins({p_user_id, p_amount}) -> gibt den NEUEN Coin-Stand zurueck.
--     Bei zu wenig Coins: KEIN Abzug, aktueller Stand wird unveraendert
--     zurueckgegeben (die App uebernimmt den Rueckgabewert 1:1).
create or replace function public.spend_coins(
  p_user_id uuid,
  p_amount  int
)
returns int
language plpgsql
security definer
set search_path = public
as $$
declare
  v_cur int;
begin
  select coalesce(geo_coins, 0) into v_cur
    from public.profiles where id = p_user_id;
  if v_cur is null then
    return 0;                       -- kein Profil
  end if;
  if p_amount is null or p_amount <= 0 then
    return v_cur;                   -- nichts abzuziehen
  end if;
  if v_cur < p_amount then
    return v_cur;                   -- zu wenig Coins -> kein Abzug
  end if;
  update public.profiles
     set geo_coins = v_cur - p_amount
   where id = p_user_id
   returning geo_coins into v_cur;
  return v_cur;
end;
$$;


-- 7d. upsert_stamp({p_user_id, p_country_code, p_perfect})
--     -> Upsert in passport_stamps + Mastery-Neuberechnung. returns void.
--     Schwellen: Bronze>=3v, Silber>=10v+3p, Gold>=25v+10p.
create or replace function public.upsert_stamp(
  p_user_id      uuid,
  p_country_code text,
  p_perfect      boolean default false
)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  rec public.passport_stamps;
  new_mastery smallint;
begin
  insert into public.passport_stamps (user_id, country_code, visits, perfect_rounds)
  values (p_user_id, p_country_code, 1, case when p_perfect then 1 else 0 end)
  on conflict (user_id, country_code) do update
    set visits         = passport_stamps.visits + 1,
        perfect_rounds = passport_stamps.perfect_rounds + (case when p_perfect then 1 else 0 end),
        updated_at     = now()
  returning * into rec;

  new_mastery := 0;
  if rec.visits >= 3  then new_mastery := 1; end if;
  if rec.visits >= 10 and rec.perfect_rounds >= 3  then new_mastery := 2; end if;
  if rec.visits >= 25 and rec.perfect_rounds >= 10 then new_mastery := 3; end if;

  if new_mastery <> rec.mastery_level then
    update public.passport_stamps
       set mastery_level = new_mastery
     where id = rec.id;
  end if;
end;
$$;


-- 7e. get_prev_week_rank({p_user_id})
--     -> json {score, rank, total} fuer die Vorwoche (aus game_sessions).
create or replace function public.get_prev_week_rank(p_user_id uuid)
returns json
language plpgsql
security definer
set search_path = public
as $$
declare
  v_wk_start timestamptz := date_trunc('week', now() at time zone 'UTC') - interval '7 days';
  v_wk_end   timestamptz := date_trunc('week', now() at time zone 'UTC');
  v_my_score bigint := 0;
  v_rank     int    := 1;
  v_total    int    := 0;
begin
  select coalesce(sum(score), 0)
    into v_my_score
    from public.game_sessions
   where user_id    = p_user_id
     and created_at >= v_wk_start
     and created_at <  v_wk_end;

  with weekly as (
    select user_id, sum(score) as ws
      from public.game_sessions
     where created_at >= v_wk_start
       and created_at <  v_wk_end
     group by user_id
  )
  select
    coalesce((select count(*) + 1 from weekly where ws > v_my_score), 1),
    coalesce((select count(*)      from weekly), 0)
    into v_rank, v_total;

  return json_build_object('score', v_my_score, 'rank', v_rank, 'total', v_total);
end;
$$;


-- 7f. update_league({p_user_id, p_new_league, p_eval_week})
--     -> schreibt current_league + last_eval_week atomar. returns void.
create or replace function public.update_league(
  p_user_id    uuid,
  p_new_league text,
  p_eval_week  text
)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  update public.profiles
     set current_league = p_new_league,
         last_eval_week = p_eval_week
   where id = p_user_id;
end;
$$;


-- ════════════════════════════════════════════════════════════════════════════
-- 8. VIEW: leaderboard_weekly   (von gen.py fetchLeaderboard gelesen)
-- ----------------------------------------------------------------------------
-- gen.py: sb.from("leaderboard_weekly").select("*").eq("mode",mode)
--                                       .order("rank").limit(30)
-- renderLeaderboard nutzt pro Zeile: mode, user_id, username, best_score, rank.
-- Bester Score pro (mode,user) in der laufenden ISO-Woche, Rang je Modus.
-- Die View laeuft als Definer (Owner) -> umgeht RLS gezielt fuer die
-- oeffentliche Bestenliste, exponiert aber NUR unkritische Felder
-- (kein E-Mail, kein total_score/coins) -> kein RLS-Leck wie das alte B1.
-- ════════════════════════════════════════════════════════════════════════════
create or replace view public.leaderboard_weekly as
with weekly as (
  select gs.mode,
         gs.user_id,
         max(gs.score) as best_score
    from public.game_sessions gs
   where gs.user_id is not null
     and gs.created_at >= date_trunc('week', now() at time zone 'UTC')
     and gs.created_at <  date_trunc('week', now() at time zone 'UTC') + interval '7 days'
   group by gs.mode, gs.user_id
)
select
  w.mode,
  w.user_id,
  coalesce(p.username, 'Anonym') as username,
  w.best_score,
  row_number() over (partition by w.mode order by w.best_score desc) as rank
from weekly w
left join public.profiles p on p.id = w.user_id;


-- ════════════════════════════════════════════════════════════════════════════
-- 9. ROW-LEVEL SECURITY  (auf allen Tabellen aktiv; Zugriff nur ueber RPCs
--    bzw. eigene Zeile; Score/Coins-Writes laufen ausschliesslich ueber die
--    SECURITY-DEFINER-RPCs).
-- ════════════════════════════════════════════════════════════════════════════

-- ── profiles ────────────────────────────────────────────────────────────────
alter table public.profiles enable row level security;

drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
  on public.profiles for select using (auth.uid() = id);

drop policy if exists "profiles_insert_own" on public.profiles;
create policy "profiles_insert_own"
  on public.profiles for insert with check (auth.uid() = id);

drop policy if exists "profiles_update_own" on public.profiles;
create policy "profiles_update_own"
  on public.profiles for update
  using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists "profiles_delete_own" on public.profiles;
create policy "profiles_delete_own"
  on public.profiles for delete using (auth.uid() = id);
-- Bewusst KEINE "using(true)"-Lesepolicy auf profiles (altes RLS-Leck B1).
-- Bestenliste laeuft ueber die eingeschraenkte View leaderboard_weekly.

-- ── game_sessions ───────────────────────────────────────────────────────────
alter table public.game_sessions enable row level security;

drop policy if exists "sessions_insert_own" on public.game_sessions;
create policy "sessions_insert_own"
  on public.game_sessions for insert with check (auth.uid() = user_id);

drop policy if exists "sessions_select_own" on public.game_sessions;
create policy "sessions_select_own"
  on public.game_sessions for select using (auth.uid() = user_id);

-- ── passport_stamps ─────────────────────────────────────────────────────────
alter table public.passport_stamps enable row level security;

drop policy if exists "stamps_owner_all" on public.passport_stamps;
create policy "stamps_owner_all"
  on public.passport_stamps for all
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ── user_stamps ─────────────────────────────────────────────────────────────
alter table public.user_stamps enable row level security;

drop policy if exists "user_stamps_owner_all" on public.user_stamps;
create policy "user_stamps_owner_all"
  on public.user_stamps for all
  using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ── stamps (oeffentliche Lookup-Tabelle, nicht sensibel) ─────────────────────
alter table public.stamps enable row level security;

drop policy if exists "stamps_public_read" on public.stamps;
create policy "stamps_public_read"
  on public.stamps for select using (true);

-- ── feedback ────────────────────────────────────────────────────────────────
alter table public.feedback enable row level security;

drop policy if exists "feedback_insert_all" on public.feedback;
create policy "feedback_insert_all"
  on public.feedback for insert with check (true);

drop policy if exists "feedback_select_own" on public.feedback;
create policy "feedback_select_own"
  on public.feedback for select using (auth.uid() = user_id);

-- Admin liest alles ueber app_metadata.admin (NICHT vom User editierbar).
drop policy if exists "feedback_select_admin" on public.feedback;
create policy "feedback_select_admin"
  on public.feedback for select using (
    coalesce((auth.jwt() -> 'app_metadata' ->> 'admin')::boolean, false)
  );


-- ════════════════════════════════════════════════════════════════════════════
-- 10. GRANTS  (PostgREST-Zugriff via anon/authenticated; RLS bleibt aktiv)
-- ════════════════════════════════════════════════════════════════════════════
grant usage on schema public to anon, authenticated;

-- Tabellen
grant select, insert, update, delete on public.profiles        to authenticated;
grant select, insert                 on public.game_sessions    to authenticated;
grant select, insert, update, delete on public.passport_stamps to authenticated;
grant select, insert, update, delete on public.user_stamps      to authenticated;
grant select                         on public.stamps           to anon, authenticated;
grant select, insert                 on public.feedback         to anon, authenticated;

-- View (Bestenliste): oeffentlich lesbar
grant select on public.leaderboard_weekly to anon, authenticated;

-- RPCs
grant execute on function public.add_score(uuid, int, int, int, bigint) to anon, authenticated;
grant execute on function public.add_coins(uuid, int)                    to anon, authenticated;
grant execute on function public.spend_coins(uuid, int)                  to anon, authenticated;
grant execute on function public.upsert_stamp(uuid, text, boolean)       to anon, authenticated;
grant execute on function public.get_prev_week_rank(uuid)                to anon, authenticated;
grant execute on function public.update_league(uuid, text, text)         to anon, authenticated;


-- ════════════════════════════════════════════════════════════════════════════
-- 11. PostgREST Schema-Cache neu laden (damit RPCs/Embeds sofort greifen)
-- ════════════════════════════════════════════════════════════════════════════
notify pgrst, 'reload schema';

-- Fertig ✓
-- ----------------------------------------------------------------------------
-- HINWEISE / ANNAHMEN (siehe Zusammenfassung im Chat):
--  1) plates_collected ist TEXT (nicht jsonb) — die App speichert/liest einen
--     JSON-String. ARCHITECTURE.md §10 nennt jsonb; gen.py ist massgeblich.
--  2) Liga-Spalten heissen current_league (text) + last_eval_week (text),
--     NICHT league_id/league_score (die stehen in §10, werden aber von gen.py
--     nicht benutzt). Falls doch benoetigt, koennen sie ergaenzt werden.
--  3) Reisepass-Lese/Schreib-Inkonsistenz der App: upsert_stamp schreibt in
--     passport_stamps, die Anzeige liest aber user_stamps+stamps. Beide Pfade
--     sind angelegt; user_stamps/stamps bleiben leer, bis die App vereinheitlicht
--     wird. Die Anzeige gefuellter Stempel erfordert diesen App-Fix.
--  4) Admin-Feedback-Lesen setzt raw_app_meta_data {"admin": true} am Account
--     voraus (separat setzen). daily_challenges-Tabelle wurde weggelassen, da
--     die Daily Challenge rein clientseitig berechnet wird.
-- ----------------------------------------------------------------------------
