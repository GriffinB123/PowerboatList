---
description: Run the boat search script
allowed-tools: Bash
---

Run the PowerboatList search:

1. Check `.env` exists: `test -f .env && echo "OK" || echo "MISSING"`
2. If missing, warn user to copy from `.env.example`
3. Run: `python3 search_boats.py`
4. Report results summary
