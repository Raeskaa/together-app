-- Shared Planner — migrate the existing remote D1 to v2 and blank the slate.
-- (The two ALTER TABLE adds are run from migrate.sh so a re-run doesn't abort.)

CREATE TABLE IF NOT EXISTS project_materials (
  id         TEXT PRIMARY KEY,
  project_id TEXT,
  title      TEXT,
  url        TEXT,
  sort       INTEGER,
  created_at INTEGER
);

-- blank slate (keeps settings / names)
DELETE FROM tasks;
DELETE FROM projects;
DELETE FROM project_materials;
DELETE FROM habit_logs;
DELETE FROM journal;
DELETE FROM routines;
DELETE FROM deadlines;

UPDATE settings SET value='' WHERE key='weekTopic';
