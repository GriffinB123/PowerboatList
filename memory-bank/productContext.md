# Product Context

## The Problem
Finding small powerboats with high horsepower ratings is difficult. Most manufacturer sites are unstandardized, and "13 foot" boats range from 12'8" to 13'11". Enthusiasts specifically want the maximum length possible under 14 feet (often for registration/storage reasons) with maximum power (40HP+). Manually searching forums and archives for old specs is tedious.

## The Solution
A "Ralph Loop" inspired AI agent that:
1. Generates intelligent search queries for specific manufacturers.
2. Scrapes search results.
3. Uses an LLM (Claude) to structure the unstructured data.
4. Filters strictly on the dimension/power requirements.
5. Outputs a clean spreadsheet.

## User Experience requirements
- **One-click**: The user should ideally just click "Run" in Colab.
- **Transparent**: The user sees what boats are found and why.
- **Resilient**: If an API key fails or a site is down, it shouldn't crash the whole run.
