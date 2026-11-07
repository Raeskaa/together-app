-- Shared Planner — spaces (ADDITIVE, no data loss). Run by migrate3.sh after the space_id columns are added.
-- People belong to spaces; every project, task, habit, note, topic and journal entry lives in one space.
-- Today's two-person data moves into one space, "hate club" (kind partner). Safe to re-run.

CREATE TABLE IF NOT EXISTS people (
  id         TEXT PRIMARY KEY,  -- p_…
  name       TEXT,
  color      TEXT,
  created_at INTEGER
);
CREATE TABLE IF NOT EXISTS spaces (
  id         TEXT PRIMARY KEY,  -- s_…
  name       TEXT,
  kind       TEXT,              -- partner | friends | team | solo
  created_at INTEGER
);
CREATE TABLE IF NOT EXISTS members (
  id         TEXT PRIMARY KEY,  -- <space_id>:<person_id>
  space_id   TEXT,
  person_id  TEXT,
  role       TEXT,              -- owner | member
  joined_at  INTEGER
);

-- the two people, named from the old settings keys
INSERT OR IGNORE INTO people (id,name,color,created_at) VALUES
  ('p_mahesh',  COALESCE(NULLIF((SELECT value FROM settings WHERE key='meName'),''),'Mahesh'),       '#15171A', 1762560000000),
  ('p_partner', COALESCE(NULLIF((SELECT value FROM settings WHERE key='partnerName'),''),'Partner'), '#5B6B86', 1762560000001);
INSERT OR IGNORE INTO spaces (id,name,kind,created_at) VALUES ('s_hateclub','hate club','partner',1762560000000);
INSERT OR IGNORE INTO members (id,space_id,person_id,role,joined_at) VALUES
  ('s_hateclub:p_mahesh','s_hateclub','p_mahesh','owner',1762560000000),
  ('s_hateclub:p_partner','s_hateclub','p_partner','member',1762560000001);

-- everything that exists today lives in that space
UPDATE projects SET space_id='s_hateclub' WHERE space_id IS NULL OR space_id='';
UPDATE tasks    SET space_id='s_hateclub' WHERE space_id IS NULL OR space_id='';
UPDATE habits   SET space_id='s_hateclub' WHERE space_id IS NULL OR space_id='';
UPDATE notes    SET space_id='s_hateclub' WHERE space_id IS NULL OR space_id='';
UPDATE topics   SET space_id='s_hateclub' WHERE space_id IS NULL OR space_id='';
UPDATE journal  SET space_id='s_hateclub' WHERE space_id IS NULL OR space_id='';

-- owners become people (or everyone); only old values are touched, so a re-run changes nothing
UPDATE projects SET owner=CASE owner WHEN 'me' THEN 'p_mahesh' WHEN 'partner' THEN 'p_partner' ELSE 'everyone' END WHERE owner IN ('me','partner','shared') OR owner IS NULL OR owner='';
UPDATE tasks    SET owner=CASE owner WHEN 'me' THEN 'p_mahesh' WHEN 'partner' THEN 'p_partner' ELSE 'everyone' END WHERE owner IN ('me','partner','shared') OR owner IS NULL OR owner='';
UPDATE habits   SET owner=CASE owner WHEN 'me' THEN 'p_mahesh' WHEN 'partner' THEN 'p_partner' ELSE 'everyone' END WHERE owner IN ('me','partner','shared') OR owner IS NULL OR owner='';
UPDATE notes    SET owner=CASE owner WHEN 'me' THEN 'p_mahesh' WHEN 'partner' THEN 'p_partner' ELSE 'everyone' END WHERE owner IN ('me','partner','shared') OR owner IS NULL OR owner='';
UPDATE topics   SET owner=CASE owner WHEN 'me' THEN 'p_mahesh' WHEN 'partner' THEN 'p_partner' ELSE 'everyone' END WHERE owner IN ('me','partner','shared') OR owner IS NULL OR owner='';
UPDATE journal  SET owner=CASE owner WHEN 'me' THEN 'p_mahesh' WHEN 'partner' THEN 'p_partner' ELSE owner END WHERE owner IN ('me','partner');
-- journal ids are <date>_<owner>
UPDATE journal SET id = date || '_' || owner WHERE id = date || '_me' OR id = date || '_partner';

-- the shared focus timer and the wave become one row per space
INSERT OR IGNORE INTO focus (id,status,label,minutes,ends_at,remaining,started_by,updated_at)
  SELECT 's_hateclub',status,label,minutes,ends_at,remaining,started_by,updated_at FROM focus WHERE id='shared';
INSERT OR IGNORE INTO focus (id,status,label,minutes,ends_at,remaining,started_by,updated_at)
  VALUES ('s_hateclub','idle','',25,0,0,'',0);
DELETE FROM focus WHERE id='shared';
UPDATE focus SET started_by=CASE started_by WHEN 'me' THEN 'p_mahesh' ELSE 'p_partner' END WHERE started_by IN ('me','partner');
INSERT OR IGNORE INTO waves (id,emoji,sender,created_at) SELECT 's_hateclub',emoji,sender,created_at FROM waves WHERE id='latest';
DELETE FROM waves WHERE id='latest';
UPDATE waves SET sender=CASE sender WHEN 'me' THEN 'p_mahesh' ELSE 'p_partner' END WHERE sender IN ('me','partner');
