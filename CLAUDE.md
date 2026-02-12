# PowerboatList

AI-powered tool to find production powerboats matching specific criteria (13'6"-13'11", 40+ HP) using Brave Search + Claude APIs.

> **Note:** This file contains project-specific instructions. Global standards (permissions, git workflow, code style principles, MCP usage) are defined in `~/.claude/CLAUDE.md`.

---

## Quick Reference

```bash
# Run search
python search_boats.py

# Run tests
python -m pytest test_search_boats.py -v

# Install in dev mode
pip install -e .

# Setup
cp .env.example .env  # then add API keys
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8+ |
| APIs | Brave Search, Anthropic Claude |
| Code Style | Black (enforced via pre-commit) |
| Testing | pytest |
| Notebook | Jupyter (Google Colab compatible) |

---

## Project Structure

```
PowerboatList/
├── search_boats.py          # Main search script
├── powerboat_search.ipynb   # Google Colab notebook
├── test_search_boats.py     # Unit tests
├── config_template.py       # Configuration template
├── setup.py                 # Package setup
├── .env.example             # Environment template
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Dev dependencies
├── pytest.ini               # Test configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
└── memory-bank/             # Project documentation
```

---

## Architecture

**Data Flow:**
```
Claude (query gen) → Brave Search API → Claude (extraction) → Filter → CSV/Sheets
```

**Key Parameters** (in `config_template.py`):
```python
MIN_LENGTH = 13.5      # 13'6" in feet
MAX_LENGTH = 13.92     # 13'11" in feet
MIN_HORSEPOWER = 40
```

---

## Project-Specific Style

- **Formatter:** Black (run via pre-commit or `black .`)
- **Docstrings:** Google-style
- **Type hints:** Encouraged but not enforced
- Pre-commit runs Black + basic linting on commit

---

## Forbidden Files

Do not commit or read unnecessarily:
- `.env` — contains Brave Search and Anthropic API keys
- `boats.db` — SQLite runtime database
- `*.log` — runtime logs
- `boats.csv` — output artifact
- `PowerboatList/` subdirectory — legacy/duplicate, ignore

---

## Environment Variables

Required in `.env`:
```
BRAVE_API_KEY=your_brave_search_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

---

## Testing

```bash
# Run all tests
python -m pytest test_search_boats.py -v

# Run specific test
python -m pytest test_search_boats.py::TestBoatFiltering -v
```

Tests cover: filtering logic, duplicate detection, boundary conditions, API mocking.

---

## Parallel Work

### Git Worktrees
```bash
git worktree add ../PowerboatList-feature -b feature-name
git worktree remove ../PowerboatList-feature
```

### Agent Teams
Claude automatically spawns agent teams for complex tasks (cross-layer features, multi-perspective reviews, competing-hypothesis debugging). No commands needed — see global CLAUDE.md for trigger rules.

---

## Debugging (This Project)

| Issue | Solution |
|-------|----------|
| API key errors | Verify `.env` exists and has valid keys |
| No results | Check Brave Search API quota (2,000/month free) |
| Import errors | Run `pip install -e .` or `pip install -r requirements.txt` |
| Pre-commit fails | Run `black .` to format, then retry commit |
