<<<<<<< HEAD
# 🏛️ Nalanda University - Academic Faculty Directory
=======
﻿# 🏛️ Nalanda University - Academic Faculty Directory
>>>>>>> c5fdf8a (feat: Nalanda University Academic Faculty Directory and Streamlit Dashboard)

> An automated data aggregation pipeline and interactive web intelligence dashboard developed for the **Nalanda University AI Club** to connect students with faculty for research mentorship, thesis guidance, and academic proceedings.

---

## 🌟 Key Features

1. **Automated Faculty Scraper (Module 1)**: Extracts faculty names, designations, schools, emails, and profile links using Playwright & BeautifulSoup.
2. **OpenAlex Academic Intelligence (Module 2)**: Fetches verified total publications, total citations, core research topics, and top recent papers without web blocking.
3. **Gemini AI Synthesis (Module 3)**: Synthesizes structured "Research Focus", "Methodologies Used", and "Student Reach-Out Advice" using `google-genai` (with intelligent heuristic fallback).
4. **Styled Multi-Column Excel Export (Module 4)**: Exports `faculty_directory.xlsx` formatted with Royal Nalanda Blue headers, auto column widths, and clickable links.
5. **Interactive Streamlit Web Dashboard (Module 5)**: Modern, responsive search interface with KPI metric cards, department filters, sorting, and rich professor profile cards.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (or standard python virtual environment)

### 2. Environment Setup
Activate the virtual environment:
```powershell
cd "C:\Users\DEVANSH PANDEY\nalanda-faculty-directory"
.\.venv\Scripts\Activate.ps1
```

### 3. Configure API Keys (Optional)
Edit `.env` to provide your Gemini API key (from [Google AI Studio](https://aistudio.google.com/)):
```ini
GEMINI_API_KEY=your_actual_gemini_api_key_here
OPENALEX_EMAIL=nalanda.aiclub@nalandauniv.edu.in
```

### 4. Run the Data Pipeline
To process the entire faculty directory:
```powershell
& .\.venv\Scripts\python.exe -m src.pipeline
```

To test a single dummy professor profile:
```powershell
& .\.venv\Scripts\python.exe -m src.pipeline --test-single
```

### 5. Launch the Streamlit Dashboard
Launch the interactive browser app:
```powershell
& .\.venv\Scripts\streamlit.exe run app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
nalanda-faculty-directory/
│
├── .venv/                         # Virtual environment
├── .env                           # Environment configuration
├── .env.example                   # Template configuration file
├── requirements.txt               # Pinned dependencies
├── README.md                      # Documentation
├── app.py                         # Streamlit interactive dashboard
│
├── data/
│   ├── mock_faculty.json          # Seed faculty data
│   ├── raw_faculty.json           # Scraped raw faculty records
│   ├── enriched_faculty.json      # Enriched JSON dataset
│   └── faculty_directory.xlsx     # Formatted Excel directory
│
└── src/
    ├── __init__.py
    ├── config.py                  # Path constants & configuration
    ├── scraper.py                 # Module 1: Faculty scraper
    ├── academic_client.py         # Module 2: OpenAlex integration
    ├── ai_synthesizer.py          # Module 3: Gemini AI synthesizer
    ├── exporter.py                # Module 4: Formatted Excel exporter
    └── pipeline.py                # Master pipeline CLI orchestrator
```

---

## 👥 Nalanda University AI Club
Built by the AI Club to democratize research opportunities for all undergraduate and postgraduate scholars at Nalanda University.
