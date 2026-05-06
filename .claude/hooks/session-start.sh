#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Ruflo first: keep activation independent of project-dir state and of the
# project-dependency installs below.
if ! command -v ruflo >/dev/null 2>&1; then
  npm install -g ruflo@latest
fi

# Default CLAUDE_PROJECT_DIR so set -u does not abort when the harness omits it.
cd "${CLAUDE_PROJECT_DIR:-.}"

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
