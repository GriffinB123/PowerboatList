#!/bin/bash
# Auto-approve common dev commands without prompting
# Triggered by PermissionRequest hook

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [[ "$COMMAND" =~ ^python3?\ (-m\ pytest|search_boats|setup\.py) ]] || \
   [[ "$COMMAND" =~ ^pip3?\ install ]] || \
   [[ "$COMMAND" =~ ^black ]] || \
   [[ "$COMMAND" =~ ^lsof ]] || \
   [[ "$COMMAND" =~ ^curl ]] || \
   [[ "$COMMAND" =~ ^sqlite3 ]] || \
   [[ "$COMMAND" =~ ^git\ (init|status|diff|log|branch|add|remote|commit|push) ]] || \
   [[ "$COMMAND" =~ ^gh\ (repo|pr|issue|auth|api) ]] || \
   [[ "$COMMAND" =~ ^/opt/homebrew/bin/gh ]] || \
   [[ "$COMMAND" =~ ^/opt/homebrew/bin/brew ]]; then

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

exit 0
