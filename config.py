"""
Configuration file for PDF parsing and NLP processing
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (Set these as environment variables or replace with your keys)
LLAMA_PARSE_API_KEY = os.getenv("LLAMA_PARSE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
MARKDOWN_DIR = OUTPUT_DIR / "markdown"
NATURAL_LANGUAGE_DIR = OUTPUT_DIR / "natural_language"

# Create directories if they don't exist
MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
NATURAL_LANGUAGE_DIR.mkdir(parents=True, exist_ok=True)

# Llama Parse Configuration
LLAMA_PARSE_CONFIG = {
    "tier": "agentic_plus",
    "version": "latest",
    "high_res_ocr": True,
    "adaptive_long_table": True,
    "outlined_table_extraction": True,
    "output_tables_as_HTML": True,
    "precise_bounding_box": True,
    "page_separator": "\n\n---\n\n",
    "max_pages": 0,
}

# Claude AI Configuration
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 8000

