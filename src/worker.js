// Shared Planner — Cloudflare Worker: static assets + small JSON API over D1.
import { handleMcp, claudeApi } from './claude.js';
// Two people, one shared space, protected by a shared passcode (signed cookie).

const TABLES = {
  tasks: ['id', 'title', 'project', 'owner', 'type', 'date', 'time', 'due', 'due_time', 'done', 'subtodos', 'parent_id', 'sort', 'created_at', 'space_id', 'done_at', 'done_by'],
  projects: ['id', 'name', 'color', 'owner', 'kind', 'start_date', 'end_date', 'description', 'archived', 'sort', 'created_at', 'space_id'],
  project_materials: ['id', 'project_id', 'title', 'url', 'sort', 'created_at'],
  journal: ['id', 'date', 'owner', 'text', 'tag', 'updated_at', 'space_id'],
  habits: ['id', 'name', 'kind', 'owner', 'unit', 'target', 'caption', 'color', 'sort', 'archived', 'created_at', 'space_id'],
  topics: ['id', 'week', 'title', 'owner', 'notes', 'sort', 'created_at', 'space_id'],
  topic_links: ['id', 'topic_id', 'title', 'url', 'sort', 'created_at'],
  notes: ['id', 'text', 'color', 'owner', 'date', 'created_at', 'space_id'],
  focus: ['id', 'status', 'label', 'minutes', 'ends_at', 'remaining', 'started_by', 'updated_at'],
  waves: ['id', 'emoji', 'sender', 'created_at'],
  people: ['id', 'name', 'color', 'created_at'],
  spaces: ['id', 'name', 'kind', 'created_at'],
  members: ['id', 'space_id', 'person_id', 'role', 'joined_at'],
  focus_log: ['id', 'space_id', 'person_id', 'minutes', 'label', 'ended_at'],
};

// Everything lives in a space. Until there is more than one, rows without one belong to this one.
const DEFAULT_SPACE = 's_hateclub';
// What a tab still running the two-person app writes, and what it means now.
const LEGACY_OWNER = { me: 'p_mahesh', partner: 'p_partner', shared: 'everyone' };
const PERSON_COLS = ['owner', 'sender', 'started_by'];

function normalizeRow(table, row, isNew) {
  const r = { ...row };
  for (const c of PERSON_COLS) if (c in r && r[c] in LEGACY_OWNER) r[c] = LEGACY_OWNER[r[c]];
  // a journal entry without a space is private on purpose; every other row lives in one
  if (isNew && table !== 'journal' && TABLES[table].includes('space_id') && !r.space_id) r.space_id = DEFAULT_SPACE;
  if ((table === 'focus' && r.id === 'shared') || (table === 'waves' && r.id === 'latest')) r.id = DEFAULT_SPACE;
  if (table === 'journal' && typeof r.id === 'string') r.id = r.id.replace(/^(\d{4}-\d{2}-\d{2})_(me|partner)$/, (m, d, o) => d + '_' + LEGACY_OWNER[o]);
  return r;
}
function normalizeId(table, id) {
  if ((table === 'focus' && id === 'shared') || (table === 'waves' && id === 'latest')) return DEFAULT_SPACE;
  if (table === 'journal' && typeof id === 'string') return id.replace(/^(\d{4}-\d{2}-\d{2})_(me|partner)$/, (m, d, o) => d + '_' + LEGACY_OWNER[o]);
  return id;
}
// Old tabs still save names as settings keys; keep the people in step.
function legacyNameStatements(env, patch) {
  const out = [];
  const pairs = [['meName', 'p_mahesh'], ['partnerName', 'p_partner']];
  for (const [k, pid] of pairs) {
    if (patch[k] != null && String(patch[k]).trim()) out.push(env.DB.prepare('UPDATE people SET name=?1 WHERE id=?2').bind(String(patch[k]).trim(), pid));
  }
  return out;
}

const COOKIE = 'sp';
const MAXAGE = 60 * 60 * 24 * 180; // 180 days

function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...headers },
  });
}

const enc = new TextEncoder();
async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(msg));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
// v1.<exp>.<sig> is the old shared-passcode cookie: it can only set up an account.
// v2.<person>.<exp>.<sig> is a signed-in person.
async function makeToken(secret, personId) {
  const exp = Date.now() + MAXAGE * 1000;
  const body = personId ? 'v2.' + personId + '.' + exp : 'v1.' + exp;
  return body + '.' + (await hmac(secret, body));
}
function sameString(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
// null | { person: null } (passcode only) | { person: 'p_…' }
async function readToken(secret, token) {
  if (!token) return null;
  const parts = token.split('.');
  let body, sig, exp, person = null;
  if (parts[0] === 'v1' && parts.length === 3) { exp = Number(parts[1]); body = 'v1.' + parts[1]; sig = parts[2]; }
  else if (parts[0] === 'v2' && parts.length === 4) { person = parts[1]; exp = Number(parts[2]); body = parts.slice(0, 3).join('.'); sig = parts[3]; }
  else return null;
  if (!exp || Date.now() > exp) return null;
  return sameString(await hmac(secret, body), sig) ? { person } : null;
}
function sessionCookie(url, token) {
  const sec = url.protocol === 'https:' ? '; Secure' : '';
  return `${COOKIE}=${token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=${MAXAGE}${sec}`;
}

// ---- passwords: PBKDF2-SHA256 with a random salt per person ----
// 50k rounds is ~4 ms, well inside the Workers free-plan 10 ms CPU budget; stored per person so it can be raised later.
const PBKDF2_ITER = 50000;
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
function unhex(h) { const a = new Uint8Array(h.length / 2); for (let i = 0; i < a.length; i++) a[i] = parseInt(h.substr(i * 2, 2), 16); return a; }
async function hashPassword(password, saltHex, iter) {
  const key = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: unhex(saltHex), iterations: iter }, key, 256);
  return hex(bits);
}
async function newPasswordFields(password) {
  const salt = hex(crypto.getRandomValues(new Uint8Array(16)));
  return { pass_salt: salt, pass_iter: PBKDF2_ITER, pass_hash: await hashPassword(password, salt, PBKDF2_ITER) };
}
const USERNAME_RE = /^[a-z0-9._-]{3,24}$/;
const MIN_PASSWORD = 8;

// ---- too many wrong tries: 5, then a 1-minute wait ----
const LOCK_AFTER = 5;
const LOCK_MS = 60 * 1000;
async function lockOf(env, key) {
  return (await env.DB.prepare('SELECT fails, locked_until FROM login_attempts WHERE key=?1').bind(key).first()) || { fails: 0, locked_until: 0 };
}
async function noteFail(env, key) {
  const st = await lockOf(env, key);
  const fails = (st.fails || 0) + 1;
  const lockedUntil = fails >= LOCK_AFTER ? Date.now() + LOCK_MS : 0;
  await env.DB.prepare('INSERT INTO login_attempts (key,fails,locked_until) VALUES (?1,?2,?3) ON CONFLICT(key) DO UPDATE SET fails=excluded.fails, locked_until=excluded.locked_until')
    .bind(key, lockedUntil ? 0 : fails, lockedUntil).run();
  return lockedUntil ? { locked: true, wait: Math.ceil(LOCK_MS / 1000) } : { left: LOCK_AFTER - fails };
}
async function locked(env, key) {
  const st = await lockOf(env, key);
  return st.locked_until && Date.now() < st.locked_until ? Math.ceil((st.locked_until - Date.now()) / 1000) : 0;
}
const clearFails = (env, key) => env.DB.prepare('DELETE FROM login_attempts WHERE key=?1').bind(key).run();

function cookie(req, name) {
  const c = req.headers.get('cookie') || '';
  const m = c.match(new RegExp('(?:^|; )' + name + '=([^;]+)'));
  return m ? decodeURIComponent(m[1]) : null;
}
function secret(env) {
  return env.SESSION_SECRET || 'dev-only-secret';
}
// what the Claude connector borrows from here
function claudeDeps(env) {
  return { hmac, sameString, secret: secret(env), opStatements };
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    // Claude's private link: /mcp/<token> (or /mcp with a bearer token)
    if (url.pathname === '/mcp' || url.pathname.startsWith('/mcp/')) {
      try {
        return await handleMcp(req, env, url, claudeDeps(env));
      } catch (e) {
        return json({ jsonrpc: '2.0', id: null, error: { code: -32603, message: 'Server error' } }, 500);
      }
    }
    if (url.pathname.startsWith('/api/')) {
      try {
        return await api(req, env, url);
      } catch (e) {
        return json({ error: String((e && e.message) || e) }, 500);
      }
    }
    if (env.ASSETS) return env.ASSETS.fetch(req);
    return new Response('Not found', { status: 404 });
  },
};

async function api(req, env, url) {
  const p = url.pathname;

  const ip = req.headers.get('cf-connecting-ip') || 'local';

  // Sign in with your own username + password.
  if (p === '/api/login' && req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    const username = String(b.username || '').trim().toLowerCase();
    const password = String(b.password || '');
    if (!username || !password) return json({ ok: false, error: 'missing' }, 400);
    const key = 'u:' + username;
    const wait = await locked(env, key);
    if (wait) return json({ ok: false, error: 'locked', wait }, 429);
    const person = await env.DB.prepare('SELECT id, pass_hash, pass_salt, pass_iter FROM people WHERE username=?1').bind(username).first();
    const ok = !!(person && person.pass_hash && sameString(await hashPassword(password, person.pass_salt, person.pass_iter || PBKDF2_ITER), person.pass_hash));
    if (!ok) {
      const f = await noteFail(env, key);
      return json({ ok: false, error: f.locked ? 'locked' : 'wrong', left: f.left || 0, wait: f.wait || 0 }, f.locked ? 429 : 401);
    }
    await clearFails(env, key);
    return json({ ok: true }, 200, { 'set-cookie': sessionCookie(url, await makeToken(secret(env), person.id)) });
  }
  // First time: the shared passcode opens setup (only setup) so each of you can make your own sign-in.
  if (p === '/api/setup' && req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    const real = (env.PLANNER_PASSCODE || '').trim();
    if (!real) return json({ ok: false, error: 'no_passcode' }, 500);
    const key = 'pc:' + ip;
    const wait = await locked(env, key);
    if (wait) return json({ ok: false, error: 'locked', wait }, 429);
    if (!sameString(String(b.passcode || '').trim(), real)) {
      const f = await noteFail(env, key);
      return json({ ok: false, error: f.locked ? 'locked' : 'wrong', left: f.left || 0, wait: f.wait || 0 }, f.locked ? 429 : 401);
    }
    await clearFails(env, key);
    return json({ ok: true }, 200, { 'set-cookie': sessionCookie(url, await makeToken(secret(env), null)) });
  }
  if (p === '/api/logout' && req.method === 'POST') {
    return json({ ok: true }, 200, { 'set-cookie': `${COOKIE}=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0` });
  }

  const tok = await readToken(secret(env), cookie(req, COOKIE));
  if (!tok) return json({ error: 'unauthorized' }, 401);

  // Who am I? A passcode-only cookie gets the people who still need a sign-in.
  if (p === '/api/me' && req.method === 'GET') {
    if (!tok.person) {
      const open = await env.DB.prepare("SELECT id, name FROM people WHERE pass_hash IS NULL OR pass_hash='' ORDER BY created_at").all();
      return json({ person: null, claimable: open.results || [] });
    }
    const me = await env.DB.prepare('SELECT id, name, color, username FROM people WHERE id=?1').bind(tok.person).first();
    return me ? json({ person: me }) : json({ error: 'unauthorized' }, 401);
  }
  // Make your sign-in: pick yourself, choose a username + password.
  if (p === '/api/claim' && req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    const pid = String(b.person_id || '');
    const username = String(b.username || '').trim().toLowerCase();
    const password = String(b.password || '');
    const name = String(b.name || '').trim();
    if (!USERNAME_RE.test(username)) return json({ ok: false, error: 'bad_username' }, 400);
    if (password.length < MIN_PASSWORD) return json({ ok: false, error: 'short_password' }, 400);
    const person = await env.DB.prepare('SELECT id, pass_hash FROM people WHERE id=?1').bind(pid).first();
    if (!person) return json({ ok: false, error: 'no_person' }, 404);
    if (person.pass_hash) return json({ ok: false, error: 'taken_person' }, 409);
    const clash = await env.DB.prepare('SELECT id FROM people WHERE username=?1 AND id!=?2').bind(username, pid).first();
    if (clash) return json({ ok: false, error: 'taken_username' }, 409);
    const f = await newPasswordFields(password);
    await env.DB.prepare("UPDATE people SET username=?1, pass_hash=?2, pass_salt=?3, pass_iter=?4, name=COALESCE(NULLIF(?5,''), name) WHERE id=?6")
      .bind(username, f.pass_hash, f.pass_salt, f.pass_iter, name, pid).run();
    return json({ ok: true }, 200, { 'set-cookie': sessionCookie(url, await makeToken(secret(env), pid)) });
  }

  // Everything else needs a signed-in person.
  if (!tok.person) return json({ error: 'account_needed' }, 401);
  const me = tok.person;

  // Settings › Claude: your private link, make a new one, or turn it off
  if (p === '/api/claude') return claudeApi(req, env, url, me, claudeDeps(env));

  if (p === '/api/password' && req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    const key = 'u:' + me;
    const wait = await locked(env, key);
    if (wait) return json({ ok: false, error: 'locked', wait }, 429);
    const person = await env.DB.prepare('SELECT pass_hash, pass_salt, pass_iter FROM people WHERE id=?1').bind(me).first();
    if (!person || !sameString(await hashPassword(String(b.current || ''), person.pass_salt, person.pass_iter || PBKDF2_ITER), person.pass_hash)) {
      const f = await noteFail(env, key);
      return json({ ok: false, error: f.locked ? 'locked' : 'wrong', left: f.left || 0 }, f.locked ? 429 : 401);
    }
    const next = String(b.next || '');
    if (next.length < MIN_PASSWORD) return json({ ok: false, error: 'short_password' }, 400);
    await clearFails(env, key);
    const f = await newPasswordFields(next);
    await env.DB.prepare('UPDATE people SET pass_hash=?1, pass_salt=?2, pass_iter=?3 WHERE id=?4').bind(f.pass_hash, f.pass_salt, f.pass_iter, me).run();
    return json({ ok: true });
  }

  if (p === '/api/state' && req.method === 'GET') return json(await loadState(env, me));

  // The app's outbox: a list of changes applied together in one D1 batch (all or nothing).
  if (p === '/api/ops' && req.method === 'POST') {
    const ops = ((await req.json().catch(() => ({}))).ops) || [];
    if (!Array.isArray(ops) || ops.length > 100) return json({ error: 'bad ops' }, 400);
    let stmts;
    try {
      stmts = ops.flatMap((o) => opStatements(env, o, me));
    } catch (e) {
      return json({ error: String((e && e.message) || e) }, 400);
    }
    if (stmts.length) await env.DB.batch(stmts);
    return json({ ok: true, n: ops.length });
  }

  if (p === '/api/op' && req.method === 'POST') {
    await applyOp(env, await req.json(), me);
    return json({ ok: true });
  }
  if (p === '/api/habit' && req.method === 'POST') {
    const b = await req.json();
    const val = Math.max(0, parseInt(b.value, 10) || 0);
    await env.DB.prepare('INSERT INTO habit_logs (date,habit,value) VALUES (?1,?2,?3) ON CONFLICT(date,habit) DO UPDATE SET value=excluded.value')
      .bind(String(b.date), String(b.habit), val)
      .run();
    return json({ ok: true });
  }
  if (p === '/api/settings' && req.method === 'POST') {
    const patch = (await req.json()).patch || {};
    const stmts = Object.keys(patch).map((k) =>
      env.DB.prepare('INSERT INTO settings (key,value) VALUES (?1,?2) ON CONFLICT(key) DO UPDATE SET value=excluded.value').bind(k, patch[k] == null ? '' : String(patch[k])),
    ).concat(legacyNameStatements(env, patch));
    if (stmts.length) await env.DB.batch(stmts);
    return json({ ok: true });
  }
  return json({ error: 'not found' }, 404);
}

function parseJSON(v, fallback) {
  try {
    return v ? JSON.parse(v) : fallback;
  } catch (e) {
    return fallback;
  }
}

async function loadState(env, me) {
  // only the spaces you're in; journal entries are yours, or shared into one of your spaces
  const MINE = 'SELECT space_id FROM members WHERE person_id=?1';
  const inMine = (t, order) => env.DB.prepare('SELECT * FROM ' + t + ' WHERE space_id IN (' + MINE + ') OR space_id IS NULL ORDER BY ' + order).bind(me).all();
  const [settings, projects, materials, routines, tasks, journal, habitDefs, habitLogs, topics, topicLinks, notes, focus, waves, people, spaces, members, focusLog, journalDays] = await Promise.all([
    env.DB.prepare('SELECT key,value FROM settings').all(),
    inMine('projects', 'sort, created_at'),
    env.DB.prepare('SELECT * FROM project_materials ORDER BY sort, created_at').all(),
    env.DB.prepare('SELECT id,title,"start" AS start,"end" AS end,owner,days,note,sort FROM routines ORDER BY sort, "start"').all(),
    inMine('tasks', 'created_at'),
    env.DB.prepare('SELECT * FROM journal WHERE owner=?1 OR space_id IN (' + MINE + ') ORDER BY date DESC').bind(me).all(),
    inMine('habits', 'sort, created_at'),
    env.DB.prepare('SELECT date,habit,value FROM habit_logs').all(),
    inMine('topics', 'week DESC, created_at DESC'),
    env.DB.prepare('SELECT * FROM topic_links ORDER BY sort, created_at').all(),
    inMine('notes', 'created_at DESC'),
    env.DB.prepare('SELECT * FROM focus WHERE id IN (' + MINE + ')').bind(me).all(),
    env.DB.prepare('SELECT * FROM waves WHERE id IN (' + MINE + ')').bind(me).all(),
    env.DB.prepare("SELECT id, name, color, created_at, (pass_hash IS NOT NULL AND pass_hash!='') AS claimed FROM people WHERE id=?1 OR id IN (SELECT person_id FROM members WHERE space_id IN (" + MINE + ')) ORDER BY created_at').bind(me).all(),
    env.DB.prepare('SELECT * FROM spaces WHERE id IN (' + MINE + ') ORDER BY created_at').bind(me).all(),
    env.DB.prepare('SELECT * FROM members WHERE space_id IN (' + MINE + ') ORDER BY joined_at').bind(me).all(),
    env.DB.prepare('SELECT * FROM focus_log WHERE space_id IN (' + MINE + ') ORDER BY ended_at').bind(me).all(),
    // which days each person in your spaces wrote, for the week board: dates only, never the text of a private entry
    env.DB.prepare("SELECT date, owner FROM journal WHERE trim(coalesce(text,''))!='' AND owner IN (SELECT person_id FROM members WHERE space_id IN (" + MINE + '))').bind(me).all(),
  ]);
  const rowFor = (rows, ids) => (rows.results || []).find((r) => ids.includes(r.id)) || null;

  const s = {};
  for (const r of settings.results || []) { s[r.key] = r.value; }
  const tk = (tasks.results || []).map((t) => ({ ...t, done: !!t.done, subtodos: parseJSON(t.subtodos, []) }));

  return {
    settings: s,
    projects: projects.results || [],
    project_materials: materials.results || [],
    routines: routines.results || [],
    tasks: tk,
    journal: journal.results || [],
    habits: habitDefs.results || [],
    habit_logs: habitLogs.results || [],
    topics: topics.results || [],
    topic_links: topicLinks.results || [],
    notes: notes.results || [],
    // one focus timer and one wave per space; focus/wave are the default space's, for older tabs
    focus_all: focus.results || [],
    wave_all: waves.results || [],
    focus: rowFor(focus, [DEFAULT_SPACE, 'shared']),
    wave: rowFor(waves, [DEFAULT_SPACE, 'latest']),
    people: people.results || [],
    spaces: spaces.results || [],
    members: members.results || [],
    focus_log: focusLog.results || [],
    journal_days: journalDays.results || [],
    me,
  };
}

// What each delete also removes, so nothing is left orphaned.
const CASCADE = {
  projects: [['tasks', 'project'], ['project_materials', 'project_id']],
  tasks: [['tasks', 'parent_id']],
  habits: [['habit_logs', 'habit']],
  topics: [['topic_links', 'topic_id']],
};

function toCol(c, v) {
  if (c === 'subtodos') return JSON.stringify(Array.isArray(v) ? v : parseJSON(v, []));
  if (c === 'done') return v ? 1 : 0;
  return v === undefined ? null : v;
}

// One outbox change → the D1 statements for it. Throws on anything not whitelisted.
function opStatements(env, o, me) {
  if (!o || typeof o !== 'object') throw new Error('bad op');
  // the server records who finished a task and when, so points can't be claimed from the browser
  if (o.table === 'tasks' && o.op === 'patch' && o.fields && 'done' in o.fields) {
    o = { ...o, fields: { ...o.fields, done_at: o.fields.done ? Date.now() : null, done_by: o.fields.done ? me : null } };
  }
  if (o.table === 'tasks' && o.op === 'upsert' && o.row) {
    o = { ...o, row: { ...o.row, done_at: o.row.done ? (o.row.done_at || Date.now()) : null, done_by: o.row.done ? (o.row.done_by || me) : null } };
  }
  // people, spaces and members aren't edited from the app, except your own name and colour
  if (o.table === 'people') {
    if (o.op !== 'patch' || o.id !== me) throw new Error('you can only rename yourself');
    o = { ...o, fields: { name: o.fields && o.fields.name, color: o.fields && o.fields.color } };
    if (o.fields.color == null) delete o.fields.color;
    if (o.fields.name == null) delete o.fields.name;
  }
  if (o.table === 'spaces' || o.table === 'members') throw new Error('read only');
  if (o.op === 'settings') {
    const patch = o.patch || {};
    return Object.keys(patch).map((k) =>
      env.DB.prepare('INSERT INTO settings (key,value) VALUES (?1,?2) ON CONFLICT(key) DO UPDATE SET value=excluded.value').bind(k, patch[k] == null ? '' : String(patch[k])),
    ).concat(legacyNameStatements(env, patch));
  }
  if (o.op === 'habit') {
    const date = String(o.date || ''), habit = String(o.habit || '');
    if (!date || !habit) throw new Error('bad habit op');
    if (o.delta != null) {
      // +1 / −1 is applied on the server, so taps from two phones both count
      const d = parseInt(o.delta, 10) || 0;
      return [env.DB.prepare('INSERT INTO habit_logs (date,habit,value) VALUES (?1,?2,MAX(0,?3)) ON CONFLICT(date,habit) DO UPDATE SET value=MAX(0,habit_logs.value+?3)').bind(date, habit, d)];
    }
    const val = Math.max(0, parseInt(o.value, 10) || 0);
    return [env.DB.prepare('INSERT INTO habit_logs (date,habit,value) VALUES (?1,?2,?3) ON CONFLICT(date,habit) DO UPDATE SET value=excluded.value').bind(date, habit, val)];
  }
  const cols = TABLES[o.table];
  if (!cols) throw new Error('bad table');
  if (o.op === 'delete') {
    const id = normalizeId(o.table, o.id || (o.row && o.row.id));
    if (!id) throw new Error('delete needs an id');
    const out = (CASCADE[o.table] || []).map(([t, c]) => env.DB.prepare('DELETE FROM ' + t + ' WHERE ' + c + '=?1').bind(id));
    out.push(env.DB.prepare('DELETE FROM ' + o.table + ' WHERE id=?1').bind(id));
    return out;
  }
  if (o.op === 'patch') {
    // only the fields that changed, so one person's edit never rewrites the other's
    const fields = normalizeRow(o.table, o.fields || {}, false);
    const set = Object.keys(fields).filter((c) => c !== 'id' && cols.includes(c));
    if (!o.id || !set.length) return [];
    const sql = 'UPDATE ' + o.table + ' SET ' + set.map((c, i) => c + '=?' + (i + 1)).join(',') + ' WHERE id=?' + (set.length + 1);
    return [env.DB.prepare(sql).bind(...set.map((c) => toCol(c, fields[c])), normalizeId(o.table, o.id))];
  }
  if (o.op === 'upsert') {
    const row = normalizeRow(o.table, o.row || {}, true);
    if (!row.id) throw new Error('upsert needs an id');
    const placeholders = cols.map((_, i) => '?' + (i + 1)).join(',');
    const updates = cols.filter((c) => c !== 'id').map((c) => c + '=excluded.' + c).join(',');
    const sql = 'INSERT INTO ' + o.table + ' (' + cols.join(',') + ') VALUES (' + placeholders + ') ON CONFLICT(id) DO UPDATE SET ' + updates;
    return [env.DB.prepare(sql).bind(...cols.map((c) => toCol(c, row[c])))];
  }
  throw new Error('bad op');
}

async function applyOp(env, b, me) {
  if (b && ['people', 'spaces', 'members'].includes(b.table)) throw new Error('read only');
  const table = b.table;
  const cols = TABLES[table];
  if (!cols) throw new Error('bad table');

  if (b.op === 'delete') {
    const id = normalizeId(table, (b.row && b.row.id) || b.id);
    await env.DB.prepare('DELETE FROM ' + table + ' WHERE id=?1').bind(id).run();
    return;
  }

  const row = normalizeRow(table, b.row || {}, true);
  const vals = cols.map((c) => {
    let v = row[c];
    if (c === 'subtodos') return JSON.stringify(Array.isArray(v) ? v : parseJSON(v, []));
    if (c === 'done') return v ? 1 : 0;
    return v === undefined ? null : v;
  });
  const placeholders = cols.map((_, i) => '?' + (i + 1)).join(',');
  const updates = cols
    .filter((c) => c !== 'id')
    .map((c) => c + '=excluded.' + c)
    .join(',');
  const sql = 'INSERT INTO ' + table + ' (' + cols.join(',') + ') VALUES (' + placeholders + ') ON CONFLICT(id) DO UPDATE SET ' + updates;
  await env.DB.prepare(sql).bind(...vals).run();
}
