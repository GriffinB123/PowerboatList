# Powerboat Database Search

AI-powered tool to find all production powerboats between 13'6" and 13'11" in length, rated for 40+ HP.

## Features
- 🔍 Automated web search using Brave Search API
- 🤖 AI-powered specification extraction using Claude API
- 📊 Real-time results stored in Google Sheets
- ☁️ 100% cloud-based - runs in Google Colab
- 💰 Cost-effective (~$10-20 total)

## Quick Start

### 1. Set Up API Keys
You'll need:
- **Brave Search API Key** (free tier: 2,000 searches/month)
  - Get it at: https://brave.com/search/api/
- **Anthropic API Key** (for Claude)
  - Get it at: https://console.anthropic.com/
- **Google Sheets** (free with Google account)

### 2. Run in Google Colab

**Click here to open in Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GriffinB123/PowerboatList/blob/main/powerboat_search.ipynb)

### 3. Follow the Notebook Instructions
1. Click "Connect" in Colab
2. Enter your API keys when prompted
3. Enter your Google Sheet URL
4. Click "Run All" or run cells one by one
5. Watch results populate in real-time!

## Project Structure
```
powerboat-search/
├── README.md                    # This file
├── powerboat_search.ipynb       # Main Colab notebook (run this!)
├── search_boats.py              # Core search logic
├── config_template.py           # Configuration template
├── requirements.txt             # Python dependencies
├── QUICKSTART.md                # Detailed setup guide
└── .gitignore                   # Git ignore file
```

## How It Works

1. **Query Generation**: Claude generates intelligent search queries for each boat manufacturer
2. **Web Search**: Brave Search API finds relevant pages with boat specifications
3. **Data Extraction**: Claude extracts and validates specifications from search results
4. **Filtering**: Only boats matching criteria (13'6"-13'11", 40+ HP) are kept
5. **Storage**: Results are automatically added to your Google Sheet in real-time

## Cost Estimates
- Brave Search API: Free tier (2,000 queries) or $5/month
- Claude API: ~$10-15 for complete search
- Google Sheets: Free
- **Total: $10-20**

## Customization

Edit these parameters in the notebook:
- Length range (currently 13'6" to 13'11")
- Minimum horsepower (currently 40 HP)
- Manufacturer list
- Search depth/thoroughness

## Troubleshooting

**"API Key Invalid"**: Double-check your keys are correct and active
**"Rate Limit Exceeded"**: Wait an hour or upgrade to paid tier
**"No Results Found"**: Try expanding the manufacturer list or search parameters

## Contributing
Found a boat that was missed? Submit a PR or open an issue!

## License
MIT License - feel free to modify and use for your own projects.