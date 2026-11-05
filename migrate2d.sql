-- Shared Planner — additive migration (SAFE, no data loss).
-- Brings the live DB up to date: notes board, shared focus timer, waves (presence pings).
-- The tasks.due_time column is added by migrate2d.sh (ALTER can't use IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS notes (
  id         TEXT PRIMARY KEY,
  text       TEXT,
  color      TEXT,
  owner      TEXT,
  date       TEXT,
  created_at INTEGER
);

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

-- one shared "wave" ping (a heart/emoji sent to each other); single row id='latest'
CREATE TABLE IF NOT EXISTS waves (
  id         TEXT PRIMARY KEY,
  emoji      TEXT,
  sender     TEXT,
  created_at INTEGER
);
