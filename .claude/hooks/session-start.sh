#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install dependencies based on what exists in the project
cd "$CLAUDE_PROJECT_DIR"

# Node.js
if [ -f "package.json" ]; then
  npm install
fi

# Python
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
  pip install -e .
fi

# Go
if [ -f "go.mod" ]; then
  go mod download
fi

# Ruby
if [ -f "Gemfile" ]; then
  bundle install
fi

# Rust
if [ -f "Cargo.toml" ]; then
  cargo fetch
fi

# Ruflo agent orchestration (global, idempotent: installs once per cached sandbox)
if ! command -v ruflo >/dev/null 2>&1; then
  npm install -g ruflo@latest
fi
