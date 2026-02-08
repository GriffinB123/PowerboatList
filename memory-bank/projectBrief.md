# Project Brief

## Purpose
Build an AI-powered tool to automatically find production powerboats that meet specific, tight criteria: between 13'6" and 13'11" in length, with a maximum horsepower rating of 40HP or greater.

## Target Users
- Boat enthusiasts looking for specific "micro-skiffs" or small performance boats.
- Buyers who need to filter thousands of models down to a specific size/power ratio.

## Core Features
- **Automated Search**: Uses Brave Search API to scan the web.
- **AI Extraction**: Uses Claude to read messy HTML/text and extract specs (Length, HP, Beam).
- **Filtering**: Strict logic to keep only boats in the 13.5' - 13.92' range with 40+ HP.
- **Cloud Native**: Runs entirely in Google Colab (no local setup required).
