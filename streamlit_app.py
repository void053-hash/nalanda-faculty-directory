import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import streamlit as st
import pandas as pd

from src.config import OUTPUT_EXCEL_FILE, ENRICHED_FACULTY_FILE
from src.pipeline import run_pipeline
from src.exporter import export_to_excel

# Configure Streamlit Page
st.set_page_config(
    page_title="Nalanda University Faculty Directory | AI Club",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Academic UI
st.markdown("""
<style>
    /* Main Theme Variables */
    :root {
        --primary-color: #1B365D;
        --secondary-color: #C5A059;
        --bg-light: #F8FAFC;
        --card-bg: #FFFFFF;
        --border-color: #E2E8F0;
        --text-dark: #0F172A;
        --text-muted: #64748B;
    }

    /* Page Header */
    .main-header {
        background: linear-gradient(135deg, #1B365D 0%, #2A4365 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(27, 54, 93, 0.25);
    }
    .main-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
    }
    .main-header p {
        font-size: 1.1rem;
        color: #E2E8F0;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .badge-club {
        display: inline-block;
        background-color: #C5A059;
        color: #1B365D;
        font-weight: 700;
        font-size: 0.8rem;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Stat KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.2rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B365D;
        margin-top: 0.2rem;
    }

    /* Professor Profile Card */
    .prof-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
        transition: all 0.25s ease;
    }
    .prof-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.08);
    }
    .prof-header {
        display: flex;
        align-items: flex-start;
        gap: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .avatar-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1B365D 0%, #3182CE 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: 700;
        flex-shrink: 0;
        box-shadow: 0 4px 10px rgba(27, 54, 93, 0.2);
    }
    .prof-title-box h3 {
        margin: 0;
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
    }
    .prof-designation {
        color: #64748B;
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 0.15rem;
    }
    .prof-dept-badge {
        display: inline-block;
        background: #EFF6FF;
        color: #1E40AF;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.35rem;
    }

    /* Tag Pills */
    .tag-pill {
        display: inline-block;
        background: #F1F5F9;
        color: #334155;
        padding: 0.25rem 0.7rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        border: 1px solid #E2E8F0;
    }
    .method-pill {
        display: inline-block;
        background: #FEF3C7;
        color: #92400E;
        padding: 0.25rem 0.7rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        border: 1px solid #FDE68A;
    }

    /* Reach out callout box */
    .reach-out-box {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .reach-out-title {
        color: #166534;
        font-weight: 700;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 0.3rem;
    }
    .reach-out-text {
        color: #14532D;
        font-size: 0.9rem;
        line-height: 1.45;
        margin: 0;
    }

    /* Action buttons */
    .btn-contact {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background-color: #1B365D;
        color: #FFFFFF !important;
        text-decoration: none !important;
        padding: 0.4rem 0.9rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        transition: background-color 0.2s ease;
    }
    .btn-contact:hover {
        background-color: #2A4365;
    }
    .btn-outline {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background-color: #FFFFFF;
        color: #334155 !important;
        text-decoration: none !important;
        padding: 0.4rem 0.9rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #CBD5E1;
        transition: all 0.2s ease;
    }
    .btn-outline:hover {
        background-color: #F8FAFC;
        border-color: #94A3B8;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_directory_data(_mtime: float = 0.0) -> List[Dict[str, Any]]:
    """Loads enriched faculty directory dataset from JSON or triggers pipeline if missing."""
    if ENRICHED_FACULTY_FILE.exists():
        try:
            with open(ENRICHED_FACULTY_FILE, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error reading cache: {e}")
            
    # If not existing, run pipeline to generate initial data
    with st.spinner("Initializing Nalanda Faculty Directory pipeline..."):
        res = run_pipeline()
        return res.get("records", [])


def get_excel_bytes(faculty_list: List[Dict[str, Any]]) -> bytes:
    """Returns binary bytes of the Excel directory, ensuring fresh valid export."""
    if OUTPUT_EXCEL_FILE.exists():
        try:
            with open(OUTPUT_EXCEL_FILE, "rb") as f:
                content = f.read()
                if len(content) > 100:
                    return content
        except Exception:
            pass
            
    # Generate Excel if not found
    export_to_excel(faculty_list, output_path=OUTPUT_EXCEL_FILE)
    with open(OUTPUT_EXCEL_FILE, "rb") as f:
        return f.read()


def get_initials(name: str) -> str:
    """Extracts 2-letter initials from name."""
    parts = [p for p in name.replace("Prof.", "").replace("Dr.", "").replace("(", "").replace(")", "").split() if p]
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    elif len(parts) == 1:
        return parts[0][:2].upper()
    return "NU"


def main():
    # Load Data First
    mtime = ENRICHED_FACULTY_FILE.stat().st_mtime if ENRICHED_FACULTY_FILE.exists() else 0.0
    faculty_data = load_directory_data(_mtime=mtime)

    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Nalanda_University_Logo.svg/240px-Nalanda_University_Logo.svg.png", width=120) if False else None
        st.markdown("### 🏛️ Nalanda AI Club")
        st.markdown("**Academic Faculty Directory**")
        st.caption("Centralized intelligence platform for student-faculty research connectivity.")
        
        st.divider()
        
        # Download Excel
        st.markdown("#### 📥 Offline Export")
        if faculty_data:
            excel_bytes = get_excel_bytes(faculty_data)
            st.download_button(
                label="📊 Download Excel Directory (.xlsx)",
                data=excel_bytes,
                file_name="nalanda_faculty_directory.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="sidebar_download_excel"
            )
        else:
            st.warning("Excel file not generated yet. Run pipeline below.")
            
        st.divider()
        
        # Pipeline Refresh Trigger
        st.markdown("#### 🔄 Pipeline Operations")
        if st.button("🚀 Re-run Full Data Pipeline", use_container_width=True):
            with st.spinner("Scraping, Enriching with OpenAlex & AI Synthesizing..."):
                run_pipeline(force_refresh=True)
                st.cache_data.clear()
                st.success("Pipeline executed successfully! Reloading...")
                st.rerun()

        st.divider()
        
        # Student Reach-Out Tips
        st.markdown("#### 💡 Tips for Students")
        st.markdown("""
        - **Read 1 Recent Paper**: Reference specific findings in your reach-out email.
        - **Highlight Methodologies**: Mention your experience or eagerness to learn their specific tools (e.g. CGE, Epigraphy, Hermeneutics).
        - **Be Concise**: Keep initial intro emails under 200 words with your CV attached.
        """)

    # Main Page Header
    st.markdown("""
    <div class="main-header">
        <div class="badge-club">Nalanda University AI Club Initiative</div>
        <h1>Academic Faculty Directory</h1>
        <p>Explore professor profiles, research methodologies, OpenAlex publication metrics, and AI mentorship guidance.</p>
    </div>
    """, unsafe_allow_html=True)

    if not faculty_data:
        st.error("No faculty records available. Please run the pipeline from the sidebar.")
        return

    # Calculate Overview Stats
    total_faculty = len(faculty_data)
    total_works = sum(f.get("total_works", 0) for f in faculty_data)
    total_citations = sum(f.get("total_citations", 0) for f in faculty_data)
    departments = sorted(list(set(f.get("department", "Other") for f in faculty_data)))
    total_schools = len(departments)

    # KPI Stat Cards
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Faculty Members</div>
            <div class="kpi-value">{total_faculty}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Academic Publications</div>
            <div class="kpi-value">{total_works}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Citations</div>
            <div class="kpi-value">{total_citations:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Schools & Departments</div>
            <div class="kpi-value">{total_schools}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search & Filter Controls
    col_search, col_dept, col_sort = st.columns([2, 1.5, 1])
    
    with col_search:
        search_query = st.text_input(
            "🔍 Search Directory",
            placeholder="Search by name, research topic, methodology (e.g. CGE, Epigraphy, Climate)..."
        ).strip().lower()
        
    with col_dept:
        dept_filter = st.multiselect(
            "🏛️ Filter by School / Department",
            options=departments,
            default=[]
        )
        
    with col_sort:
        sort_by = st.selectbox(
            "⚡ Sort By",
            options=["Highest Citations", "Most Publications", "Name (A-Z)"]
        )

    # Filter Logic
    filtered_data = []
    for f in faculty_data:
        # Department filter
        if dept_filter and f.get("department") not in dept_filter:
            continue
            
        # Keyword search
        if search_query:
            matchable_text = " ".join([
                f.get("name", ""),
                f.get("department", ""),
                f.get("designation", ""),
                f.get("bio", ""),
                f.get("research_focus", ""),
                f.get("methodologies_used", ""),
                f.get("student_reach_out_summary", ""),
                " ".join(f.get("core_topics", [])),
                " ".join([p.get("title", "") for p in f.get("top_papers", [])])
            ]).lower()
            
            if search_query not in matchable_text:
                continue
                
        filtered_data.append(f)

    # Sort Logic
    if sort_by == "Highest Citations":
        filtered_data.sort(key=lambda x: x.get("total_citations", 0), reverse=True)
    elif sort_by == "Most Publications":
        filtered_data.sort(key=lambda x: x.get("total_works", 0), reverse=True)
    elif sort_by == "Name (A-Z)":
        filtered_data.sort(key=lambda x: x.get("name", ""))

    col_count, col_dl = st.columns([3, 1])
    with col_count:
        st.markdown(f"**Showing {len(filtered_data)} of {total_faculty} Faculty Profiles**")
    with col_dl:
        excel_bytes = get_excel_bytes(faculty_data)
        st.download_button(
            label="📥 Download Excel (.xlsx)",
            data=excel_bytes,
            file_name="nalanda_faculty_directory.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="main_download_excel"
        )
    st.divider()

    if not filtered_data:
        st.info("No faculty profiles matched your search or filter criteria. Try adjusting the keywords or clearing filters.")
        return

    # Render Faculty Profile Cards
    for fac in filtered_data:
        name = fac.get("name", "Unknown Faculty")
        desig = fac.get("designation", "Faculty Member")
        dept = fac.get("department", "Nalanda University")
        email = fac.get("email", "")
        profile_url = fac.get("profile_url", "https://nalandauniv.edu.in")
        citations = fac.get("total_citations", 0)
        works = fac.get("total_works", 0)
        topics = fac.get("core_topics", [])
        methods = fac.get("methodologies_used", "")
        focus = fac.get("research_focus", "")
        reach_out = fac.get("student_reach_out_summary", "")
        top_papers = fac.get("top_papers", [])
        initials = get_initials(name)
        
        # Build Profile Card
        with st.container():
            # Card Header
            st.markdown(f"""
            <div class="prof-card">
                <div class="prof-header">
                    <div class="avatar-circle">{initials}</div>
                    <div class="prof-title-box">
                        <h3>{name}</h3>
                        <div class="prof-designation">{desig}</div>
                        <div class="prof-dept-badge">{dept}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Action Buttons & Stats Row
            col_actions, col_stats = st.columns([1.5, 2])
            with col_actions:
                btn_html = ""
                if email:
                    btn_html += f'<a class="btn-contact" href="mailto:{email}">✉️ Email Professor</a> '
                if profile_url:
                    btn_html += f'<a class="btn-outline" href="{profile_url}" target="_blank">🌐 University Profile ↗</a>'
                st.markdown(btn_html, unsafe_allow_html=True)
                
            with col_stats:
                st.markdown(f"""
                <div style="display: flex; gap: 0.8rem; justify-content: flex-end; align-items: center;">
                    <span style="font-size: 0.85rem; color: #64748B;">📚 <strong>{works}</strong> Works</span>
                    <span style="font-size: 0.85rem; color: #64748B;">🌟 <strong>{citations:,}</strong> Citations</span>
                    <span style="font-size: 0.8rem; background: #EEF2F6; padding: 0.2rem 0.5rem; border-radius: 4px; color: #475569;">OpenAlex Verified</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

            # Research Focus
            if focus:
                st.markdown(f"**🎯 Research Focus & Trajectory:**")
                st.markdown(f"<p style='color: #334155; font-size: 0.95rem; line-height: 1.5; margin-bottom: 0.8rem;'>{focus}</p>", unsafe_allow_html=True)

            # Methodologies Tags
            if methods:
                method_tags_html = "".join([f'<span class="method-pill">⚙️ {m.strip()}</span>' for m in methods.split(",") if m.strip()])
                st.markdown(f"**🔬 Key Methodologies & Techniques:**")
                st.markdown(f"<div style='margin-bottom: 0.8rem;'>{method_tags_html}</div>", unsafe_allow_html=True)

            # Core Topics Tags
            if topics:
                topic_tags_html = "".join([f'<span class="tag-pill">🏷️ {t}</span>' for t in topics])
                st.markdown(f"<div style='margin-bottom: 0.8rem;'>{topic_tags_html}</div>", unsafe_allow_html=True)

            # Student Reach-Out Highlight Box
            if reach_out:
                st.markdown(f"""
                <div class="reach-out-box">
                    <div class="reach-out-title">💡 Student Mentorship & Reach-Out Guide</div>
                    <p class="reach-out-text">{reach_out}</p>
                </div>
                """, unsafe_allow_html=True)

            # Top Recent Publications Accordion
            if top_papers:
                with st.expander(f"📄 Recent Publications ({len(top_papers)})", expanded=False):
                    for p_idx, p in enumerate(top_papers, 1):
                        p_title = p.get("title", "Untitled Publication")
                        p_year = p.get("year", "N/A")
                        p_cites = p.get("citations", 0)
                        p_venue = p.get("venue", "Academic Journal")
                        p_doi = p.get("doi_url", "")
                        
                        doi_link_html = f'<a href="{p_doi}" target="_blank" style="color: #2563EB; text-decoration: none; font-weight: 500;">View Paper ↗</a>' if p_doi else ""
                        
                        st.markdown(f"""
                        <div style="padding: 0.6rem 0; border-bottom: 1px solid #F1F5F9;">
                            <div style="font-weight: 600; color: #1E293B; font-size: 0.95rem;">{p_idx}. {p_title}</div>
                            <div style="font-size: 0.85rem; color: #64748B; margin-top: 0.2rem;">
                                📅 {p_year} &nbsp;|&nbsp; 🏛️ {p_venue} &nbsp;|&nbsp; 🌟 {p_cites} citations &nbsp;|&nbsp; {doi_link_html}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
