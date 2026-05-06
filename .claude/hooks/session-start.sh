#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Ruflo agent orchestration (global, idempotent: installs once per cached sandbox).
# Run before the project cd so ruflo activation is not coupled to project-dir state
# or to the success of any project-dependency install below.
if ! command -v ruflo >/dev/null 2>&1; then
  npm install -g ruflo@latest
fi

# Install dependencies based on what exists in the project.
# Default CLAUDE_PROJECT_DIR to pwd so set -u does not abort when the harness
# omits the variable; the hook is invoked from the repo root in that case.
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

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
