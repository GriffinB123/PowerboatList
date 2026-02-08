---
argument-hint: [specific test class or file]
description: Run pytest and fix any failures
allowed-tools: Bash, Read, Edit, Write
---

Run tests and fix any failures automatically.

Target: $ARGUMENTS (or all tests if not specified)

Steps:
1. Run `python3 -m pytest test_search_boats.py -v` (or specific test if provided)
2. If tests pass, report success
3. If tests fail:
   - Analyze the failure
   - Fix the code
   - Re-run tests
   - Repeat until passing

Don't ask for permission to fix — just fix and verify.
