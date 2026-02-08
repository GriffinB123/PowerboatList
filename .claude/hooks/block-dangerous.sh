#!/bin/bash
# Block dangerous commands before they execute
# Triggered by PreToolUse hook

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [[ "$COMMAND" =~ rm\ -rf\ / ]] || \
   [[ "$COMMAND" =~ rm\ -rf\ \~ ]] || \
   [[ "$COMMAND" =~ rm\ -rf\ \$HOME ]] || \
   [[ "$COMMAND" =~ git\ push.*--force ]] || \
   [[ "$COMMAND" =~ git\ reset\ --hard ]] || \
   [[ "$COMMAND" =~ DROP\ TABLE ]] || \
   [[ "$COMMAND" =~ DELETE\ FROM.*WHERE\ 1 ]]; then

  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by safety hook"
    }
  }'
  exit 0
fi

exit 0
