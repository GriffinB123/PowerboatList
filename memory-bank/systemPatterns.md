# System Patterns

## Architecture
```mermaid
graph TD
    A[Input: Manufacturers] --> B[Query Generator (Claude)]
    B --> C[Web Search (Brave API)]
    C --> D[Result Parser (Claude)]
    D --> E[Filter Logic (Python)]
    E --> F[Output (Google Sheets/CSV)]
```

## Key Decisions
- **Brave Search vs Google**: Brave Search has a cheap/free API that is easier to use than Google Custom Search JSON API.
- **Colab First**: Chosen to allow users to run this without installing Python locally.
- **Two-Stage AI**:
    1.  **Stage 1 (Query)**: "How do I find specs for X?" -> Generates better keywords than a template.
    2.  **Stage 2 (Extraction)**: "Read this snippet, find Length/HP" -> Handles messy HTML/text better than Regex.

## Code Structure
- `search_boats.py`: Core logic module. Designed to be imported *or* run standalone.
- `powerboat_search.ipynb`: The UI layer. Handles API keys and display.
