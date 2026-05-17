-- Phase 93: plates_collected column
-- Run this once in your Supabase SQL Editor (or via MCP below)
-- Safe to run multiple times (IF NOT EXISTS).

ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS plates_collected TEXT DEFAULT '[]';

-- Optional: backfill existing rows to an empty JSON array
UPDATE profiles
  SET plates_collected = '[]'
  WHERE plates_collected IS NULL;
