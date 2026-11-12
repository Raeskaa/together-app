#!/usr/bin/env bash
# One-shot deploy for Shared Planner → your personal Cloudflare account.
# Run from your own terminal (where `wrangler login` is active):
#     cd /Users/design/shared-planner && bash deploy.sh
set -euo pipefail
cd "$(dirname "$0")"

# ===== 1. The shared setup passcode. Set it in your env before running, or edit the fallback. =====
PASSCODE="${PLANNER_PASSCODE:-change-me}"

echo "──────── account check ────────"
echo "Make sure the account below is YOUR PERSONAL one (not Trueleap). Ctrl-C to abort if wrong."
npx wrangler whoami
echo

echo "──────── D1 database ────────"
CREATE_OUT="$(npx wrangler d1 create shared-planner 2>&1 || true)"
echo "$CREATE_OUT"
DBID="$(printf '%s' "$CREATE_OUT" | grep -oiE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1 || true)"
if [ -z "$DBID" ]; then
  # already existed — look it up
  DBID="$(npx wrangler d1 list --json 2>/dev/null | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{const a=JSON.parse(s);const m=a.find(x=>x.name==="shared-planner");process.stdout.write(m&&(m.uuid||m.database_id)||"")}catch(e){}})')"
fi
if [ -z "$DBID" ]; then echo "ERROR: could not determine the D1 database_id."; exit 1; fi
echo "database_id = $DBID"

# write the id into wrangler.toml
DBID="$DBID" node -e 'const fs=require("fs");const p="wrangler.toml";let t=fs.readFileSync(p,"utf8");t=t.replace(/database_id = "[^"]*"/,`database_id = "${process.env.DBID}"`);fs.writeFileSync(p,t);console.log("wrangler.toml updated");'

echo "──────── schema + seed (remote) ────────"
npx wrangler d1 execute shared-planner --remote --file=schema.sql

echo "──────── deploy ────────"
npx wrangler deploy

echo "──────── secrets ────────"
openssl rand -hex 32 | npx wrangler secret put SESSION_SECRET
printf '%s' "$PASSCODE" | npx wrangler secret put PLANNER_PASSCODE

echo
echo "✅ Deployed. Open the *.workers.dev URL printed under 'deploy' above."
echo "   Shared passcode: $PASSCODE   (change later: edit PASSCODE and re-run, or: npx wrangler secret put PLANNER_PASSCODE)"
