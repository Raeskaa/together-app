#!/usr/bin/env bash
# Shared Planner — migrate the LIVE D1 to v2 (Calendar + Projects) and blank the slate, then redeploy.
# Run in your own terminal: cd /Users/design/shared-planner && bash migrate.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "──────── account check ────────"
echo "Must be your PERSONAL account (mahesh-3dd). Ctrl-C if it's Trueleap."
npx wrangler whoami
echo

echo "──────── add new project columns (safe if they already exist) ────────"
npx wrangler d1 execute shared-planner --remote --command 'ALTER TABLE projects ADD COLUMN description TEXT' 2>/dev/null \
  && echo "  + description" || echo "  description already present (ok)"
npx wrangler d1 execute shared-planner --remote --command 'ALTER TABLE projects ADD COLUMN archived INTEGER DEFAULT 0' 2>/dev/null \
  && echo "  + archived" || echo "  archived already present (ok)"

echo "──────── create project_materials + blank the slate ────────"
npx wrangler d1 execute shared-planner --remote --file=migrate.sql

echo "──────── deploy ────────"
npx wrangler deploy

echo
echo "✅ Migrated to v2 and redeployed."
echo "   Open https://shared-planner.mahesh-3dd.workers.dev  (passcode unchanged: planner2027)"
