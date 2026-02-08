# Configuration Template
# Copy this file to 'config.py' and add your actual API keys
# NEVER commit config.py to GitHub!

# API Keys
BRAVE_API_KEY = "your_brave_api_key_here"
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"

# Google Sheet URL
GOOGLE_SHEET_URL = "your_google_sheet_url_here"

# Search Parameters
MIN_LENGTH = 13.5  # 13'6" in feet
MAX_LENGTH = 13.92  # 13'11" in feet
MIN_HORSEPOWER = 40

# Boat Manufacturers to Search
MANUFACTURERS = [
    "Boston Whaler",
    "Glastron",
    "MFG",
    "Starcraft",
    "Alumacraft",
    "Lund",
    "Crestliner",
    "Smoker Craft",
    "Princecraft",
    "Legend",
    "Larson",
    "Four Winns",
    "Sea Ray",
    "Bayliner",
    "Tracker",
    "Ranger",
    "Skeeter",
    "Bass Cat",
    "Triton",
    "Nitro",
    "Champion",
    "Stratos",
    "Javelin",
    "Gambler",
    "Hydra-Sports",
    "Mako",
    "Aquasport",
    "Wellcraft",
    "Grumman",
    "Sylvan",
    "Mirrocraft",
    "Polar Kraft",
    "G3 Boats",
    "Xpress Boats",
    "War Eagle",
    "SeaArk",
    "Alweld",
    "Xtreme Boats",
    "Excel Boats",
]

# Search Settings
QUERIES_PER_MANUFACTURER = 3
MAX_SEARCH_RESULTS_PER_QUERY = 10
DELAY_BETWEEN_SEARCHES = 1  # seconds
