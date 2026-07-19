-- Phase 584: Security-Fixes für Supabase (im SQL Editor ausführen)
-- Behebt: 1) anonymer Lesezugriff auf ALLE feedback-Einträge
--         2) Admin-Rechte über erratbaren Username 'Andre'
--         3) setzt app_metadata.admin für den Admin-Account (für Client-UI + RLS)

-- ── 1. feedback_select_own reparieren ─────────────────────────────────────
-- Alte Policy erlaubte "OR auth.uid() IS NULL" → jeder anonyme Besucher
-- konnte sämtliche Feedback-Einträge (inkl. Usernamen) lesen.
DROP POLICY IF EXISTS "feedback_select_own" ON public.feedback;
CREATE POLICY "feedback_select_own" ON public.feedback
  FOR SELECT USING (auth.uid() = user_id);

-- ── 2. Admin-Policy an JWT-Claim statt Username binden ────────────────────
-- Alte Policy: username='Andre' in profiles → jeder, der sich 'Andre' nennt
-- (falls der Name je frei wird), hätte Admin-Lesezugriff.
DROP POLICY IF EXISTS "feedback_select_admin" ON public.feedback;
CREATE POLICY "feedback_select_admin" ON public.feedback
  FOR SELECT USING (
    COALESCE((auth.jwt() -> 'app_metadata' ->> 'admin')::boolean, false)
  );

-- ── 3. Admin-Flag setzen (app_metadata ist NICHT vom User editierbar) ─────
-- Client (Phase 584) prüft jetzt sbUser.app_metadata.admin === true.
UPDATE auth.users
SET raw_app_meta_data = COALESCE(raw_app_meta_data, '{}'::jsonb) || '{"admin": true}'::jsonb
WHERE email = 'andre69190@gmail.com';

-- WICHTIG: Danach einmal aus- und wieder einloggen, damit das JWT den
-- neuen app_metadata-Claim enthält.

-- ── 4. Kontrolle ──────────────────────────────────────────────────────────
-- SELECT policyname, cmd, qual FROM pg_policies WHERE tablename = 'feedback';
-- SELECT email, raw_app_meta_data FROM auth.users WHERE email = 'andre69190@gmail.com';

-- Optional (empfohlen): Spam-Schutz für feedback-INSERT, z. B. Rate-Limit
-- über eine Edge Function oder einen einfachen Längen-Check:
-- (NOT VALID = bestehende Zeilen werden nicht geprüft, nur neue)
ALTER TABLE public.feedback
  ADD CONSTRAINT feedback_message_len CHECK (char_length(message) <= 2000) NOT VALID;
ALTER TABLE public.feedback
  ADD CONSTRAINT feedback_username_len CHECK (username IS NULL OR char_length(username) <= 20) NOT VALID;
