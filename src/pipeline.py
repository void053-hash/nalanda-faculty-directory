import sys
import argparse
import logging
from typing import List, Dict, Any

from src.scraper import get_faculty_data
from src.academic_client import enrich_faculty_academic_data
from src.ai_synthesizer import synthesize_faculty_profile
from src.exporter import export_to_excel
from src.config import OUTPUT_EXCEL_FILE

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("PipelineOrchestrator")


def run_pipeline(test_single: bool = False, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Orchestrates the full end-to-end data pipeline:
    1. Scrape Faculty (Playwright/BS4/Mock)
    2. Enrich Academic Data (OpenAlex API)
    3. Synthesize AI Insights (Gemini LLM)
    4. Export Formatted Excel Spreadsheet (.xlsx)
    """
    logger.info("==========================================================")
    logger.info("  NALANDA UNIVERSITY AI CLUB - FACULTY DIRECTORY PIPELINE ")
    logger.info("==========================================================")

    # Step 1: Faculty Data Acquisition
    logger.info(">>> Step 1/4: Scraping / Loading Faculty Directory...")
    faculty_records = get_faculty_data(force_refresh=force_refresh)
    
    if not faculty_records:
        logger.error("No faculty records found. Aborting pipeline.")
        return {"status": "failed", "error": "No faculty records"}

    if test_single:
        logger.info("[TEST MODE] Processing single professor profile for end-to-end verification.")
        faculty_records = faculty_records[:1]
        
    logger.info(f"Loaded {len(faculty_records)} faculty profiles to process.")

    enriched_records: List[Dict[str, Any]] = []
    
    for idx, fac in enumerate(faculty_records, 1):
        name = fac.get("name", "Unknown")
        dept = fac.get("department", "Unknown Department")
        logger.info(f"\n--- [{idx}/{len(faculty_records)}] Processing: {name} ({dept}) ---")

        # Step 2: OpenAlex Academic Data
        logger.info(f"Querying OpenAlex academic metrics for '{name}'...")
        fac_academic = enrich_faculty_academic_data(fac)
        logger.info(f"Metrics: {fac_academic.get('total_citations', 0)} citations, {fac_academic.get('total_works', 0)} works, {len(fac_academic.get('top_papers', []))} papers retrieved.")

        # Step 3: AI Synthesis
        logger.info(f"Synthesizing student reach-out advice and methodologies for '{name}'...")
        fac_complete = synthesize_faculty_profile(fac_academic)

        enriched_records.append(fac_complete)

    # Step 4: Excel Export
    logger.info("\n>>> Step 4/4: Formatting and Exporting Excel Directory...")
    df = export_to_excel(enriched_records, output_path=OUTPUT_EXCEL_FILE)

    logger.info("==========================================================")
    logger.info(f" PIPELINE COMPLETED SUCCESSFULLY! ")
    logger.info(f" - Processed Profiles: {len(enriched_records)}")
    logger.info(f" - Excel Output: {OUTPUT_EXCEL_FILE.resolve()}")
    logger.info("==========================================================")

    return {
        "status": "success",
        "count": len(enriched_records),
        "excel_path": str(OUTPUT_EXCEL_FILE),
        "records": enriched_records
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nalanda University Faculty Directory Pipeline")
    parser.add_argument("--test-single", action="store_true", help="Process only 1 profile for fast testing")
    parser.add_argument("--force-refresh", action="store_true", help="Force live web scraping")
    
    args = parser.parse_args()
    result = run_pipeline(test_single=args.test_single, force_refresh=args.force_refresh)
    
    if result.get("status") == "success":
        sys.exit(0)
    else:
        sys.exit(1)
