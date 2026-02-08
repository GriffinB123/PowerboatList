# PowerboatList - Usage Examples

This document provides examples of using PowerboatList to find boats matching your criteria.

## Example 1: Basic Search (3 Manufacturers)

```bash
python search_boats.py
```

**Sample Output:**
```
Starting Powerboat Search...

Processing Boston Whaler...
Searching for: Boston Whaler boats 13-14 feet specifications
  Found candidate: Boston Whaler 130 Sport

Processing Carolina Skiff...
Searching for: Carolina Skiff existing 13 foot boat models specs
  Found candidate: Carolina Skiff JVX 13

Processing Gheenoe...
Searching for: Gheenoe 13'6" to 13'11" boat reviews

--- Filtering Results ---

Found 2 valid boats:
- Boston Whaler 130 Sport: 13.5ft, 40HP
- Carolina Skiff JVX 13: 13.75ft, 50HP

✓ Results saved to: powerboat_results_20260109_083045.csv
```

## Example 2: Expected CSV Output

**File: powerboat_results_20260109_083045.csv**

```csv
make,model,length_ft,max_hp,dry_weight_lbs,beam_inches
Boston Whaler,130 Sport,13.5,40,475,59
Carolina Skiff,JVX 13,13.75,50,425,64
Gheenoe,Classic,13.5,40,125,48
MFG,1300SC,13.83,50,550,62
```

## Example 3: Google Colab Output

When running in Google Colab, results populate in your Google Sheet in real-time:

| Manufacturer | Model | Length (ft) | Max HP | URL | Notes |
|--------------|-------|-------------|---------|-----|-------|
| Boston Whaler | 130 Sport | 13.5 | 40 | https://... | Classic design |
| Carolina Skiff | JVX 13 | 13.75 | 50 | https://... | Shallow draft |
| Gheenoe | Classic | 13.5 | 40 | https://... | Ultra-light |

## Example 4: Customizing Search Parameters

Edit your `.env` file or notebook cell to adjust criteria:

```python
# Search for slightly different range
MIN_LENGTH = 13.0      # 13'0"
MAX_LENGTH = 14.0      # 14'0"
MIN_HORSEPOWER = 30    # Lower HP requirement

# Expand manufacturer list
MANUFACTURERS = [
    "Boston Whaler",
    "Carolina Skiff",
    "Gheenoe",
    "Blazer Boats",
    "Duracraft",
    # Add your favorites...
]
```

## Example 5: Testing with Limited Manufacturers

For testing or debugging, modify the script to use fewer manufacturers:

```python
# In search_boats.py, find this line:
manufacturers = ["Boston Whaler", "Carolina Skiff", "Gheenoe"]

# This limits the search to 3 manufacturers for faster testing
```

## Example 6: Reading Results

**Python Script to Analyze CSV:**

```python
import pandas as pd

# Load results
df = pd.read_csv('powerboat_results_20260109_083045.csv')

# Find lightest boat
lightest = df.loc[df['dry_weight_lbs'].idxmin()]
print(f"Lightest: {lightest['make']} {lightest['model']} - {lightest['dry_weight_lbs']} lbs")

# Find highest HP
most_powerful = df.loc[df['max_hp'].idxmax()]
print(f"Most Powerful: {most_powerful['make']} {most_powerful['model']} - {most_powerful['max_hp']} HP")

# Group by manufacturer
by_manufacturer = df.groupby('make').size()
print(f"\nBoats per manufacturer:\n{by_manufacturer}")
```

## Example 7: Expected API Costs

For a typical search:

**Small Search (5 manufacturers, 3 queries each):**
- Brave Search: 15 queries = Free (within 2,000/month limit)
- Claude API: ~45 requests × $0.25/1K tokens = ~$2-3
- Total: **~$2-3**

**Full Search (50 manufacturers, 3 queries each):**
- Brave Search: 150 queries = Free (within 2,000/month limit)
- Claude API: ~450 requests = ~$10-15
- Total: **~$10-15**

## Example 8: Error Handling

The script gracefully handles common errors:

```
Error: BRAVE_API_KEY is not set in environment or .env file.
Please obtain a key from https://brave.com/search/api/

Error searching for 'Boston Whaler specs': 429 Rate Limit Exceeded
[Script continues with other manufacturers...]

Warning: ANTHROPIC_API_KEY not found. Specs extraction will be disabled.
[Falls back to basic search queries]
```

## Example 9: Running Tests

```bash
# Run unit tests
python -m unittest test_search_boats.py

# Run with verbose output
python -m unittest test_search_boats.py -v

# Expected output:
test_filter_boundary_conditions (__main__.TestFilterBoats) ... ok
test_filter_handles_invalid_data (__main__.TestFilterBoats) ... ok
test_filter_removes_duplicates (__main__.TestFilterBoats) ... ok
test_filter_valid_boats (__main__.TestFilterBoats) ... ok
...
----------------------------------------------------------------------
Ran 9 tests in 0.043s

OK
```

## Example 10: Integration with Other Tools

**Export to Excel:**
```python
import pandas as pd

df = pd.read_csv('powerboat_results_20260109_083045.csv')
df.to_excel('powerboat_results.xlsx', index=False)
```

**Filter and Sort:**
```python
# Find boats under 500 lbs
lightweight = df[df['dry_weight_lbs'] < 500]

# Sort by length
sorted_by_length = df.sort_values('length_ft')

# Filter by manufacturer
whaler_boats = df[df['make'] == 'Boston Whaler']
```

## Tips for Best Results

1. **Start Small**: Test with 2-3 manufacturers first
2. **Check API Usage**: Monitor your Anthropic dashboard
3. **Save Results**: Back up CSV files regularly
4. **Verify Data**: Cross-check critical specs with manufacturer websites
5. **Expand Gradually**: Add more manufacturers as you verify results

## Common Use Cases

- **Boat Shopping**: Find all options in your desired size range
- **Market Research**: Analyze what's available in a specific segment
- **Comparison**: Export to spreadsheet for side-by-side comparison
- **Dealer Research**: Identify brands to stock in a specific size
- **Historical Data**: Track model availability over time

## Getting Help

If results seem incomplete:
1. Check API keys are valid
2. Verify internet connection
3. Try expanding search queries
4. Check Brave Search and Claude API status pages
5. Review error messages for specific issues
