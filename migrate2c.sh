#!/usr/bin/env bash
# Shared Planner — add the notes board + shared focus timer (additive, no data loss),
# plus the warmer copy. Run in your own terminal:
#   cd /Users/design/shared-planner && bash migrate2c.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "──────── account check ────────"
echo "Must be the mahesh@trueleap.io account that hosts hate club (workers subdomain mahesh-3dd). Ctrl-C if it isn't."
npx wrangler whoami
echo

echo "──────── add notes + focus tables (additive, keeps your data) ────────"
npx wrangler d1 execute shared-planner --remote --file=migrate2c.sql

echo "──────── deploy ────────"
npx wrangler deploy

echo
echo "✅ Notes board + shared focus timer + warmer copy are live."
echo "   Open https://shared-planner.mahesh-3dd.workers.dev"
