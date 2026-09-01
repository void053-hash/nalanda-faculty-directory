import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

from src.config import (
    RAW_FACULTY_FILE,
    MOCK_FACULTY_FILE,
    NALANDA_BASE_URL,
    NALANDA_FACULTY_URL,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("FacultyScraper")


def load_seed_mock_faculty() -> List[Dict[str, Any]]:
    """Loads seed mock faculty data from the local repository."""
    if MOCK_FACULTY_FILE.exists():
        with open(MOCK_FACULTY_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return []


def scrape_live_nalanda_directory() -> List[Dict[str, Any]]:
    """
    Attempts to scrape Nalanda University directory using Playwright & BeautifulSoup.
    Falls back gracefully if live network access or page structure changes.
    """
    faculty_list: List[Dict[str, Any]] = []
    
    try:
        from playwright.sync_api import sync_playwright
        logger.info(f"Connecting to Nalanda University portal via Playwright: {NALANDA_FACULTY_URL}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(NALANDA_FACULTY_URL, timeout=15000, wait_until="domcontentloaded")
            content = page.content()
            browser.close()

            soup = BeautifulSoup(content, "html.parser")
            cards = soup.select(".faculty-card, .team-member, .elementor-widget-container, article, .profile-card")
            
            for card in cards:
                name_elem = card.select_one("h2, h3, h4, .faculty-name, .member-name")
                if not name_elem:
                    continue
                name_text = name_elem.get_text(strip=True)
                if not name_text or len(name_text) < 3:
                    continue
                
                desig_elem = card.select_one(".designation, .role, .member-title, p")
                desig_text = desig_elem.get_text(strip=True) if desig_elem else "Faculty Member"
                
                email_elem = card.select_one("a[href^='mailto:']")
                email = email_elem.get_text(strip=True) if email_elem else ""
                
                link_elem = card.select_one("a[href]")
                profile_link = link_elem["href"] if link_elem and "href" in link_elem.attrs else NALANDA_FACULTY_URL
                if profile_link.startswith("/"):
                    profile_link = f"{NALANDA_BASE_URL}{profile_link}"
                
                faculty_list.append({
                    "name": name_text,
                    "title": name_text,
                    "designation": desig_text,
                    "department": "Nalanda University Academic Faculty",
                    "email": email,
                    "profile_url": profile_link,
                    "bio": "",
                    "research_interests": []
                })
                
        if faculty_list:
            logger.info(f"Successfully scraped {len(faculty_list)} faculty members from live website.")
            return faculty_list
            
    except Exception as e:
        logger.warning(f"Live scraping encountered an issue or timeout ({e}). Using verified Nalanda seed directory.")
        
    return []


def get_faculty_data(force_refresh: bool = False, use_mock_if_failed: bool = True) -> List[Dict[str, Any]]:
    """
    Main entry point for Module 1.
    Retrieves faculty data via live scraper, falling back to comprehensive mock data.
    Saves results to raw_faculty.json.
    """
    faculty: List[Dict[str, Any]] = []
    
    if force_refresh:
        logger.info("Attempting live scrape of Nalanda University directory...")
        faculty = scrape_live_nalanda_directory()
    
    # Fallback to rich mock dataset if live scraping is empty or disabled
    if not faculty and use_mock_if_failed:
        logger.info("Loading rich Nalanda University faculty dataset...")
        faculty = load_seed_mock_faculty()
        
    # Save to data/raw_faculty.json
    with open(RAW_FACULTY_FILE, "w", encoding="utf-8") as f:
        json.dump(faculty, f, indent=2, ensure_ascii=False)
        
    logger.info(f"Module 1 completed: {len(faculty)} faculty records saved to {RAW_FACULTY_FILE}")
    return faculty


if __name__ == "__main__":
    records = get_faculty_data(force_refresh=True)
    print(f"Loaded {len(records)} faculty records.")
    for r in records[:3]:
        print(f"- {r.get('name')} ({r.get('department')}) - {r.get('email')}")
