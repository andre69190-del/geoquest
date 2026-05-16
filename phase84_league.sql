-- ============================================================
-- Phase 84: Kompetitives Wochen-Liga-System
-- In Supabase SQL Editor ausführen
-- ============================================================

-- 1. Spalten zur profiles-Tabelle hinzufügen
ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS current_league  VARCHAR(20) DEFAULT 'Bronze',
  ADD COLUMN IF NOT EXISTS last_eval_week  VARCHAR(10) DEFAULT '';

-- Index für Liga-Abfragen
CREATE INDEX IF NOT EXISTS idx_profiles_league ON profiles(current_league);


-- ============================================================
-- 2. RPC: Vorwoche-Rang des Spielers ermitteln
--    Gibt score, rank und total zurück.
--    rank  = wie viele Spieler hatten MEHR Punkte (1-basiert)
--    total = wie viele Spieler haben überhaupt gespielt
-- ============================================================
CREATE OR REPLACE FUNCTION get_prev_week_rank(p_user_id UUID)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_wk_start  TIMESTAMPTZ := date_trunc('week', now() AT TIME ZONE 'UTC') - INTERVAL '7 days';
  v_wk_end    TIMESTAMPTZ := date_trunc('week', now() AT TIME ZONE 'UTC');
  v_my_score  BIGINT      := 0;
  v_rank      INT         := 1;
  v_total     INT         := 0;
BEGIN
  -- Gesamtpunkte des Spielers in der Vorwoche
  SELECT COALESCE(SUM(score), 0)
    INTO v_my_score
    FROM game_sessions
   WHERE user_id    = p_user_id
     AND created_at >= v_wk_start
     AND created_at <  v_wk_end;

  -- Globaler Rang (Spieler mit MEHR Punkten zählen als Rank-Vorgänger)
  WITH weekly AS (
    SELECT user_id, SUM(score) AS ws
      FROM game_sessions
     WHERE created_at >= v_wk_start
       AND created_at <  v_wk_end
     GROUP BY user_id
  )
  SELECT
    COALESCE((SELECT COUNT(*) + 1 FROM weekly WHERE ws > v_my_score), 1),
    COALESCE((SELECT COUNT(*) FROM weekly), 0)
  INTO v_rank, v_total;

  RETURN json_build_object(
    'score', v_my_score,
    'rank',  v_rank,
    'total', v_total
  );
END;
$$;

-- Berechtigungen für angemeldete Nutzer
GRANT EXECUTE ON FUNCTION get_prev_week_rank(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION get_prev_week_rank(UUID) TO anon;


-- ============================================================
-- 3. RPC: update_league  (atomisch, verhindert Race Conditions)
--    Schreibt current_league + last_eval_week in einem Schritt
-- ============================================================
CREATE OR REPLACE FUNCTION update_league(
  p_user_id       UUID,
  p_new_league    VARCHAR,
  p_eval_week     VARCHAR
)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  UPDATE profiles
     SET current_league = p_new_league,
         last_eval_week = p_eval_week
   WHERE id = p_user_id;
END;
$$;

GRANT EXECUTE ON FUNCTION update_league(UUID, VARCHAR, VARCHAR) TO authenticated;
GRANT EXECUTE ON FUNCTION update_league(UUID, VARCHAR, VARCHAR) TO anon;


-- ============================================================
-- 4. Bestehende Benutzer: Bronze-Liga als Default setzen
--    (falls current_league noch NULL ist)
-- ============================================================
UPDATE profiles
   SET current_league = 'Bronze'
 WHERE current_league IS NULL OR current_league = '';
