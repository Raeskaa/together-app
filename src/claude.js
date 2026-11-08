// hate club for Claude: a small MCP server (Streamable HTTP, stateless JSON replies).
// Each person gets a private link /mcp/<token>. Claude acts as that person: it can see their tasks,
// add one, tick one off, reopen one, or move one to another day. Writes go through the app's own
// opStatements, so the server still stamps done_by / done_at and the points work the same.

export const CLAUDE_TABLE =
  'CREATE TABLE IF NOT EXISTS claude_links (person_id TEXT PRIMARY KEY, ver INTEGER NOT NULL DEFAULT 0, active INTEGER NOT NULL DEFAULT 0, created_at INTEGER, last_used_at INTEGER, last_action TEXT)';

const TZ = 'Asia/Kolkata'; // you're both on IST
const DAY_START_HOUR = 4; // the app's day turns over at 4am
const PROTOCOLS = ['2025-11-25', '2025-06-18', '2025-03-26', '2024-11-05'];
const PTS = { task: 10, sub: 3, ontime: 5, help: 5 };
const EVENT_TYPES = ['event', 'meeting'];

// ---- the private link ----
const b64u = (s) => btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const unb64u = (s) => { try { return atob(s.replace(/-/g, '+').replace(/_/g, '/')); } catch (e) { return ''; } };

async function linkSig(d, person, ver) {
  return (await d.hmac(d.secret, 'claude:' + person + ':' + ver)).slice(0, 40);
}
export async function claudeToken(d, person, ver) {
  return 'hc_' + b64u(person) + '.' + (await linkSig(d, person, ver));
}
// → person id, or null
async function personFromToken(env, d, token) {
  const m = /^hc_([A-Za-z0-9_-]+)\.([0-9a-f]{40})$/.exec(token || '');
  if (!m) return null;
  const person = unb64u(m[1]);
  if (!person) return null;
  await env.DB.prepare(CLAUDE_TABLE).run();
  const row = await env.DB.prepare('SELECT ver, active FROM claude_links WHERE person_id=?1').bind(person).first();
  if (!row || !row.active) return null;
  return d.sameString(await linkSig(d, person, row.ver), m[2]) ? person : null;
}

// ---- days, the app's way ----
function dayOf(ms) {
  return new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(ms - DAY_START_HOUR * 3600e3));
}
const today = () => dayOf(Date.now());
function addDays(ymd, n) {
  const [y, m, dd] = ymd.split('-').map(Number);
  const t = new Date(Date.UTC(y, m - 1, dd + n));
  return t.toISOString().slice(0, 10);
}
const WEEKDAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
// 'today' | 'tomorrow' | 'yesterday' | a weekday (this one or the next) | YYYY-MM-DD → YYYY-MM-DD, '' for none, null if unreadable
function readDay(v) {
  if (v == null) return undefined;
  const s = String(v).trim().toLowerCase();
  if (!s || s === 'none' || s === 'no date' || s === 'clear') return '';
  const t = today();
  if (s === 'today') return t;
  if (s === 'tomorrow') return addDays(t, 1);
  if (s === 'yesterday') return addDays(t, -1);
  const w = WEEKDAYS.findIndex((x) => x === s || x.slice(0, 3) === s);
  if (w >= 0) {
    const [y, m, dd] = t.split('-').map(Number);
    const now = new Date(Date.UTC(y, m - 1, dd)).getUTCDay();
    return addDays(t, (w - now + 7) % 7);
  }
  if (/^\d{4}-\d{2}-\d{2}$/.test(s)) return s;
  return null;
}
function prettyDay(ymd) {
  if (!ymd) return '';
  const t = today();
  if (ymd === t) return 'today';
  if (ymd === addDays(t, 1)) return 'tomorrow';
  if (ymd === addDays(t, -1)) return 'yesterday';
  const [y, m, dd] = ymd.split('-').map(Number);
  return new Date(Date.UTC(y, m - 1, dd)).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' });
}

// ---- reading your world ----
async function world(env, me) {
  const MINE = 'SELECT space_id FROM members WHERE person_id=?1';
  const [tasks, projects, people, space] = await Promise.all([
    env.DB.prepare('SELECT * FROM tasks WHERE space_id IN (' + MINE + ') OR space_id IS NULL').bind(me).all(),
    env.DB.prepare('SELECT id, name, archived FROM projects WHERE space_id IN (' + MINE + ') OR space_id IS NULL').bind(me).all(),
    env.DB.prepare('SELECT id, name FROM people WHERE id=?1 OR id IN (SELECT person_id FROM members WHERE space_id IN (' + MINE + '))').bind(me).all(),
    env.DB.prepare('SELECT space_id FROM members WHERE person_id=?1 ORDER BY joined_at LIMIT 1').bind(me).first(),
  ]);
  const ppl = people.results || [];
  const partner = ppl.find((p) => p.id !== me) || null;
  return {
    me,
    partner: partner && partner.id,
    space: (space && space.space_id) || 's_hateclub',
    names: Object.fromEntries(ppl.map((p) => [p.id, p.name || p.id])),
    projects: (projects.results || []).filter((p) => !p.archived),
    tasks: (tasks.results || []).map((t) => ({ ...t, done: !!t.done })),
  };
}
function ownerName(w, o) {
  if (o === 'everyone') return 'both of you';
  if (o === w.me) return 'you';
  return w.names[o] || 'your partner';
}
function projectName(w, id) {
  const p = w.projects.find((x) => x.id === id);
  return p ? p.name : '';
}
function describe(w, t) {
  const bits = [];
  const p = projectName(w, t.project);
  if (p) bits.push(p);
  if (t.date) bits.push('on ' + prettyDay(t.date) + (t.time ? ' ' + t.time : ''));
  if (t.due) bits.push('due ' + prettyDay(t.due));
  bits.push(ownerName(w, t.owner));
  return (t.done ? '[x] ' : '[ ] ') + t.title + ' (' + bits.join(', ') + ') · id ' + t.id;
}
function brief(w, t) {
  return { id: t.id, title: t.title, done: t.done, date: t.date || null, time: t.time || null, due: t.due || null, project: projectName(w, t.project) || null, owner: ownerName(w, t.owner), subtask_of: t.parent_id || null };
}
function whoFilter(w, who) {
  if (who === 'me') return (t) => t.owner === w.me || t.owner === 'everyone';
  if (who === 'partner') return (t) => t.owner === w.partner || t.owner === 'everyone';
  if (who === 'both') return (t) => t.owner === 'everyone';
  return () => true;
}
// a task by id, or by words in its title among the given pool
function findTask(w, args, pool) {
  if (args.id) {
    const t = w.tasks.find((x) => x.id === String(args.id));
    if (!t) throw new Error('No task with id ' + args.id + '.');
    return t;
  }
  const q = String(args.title || '').trim().toLowerCase();
  if (!q) throw new Error('Give the task id, or a few words from its title.');
  const hits = pool.filter((t) => (t.title || '').toLowerCase().includes(q));
  const exact = hits.filter((t) => (t.title || '').toLowerCase() === q);
  const pick = exact.length === 1 ? exact : hits;
  if (pick.length === 1) return pick[0];
  if (!pick.length) throw new Error('No task matches "' + args.title + '". Use list_tasks to see them.');
  throw new Error('More than one task matches "' + args.title + '". Which one?\n' + pick.slice(0, 8).map((t) => '- ' + describe(w, t)).join('\n'));
}
function points(t, doneDay, by) {
  if (EVENT_TYPES.includes(t.type)) return { n: 0, onTime: false, helped: false };
  const onTime = !!t.due && doneDay <= t.due;
  const helped = t.owner !== by;
  return { n: (t.parent_id ? PTS.sub : PTS.task) + (onTime ? PTS.ontime : 0) + (helped ? PTS.help : 0), onTime, helped };
}
function matchProject(w, name) {
  if (name == null || String(name).trim() === '') return '';
  const q = String(name).trim().toLowerCase();
  const exact = w.projects.find((p) => (p.name || '').toLowerCase() === q);
  if (exact) return exact.id;
  const hits = w.projects.filter((p) => (p.name || '').toLowerCase().includes(q));
  if (hits.length === 1) return hits[0].id;
  const names = w.projects.map((p) => p.name).join(', ') || 'none yet';
  throw new Error((hits.length ? 'More than one project matches "' : 'No project called "') + name + '". Projects: ' + names + '.');
}
function uid(pre) {
  return pre + '_' + Date.now().toString(36) + Math.floor(Math.random() * 1e6).toString(36);
}
const out = (text, structured) => ({ content: [{ type: 'text', text }], ...(structured ? { structuredContent: structured } : {}) });

// ---- the tools ----
const DAY_HELP = '"today", "tomorrow", a weekday like "friday", or YYYY-MM-DD';
const TOOLS = [
  {
    name: 'list_tasks',
    title: 'See tasks',
    description: 'List tasks in hate club. Use this first to find a task before ticking it off. "today" means planned for today or due today, plus anything carried over from earlier days.',
    inputSchema: {
      type: 'object',
      properties: {
        when: { type: 'string', enum: ['today', 'overdue', 'upcoming', 'no_date', 'done_today', 'all_open'], description: 'Which tasks. Default "today".' },
        who: { type: 'string', enum: ['me', 'partner', 'both', 'anyone'], description: '"me" = mine plus shared ones; "both" = only shared ones. Default "anyone".' },
        project: { type: 'string', description: 'Only tasks in a project whose name contains this.' },
      },
    },
    annotations: { readOnlyHint: true },
  },
  {
    name: 'add_task',
    title: 'Add a task',
    description: 'Add a task to hate club. It is yours unless you say who.',
    inputSchema: {
      type: 'object',
      required: ['title'],
      properties: {
        title: { type: 'string', description: 'What needs doing, short.' },
        date: { type: 'string', description: 'The day to do it: ' + DAY_HELP + '. Leave out for no day.' },
        time: { type: 'string', description: 'A time on that day, HH:MM (24h).' },
        due: { type: 'string', description: 'The deadline: ' + DAY_HELP + '. Finishing on or before it earns +5.' },
        project: { type: 'string', description: 'The project it belongs to, by name.' },
        who: { type: 'string', enum: ['me', 'partner', 'both'], description: 'Whose task it is. Default "me".' },
        subtask_of: { type: 'string', description: 'The id of a task this is a step of.' },
      },
    },
  },
  {
    name: 'complete_task',
    title: 'Tick a task off',
    description: 'Mark a task done ("kill" it). Give its id, or a few words from its title. It counts as done by you, so the points are yours (+5 more if it is your partner\'s and you helped).',
    inputSchema: {
      type: 'object',
      properties: { id: { type: 'string' }, title: { type: 'string', description: 'Words from the title, if you have no id.' } },
    },
    annotations: { idempotentHint: true },
  },
  {
    name: 'reopen_task',
    title: 'Reopen a task',
    description: 'Undo a tick: mark a done task as not done again (its points go away).',
    inputSchema: {
      type: 'object',
      properties: { id: { type: 'string' }, title: { type: 'string', description: 'Words from the title, if you have no id.' } },
    },
    annotations: { idempotentHint: true },
  },
  {
    name: 'move_task',
    title: 'Move a task to another day',
    description: 'Change the day a task is planned for (not its deadline).',
    inputSchema: {
      type: 'object',
      required: ['date'],
      properties: {
        id: { type: 'string' },
        title: { type: 'string', description: 'Words from the title, if you have no id.' },
        date: { type: 'string', description: 'The new day: ' + DAY_HELP + ', or "none" to take it off the calendar.' },
      },
    },
  },
];

async function callTool(env, d, me, name, args) {
  args = args || {};
  const w = await world(env, me);
  const t0 = today();
  const write = async (ops) => {
    const stmts = ops.flatMap((o) => d.opStatements(env, o, me));
    if (stmts.length) await env.DB.batch(stmts);
  };

  if (name === 'list_tasks') {
    const when = args.when || 'today';
    let list = w.tasks.filter((t) => !EVENT_TYPES.includes(t.type) || when === 'today').filter(whoFilter(w, args.who || 'anyone'));
    if (args.project) {
      const q = String(args.project).toLowerCase();
      const ids = w.projects.filter((p) => (p.name || '').toLowerCase().includes(q)).map((p) => p.id);
      list = list.filter((t) => ids.includes(t.project));
    }
    const late = (t) => !t.done && ((t.due && t.due < t0) || (!t.due && t.date && t.date < t0));
    if (when === 'today') list = list.filter((t) => (!t.done && (t.date === t0 || t.due === t0 || late(t))) || (t.done && t.date === t0));
    else if (when === 'overdue') list = list.filter(late);
    else if (when === 'upcoming') list = list.filter((t) => !t.done && ((t.date && t.date > t0) || (t.due && t.due > t0))).sort((a, b) => ((a.date || a.due) < (b.date || b.due) ? -1 : 1));
    else if (when === 'no_date') list = list.filter((t) => !t.done && !t.date && !t.due);
    else if (when === 'done_today') list = list.filter((t) => t.done && t.done_at && dayOf(t.done_at) === t0);
    else list = list.filter((t) => !t.done);
    list = list.slice(0, 60);
    const head = list.length ? list.length + ' task' + (list.length > 1 ? 's' : '') + ' (' + when.replace('_', ' ') + ', today is ' + t0 + '):' : 'No tasks for "' + when.replace('_', ' ') + '" (today is ' + t0 + ').';
    return out([head].concat(list.map((t) => '- ' + describe(w, t))).join('\n'), { today: t0, tasks: list.map((t) => brief(w, t)) });
  }

  if (name === 'add_task') {
    const title = String(args.title || '').trim();
    if (!title) throw new Error('A task needs a title.');
    if (title.length > 300) throw new Error('That title is too long; keep it under 300 characters.');
    const date = readDay(args.date), due = readDay(args.due);
    if (date === null) throw new Error('Could not read the day "' + args.date + '". Use ' + DAY_HELP + '.');
    if (due === null) throw new Error('Could not read the deadline "' + args.due + '". Use ' + DAY_HELP + '.');
    const time = args.time ? String(args.time).trim() : '';
    if (time && !/^([01]\d|2[0-3]):[0-5]\d$/.test(time)) throw new Error('Time must be HH:MM, 24-hour.');
    const owner = args.who === 'partner' ? w.partner || me : args.who === 'both' ? 'everyone' : me;
    let parent = null, project = matchProject(w, args.project);
    if (args.subtask_of) {
      const p = w.tasks.find((x) => x.id === String(args.subtask_of));
      if (!p) throw new Error('No task with id ' + args.subtask_of + ' to add a step to.');
      parent = p.id;
      if (!project) project = p.project || '';
    }
    const row = { id: uid('tk'), title, project, owner, type: 'task', date: date || '', time: date ? time : '', due: due || '', due_time: '', done: false, subtodos: '[]', parent_id: parent, sort: 0, created_at: Date.now(), space_id: w.space };
    await write([{ op: 'upsert', table: 'tasks', row }]);
    return { result: out('Added: ' + describe(w, row), { task: brief(w, row) }), action: 'added "' + title + '"' };
  }

  if (name === 'complete_task') {
    const t = findTask(w, args, w.tasks.filter((x) => !x.done));
    if (t.done) return { result: out('Already done: ' + describe(w, t), { task: brief(w, t) }), action: null };
    await write([{ op: 'patch', table: 'tasks', id: t.id, fields: { done: true } }]);
    const r = points(t, t0, me);
    const why = [r.onTime ? 'on time' : '', r.helped && t.owner !== 'everyone' ? 'helped ' + (w.names[t.owner] || 'your partner') : ''].filter(Boolean).join(', ');
    const msg = 'Ticked off "' + t.title + '".' + (r.n ? ' +' + r.n + ' points' + (why ? ' (' + why + ')' : '') + '.' : '');
    return { result: out(msg, { task: { ...brief(w, t), done: true }, points: r.n }), action: 'ticked off "' + t.title + '"' };
  }

  if (name === 'reopen_task') {
    const t = findTask(w, args, w.tasks.filter((x) => x.done));
    if (!t.done) return { result: out('That one is still open: ' + describe(w, t), { task: brief(w, t) }), action: null };
    await write([{ op: 'patch', table: 'tasks', id: t.id, fields: { done: false } }]);
    return { result: out('Reopened "' + t.title + '".', { task: { ...brief(w, t), done: false } }), action: 'reopened "' + t.title + '"' };
  }

  if (name === 'move_task') {
    const t = findTask(w, args, w.tasks.filter((x) => !x.done));
    const date = readDay(args.date);
    if (date == null) throw new Error('Could not read the day "' + args.date + '". Use ' + DAY_HELP + ', or "none".');
    await write([{ op: 'patch', table: 'tasks', id: t.id, fields: date ? { date } : { date: '', time: '' } }]);
    const moved = { ...t, date, time: date ? t.time : '' };
    return { result: out((date ? 'Moved "' + t.title + '" to ' + prettyDay(date) + '.' : 'Took "' + t.title + '" off the calendar.'), { task: brief(w, moved) }), action: 'moved "' + t.title + '"' };
  }

  throw new Error('Unknown tool: ' + name);
}

const INSTRUCTIONS =
  'hate club is a shared planner for two people who compete on points each week (Mon–Sun). ' +
  'You act as the person whose link this is. Before ticking a task off, find it with list_tasks and use its id; ' +
  'if a title matches more than one task, ask which. Only tick off what the person says is finished. ' +
  'Dates are in India time, and a day turns over at 4am.';

// ---- JSON-RPC over HTTP ----
function rpcError(id, code, message) {
  return { jsonrpc: '2.0', id: id == null ? null : id, error: { code, message } };
}
async function handleOne(env, d, me, msg) {
  if (!msg || msg.jsonrpc !== '2.0' || typeof msg.method !== 'string') return rpcError(msg && msg.id, -32600, 'Invalid request');
  const isNote = !('id' in msg);
  const { method, params = {} } = msg;
  if (isNote) return null; // notifications/initialized, cancelled… nothing to say back
  if (method === 'initialize') {
    const asked = params.protocolVersion;
    return {
      jsonrpc: '2.0', id: msg.id,
      result: {
        protocolVersion: PROTOCOLS.includes(asked) ? asked : PROTOCOLS[1],
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: 'hate-club', title: 'hate club', version: '1.0.0' },
        instructions: INSTRUCTIONS,
      },
    };
  }
  if (method === 'ping') return { jsonrpc: '2.0', id: msg.id, result: {} };
  if (method === 'tools/list') return { jsonrpc: '2.0', id: msg.id, result: { tools: TOOLS } };
  if (method === 'tools/call') {
    const name = params.name;
    if (!TOOLS.find((t) => t.name === name)) return rpcError(msg.id, -32602, 'Unknown tool: ' + name);
    try {
      const r = await callTool(env, d, me, name, params.arguments);
      const result = r.result || r;
      if (r.action) await env.DB.prepare('UPDATE claude_links SET last_used_at=?1, last_action=?2 WHERE person_id=?3').bind(Date.now(), r.action, me).run();
      else await env.DB.prepare('UPDATE claude_links SET last_used_at=?1 WHERE person_id=?2').bind(Date.now(), me).run();
      return { jsonrpc: '2.0', id: msg.id, result };
    } catch (e) {
      return { jsonrpc: '2.0', id: msg.id, result: { content: [{ type: 'text', text: String((e && e.message) || e) }], isError: true } };
    }
  }
  if (method === 'resources/list') return { jsonrpc: '2.0', id: msg.id, result: { resources: [] } };
  if (method === 'prompts/list') return { jsonrpc: '2.0', id: msg.id, result: { prompts: [] } };
  return rpcError(msg.id, -32601, 'Method not found: ' + method);
}

// d = { hmac, sameString, secret, opStatements }
export async function handleMcp(req, env, url, d) {
  const plain = (status, text) => new Response(text, { status, headers: { 'content-type': 'text/plain; charset=utf-8', 'cache-control': 'no-store' } });
  const fromPath = url.pathname.startsWith('/mcp/') ? decodeURIComponent(url.pathname.slice(5)) : '';
  const auth = req.headers.get('authorization') || '';
  const token = fromPath || (auth.toLowerCase().startsWith('bearer ') ? auth.slice(7).trim() : '');
  const me = await personFromToken(env, d, token);
  // a wrong link looks like no link at all
  if (!me) return plain(404, 'Not found');
  if (req.method === 'GET') return plain(405, 'This server answers POST only.');
  if (req.method === 'DELETE') return new Response(null, { status: 204 });
  if (req.method !== 'POST') return plain(405, 'Method not allowed');
  let body;
  try { body = await req.json(); } catch (e) { return new Response(JSON.stringify(rpcError(null, -32700, 'Parse error')), { status: 400, headers: { 'content-type': 'application/json' } }); }
  const many = Array.isArray(body);
  const replies = [];
  for (const m of many ? body : [body]) {
    const r = await handleOne(env, d, me, m);
    if (r) replies.push(r);
  }
  if (!replies.length) return new Response(null, { status: 202 });
  return new Response(JSON.stringify(many ? replies : replies[0]), { status: 200, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
}

// The app's side: GET /api/claude (status + link), POST /api/claude {action:'new'|'off'}
export async function claudeApi(req, env, url, me, d) {
  await env.DB.prepare(CLAUDE_TABLE).run();
  const read = () => env.DB.prepare('SELECT ver, active, created_at, last_used_at, last_action FROM claude_links WHERE person_id=?1').bind(me).first();
  if (req.method === 'POST') {
    const b = await req.json().catch(() => ({}));
    if (b.action === 'new') {
      await env.DB.prepare('INSERT INTO claude_links (person_id, ver, active, created_at) VALUES (?1, 1, 1, ?2) ON CONFLICT(person_id) DO UPDATE SET ver=claude_links.ver+1, active=1, created_at=?2, last_used_at=NULL, last_action=NULL').bind(me, Date.now()).run();
    } else if (b.action === 'off') {
      // bump the version too, so the old link stays dead if it's turned on again
      await env.DB.prepare('UPDATE claude_links SET active=0, ver=ver+1 WHERE person_id=?1').bind(me).run();
    } else {
      return new Response(JSON.stringify({ error: 'bad action' }), { status: 400, headers: { 'content-type': 'application/json' } });
    }
  }
  const row = await read();
  const on = !!(row && row.active);
  const body = { active: on, created_at: (row && row.created_at) || null, last_used_at: (row && row.last_used_at) || null, last_action: (row && row.last_action) || null };
  if (on) body.link = url.origin + '/mcp/' + (await claudeToken(d, me, row.ver));
  return new Response(JSON.stringify(body), { status: 200, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
}
