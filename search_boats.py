import os
import time
import json
import requests
import sqlite3
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv
import anthropic
from bs4 import BeautifulSoup

# Database configuration
DB_FILE = "boats.db"

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('powerboat_search.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

# Initialize Claude Client
try:
    if ANTHROPIC_API_KEY:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        logger.info("✓ Claude AI client initialized successfully")
    else:
        client = None
        logger.warning("⚠ ANTHROPIC_API_KEY not found. Specs extraction will be disabled.")
        logger.warning("  Get your API key at: https://console.anthropic.com/")
except Exception as e:
    client = None
    logger.error(f"✗ Error initializing Claude client: {e}")

def init_database():
    """Initialize SQLite database with boats table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            length_ft REAL,
            max_hp INTEGER,
            dry_weight_lbs INTEGER,
            beam_inches INTEGER,
            source_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(make, model)
        )
    ''')
    conn.commit()
    conn.close()
    logger.info(f"✓ Database initialized: {DB_FILE}")

def upsert_boat(boat_data: Dict) -> bool:
    """
    Insert or update a boat in the database.
    Returns True if inserted (new), False if updated (existing).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    make = boat_data.get('make', '')
    model = boat_data.get('model', '')
    length_ft = boat_data.get('length_ft')
    max_hp = boat_data.get('max_hp')
    dry_weight = boat_data.get('dry_weight_lbs')
    beam = boat_data.get('beam_inches')
    source_url = boat_data.get('source_url', '')

    # Check if exists
    cursor.execute('SELECT id, model FROM boats WHERE make = ? AND model = ?', (make, model))
    existing = cursor.fetchone()

    if existing:
        # Update - fill in missing fields, prefer longer model name
        cursor.execute('''
            UPDATE boats SET
                length_ft = COALESCE(?, length_ft),
                max_hp = COALESCE(?, max_hp),
                dry_weight_lbs = COALESCE(?, dry_weight_lbs),
                beam_inches = COALESCE(?, beam_inches),
                source_url = COALESCE(?, source_url),
                updated_at = CURRENT_TIMESTAMP
            WHERE make = ? AND model = ?
        ''', (length_ft, max_hp, dry_weight, beam, source_url, make, model))
        conn.commit()
        conn.close()
        return False
    else:
        # Insert new
        cursor.execute('''
            INSERT INTO boats (make, model, length_ft, max_hp, dry_weight_lbs, beam_inches, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (make, model, length_ft, max_hp, dry_weight, beam, source_url))
        conn.commit()
        conn.close()
        return True

def find_duplicate_in_db(boat_data: Dict, length_tolerance: float = 0.5) -> Optional[Dict]:
    """
    Check if a similar boat exists in the database using fuzzy matching.
    Returns the existing boat data if found, None otherwise.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    new_make = boat_data.get('make', '').lower()
    new_model_norm = normalize_model_name(boat_data.get('model', ''))
    new_length = float(boat_data.get('length_ft', 0))

    cursor.execute('SELECT id, make, model, length_ft FROM boats WHERE LOWER(make) = ?', (new_make,))
    rows = cursor.fetchall()

    for row in rows:
        existing_id, existing_make, existing_model, existing_length = row
        existing_model_norm = normalize_model_name(existing_model)

        # Check length similarity
        if existing_length and abs(new_length - existing_length) > length_tolerance:
            continue

        # Check model name similarity
        if (new_model_norm == existing_model_norm or
            new_model_norm in existing_model_norm or
            existing_model_norm in new_model_norm):
            conn.close()
            return {'id': existing_id, 'make': existing_make, 'model': existing_model, 'length_ft': existing_length}

    conn.close()
    return None

def update_boat_by_id(boat_id: int, boat_data: Dict):
    """Update an existing boat by ID, merging in new data."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get current data
    cursor.execute('SELECT model, dry_weight_lbs, beam_inches FROM boats WHERE id = ?', (boat_id,))
    current = cursor.fetchone()

    if current:
        current_model, current_weight, current_beam = current
        new_model = boat_data.get('model', '')

        # Prefer longer/more specific model name
        final_model = new_model if len(new_model) > len(current_model) else current_model

        cursor.execute('''
            UPDATE boats SET
                model = ?,
                dry_weight_lbs = COALESCE(?, dry_weight_lbs),
                beam_inches = COALESCE(?, beam_inches),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (final_model, boat_data.get('dry_weight_lbs'), boat_data.get('beam_inches'), boat_id))
        conn.commit()

    conn.close()

def generate_search_queries(manufacturer: str) -> List[str]:
    """
    Uses Claude to generate targeted search queries for a specific manufacturer.
    """
    default_queries = [
        f"{manufacturer} boats 13-14 feet specifications",
        f"{manufacturer} existing 13 foot boat models specs",
        f"{manufacturer} 13'6\" to 13'11\" boat reviews"
    ]

    if not client:
        return default_queries
    
    prompt = f"""
    I am looking for detailed specifications for powerboats made by {manufacturer}.
    Specifically, I need to find models that are between 13 feet (13')
    and 14 feet (14') in length.
    
    Please generate 3 specific search queries that would help me find:
    1. Current model specifications
    2. Archived model specifications (if applicable)
    3. Forum discussions or owner details about length and horsepower for this size range.
    
    Return ONLY a JSON array of strings, nothing else. Example: ["query1", "query2"]
    """
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        # Clean up code blocks if present
        if "```" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
            
        queries = json.loads(content)
        if isinstance(queries, list) and len(queries) > 0:
            return queries
        return default_queries
    except Exception as e:
        print(f"Error generating queries for {manufacturer}: {e}")
        return default_queries

def search_web(query: str) -> List[Dict]:
    """
    Searches the web using Brave Search API.
    """
    if not BRAVE_API_KEY:
        logger.warning("⚠ BRAVE_API_KEY not set. Skipping search.")
        logger.warning("  Get your API key at: https://brave.com/search/api/")
        return []

    logger.info(f"🔍 Searching: {query}")
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {"q": query, "count": 10}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        if 'web' in data and 'results' in data['web']:
            results = data['web']['results']
            
        return results
    except Exception as e:
        print(f"Error searching for '{query}': {e}")
        return []

def fetch_webpage(url: str) -> Optional[str]:
    """
    Fetches webpage content and extracts text.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text content
        text = soup.get_text(separator=' ', strip=True)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        # Limit to first 8000 chars to avoid token limits
        return text[:8000]
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None

def extract_specs(text_content: str) -> Optional[Dict]:
    """
    Uses Claude to extract boat specifications from text content.
    """
    if not client:
        return None
        
    prompt = f"""
    Analyze the following text and extract specifications for powerboats mentioned.
    Look for boats in the 10-18 foot range.

    Text:
    {text_content[:4000]}

    Return a JSON array of boat objects. Each object should have:
    - make (string)
    - model (string)
    - length_ft (float, the LOA/overall length in feet)
    - max_hp (int, maximum horsepower rating)
    - dry_weight_lbs (int, optional)
    - beam_inches (int, optional)

    Return an empty array [] if no boats with specs are found.
    Only include boats where you can determine both length AND max HP from the text.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text
        
        # Check for empty/null before parsing
        if "null" in content.lower() and len(content) < 20:
            return []
        if content.strip() == "[]":
            return []

        # Clean up code blocks
        if "```json" in content:
            content = content.split("```json")[-1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Find JSON array in response (handle preamble text)
        if "[" in content:
            start = content.find("[")
            end = content.rfind("]") + 1
            if start != -1 and end > start:
                content = content[start:end]

        data = json.loads(content)
        # Ensure we return a list
        if isinstance(data, dict):
            data = [data]
        result = data if isinstance(data, list) else []
        if result:
            logger.info(f"   Extracted {len(result)} boats from page")
        return result
    except json.JSONDecodeError as e:
        logger.warning(f"   JSON parse error: {e} - Content: {content[:100]}")
        return []
    except Exception as e:
        print(f"Error extracting specs: {e}")
        return []

def normalize_model_name(model: str) -> str:
    """
    Normalizes a model name for duplicate comparison.
    Removes leading numbers (like '130' in '130 Super Sport') and extra whitespace.
    """
    model = model.lower().strip()
    # Remove leading numbers followed by space (e.g., "130 super sport" -> "super sport")
    model = re.sub(r'^\d+\s*', '', model)
    # Remove common suffixes/prefixes that might vary
    model = re.sub(r'\s+', ' ', model)  # Normalize whitespace
    return model

def is_duplicate_boat(new_boat: Dict, seen_boats: List[Dict], length_tolerance: float = 0.5) -> bool:
    """
    Checks if a boat is a duplicate of any previously seen boat.
    Uses fuzzy matching on model names and length similarity.
    """
    new_make = new_boat.get('make', '').lower()
    new_model = new_boat.get('model', '')
    new_model_norm = normalize_model_name(new_model)
    new_length = float(new_boat.get('length_ft', 0))

    for seen in seen_boats:
        seen_make = seen.get('make', '').lower()
        seen_model = seen.get('model', '')
        seen_model_norm = normalize_model_name(seen_model)
        seen_length = float(seen.get('length_ft', 0))

        # Must be same manufacturer
        if new_make != seen_make:
            continue

        # Check length similarity
        if abs(new_length - seen_length) > length_tolerance:
            continue

        # Check model name similarity:
        # 1. Exact normalized match
        # 2. One contains the other
        # 3. One is a substring of the other (after normalization)
        if (new_model_norm == seen_model_norm or
            new_model_norm in seen_model_norm or
            seen_model_norm in new_model_norm):
            return True

    return False

def merge_boat_data(existing: Dict, new: Dict) -> Dict:
    """
    Merges boat data, preferring non-empty values and more specific model names.
    """
    merged = existing.copy()

    # Prefer longer/more specific model name
    if len(new.get('model', '')) > len(existing.get('model', '')):
        merged['model'] = new['model']

    # Fill in missing optional fields
    for field in ['dry_weight_lbs', 'beam_inches']:
        if not merged.get(field) and new.get(field):
            merged[field] = new[field]

    return merged

def filter_boats(boats: List[Dict]) -> List[Dict]:
    """
    Filters a list of boats based on length and HP criteria.
    """
    filtered = []
    seen = set()

    for boat in boats:
        try:
            length = float(boat.get('length_ft', 0))
            hp = int(boat.get('max_hp', 0))
            make = boat.get('make', 'Unknown')
            model = boat.get('model', 'Unknown')

            # Create a unique key to prevent duplicates
            key = f"{make}-{model}".lower()

            # 13' = 13.0, 14' = 14.0
            if 13.0 <= length <= 14.0 and hp >= 40:
                if key not in seen:
                    filtered.append(boat)
                    seen.add(key)
        except (ValueError, TypeError):
            continue

    return filtered

def save_to_csv(boats: List[Dict], filename: str = "powerboat_results.csv"):
    """
    Save boat results to CSV file.
    """
    if not boats:
        print(f"No boats to save to {filename}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_with_timestamp = filename.replace(".csv", f"_{timestamp}.csv")

    fieldnames = ['make', 'model', 'length_ft', 'max_hp', 'dry_weight_lbs', 'beam_inches']

    try:
        with open(filename_with_timestamp, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(boats)

        print(f"\n✓ Results saved to: {filename_with_timestamp}")
        return filename_with_timestamp
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

def main():
    logger.info("=" * 60)
    logger.info("🚤 Starting Powerboat Search...")
    logger.info("   Target: 13'-14' boats with 40+ HP")
    logger.info("=" * 60)

    if not BRAVE_API_KEY:
        logger.error("✗ BRAVE_API_KEY is not set in environment or .env file.")
        logger.error("  Please obtain a key from https://brave.com/search/api/")
        logger.error("  Add it to your .env file or export as environment variable")
        return

    if not ANTHROPIC_API_KEY:
        logger.error("✗ ANTHROPIC_API_KEY is not set in environment or .env file.")
        logger.error("  Please obtain a key from https://console.anthropic.com/")
        logger.error("  Add it to your .env file or export as environment variable")
        return

    # Initialize database
    init_database()

    # Limited list for testing
    manufacturers = ["Boston Whaler", "Carolina Skiff", "Gheenoe"]
    new_boats_count = 0
    updated_boats_count = 0

    for make in manufacturers:
        print(f"\nProcessing {make}...")
        queries = generate_search_queries(make)

        # Limit to 1 query per manufacturer to save API credits during initial test
        for query in queries[:1]:
            search_results = search_web(query)

            # Limit to top 3 results
            for result in search_results[:3]:
                url = result.get('url', '')
                title = result.get('title', '')

                # Fetch full webpage content
                logger.info(f"   Fetching: {title[:50]}...")
                content = fetch_webpage(url)

                if not content:
                    # Fallback to title/description if fetch fails
                    content = f"Title: {title}\nDescription: {result.get('description', '')}"

                boats_found = extract_specs(content)
                for boat_data in boats_found:
                    # Filter check
                    try:
                        length = float(boat_data.get('length_ft', 0))
                        hp = int(boat_data.get('max_hp', 0))
                        boat_data['source_url'] = url  # Track source

                        # Debug: show what was extracted
                        logger.info(f"   Found: {boat_data.get('make')} {boat_data.get('model')} - {length}' / {hp}HP")

                        # 13' = 13.0, 14' = 14.0
                        if 13.0 <= length <= 14.0 and hp >= 40:
                            # Check for duplicates in database using fuzzy matching
                            existing = find_duplicate_in_db(boat_data)

                            if existing:
                                # Update existing boat with new data
                                update_boat_by_id(existing['id'], boat_data)
                                logger.info(f"   📝 Updated: {existing['model']} with data from {boat_data.get('model')}")
                                updated_boats_count += 1
                            else:
                                # Insert new boat - writes to DB immediately
                                if upsert_boat(boat_data):
                                    print(f"  ✅ NEW: {boat_data.get('make')} {boat_data.get('model')}")
                                    new_boats_count += 1
                                else:
                                    logger.info(f"   📝 Updated existing: {boat_data.get('model')}")
                                    updated_boats_count += 1
                    except (ValueError, TypeError):
                        pass

            # Be nice to APIs
            time.sleep(1)

    # Get final count from database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM boats')
    total_boats = cursor.fetchone()[0]
    conn.close()

    print(f"\n{'='*60}")
    print(f"Search Complete!")
    print(f"  New boats added: {new_boats_count}")
    print(f"  Boats updated: {updated_boats_count}")
    print(f"  Total in database: {total_boats}")
    print(f"{'='*60}")
    print(f"\nWatch live: sqlite3 {DB_FILE} 'SELECT * FROM boats'")
    print(f"Or use: watch -n 1 \"sqlite3 {DB_FILE} 'SELECT make, model, length_ft, max_hp FROM boats'\"")


if __name__ == "__main__":
    main()
