-- Shared Planner — Phase 2b additive migration: configurable habits + weekly topics.
-- Safe + additive: creates new tables, seeds the 3 starter habits. Does NOT touch existing data.

CREATE TABLE IF NOT EXISTS habits (
  id         TEXT PRIMARY KEY,
  name       TEXT,
  kind       TEXT,              -- check | count
  owner      TEXT,              -- me | partner | shared
  unit       TEXT,
  target     INTEGER,
  caption    TEXT,
  color      TEXT,
  sort       INTEGER,
  archived   INTEGER DEFAULT 0,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS topics (
  id         TEXT PRIMARY KEY,
  week       TEXT,              -- YYYY-MM-DD (week's Sunday)
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

-- starter habits (ids match the previous fixed keys so any old logs line up). Editable/deletable.
INSERT OR IGNORE INTO habits (id,name,kind,owner,unit,target,caption,color,sort,created_at) VALUES
  ('cigs','Cigarettes','count','me','cigs',76,'4 → 1 pack by 30 Nov','#C2704B',1,1762050000000),
  ('read','Read · 1 hour','check','me','',NULL,'Build the streak','#1F6FEB',2,1762050000001),
  ('art','Art & posting','check','me','',NULL,'','#2E9E6B',3,1762050000002);
