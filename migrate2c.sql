-- Shared Planner — additive migration: a notes board (multiple colored notes per person).
-- Safe + additive: creates the notes table only. Touches nothing else.

CREATE TABLE IF NOT EXISTS notes (
  id         TEXT PRIMARY KEY,
  text       TEXT,
  color      TEXT,
  owner      TEXT,
  date       TEXT,
  created_at INTEGER
);

-- one shared focus/pomodoro timer both people see live (single row id='shared')
CREATE TABLE IF NOT EXISTS focus (
  id         TEXT PRIMARY KEY,
  status     TEXT,
  label      TEXT,
  minutes    INTEGER,
  ends_at    INTEGER,
  remaining  INTEGER,
  started_by TEXT,
  updated_at INTEGER
);
INSERT OR IGNORE INTO focus (id,status,label,minutes,ends_at,remaining,started_by,updated_at)
  VALUES ('shared','idle','',25,0,0,'',0);
