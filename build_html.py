import json
from pathlib import Path

root = Path(__file__).resolve().parent
data_file = root / "data" / "enriched_faculty.json"
faculty_data = json.loads(data_file.read_text(encoding="utf-8-sig"))

public_dir = root / "public"
public_dir.mkdir(exist_ok=True)

# Copy assets
(public_dir / "faculty_data.json").write_text(json.dumps(faculty_data, ensure_ascii=False, indent=2), encoding="utf-8")
excel_src = root / "data" / "faculty_directory.xlsx"
if excel_src.exists():
    (public_dir / "faculty_directory.xlsx").write_bytes(excel_src.read_bytes())

data_json_str = json.dumps(faculty_data, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nalanda University Faculty Directory | AI Club</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            nalanda: {
              navy: '#1B365D',
              dark: '#0F172A',
              gold: '#C5A059'
            }
          }
        }
      }
    }
  </script>
  <style>
    body {
      background-color: #F8FAFC;
      color: #0F172A;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .hero-banner {
      background: linear-gradient(135deg, #1B365D 0%, #1E293B 100%);
    }
    .shadow-soft {
      box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.06);
    }
    .shadow-hover:hover {
      box-shadow: 0 12px 30px -4px rgba(27, 54, 93, 0.12);
      transform: translateY(-2px);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- Header -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="text-2xl">&#127963;</span>
        <div>
          <span class="font-bold text-[#1B365D] text-lg leading-tight block">Nalanda University</span>
          <span class="text-xs text-slate-500 font-medium tracking-wide uppercase">AI Club Initiative</span>
        </div>
      </div>
      <div>
        <a href="faculty_directory.xlsx" download="nalanda_faculty_directory.xlsx" class="inline-flex items-center space-x-2 bg-[#1B365D] hover:bg-slate-800 text-white text-xs sm:text-sm font-semibold px-4 py-2 rounded-lg shadow transition">
          <span>&#128229;</span>
          <span>Download Excel (.xlsx)</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <div class="hero-banner text-white py-12 px-4 sm:px-6 lg:px-8 shadow-md">
    <div class="max-w-7xl mx-auto text-center">
      <div class="inline-block bg-[#C5A059] text-[#1B365D] font-bold text-xs px-3 py-1 rounded-full uppercase tracking-wider mb-4">
        Student-Faculty Research Connectivity
      </div>
      <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight mb-4">
        Academic Faculty Directory
      </h1>
      <p class="text-slate-300 max-w-2xl mx-auto text-sm sm:text-base">
        Explore professor profiles, research methodologies, OpenAlex publication metrics, and student reach-out guidance across all schools at Nalanda University.
      </p>

      <!-- KPI Summary -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mt-8 text-left">
        <div class="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/10">
          <div class="text-xs uppercase text-slate-300 font-semibold">Faculty Indexed</div>
          <div id="kpi-faculty" class="text-2xl sm:text-3xl font-extrabold text-white mt-1">38</div>
        </div>
        <div class="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/10">
          <div class="text-xs uppercase text-slate-300 font-semibold">Publications</div>
          <div id="kpi-works" class="text-2xl sm:text-3xl font-extrabold text-white mt-1">1,200+</div>
        </div>
        <div class="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/10">
          <div class="text-xs uppercase text-slate-300 font-semibold">Total Citations</div>
          <div id="kpi-cites" class="text-2xl sm:text-3xl font-extrabold text-white mt-1">50,000+</div>
        </div>
        <div class="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/10">
          <div class="text-xs uppercase text-slate-300 font-semibold">Schools & Depts</div>
          <div id="kpi-schools" class="text-2xl sm:text-3xl font-extrabold text-white mt-1">8</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Search & Filter Controls -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow w-full">
    <div class="bg-white p-5 rounded-2xl border border-slate-200 shadow-soft mb-8">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
        <!-- Search -->
        <div class="md:col-span-5">
          <label class="block text-xs font-bold text-slate-600 uppercase mb-1">&#128269; Search Directory</label>
          <input 
            type="text" 
            id="searchInput" 
            placeholder="Search by name, topic, methodology (e.g. CGE, Epigraphy, Climate)..."
            class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-lg text-sm text-slate-900 focus:ring-2 focus:ring-[#1B365D] focus:outline-none transition"
          />
        </div>

        <!-- School Filter -->
        <div class="md:col-span-4">
          <label class="block text-xs font-bold text-slate-600 uppercase mb-1">&#127963; Filter by School</label>
          <select 
            id="schoolFilter" 
            class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-lg text-sm text-slate-900 focus:ring-2 focus:ring-[#1B365D] focus:outline-none transition"
          >
            <option value="">All Schools & Departments</option>
          </select>
        </div>

        <!-- Sort -->
        <div class="md:col-span-3">
          <label class="block text-xs font-bold text-slate-600 uppercase mb-1">&#9889; Sort By</label>
          <select 
            id="sortBy" 
            class="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-lg text-sm text-slate-900 focus:ring-2 focus:ring-[#1B365D] focus:outline-none transition"
          >
            <option value="citations">Highest Citations</option>
            <option value="works">Most Publications</option>
            <option value="name">Name (A-Z)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Active Count & Download Action -->
    <div class="flex flex-col sm:flex-row justify-between items-center mb-6 gap-3">
      <div class="text-sm text-slate-600 font-medium">
        Showing <span id="visibleCount" class="font-bold text-[#1B365D]">0</span> of <span id="totalCount" class="font-bold">0</span> Faculty Profiles
      </div>
      <a href="faculty_directory.xlsx" download="nalanda_faculty_directory.xlsx" class="text-xs font-semibold text-[#1B365D] hover:text-blue-700 flex items-center gap-1.5 transition">
        <span>&#128202; Download Full Excel Directory (.xlsx)</span>
        <span>&rarr;</span>
      </a>
    </div>

    <!-- Faculty Cards Grid -->
    <div id="facultyGrid" class="space-y-6"></div>
  </main>

  <!-- Footer -->
  <footer class="bg-white border-t border-slate-200 py-8 px-4 sm:px-6 lg:px-8 mt-12 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4">
      <div class="flex items-center space-x-2">
        <span>&#127963;</span>
        <span class="font-semibold text-slate-700">Nalanda University AI Club</span>
        <span>&bull; Academic Faculty Intelligence</span>
      </div>
      <div class="flex items-center space-x-4">
        <a href="https://nalandauniv.edu.in" target="_blank" class="hover:text-[#1B365D] transition">University Portal</a>
        <a href="faculty_directory.xlsx" download class="hover:text-[#1B365D] transition">Offline Excel Export</a>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script>
    const facultyData = """ + data_json_str + """;

    function getInitials(name) {
      const clean = name.replace(/Prof\\.|Dr\\.|\\(|\\)/g, '').trim();
      const parts = clean.split(/\\s+/);
      if (parts.length >= 2) {
        return (parts[0][0] + parts[1][0]).toUpperCase();
      }
      return (parts[0] ? parts[0].slice(0, 2) : 'NU').toUpperCase();
    }

    function initSchools() {
      const schools = [...new Set(facultyData.map(f => f.department).filter(Boolean))].sort();
      const select = document.getElementById('schoolFilter');
      schools.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s;
        opt.textContent = s;
        select.appendChild(opt);
      });
      document.getElementById('kpi-schools').textContent = schools.length;
    }

    function updateKPIs() {
      document.getElementById('kpi-faculty').textContent = facultyData.length;
      const totalWorks = facultyData.reduce((acc, f) => acc + (f.total_works || 0), 0);
      const totalCites = facultyData.reduce((acc, f) => acc + (f.total_citations || 0), 0);
      document.getElementById('kpi-works').textContent = totalWorks.toLocaleString();
      document.getElementById('kpi-cites').textContent = totalCites.toLocaleString();
      document.getElementById('totalCount').textContent = facultyData.length;
    }

    function renderCards() {
      const query = document.getElementById('searchInput').value.toLowerCase().trim();
      const selectedSchool = document.getElementById('schoolFilter').value;
      const sortBy = document.getElementById('sortBy').value;

      let filtered = facultyData.filter(f => {
        if (selectedSchool && f.department !== selectedSchool) return false;
        if (!query) return true;

        const hay = [
          f.name || '',
          f.department || '',
          f.designation || '',
          f.bio || '',
          f.research_focus || '',
          f.methodologies_used || '',
          f.student_reach_out_summary || '',
          (f.core_topics || []).join(' '),
          (f.top_papers || []).map(p => p.title || '').join(' ')
        ].join(' ').toLowerCase();

        return hay.includes(query);
      });

      if (sortBy === 'citations') {
        filtered.sort((a, b) => (b.total_citations || 0) - (a.total_citations || 0));
      } else if (sortBy === 'works') {
        filtered.sort((a, b) => (b.total_works || 0) - (a.total_works || 0));
      } else if (sortBy === 'name') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
      }

      document.getElementById('visibleCount').textContent = filtered.length;
      const grid = document.getElementById('facultyGrid');
      grid.innerHTML = '';

      if (filtered.length === 0) {
        grid.innerHTML = `
          <div class="bg-white rounded-2xl p-12 text-center border border-slate-200">
            <span class="text-4xl mb-3 block">&#128269;</span>
            <h3 class="text-lg font-bold text-slate-800">No matching faculty members found</h3>
            <p class="text-sm text-slate-500 mt-1">Try broadening your search keywords or resetting the school filter.</p>
          </div>
        `;
        return;
      }

      filtered.forEach(fac => {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-2xl p-6 sm:p-7 border border-slate-200 shadow-soft shadow-hover transition duration-200';
        
        const initials = getInitials(fac.name || 'NU');
        const works = fac.total_works || 0;
        const citations = (fac.total_citations || 0).toLocaleString();
        const methods = (fac.methodologies_used || '').split(',').map(m => m.trim()).filter(Boolean);
        const topics = fac.core_topics || [];
        const papers = fac.top_papers || [];

        let papersHtml = '';
        if (papers.length > 0) {
          papersHtml = `
            <details class="group mt-4 pt-4 border-t border-slate-100">
              <summary class="cursor-pointer text-xs font-bold text-slate-700 hover:text-[#1B365D] flex items-center justify-between">
                <span>&#128196; Top Recent Publications (${papers.length})</span>
                <span class="text-slate-400 group-open:rotate-180 transition">&darr;</span>
              </summary>
              <div class="mt-3 space-y-3 pl-2">
                ${papers.map((p, pIdx) => `
                  <div class="text-xs border-l-2 border-slate-200 pl-3 py-1">
                    <div class="font-semibold text-slate-800">${pIdx + 1}. ${p.title || 'Untitled'}</div>
                    <div class="text-slate-500 mt-0.5 flex flex-wrap items-center gap-2">
                      <span>&#128197; ${p.year || 'N/A'}</span>
                      <span>&bull;</span>
                      <span>&#127963; ${p.venue || 'Academic Journal'}</span>
                      <span>&bull;</span>
                      <span>&#127775; ${p.citations || 0} citations</span>
                      ${p.doi_url ? `<a href="${p.doi_url}" target="_blank" class="text-blue-600 font-semibold hover:underline ml-1">View Paper &rarr;</a>` : ''}
                    </div>
                  </div>
                `).join('')}
              </div>
            </details>
          `;
        }

        card.innerHTML = `
          <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
            <div class="flex items-start space-x-4">
              <div class="w-14 h-14 rounded-full bg-gradient-to-br from-[#1B365D] to-blue-600 text-white font-bold flex items-center justify-center text-lg shadow-md flex-shrink-0">
                ${initials}
              </div>
              <div>
                <h3 class="text-xl font-extrabold text-slate-900 leading-snug">${fac.name}</h3>
                <div class="text-sm text-slate-500 font-medium">${fac.designation || 'Faculty Member'}</div>
                <div class="inline-block bg-blue-50 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded-md mt-1.5 border border-blue-100">
                  ${fac.department}
                </div>
              </div>
            </div>

            <div class="flex flex-col sm:items-end gap-2">
              <div class="flex items-center space-x-3 text-xs text-slate-600">
                <span class="bg-slate-100 px-2.5 py-1 rounded-md font-medium">&#128218; <strong>${works}</strong> Works</span>
                <span class="bg-slate-100 px-2.5 py-1 rounded-md font-medium">&#127775; <strong>${citations}</strong> Citations</span>
                <span class="bg-emerald-50 text-emerald-700 px-2 py-0.5 rounded text-[11px] font-semibold">OpenAlex</span>
              </div>
              <div class="flex items-center space-x-2 mt-1">
                ${fac.email ? `
                  <a href="mailto:${fac.email}" class="inline-flex items-center space-x-1.5 bg-[#1B365D] hover:bg-slate-800 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow-sm transition">
                    <span>&#9993;</span>
                    <span>Email</span>
                  </a>
                ` : ''}
                ${fac.profile_url ? `
                  <a href="${fac.profile_url}" target="_blank" class="inline-flex items-center space-x-1 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold px-3 py-1.5 rounded-lg border border-slate-300 shadow-sm transition">
                    <span>Profile</span>
                    <span class="text-[10px]">&#8599;</span>
                  </a>
                ` : ''}
              </div>
            </div>
          </div>

          ${fac.research_focus ? `
            <div class="mt-4">
              <div class="text-xs font-bold uppercase text-slate-500 tracking-wider mb-1">&#127919; Research Focus & Trajectory</div>
              <p class="text-sm text-slate-700 leading-relaxed">${fac.research_focus}</p>
            </div>
          ` : ''}

          ${methods.length > 0 ? `
            <div class="mt-3.5 flex flex-wrap items-center gap-1.5">
              <span class="text-xs font-bold uppercase text-slate-500 mr-1">&#9881; Methodologies:</span>
              ${methods.map(m => `
                <span class="inline-block bg-amber-50 text-amber-900 border border-amber-200 text-xs font-semibold px-2.5 py-0.5 rounded-full">
                  ${m}
                </span>
              `).join('')}
            </div>
          ` : ''}

          ${topics.length > 0 ? `
            <div class="mt-2.5 flex flex-wrap items-center gap-1.5">
              ${topics.map(t => `
                <span class="inline-block bg-slate-100 text-slate-700 border border-slate-200 text-xs font-medium px-2 py-0.5 rounded-full">
                  &#127991; ${t}
                </span>
              `).join('')}
            </div>
          ` : ''}

          ${fac.student_reach_out_summary ? `
            <div class="mt-4 bg-emerald-50/70 border border-emerald-200 rounded-xl p-3.5">
              <div class="text-xs font-bold text-emerald-800 flex items-center gap-1.5 mb-1">
                <span>&#128161;</span>
                <span>Student Mentorship & Reach-Out Guide</span>
              </div>
              <p class="text-xs sm:text-sm text-emerald-950 leading-relaxed">${fac.student_reach_out_summary}</p>
            </div>
          ` : ''}

          ${papersHtml}
        `;

        grid.appendChild(card);
      });
    }

    document.getElementById('searchInput').addEventListener('input', renderCards);
    document.getElementById('schoolFilter').addEventListener('change', renderCards);
    document.getElementById('sortBy').addEventListener('change', renderCards);

    initSchools();
    updateKPIs();
    renderCards();
  </script>
</body>
</html>
"""

out_html = public_dir / "index.html"
out_html.write_text(html_content, encoding="utf-8")
print(f"Generated {out_html} ({out_html.stat().st_size} bytes)")
