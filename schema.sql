-- Shared Planner — D1 schema v2 (Calendar + Projects). Blank slate: settings-only seed.

CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE IF NOT EXISTS projects (
  id         TEXT PRIMARY KEY,
  name       TEXT,
  color      TEXT,
  owner      TEXT,              -- me | partner | shared
  kind       TEXT,              -- plain | course | branding
  start_date TEXT,
  end_date   TEXT,
  description TEXT,
  archived   INTEGER DEFAULT 0,
  sort       INTEGER,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS project_materials (
  id         TEXT PRIMARY KEY,
  project_id TEXT,
  title      TEXT,
  url        TEXT,
  sort       INTEGER,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS routines (
  id      TEXT PRIMARY KEY,
  title   TEXT,
  "start" TEXT,
  "end"   TEXT,
  owner   TEXT,
  days    TEXT,
  note    TEXT,
  sort    INTEGER
);

CREATE TABLE IF NOT EXISTS tasks (
  id         TEXT PRIMARY KEY,
  title      TEXT,
  project    TEXT,              -- project id (optional)
  owner      TEXT,              -- me | partner | shared
  type       TEXT,              -- task | event
  date       TEXT,              -- YYYY-MM-DD (when planned / event day)
  time       TEXT,              -- events
  due        TEXT,              -- deadline date (optional)
  due_time   TEXT,              -- deadline time of day (optional, HH:MM)
  done       INTEGER,           -- 0/1
  subtodos   TEXT,              -- legacy JSON (unused in v2; subtasks are child rows)
  parent_id  TEXT,              -- set => this row is a subtask of parent_id
  sort       INTEGER,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS journal (
  id         TEXT PRIMARY KEY,  -- <date>_<owner>
  date       TEXT,
  owner      TEXT,
  text       TEXT,
  tag        TEXT,
  updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS habit_logs (
  date  TEXT,
  habit TEXT,                   -- habit id
  value INTEGER,                -- count value, or 0/1 for a check
  PRIMARY KEY (date, habit)
);

CREATE TABLE IF NOT EXISTS habits (
  id         TEXT PRIMARY KEY,
  name       TEXT,
  kind       TEXT,              -- check | count
  owner      TEXT,              -- me | partner | shared
  unit       TEXT,              -- count: label e.g. "cigs"
  target     INTEGER,           -- count: daily aim
  caption    TEXT,              -- small subtitle, e.g. "4 -> 1 pack by 30 Nov"
  color      TEXT,
  sort       INTEGER,
  archived   INTEGER DEFAULT 0,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS topics (
  id         TEXT PRIMARY KEY,
  week       TEXT,              -- YYYY-MM-DD (the week's Sunday)
  title      TEXT,
  owner      TEXT,
  notes      TEXT,
  sort       INTEGER,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS topic_links (
  id         TEXT PRIMARY KEY,
  topic_id   TEXT,
  title      TEXT,
  url        TEXT,
  sort       INTEGER,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS notes (
  id         TEXT PRIMARY KEY,
  text       TEXT,
  color      TEXT,              -- yellow | pink | blue | green | purple | peach
  owner      TEXT,
  date       TEXT,              -- YYYY-MM-DD the note was jotted
  created_at INTEGER
);

-- one shared focus/pomodoro timer both people see live (single row id='shared')
CREATE TABLE IF NOT EXISTS focus (
  id         TEXT PRIMARY KEY,  -- always 'shared'
  status     TEXT,              -- idle | running | paused
  label      TEXT,              -- what we're working on
  minutes    INTEGER,           -- total length of this session
  ends_at    INTEGER,           -- epoch ms when it finishes (while running)
  remaining  INTEGER,           -- ms left (while paused)
  started_by TEXT,              -- me | partner
  updated_at INTEGER
);
INSERT OR IGNORE INTO focus (id,status,label,minutes,ends_at,remaining,started_by,updated_at)
  VALUES ('shared','idle','',25,0,0,'',0);

-- one shared "wave" ping (a heart/emoji sent to each other); single row id='latest'
CREATE TABLE IF NOT EXISTS waves (
  id         TEXT PRIMARY KEY,  -- always 'latest'
  emoji      TEXT,
  sender     TEXT,              -- me | partner
  created_at INTEGER
);

-- seed: names + the three starter habits (editable/deletable). Everything else blank.
INSERT OR IGNORE INTO settings (key,value) VALUES
  ('meName','Mahesh'),
  ('partnerName','Partner'),
  ('weekTopic',''),
  ('cigAimToday','76');

INSERT OR IGNORE INTO habits (id,name,kind,owner,unit,target,caption,color,sort,created_at) VALUES
  ('cigs','Cigarettes','count','me','cigs',76,'4 → 1 pack by 30 Nov','#C2704B',1,1762050000000),
  ('read','Read · 1 hour','check','me','',NULL,'Build the streak','#1F6FEB',2,1762050000001),
  ('art','Art & posting','check','me','',NULL,'',' #2E9E6B',3,1762050000002);
