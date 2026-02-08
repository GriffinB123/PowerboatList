#!/bin/bash
# SessionStart hook: Verify git and gh are set up
# Outputs actionable context for Claude to fix automatically

GH="/opt/homebrew/bin/gh"
[ ! -x "$GH" ] && GH="/usr/local/bin/gh"
[ ! -x "$GH" ] && GH=$(which gh 2>/dev/null)

ACTIONS=""

if [ ! -d ".git" ]; then
  ACTIONS="ACTION REQUIRED: Initialize git repository with 'git init' before any git operations."
fi

if [ -z "$GH" ] || [ ! -x "$GH" ]; then
  ACTIONS="$ACTIONS
ACTION REQUIRED: GitHub CLI not installed. Run '/opt/homebrew/bin/brew install gh' to install."
else
  if ! $GH auth status &> /dev/null 2>&1; then
    ACTIONS="$ACTIONS
ACTION REQUIRED: GitHub CLI not authenticated. Tell user to run 'gh auth login' in their terminal (requires browser)."
  fi
  echo "GH_CLI_PATH=$GH"
fi

if [ -d ".git" ] && ! git remote get-url origin &> /dev/null 2>&1; then
  ACTIONS="$ACTIONS
NOTE: No GitHub remote configured. When user wants to push, use: $GH repo create <name> --private --source=. --push"
fi

# Check Python env
if ! command -v python3 &> /dev/null; then
  ACTIONS="$ACTIONS
ACTION REQUIRED: python3 not found. Install via 'brew install python'."
fi

# Check .env
if [ ! -f ".env" ]; then
  ACTIONS="$ACTIONS
NOTE: .env file missing. Copy from .env.example and add API keys."
fi

if [ -n "$ACTIONS" ]; then
  echo "$ACTIONS"
fi

exit 0
