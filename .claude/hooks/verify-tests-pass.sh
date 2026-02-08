#!/bin/bash
# Run after file edits to verify tests still pass
# Triggered by PostToolUse hook (async)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run for Python source files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
  exit 0
fi

# Skip test files themselves
if [[ "$FILE_PATH" =~ test_ ]] || [[ "$FILE_PATH" =~ _test\.py$ ]]; then
  exit 0
fi

RESULT=$(python3 -m pytest test_search_boats.py -v 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH. Fix before continuing.\"}"
fi
