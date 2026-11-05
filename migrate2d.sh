#!/usr/bin/env bash
# Shared Planner — bring the live DB fully up to date, then deploy (ADDITIVE, no data loss).
# Adds: notes board, shared focus timer, waves, and the tasks.due_time column.
# Safe to run even if you already ran migrate2c.sh. Run in your own terminal:
#   cd /Users/design/shared-planner && bash migrate2d.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "──────── account check ────────"
echo "Must be your PERSONAL account (mahesh-3dd). Ctrl-C if it's Trueleap."
npx wrangler whoami
echo

echo "──────── additive tables: notes, focus, waves ────────"
npx wrangler d1 execute shared-planner --remote --file=migrate2d.sql

echo "──────── add tasks.due_time (ignored if it already exists) ────────"
npx wrangler d1 execute shared-planner --remote --command "ALTER TABLE tasks ADD COLUMN due_time TEXT" || true

echo "──────── deploy ────────"
npx wrangler deploy

echo
echo "✅ Live: cohesive project cards, deadline times, the 🫶 wave, notifications,"
echo "   plus the earlier notes board + focus timer + warmer copy."
echo "   Open https://shared-planner.mahesh-3dd.workers.dev"
