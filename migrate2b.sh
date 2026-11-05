#!/usr/bin/env bash
# Shared Planner — Phase 2b: add habits/topics tables (additive, no data loss), then redeploy.
# Run in your own terminal: cd /Users/design/shared-planner && bash migrate2b.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "──────── account check ────────"
echo "Must be your PERSONAL account (mahesh-3dd). Ctrl-C if it's Trueleap."
npx wrangler whoami
echo

echo "──────── add habits/topics tables + seed starter habits (additive) ────────"
npx wrangler d1 execute shared-planner --remote --file=migrate2b.sql

echo "──────── deploy ────────"
npx wrangler deploy

echo
echo "✅ Phase 2b migrated + deployed. Open https://shared-planner.mahesh-3dd.workers.dev"
