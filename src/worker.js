// Shared Planner — Cloudflare Worker: static assets + small JSON API over D1.
// Two people, one shared space, protected by a shared passcode (signed cookie).

const TABLES = {
  tasks: ['id', 'title', 'project', 'owner', 'type', 'date', 'time', 'due', 'due_time', 'done', 'subtodos', 'parent_id', 'sort', 'created_at'],
  projects: ['id', 'name', 'color', 'owner', 'kind', 'start_date', 'end_date', 'description', 'archived', 'sort', 'created_at'],
  project_materials: ['id', 'project_id', 'title', 'url', 'sort', 'created_at'],
  journal: ['id', 'date', 'owner', 'text', 'tag', 'updated_at'],
  habits: ['id', 'name', 'kind', 'owner', 'unit', 'target', 'caption', 'color', 'sort', 'archived', 'created_at'],
  topics: ['id', 'week', 'title', 'owner', 'notes', 'sort', 'created_at'],
  topic_links: ['id', 'topic_id', 'title', 'url', 'sort', 'created_at'],
  notes: ['id', 'text', 'color', 'owner', 'date', 'created_at'],
  focus: ['id', 'status', 'label', 'minutes', 'ends_at', 'remaining', 'started_by', 'updated_at'],
  waves: ['id', 'emoji', 'sender', 'created_at'],
};

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
async function makeToken(secret) {
  const body = 'v1.' + (Date.now() + MAXAGE * 1000);
  return body + '.' + (await hmac(secret, body));
}
async function verifyToken(secret, token) {
  if (!token) return false;
  const parts = token.split('.');
  if (parts.length !== 3 || parts[0] !== 'v1') return false;
  const exp = Number(parts[1]);
  if (!exp || Date.now() > exp) return false;
  const good = await hmac(secret, 'v1.' + exp);
  if (good.length !== parts[2].length) return false;
  let diff = 0;
  for (let i = 0; i < good.length; i++) diff |= good.charCodeAt(i) ^ parts[2].charCodeAt(i);
  return diff === 0;
}
function cookie(req, name) {
  const c = req.headers.get('cookie') || '';
  const m = c.match(new RegExp('(?:^|; )' + name + '=([^;]+)'));
  return m ? decodeURIComponent(m[1]) : null;
}
function secret(env) {
  return env.SESSION_SECRET || 'dev-only-secret';
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
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

  if (p === '/api/login' && req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    const real = (env.PLANNER_PASSCODE || '').trim();
    if (!real) return json({ ok: false, error: 'No passcode configured on the server.' }, 500);
    if ((b.passcode || '').trim() === real) {
      const token = await makeToken(secret(env));
      const sec = url.protocol === 'https:' ? '; Secure' : '';
      const set = `${COOKIE}=${token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=${MAXAGE}${sec}`;
      return json({ ok: true }, 200, { 'set-cookie': set });
    }
    return json({ ok: false, error: 'Wrong passcode.' }, 401);
  }
  if (p === '/api/logout' && req.method === 'POST') {
    return json({ ok: true }, 200, { 'set-cookie': `${COOKIE}=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0` });
  }

  if (!(await verifyToken(secret(env), cookie(req, COOKIE)))) return json({ error: 'unauthorized' }, 401);

  if (p === '/api/state' && req.method === 'GET') return json(await loadState(env));

  // The app's outbox: a list of changes applied together in one D1 batch (all or nothing).
  if (p === '/api/ops' && req.method === 'POST') {
    const ops = ((await req.json().catch(() => ({}))).ops) || [];
    if (!Array.isArray(ops) || ops.length > 100) return json({ error: 'bad ops' }, 400);
    let stmts;
    try {
      stmts = ops.flatMap((o) => opStatements(env, o));
    } catch (e) {
      return json({ error: String((e && e.message) || e) }, 400);
    }
    if (stmts.length) await env.DB.batch(stmts);
    return json({ ok: true, n: ops.length });
  }

  if (p === '/api/op' && req.method === 'POST') {
    await applyOp(env, await req.json());
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
    );
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

async function loadState(env) {
  const [settings, projects, materials, routines, tasks, journal, habitDefs, habitLogs, topics, topicLinks, notes, focus, waves] = await Promise.all([
    env.DB.prepare('SELECT key,value FROM settings').all(),
    env.DB.prepare('SELECT * FROM projects ORDER BY sort, created_at').all(),
    env.DB.prepare('SELECT * FROM project_materials ORDER BY sort, created_at').all(),
    env.DB.prepare('SELECT id,title,"start" AS start,"end" AS end,owner,days,note,sort FROM routines ORDER BY sort, "start"').all(),
    env.DB.prepare('SELECT * FROM tasks ORDER BY created_at').all(),
    env.DB.prepare('SELECT * FROM journal ORDER BY date DESC').all(),
    env.DB.prepare('SELECT * FROM habits ORDER BY sort, created_at').all(),
    env.DB.prepare('SELECT date,habit,value FROM habit_logs').all(),
    env.DB.prepare('SELECT * FROM topics ORDER BY week DESC, created_at DESC').all(),
    env.DB.prepare('SELECT * FROM topic_links ORDER BY sort, created_at').all(),
    env.DB.prepare('SELECT * FROM notes ORDER BY created_at DESC').all(),
    env.DB.prepare("SELECT * FROM focus WHERE id='shared'").all(),
    env.DB.prepare("SELECT * FROM waves WHERE id='latest'").all(),
  ]);

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
    focus: (focus.results && focus.results[0]) || null,
    wave: (waves.results && waves.results[0]) || null,
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
function opStatements(env, o) {
  if (!o || typeof o !== 'object') throw new Error('bad op');
  if (o.op === 'settings') {
    const patch = o.patch || {};
    return Object.keys(patch).map((k) =>
      env.DB.prepare('INSERT INTO settings (key,value) VALUES (?1,?2) ON CONFLICT(key) DO UPDATE SET value=excluded.value').bind(k, patch[k] == null ? '' : String(patch[k])),
    );
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
    const id = o.id || (o.row && o.row.id);
    if (!id) throw new Error('delete needs an id');
    const out = (CASCADE[o.table] || []).map(([t, c]) => env.DB.prepare('DELETE FROM ' + t + ' WHERE ' + c + '=?1').bind(id));
    out.push(env.DB.prepare('DELETE FROM ' + o.table + ' WHERE id=?1').bind(id));
    return out;
  }
  if (o.op === 'patch') {
    // only the fields that changed, so one person's edit never rewrites the other's
    const fields = o.fields || {};
    const set = Object.keys(fields).filter((c) => c !== 'id' && cols.includes(c));
    if (!o.id || !set.length) return [];
    const sql = 'UPDATE ' + o.table + ' SET ' + set.map((c, i) => c + '=?' + (i + 1)).join(',') + ' WHERE id=?' + (set.length + 1);
    return [env.DB.prepare(sql).bind(...set.map((c) => toCol(c, fields[c])), o.id)];
  }
  if (o.op === 'upsert') {
    const row = o.row || {};
    if (!row.id) throw new Error('upsert needs an id');
    const placeholders = cols.map((_, i) => '?' + (i + 1)).join(',');
    const updates = cols.filter((c) => c !== 'id').map((c) => c + '=excluded.' + c).join(',');
    const sql = 'INSERT INTO ' + o.table + ' (' + cols.join(',') + ') VALUES (' + placeholders + ') ON CONFLICT(id) DO UPDATE SET ' + updates;
    return [env.DB.prepare(sql).bind(...cols.map((c) => toCol(c, row[c])))];
  }
  throw new Error('bad op');
}

async function applyOp(env, b) {
  const table = b.table;
  const cols = TABLES[table];
  if (!cols) throw new Error('bad table');

  if (b.op === 'delete') {
    const id = (b.row && b.row.id) || b.id;
    await env.DB.prepare('DELETE FROM ' + table + ' WHERE id=?1').bind(id).run();
    return;
  }

  const row = b.row || {};
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
