import json
import logging
from typing import Dict, Any, Optional

from src.config import GEMINI_API_KEY

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger("AISynthesizer")


def build_synthesis_prompt(faculty_data: Dict[str, Any]) -> str:
    """Constructs a structured prompt for Gemini model."""
    name = faculty_data.get("name", "")
    department = faculty_data.get("department", "")
    bio = faculty_data.get("bio", "")
    topics = ", ".join(faculty_data.get("core_topics", []))
    
    papers_summary = ""
    for idx, p in enumerate(faculty_data.get("top_papers", []), 1):
        papers_summary += f"\nPaper {idx}: '{p.get('title')}' ({p.get('year')})\nVenue: {p.get('venue')}\nAbstract: {p.get('abstract', 'N/A')}\n"
        
    prompt = f"""
You are the Lead Academic Advisor at Nalanda University AI Club.
Your goal is to synthesize academic data about a professor into student-friendly, actionable insights.

Faculty Profile:
- Name: {name}
- Department: {department}
- Bio/Background: {bio}
- Core Research Topics: {topics}
- Recent Publications:
{papers_summary}

Please provide a JSON response with exactly the following 3 fields:
1. "research_focus": A clear, compelling 2-3 sentence summary of their primary research domains and core questions.
2. "methodologies_used": A concise list/summary of specific methodologies, tools, models, analytical frameworks, or archival/fieldwork techniques they utilize (e.g. Econometric Modeling, Archival Epigraphy, Aerosol Sampling, Sanskrit Hermeneutics, Deep Learning).
3. "student_reach_out_summary": Practical, actionable advice for a university student on how to approach this professor for mentorship, internships, or thesis guidance (including what papers/topics to read beforehand and suggested project angles).

Respond ONLY with valid JSON in this structure:
{{
  "research_focus": "...",
  "methodologies_used": "...",
  "student_reach_out_summary": "..."
}}
"""
    return prompt.strip()


def heuristic_synthesis(faculty_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Intelligent rule-based fallback when Gemini API key is not configured.
    Generates high-quality student advice from topics and department.
    """
    name = faculty_data.get("name", "The professor")
    dept = faculty_data.get("department", "Academic Department")
    topics = faculty_data.get("core_topics", [])
    topics_str = ", ".join(topics) if topics else "interdisciplinary studies"
    bio = faculty_data.get("bio", "")
    
    # Methodologies mapping by department/topics
    dept_lower = dept.lower()
    if "environment" in dept_lower or "ecology" in dept_lower:
        methods = "Empirical Environmental Modeling, Aerosol Mass Spectrometry, Computable General Equilibrium (CGE), GIS Spatial Mapping"
        reach_out = (
            f"Familiarize yourself with recent climate/environmental policy reports and quantitative modeling tools before emailing. "
            f"Highlight your interest in {topics[0] if topics else 'environmental sustainability'} and mention specific analytical tools you want to apply."
        )
    elif "history" in dept_lower or "archaeology" in dept_lower:
        methods = "Archival Epigraphy, Material Culture Analysis, Numismatic Studies, Maritime Trade Network Mapping, Historical Hermeneutics"
        reach_out = (
            f"Review primary source collections or archaeological surveys related to {topics[0] if topics else 'Ancient Indian History'}. "
            f"In your reach-out email, mention your background in textual or material analysis and propose a clear archival inquiry."
        )
    elif "buddhist" in dept_lower or "philosophy" in dept_lower or "languages" in dept_lower:
        methods = "Textual Hermeneutics, Comparative Philosophical Analysis, Sanskrit/Pali/Tibetan Manuscript Studies, Mnemonic & Critical Theory"
        reach_out = (
            f"Read foundational texts in comparative philosophy and {topics[0] if topics else 'philosophical hermeneutics'}. "
            f"Draft a brief 1-page concept note exploring a specific philosophical or manuscript question when reaching out."
        )
    elif "international" in dept_lower or "management" in dept_lower or "economics" in dept_lower:
        methods = "Geopolitical Risk Assessment, Econometric Analysis, Qualitative Policy Analysis, Case Study Frameworks"
        reach_out = (
            f"Stay updated on current multilateral policy forums and strategic developments in {topics[0] if topics else 'regional trade & diplomacy'}. "
            f"Email a concise pitch connecting your research interests with their recent policy publications."
        )
    else:
        methods = "Quantitative Data Analysis, Qualitative Case Frameworks, Literature Synthesis, Comparative Modeling"
        reach_out = (
            f"Review {name}'s top recent papers in {topics_str}. Craft a concise email introducing your academic background and articulating your specific research questions."
        )

    focus = f"{name} conducts research in {dept}, with a strong emphasis on {topics_str}. {bio}"
    
    return {
        "research_focus": focus.strip(),
        "methodologies_used": methods,
        "student_reach_out_summary": reach_out
    }


def synthesize_faculty_profile(faculty_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for Module 3.
    Uses Gemini API if available, else falls back to heuristic synthesis.
    """
    name = faculty_data.get("name", "Faculty")
    
    if GEMINI_API_KEY:
        try:
            from google import genai
            logger.info(f"Synthesizing profile for {name} using Gemini API...")
            client = genai.Client(api_key=GEMINI_API_KEY)
            prompt = build_synthesis_prompt(faculty_data)
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )
            
            if response.text:
                synth = json.loads(response.text)
                faculty_data["research_focus"] = synth.get("research_focus", "")
                faculty_data["methodologies_used"] = synth.get("methodologies_used", "")
                faculty_data["student_reach_out_summary"] = synth.get("student_reach_out_summary", "")
                faculty_data["ai_synthesized"] = True
                return faculty_data
                
        except Exception as e:
            logger.warning(f"Gemini API call failed for {name} ({e}). Falling back to heuristic synthesis.")
            
    # Heuristic fallback
    synth = heuristic_synthesis(faculty_data)
    faculty_data["research_focus"] = synth["research_focus"]
    faculty_data["methodologies_used"] = synth["methodologies_used"]
    faculty_data["student_reach_out_summary"] = synth["student_reach_out_summary"]
    faculty_data["ai_synthesized"] = False
    return faculty_data


if __name__ == "__main__":
    sample = {
        "name": "Prof. (Dr.) Abhay Kumar Singh",
        "department": "School of Historical Studies",
        "bio": "Ancient Indian History and Maritime Trade",
        "core_topics": ["Archaeology", "Maritime Trade", "Numismatics"],
        "top_papers": [
            {
                "title": "Maritime Networks in the Indian Ocean",
                "year": 2023,
                "venue": "Historical Journal",
                "abstract": "Examines maritime trade routes between India and Southeast Asia."
            }
        ]
    }
    res = synthesize_faculty_profile(sample)
    print("AI Synthesis Output:")
    print("Focus:", res["research_focus"])
    print("Methodologies:", res["methodologies_used"])
    print("Reach-Out Advice:", res["student_reach_out_summary"])
