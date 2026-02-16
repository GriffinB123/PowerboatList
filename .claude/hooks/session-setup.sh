#!/bin/bash
# SessionStart hook: Verify git/gh setup and detect project stack
# Outputs actionable context for Claude to fix automatically

# Use full path to gh (homebrew location)
GH="/opt/homebrew/bin/gh"
[ ! -x "$GH" ] && GH="/usr/local/bin/gh"
[ ! -x "$GH" ] && GH=$(which gh 2>/dev/null)

ACTIONS=""

# Check git initialization
if [ ! -d ".git" ]; then
  ACTIONS="ACTION REQUIRED: Initialize git repository with 'git init' before any git operations."
fi

# Check gh CLI
if [ -z "$GH" ] || [ ! -x "$GH" ]; then
  ACTIONS="$ACTIONS
ACTION REQUIRED: GitHub CLI not installed. Run '/opt/homebrew/bin/brew install gh' to install."
else
  # Check gh authentication
  if ! $GH auth status &> /dev/null 2>&1; then
    ACTIONS="$ACTIONS
ACTION REQUIRED: GitHub CLI not authenticated. Tell user to run 'gh auth login' in their terminal (requires browser)."
  fi

  # Export gh path for other hooks
  echo "GH_CLI_PATH=$GH"
fi

# Check for remote origin (only if git exists)
if [ -d ".git" ] && ! git remote get-url origin &> /dev/null 2>&1; then
  ACTIONS="$ACTIONS
NOTE: No GitHub remote configured. When user wants to push, use: $GH repo create <name> --private --source=. --push"
fi

# Detect project stack
STACK="unknown"
DEV_CMD=""
TEST_CMD=""

if [ -f "package.json" ]; then
  STACK="node"
  DEV_CMD="npm run dev"
  TEST_CMD="npm test"
elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
  STACK="python"
  DEV_CMD="python app.py"
  TEST_CMD="pytest"
  if [ -f "pyproject.toml" ] && grep -q "uvicorn\|fastapi" pyproject.toml 2>/dev/null; then
    DEV_CMD="uvicorn main:app --reload"
  elif [ -f "pyproject.toml" ] && grep -q "flask" pyproject.toml 2>/dev/null; then
    DEV_CMD="python -m flask run"
  elif [ -f "requirements.txt" ] && grep -q "flask" requirements.txt 2>/dev/null; then
    DEV_CMD="python -m flask run"
  fi
elif [ -f "go.mod" ]; then
  STACK="go"
  DEV_CMD="go run ."
  TEST_CMD="go test ./..."
elif [ -f "Cargo.toml" ]; then
  STACK="rust"
  DEV_CMD="cargo run"
  TEST_CMD="cargo test"
elif [ -f "Gemfile" ]; then
  STACK="ruby"
  DEV_CMD="bundle exec rails s"
  TEST_CMD="bundle exec rspec"
fi

if [ "$STACK" != "unknown" ]; then
  echo "PROJECT_STACK=$STACK"
  echo "DEV_CMD=$DEV_CMD"
  echo "TEST_CMD=$TEST_CMD"
else
  echo "NOTE: Could not detect project stack. No package.json, pyproject.toml, go.mod, Cargo.toml, or Gemfile found."
fi

if [ -n "$ACTIONS" ]; then
  echo "$ACTIONS"
fi

exit 0
