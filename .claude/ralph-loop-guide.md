# Ralph Loop Usage Guide

## Overview

Ralph Loop is a self-referential AI development loop that allows Claude to iteratively work on tasks until completion. It uses a stop hook to prevent session exit and feeds the same prompt back repeatedly.

## Command Syntax

### Basic Usage

```bash
/ralph-loop:ralph-loop <PROMPT> [OPTIONS]
```

**IMPORTANT**: The `PROMPT` argument is **REQUIRED**. The script will fail with an "unbound variable" error if no prompt is provided.

### Options

- `--max-iterations <n>` - Maximum iterations before auto-stop (default: unlimited)
- `--completion-promise '<text>'` - Promise phrase to signal completion (use quotes for multi-word)
- `-h, --help` - Show help message

## Examples

### Simple Task
```bash
/ralph-loop:ralph-loop Build a REST API for todos --max-iterations 20
```

### With Completion Promise
```bash
/ralph-loop:ralph-loop Fix the authentication bug --completion-promise 'DONE' --max-iterations 15
```

### Complex Task
```bash
/ralph-loop:ralph-loop Create a user management system with CRUD operations, validation, and tests --completion-promise 'ALL TESTS PASSING' --max-iterations 50
```

### Multi-word Prompt
```bash
/ralph-loop:ralph-loop Refactor the database layer to use connection pooling --max-iterations 30
```

## Common Errors

### Error: "unbound variable PROMPT_PARTS[*]"

**Cause**: No prompt was provided to the command.

**Solution**: Always provide a prompt text after `/ralph-loop:ralph-loop`:

❌ **Wrong**: `/ralph-loop:ralph-loop` (no prompt)

✅ **Correct**: `/ralph-loop:ralph-loop Build a feature`

## How It Works

1. You run `/ralph-loop:ralph-loop` with a prompt
2. Claude works on the task
3. When Claude tries to exit, the stop hook intercepts
4. The stop hook feeds the **same prompt** back to Claude
5. Claude sees its previous work in files and continues iterating
6. Loop continues until:
   - Max iterations reached, OR
   - Completion promise is output (if set)

## Best Practices

### 1. Always Set Max Iterations

Use `--max-iterations` as a safety net:

```bash
/ralph-loop:ralph-loop <task> --max-iterations 20
```

### 2. Clear Completion Criteria

Include specific completion criteria in your prompt:

```bash
/ralph-loop:ralph-loop Build a todo API. Requirements: CRUD endpoints, input validation, tests passing, README with API docs. Output <promise>COMPLETE</promise> when done. --completion-promise 'COMPLETE' --max-iterations 50
```

### 3. Use Completion Promises Wisely

The completion promise must be **completely true** when output. Claude should never lie to exit the loop.

```bash
/ralph-loop:ralph-loop Implement feature X with tests --completion-promise 'ALL TESTS PASSING' --max-iterations 30
```

### 4. Incremental Goals

Break complex tasks into phases:

```bash
/ralph-loop:ralph-loop Phase 1: Setup database schema. Phase 2: Create API endpoints. Phase 3: Add tests. Output <promise>DONE</promise> when all phases complete. --completion-promise 'DONE' --max-iterations 40
```

## Monitoring Progress

View current iteration:
```bash
grep '^iteration:' .claude/ralph-loop.local.md
```

View full state:
```bash
head -10 .claude/ralph-loop.local.md
```

## Canceling a Loop

```bash
/cancel-ralph
```

## When to Use Ralph Loop

**Good for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration (e.g., getting tests to pass)
- Greenfield projects
- Tasks with automatic verification

**Not good for:**
- Tasks requiring human judgment
- One-shot operations
- Tasks with unclear success criteria
- Production debugging

## Required Arguments Summary

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `PROMPT` | ✅ **YES** | Task description | `Build a REST API` |
| `--max-iterations` | ❌ No | Safety limit | `--max-iterations 20` |
| `--completion-promise` | ❌ No | Completion signal | `--completion-promise 'DONE'` |

**Remember**: The `PROMPT` is the only required argument. Without it, the script will fail with an error.
