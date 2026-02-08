# PowerboatList

[![CI](https://github.com/YOUR_USERNAME/PowerboatList/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/PowerboatList/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

AI-powered tool to find all production powerboats between 13'6" and 13'11" in length, rated for 40+ HP.

## Features

- 🔍 Automated web search using Brave Search API
- 🤖 AI-powered specification extraction using Claude API
- 📊 Real-time results in Google Sheets (Colab version)
- 💾 CSV export (local Python version)
- ☁️ 100% cloud-based option - runs in Google Colab
- 💰 Cost-effective (~$10-20 total)

## Quick Start

### Option 1: Google Colab (Recommended)

1. Click: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GriffinB123/PowerboatList/blob/main/powerboat_search.ipynb)
2. Run all cells
3. Enter API keys when prompted
4. Watch results populate in your Google Sheet!

### Option 2: Pip Install (Recommended for Developers)

```bash
# Install from GitHub
pip install git+https://github.com/GriffinB123/PowerboatList.git

# Or install in development mode
git clone https://github.com/GriffinB123/PowerboatList.git
cd PowerboatList
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run search
powerboatlist
# or
python search_boats.py
```

### Option 3: Manual Installation

```bash
# Clone repository
git clone https://github.com/GriffinB123/PowerboatList.git
cd PowerboatList

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run search
python search_boats.py
```

## API Keys Required

- **Brave Search API** - Free tier available (2,000 searches/month)
  - Get at: https://brave.com/search/api/
- **Anthropic API** - For Claude AI (~$10-15 for full search)
  - Get at: https://console.anthropic.com/

## Project Structure

```
PowerboatList/
├── powerboat_search.ipynb   # Google Colab notebook (recommended)
├── search_boats.py           # Local Python script
├── config_template.py        # Configuration template
├── QUICKSTART.md            # Detailed setup guide
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── memory-bank/            # Project documentation
```

## How It Works

1. **Query Generation**: Claude generates intelligent search queries for each boat manufacturer
2. **Web Search**: Brave Search API finds relevant pages with boat specifications
3. **Data Extraction**: Claude extracts and validates specifications from search results
4. **Filtering**: Only boats matching criteria (13'6"-13'11", 40+ HP) are kept
5. **Storage**: Results saved to Google Sheets or CSV file

## Customization

Edit search parameters in `config_template.py` or notebook:

```python
MIN_LENGTH = 13.5      # 13'6" in feet
MAX_LENGTH = 13.92     # 13'11" in feet
MIN_HORSEPOWER = 40    # Minimum HP rating
```

Add manufacturers to the `MANUFACTURERS` list to expand your search.

## Cost Estimates

- Brave Search API: Free tier (2,000 queries) or $5/month
- Claude API: ~$10-15 for complete search
- Google Sheets: Free
- **Total: $10-20**

## Documentation

- [Quick Start Guide](QUICKSTART.md) - Detailed setup instructions
- [Usage Examples](EXAMPLES.md) - Sample outputs and use cases
- [Project Brief](memory-bank/projectBrief.md) - Project overview
- [Architecture](memory-bank/architect.md) - Technical decisions
- [Progress](memory-bank/progress.md) - Development roadmap

## Testing

Run the included unit tests to verify functionality:

```bash
python -m unittest test_search_boats.py -v
```

Tests cover:
- Boat filtering logic
- Duplicate detection
- Boundary conditions
- Error handling
- API mocking

## Troubleshooting

**"API Key Invalid"**: Double-check your keys are correct and active
**"Rate Limit Exceeded"**: Wait an hour or upgrade to paid tier
**"No Results Found"**: Try expanding the manufacturer list or search parameters

## Development Tools

### Ralph Loop

For iterative AI-driven development tasks, this project includes the Ralph Loop plugin.

```bash
/ralph-loop:ralph-loop <YOUR_TASK_DESCRIPTION> --max-iterations 20
```

## Contributing

Found a boat that was missed? Submit a PR or open an issue!

## License

MIT License - See LICENSE file
