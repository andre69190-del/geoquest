-- Phase 256: feedback-Tabelle für In-App Vorschläge
-- In Supabase SQL Editor ausführen

CREATE TABLE IF NOT EXISTS public.feedback (
  id           uuid        DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at   timestamptz DEFAULT now() NOT NULL,
  category     text        NOT NULL,       -- 'vorschlag'|'inhalt'|'bug'|'lob'|'sonstiges'
  message      text        NOT NULL,
  mode         text,                       -- aktueller Spielmodus (kann null sein)
  user_id      uuid        REFERENCES auth.users(id) ON DELETE SET NULL,
  username     text,
  lang         text        DEFAULT 'de',
  app_version  text
);

ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;

-- Jeder (auch ohne Account) darf Feedback eintragen
CREATE POLICY "feedback_insert_all" ON public.feedback
  FOR INSERT WITH CHECK (true);

-- Nur der eigene Nutzer darf seine Einträge lesen
CREATE POLICY "feedback_select_own" ON public.feedback
  FOR SELECT USING (auth.uid() = user_id OR auth.uid() IS NULL);

-- Admin (du) liest alles — ersetze die E-Mail falls nötig
CREATE POLICY "feedback_select_admin" ON public.feedback
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND username = 'Andre'
    )
  );

-- Index für schnelle Admin-Abfragen
CREATE INDEX IF NOT EXISTS feedback_created_at_idx ON public.feedback (created_at DESC);
CREATE INDEX IF NOT EXISTS feedback_category_idx   ON public.feedback (category);
