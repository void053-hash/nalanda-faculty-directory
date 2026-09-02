# 🏛️ Nalanda University - Academic Faculty Directory

> An automated data aggregation pipeline and interactive web intelligence dashboard developed for the **Nalanda University AI Club** to connect students with faculty for research mentorship, thesis guidance, and academic proceedings.

---

## 🌟 Key Features

1. **Automated Faculty Scraper (Module 1)**: Extracts faculty names, designations, schools, emails, and profile links using Playwright & BeautifulSoup.
2. **OpenAlex Academic Intelligence (Module 2)**: Fetches verified total publications, total citations, core research topics, and top recent papers without web blocking.
3. **Gemini AI Synthesis (Module 3)**: Synthesizes structured "Research Focus", "Methodologies Used", and "Student Reach-Out Advice" using `google-genai` (with intelligent heuristic fallback).
4. **Styled Multi-Column Excel Export (Module 4)**: Exports `faculty_directory.xlsx` formatted with Royal Nalanda Blue headers, auto column widths, and clickable links.
5. **Dual Web Dashboards (Module 5)**:
   - **Vercel Web Portal**: High-speed, zero-dependency responsive frontend in `public/` deployable on Vercel with 1-click.
   - **Streamlit Web Dashboard**: Python interactive dashboard in `streamlit_app.py`.

---

## 🚀 Quickstart Guide

### 1. Launch the Web App Locally (Streamlit)
- **1-Click**: Double-click `run_dashboard.bat` in Windows File Explorer.
- **Terminal (PowerShell)**:
  ```powershell
  cd "C:\Users\DEVANSH PANDEY\nalanda-faculty-directory"
  .\.venv\Scripts\streamlit.exe run streamlit_app.py
  ```

### 2. Run the Data Pipeline
- **1-Click**: Double-click `run_pipeline.bat`
- **Terminal**:
  ```powershell
  & .\.venv\Scripts\python.exe -m src.pipeline
  ```

---

## 🌐 Deploy to Vercel (For Sharing with Seniors & Faculty)

1. Connect your repository `void053-hash/nalanda-faculty-directory` to [Vercel](https://vercel.com).
2. The project includes `vercel.json` and a pre-built, ultra-fast `public/` web directory with all 38 indexed faculty members and direct Excel sheet download.
3. Vercel automatically deploys the frontend at `https://<your-project>.vercel.app`.

---

## 📁 Project Structure

```
nalanda-faculty-directory/
│
├── .venv/                         # Virtual environment
├── .env                           # Environment configuration
├── .env.example                   # Template configuration file
├── vercel.json                    # Vercel deployment configuration
├── requirements.txt               # Pinned dependencies
├── README.md                      # Documentation
├── streamlit_app.py               # Streamlit interactive dashboard
├── run_dashboard.bat              # 1-click Streamlit launcher
├── run_pipeline.bat               # 1-click pipeline runner
│
├── public/                        # Vercel static web assets
│   ├── index.html                 # Standalone web app for Vercel
│   ├── faculty_data.json          # Enriched faculty JSON dataset
│   └── faculty_directory.xlsx     # Formatted Excel directory
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

<!-- trigger fresh commit for Vercel deployment: 2026-09-02 16:26:57 -->
