#!/usr/bin/env bash
# Shared Planner — move to spaces (people + spaces + members), then deploy. ADDITIVE, no data loss, safe to re-run.
# Run in your own terminal:
#   cd /Users/design/shared-planner && bash migrate3.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "──────── account check ────────"
echo "Must be your PERSONAL account (mahesh-3dd). Ctrl-C if it's Trueleap."
npx wrangler whoami
echo

echo "──────── add space_id to each table (a column that already exists is skipped) ────────"
for t in projects tasks habits notes topics journal; do
  npx wrangler d1 execute shared-planner --remote --command "ALTER TABLE $t ADD COLUMN space_id TEXT" || true
done

echo "──────── people, spaces, members + move today's data into the 'hate club' space ────────"
npx wrangler d1 execute shared-planner --remote --file=migrate3.sql

echo "──────── deploy ────────"
npx wrangler deploy

echo
echo "✅ Live: the same two-person app, now built on spaces."
echo "   Anyone with the app open should reload it once."
echo "   Open https://shared-planner.mahesh-3dd.workers.dev"
