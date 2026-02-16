#!/bin/bash
# Auto-approve common dev commands without prompting
# Triggered by PermissionRequest hook
# Supports: Node, Python, Go, Rust, Ruby

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Auto-approve safe dev commands
if [[ "$COMMAND" =~ ^npm\ (run|test|install|build|lint|ci|start) ]] || \
   [[ "$COMMAND" =~ ^npx ]] || \
   [[ "$COMMAND" =~ ^lsof ]] || \
   [[ "$COMMAND" =~ ^curl ]] || \
   [[ "$COMMAND" =~ ^which ]] || \
   [[ "$COMMAND" =~ ^command\ -v ]] || \
   [[ "$COMMAND" =~ ^PATH= ]] || \
   [[ "$COMMAND" =~ ^git\ (init|status|diff|log|branch|add|remote|commit|push|pull|fetch|checkout|switch|stash|worktree|tag) ]] || \
   [[ "$COMMAND" =~ ^gh\ (repo|pr|issue|auth|api) ]] || \
   [[ "$COMMAND" =~ ^/opt/homebrew/bin/gh ]] || \
   [[ "$COMMAND" =~ ^/opt/homebrew/bin/brew ]] || \
   [[ "$COMMAND" =~ ^python3?\ (-m\ )?(pytest|flask|uvicorn|pip|venv|http\.server) ]] || \
   [[ "$COMMAND" =~ ^pip3?\ (install|list|show|freeze) ]] || \
   [[ "$COMMAND" =~ ^pytest ]] || \
   [[ "$COMMAND" =~ ^uv\ (run|sync|pip|venv|init) ]] || \
   [[ "$COMMAND" =~ ^go\ (run|test|build|mod|get|vet|fmt) ]] || \
   [[ "$COMMAND" =~ ^cargo\ (run|test|build|check|clippy|fmt|add) ]] || \
   [[ "$COMMAND" =~ ^bundle\ (install|exec|update) ]] || \
   [[ "$COMMAND" =~ ^rake ]] || \
   [[ "$COMMAND" =~ ^make($|\ ) ]]; then

  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PermissionRequest",
      decision: {
        behavior: "allow"
      }
    }
  }'
  exit 0
fi

# Let user decide for other commands
exit 0
