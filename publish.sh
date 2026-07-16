#!/usr/bin/env bash
# Publish Makor: stage everything, commit, push. Cloudflare rebuilds automatically.
set -e
cd "$(dirname "$0")"
MSG="${1:-Publish study update}"
git add -A
if git diff --cached --quiet; then
  echo "Nothing new to publish."
  exit 0
fi
git commit -m "$MSG"
git push
echo "Pushed. Cloudflare will rebuild; the site is usually live within two minutes."
