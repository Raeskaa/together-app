#!/usr/bin/env bash
# Shared Planner — spaces + your own sign-ins + points, then deploy. ADDITIVE, no data loss, safe to re-run.
# Includes everything in migrate3.sh, so run just this one:
#   cd /Users/design/shared-planner && bash migrate4.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "──────── account check ────────"
echo "Must be the mahesh@trueleap.io account that hosts hate club (workers subdomain mahesh-3dd). Ctrl-C if it isn't."
npx wrangler whoami
echo

add_col() {  # a column that already exists is skipped
  npx wrangler d1 execute shared-planner --remote --command "ALTER TABLE $1 ADD COLUMN $2" >/dev/null 2>&1 && echo "  + $1.$2" || echo "  · $1.$2 already there"
}

echo "──────── spaces (from migrate3) ────────"
for t in projects tasks habits notes topics journal; do add_col "$t" "space_id TEXT"; done
npx wrangler d1 execute shared-planner --remote --file=migrate3.sql

echo "──────── accounts + points ────────"
add_col people "username TEXT"
add_col people "pass_hash TEXT"
add_col people "pass_salt TEXT"
add_col people "pass_iter INTEGER"
add_col tasks "done_at INTEGER"
add_col tasks "done_by TEXT"
npx wrangler d1 execute shared-planner --remote --file=migrate4.sql

echo "──────── deploy ────────"
npx wrangler deploy

echo
echo "✅ Live. Next, each of you opens https://shared-planner.mahesh-3dd.workers.dev"
echo "   and taps 'First time? Set up your sign-in': the shared passcode once,"
echo "   then your own username + password. After that the passcode isn't needed."
