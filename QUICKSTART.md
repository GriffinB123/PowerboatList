# PowerboatList - Quick Start Guide

AI-powered tool to find production powerboats between 13'6" and 13'11" in length, rated for 40+ HP.

## Prerequisites

- Python 3.8 or higher
- Brave Search API key (free tier available)
- Anthropic API key (Claude)
- Google Account (for Sheets integration in Colab version)

## Setup Options

### Option 1: Google Colab (Recommended - No Installation)

1. **Open the Colab Notebook**
   - Click: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/PowerboatList/blob/main/powerboat_search.ipynb)

2. **Run the Setup Cell**
   - Click "Runtime" → "Run all"
   - Enter your API keys when prompted
   - Paste your Google Sheet URL

3. **Watch Results Populate**
   - Results save to your Google Sheet in real-time
   - Progress updates show in the notebook

### Option 2: Local Python Script

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PowerboatList.git
   cd PowerboatList
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_key_here
   BRAVE_API_KEY=your_brave_key_here
   ```

4. **Run the Search**
   ```bash
   python search_boats.py
   ```

## Getting API Keys

### Brave Search API
1. Visit: https://brave.com/search/api/
2. Sign up for free account
3. Get your API key (2,000 free searches/month)

### Anthropic API (Claude)
1. Visit: https://console.anthropic.com/
2. Create account and add payment method
3. Generate API key
4. Estimated cost: $10-20 for full search

## Configuration

### Search Parameters

Edit these in the script or notebook:

```python
MIN_LENGTH = 13.5      # 13'6" in feet
MAX_LENGTH = 13.92     # 13'11" in feet
MIN_HORSEPOWER = 40    # Minimum HP rating
```

### Manufacturer List

Add or remove manufacturers in the `MANUFACTURERS` list:

```python
MANUFACTURERS = [
    "Boston Whaler",
    "Carolina Skiff",
    "Gheenoe",
    # Add more...
]
```

## Usage Tips

1. **Start Small**: Test with 2-3 manufacturers first to verify API keys work
2. **Monitor Costs**: Check your Anthropic usage dashboard
3. **Rate Limiting**: Built-in delays prevent API throttling
4. **Save Results**: Export Google Sheet to CSV for backup

## Troubleshooting

### "API Key Invalid"
- Double-check your API keys are correct
- Ensure no extra spaces in `.env` file
- Verify API keys are active in your account

### "Rate Limit Exceeded"
- Brave Search: Wait an hour or upgrade to paid tier
- Claude API: Check usage limits in console

### "No Results Found"
- Try different manufacturers
- Expand search queries
- Check if manufacturer still produces boats in this size

## Cost Breakdown

- **Brave Search API**: Free tier (2,000 queries) or $5/month
- **Anthropic Claude API**: ~$10-15 for complete search of 50 manufacturers
- **Google Sheets**: Free
- **Total**: $10-20 for full database build

## Next Steps

1. Run test search with 3 manufacturers
2. Verify results in output
3. Expand manufacturer list
4. Export final results to CSV

## Support

- Issues: https://github.com/YOUR_USERNAME/PowerboatList/issues
- Documentation: See README.md
- API Docs:
  - Brave: https://brave.com/search/api/docs/
  - Claude: https://docs.anthropic.com/

## License

MIT License - See LICENSE file
