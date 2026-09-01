import os
from pathlib import Path
from dotenv import load_dotenv

# Project Root Directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(ROOT_DIR / ".env")

# API Keys & Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
OPENALEX_EMAIL = os.getenv("OPENALEX_EMAIL", "nalanda.aiclub@nalandauniv.edu.in").strip()

# Data Directory & File Paths
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True, parents=True)

MOCK_FACULTY_FILE = DATA_DIR / "mock_faculty.json"
RAW_FACULTY_FILE = DATA_DIR / "raw_faculty.json"
ENRICHED_FACULTY_FILE = DATA_DIR / "enriched_faculty.json"
OUTPUT_EXCEL_FILE = DATA_DIR / "faculty_directory.xlsx"

# Nalanda University Base URLs
NALANDA_BASE_URL = "https://nalandauniv.edu.in"
NALANDA_FACULTY_URL = "https://nalandauniv.edu.in/schools/"
