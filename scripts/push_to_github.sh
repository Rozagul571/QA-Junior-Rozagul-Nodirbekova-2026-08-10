#!/usr/bin/env bash
# One-shot: authenticate (if needed) and publish this repo to GitHub.
# Run from the repo root:  bash scripts/push_to_github.sh
set -e

REPO_NAME="QA-Junior-Rozagul-Nodirbekova-2026-08-10"

# 1) make sure gh is authenticated (opens a browser / device-code flow)
if ! gh auth status >/dev/null 2>&1; then
  echo ">> Not authenticated — starting gh login..."
  gh auth login
fi

# 2) create the GitHub repo and push the current commit
#    change --public to --private if you prefer a private repo
gh repo create "$REPO_NAME" \
  --source=. \
  --public \
  --description "QA Automation Engineer (Mobile) assignment — Enatega: manual tests, Appium POM, Postman API, answers" \
  --remote=origin \
  --push

echo ">> Done. Repo: $(gh repo view --json url -q .url)"
