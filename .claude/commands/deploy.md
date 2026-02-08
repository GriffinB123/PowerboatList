---
description: Build and publish package
allowed-tools: Bash
---

Build and publish the PowerboatList package.

Steps:
1. Run `python3 -m pytest test_search_boats.py -v` to verify tests pass
2. Run `black .` to ensure formatting
3. Run `python3 setup.py sdist bdist_wheel`
4. Report the built artifacts
