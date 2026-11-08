-- Shared Planner — D1 schema v3 (spaces). Blank slate: settings, two people, one space, starter habits.
-- People belong to spaces (members). Every project, task, habit, note, topic and journal entry has a space_id.
-- Owners are a person id (p_…) or 'everyone'.

CREATE TABLE IF NOT EXISTS people (id TEXT PRIMARY KEY, name TEXT, color TEXT, created_at INTEGER, username TEXT, pass_hash TEXT, pass_salt TEXT, pass_iter INTEGER);
CREATE UNIQUE INDEX IF NOT EXISTS people_username ON people(username);
CREATE TABLE IF NOT EXISTS login_attempts (key TEXT PRIMARY KEY, fails INTEGER, locked_until INTEGER);
CREATE TABLE IF NOT EXISTS focus_log (id TEXT PRIMARY KEY, space_id TEXT, person_id TEXT, minutes INTEGER, label TEXT, ended_at INTEGER);
CREATE TABLE IF NOT EXISTS spaces (id TEXT PRIMARY KEY, name TEXT, kind TEXT, created_at INTEGER);  -- kind: partner | friends | team | solo
CREATE TABLE IF NOT EXISTS members (id TEXT PRIMARY KEY, space_id TEXT, person_id TEXT, role TEXT, joined_at INTEGER);  -- id = <space_id>:<person_id>

CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);

CREATE TABLE IF NOT EXISTS projects (
  id         TEXT PRIMARY KEY,
  name       TEXT,
  color      TEXT,
  owner      TEXT,              -- person id | everyone
  kind       TEXT,              -- plain | course | branding
  start_date TEXT,
  end_date   TEXT,
  description TEXT,
  archived   INTEGER DEFAULT 0,
  sort       INTEGER,
  created_at INTEGER,
  space_id   TEXT
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
  owner      TEXT,              -- person id | everyone
  type       TEXT,              -- task | event
  date       TEXT,              -- YYYY-MM-DD (when planned / event day)
  time       TEXT,              -- events
  due        TEXT,              -- deadline date (optional)
  due_time   TEXT,              -- deadline time of day (optional, HH:MM)
  done       INTEGER,           -- 0/1
  subtodos   TEXT,              -- legacy JSON (unused in v2; subtasks are child rows)
  parent_id  TEXT,              -- set => this row is a subtask of parent_id
  sort       INTEGER,
  created_at INTEGER,
  space_id   TEXT,
  done_at    INTEGER,           -- when it was ticked (set by the server)
  done_by    TEXT               -- who ticked it (set by the server)
);

CREATE TABLE IF NOT EXISTS journal (
  id         TEXT PRIMARY KEY,  -- <date>_<owner>
  date       TEXT,
  owner      TEXT,
  text       TEXT,
  tag        TEXT,
  updated_at INTEGER,
  space_id   TEXT
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
  owner      TEXT,              -- person id | everyone
  unit       TEXT,              -- count: label e.g. "cigs"
  target     INTEGER,           -- count: daily aim
  caption    TEXT,              -- small subtitle, e.g. "4 -> 1 pack by 30 Nov"
  color      TEXT,
  sort       INTEGER,
  archived   INTEGER DEFAULT 0,
  created_at INTEGER,
  space_id   TEXT
);

CREATE TABLE IF NOT EXISTS topics (
  id         TEXT PRIMARY KEY,
  week       TEXT,              -- YYYY-MM-DD (the week's Sunday)
  title      TEXT,
  owner      TEXT,
  notes      TEXT,
  sort       INTEGER,
  created_at INTEGER,
  space_id   TEXT
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
  created_at INTEGER,
  space_id   TEXT
);

-- one shared focus/pomodoro timer per space (row id = the space id)
CREATE TABLE IF NOT EXISTS focus (
  id         TEXT PRIMARY KEY,  -- the space id
  status     TEXT,              -- idle | running | paused
  label      TEXT,              -- what we're working on
  minutes    INTEGER,           -- total length of this session
  ends_at    INTEGER,           -- epoch ms when it finishes (while running)
  remaining  INTEGER,           -- ms left (while paused)
  started_by TEXT,              -- person id
  updated_at INTEGER
);
INSERT OR IGNORE INTO focus (id,status,label,minutes,ends_at,remaining,started_by,updated_at)
  VALUES ('s_hateclub','idle','',25,0,0,'',0);

-- one "wave" ping per space (a heart/emoji sent to each other); row id = the space id
CREATE TABLE IF NOT EXISTS waves (
  id         TEXT PRIMARY KEY,  -- the space id
  emoji      TEXT,
  sender     TEXT,              -- person id
  created_at INTEGER
);

-- seed: the two people in one space + the three starter habits (editable/deletable). Everything else blank.
INSERT OR IGNORE INTO people (id,name,color,created_at) VALUES ('p_mahesh','Mahesh','#15171A',1762560000000),('p_partner','Partner','#5B6B86',1762560000001);
INSERT OR IGNORE INTO spaces (id,name,kind,created_at) VALUES ('s_hateclub','hate club','partner',1762560000000);
INSERT OR IGNORE INTO members (id,space_id,person_id,role,joined_at) VALUES ('s_hateclub:p_mahesh','s_hateclub','p_mahesh','owner',1762560000000),('s_hateclub:p_partner','s_hateclub','p_partner','member',1762560000001);
INSERT OR IGNORE INTO settings (key,value) VALUES
  ('meName','Mahesh'),
  ('partnerName','Partner'),
  ('weekTopic',''),
  ('cigAimToday','76');

INSERT OR IGNORE INTO habits (id,name,kind,owner,unit,target,caption,color,sort,created_at,space_id) VALUES
  ('cigs','Cigarettes','count','p_mahesh','cigs',76,'4 → 1 pack by 30 Nov','#C2704B',1,1762050000000,'s_hateclub'),
  ('read','Read · 1 hour','check','p_mahesh','',NULL,'Build the streak','#1F6FEB',2,1762050000001,'s_hateclub'),
  ('art','Art & posting','check','p_mahesh','',NULL,'','#2E9E6B',3,1762050000002,'s_hateclub');

-- Claude's private link per person (ver bumps to kill old links)
CREATE TABLE IF NOT EXISTS claude_links (person_id TEXT PRIMARY KEY, ver INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 0, created_at INTEGER, last_used_at INTEGER, last_action TEXT);
