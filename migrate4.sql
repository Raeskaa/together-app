-- Shared Planner — accounts + points (ADDITIVE, no data loss). Run by migrate4.sh after its columns are added. Safe to re-run.
-- people get their own sign-in; tasks remember who finished them and when; finished focus sessions are logged.

CREATE TABLE IF NOT EXISTS login_attempts (
  key          TEXT PRIMARY KEY,  -- u:<username> | pc:<ip>
  fails        INTEGER,
  locked_until INTEGER
);

CREATE TABLE IF NOT EXISTS focus_log (
  id         TEXT PRIMARY KEY,  -- <space>_<ends_at>_<person>, so a session is logged once
  space_id   TEXT,
  person_id  TEXT,
  minutes    INTEGER,
  label      TEXT,
  ended_at   INTEGER
);

CREATE UNIQUE INDEX IF NOT EXISTS people_username ON people(username);
