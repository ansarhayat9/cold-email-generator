import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# ── Page config (must be FIRST Streamlit call) ──────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Cold Email Generator · AI",
    page_icon="✉️",
)

# ── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root theme ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0d0f1a 0%, #131629 50%, #0d0f1a 100%);
    color: #e2e8f0;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2447 40%, #1a1040 100%);
    border: 1px solid rgba(99, 179, 237, 0.25);
    border-radius: 18px;
    padding: 2.5rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(99,179,237,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #63b3ed, #a78bfa, #63b3ed);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
    margin: 0 0 0.4rem 0;
}
@keyframes shine {
    to { background-position: 200% center; }
}
.hero-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
}


/* ── Make Input Visible & Beautiful ── */
.input-label {
    color: #a0aec0;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.stTextInput > div > div > input {
    background-color: #1a202c !important; 
    color: #f7fafc !important; 
    -webkit-text-fill-color: #f7fafc !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.98rem !important;
}
div[data-baseweb="base-input"], div[data-baseweb="input"] {
    background-color: #1a202c !important;
    border-radius: 10px !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: rgba(99,179,237,0.7) !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.2) !important;
}

/* ── Generate button ── */
.stButton > button {
    background: linear-gradient(135deg, #3182ce, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2.2rem !important;
    font-size: 0.97rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    margin-top: 5px;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,179,237,0.35) !important;
    background: linear-gradient(135deg, #4299e1, #8b5cf6) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Progress steps ── */
.steps-row {
    display: flex;
    gap: 0.6rem;
    align-items: center;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.step-chip {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 0.35rem 1rem;
    font-size: 0.82rem;
    color: #718096;
    transition: all 0.4s ease;
    white-space: nowrap;
}
.step-chip.active {
    background: rgba(99,179,237,0.15);
    border-color: rgba(99,179,237,0.5);
    color: #63b3ed;
    box-shadow: 0 0 12px rgba(99,179,237,0.2);
}
.step-chip.done {
    background: rgba(72,187,120,0.12);
    border-color: rgba(72,187,120,0.4);
    color: #48bb78;
}
.step-arrow {
    color: #4a5568;
    font-size: 0.85rem;
}

/* ── Email result card ── */
.email-card {
    background: #0d1222; /* Clean solid dark */
    border: 1px solid rgba(99,179,237,0.22);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    animation: fadeSlideUp 0.5s ease both;
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.email-card::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3182ce, #7c3aed, #3182ce);
    background-size: 200% auto;
    animation: shine 4s linear infinite;
}
.email-card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.role-badge {
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.35);
    border-radius: 8px;
    padding: 0.4rem 0.9rem;
    font-size: 0.85rem;
    color: #63b3ed;
    font-weight: 600;
}
.email-number {
    background: rgba(167,139,250,0.12);
    border: 1px solid rgba(167,139,250,0.3);
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
    color: #a78bfa;
    font-weight: 600;
}
.email-body {
    color: #cbd5e0;
    font-size: 0.95rem;
    line-height: 1.7;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

/* ── Error card ── */
.error-card {
    background: rgba(245,101,101,0.08);
    border: 1px solid rgba(245,101,101,0.35);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    color: #fc8181;
    font-size: 0.9rem;
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0b0e17 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] label {
    color: #a0aec0 !important;
    font-weight: 600 !important;
}
.sidebar-section-title {
    color: #63b3ed;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    margin-top: 1.2rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    color: #4a5568;
    font-size: 0.8rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.06);
}

/* hide default streamlit header */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Clipboard JS helper ──────────────────────────────────────────────────────
def copy_button(text: str, key: str):
    """Render a styled Copy button that copies `text` to clipboard."""
    escaped = text.replace("`", "\\`").replace("\\", "\\\\").replace("\n", "\\n").replace("'", "\\'")
    st.components.v1.html(f"""
    <style>
        .copy-btn {{
            background: rgba(99,179,237,0.12);
            border: 1px solid rgba(99,179,237,0.35);
            color: #63b3ed;
            border-radius: 8px;
            padding: 7px 18px;
            font-size: 0.83rem;
            font-weight: 600;
            cursor: pointer;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s ease;
        }}
        .copy-btn:hover {{
            background: rgba(99,179,237,0.25);
            box-shadow: 0 4px 14px rgba(99,179,237,0.25);
            transform: translateY(-1px);
        }}
        .copy-btn.copied {{
            background: rgba(72,187,120,0.15);
            border-color: rgba(72,187,120,0.4);
            color: #48bb78;
        }}
    </style>
    <button class="copy-btn" id="btn-{key}" onclick="
        var txt = `{escaped}`;
        navigator.clipboard.writeText(txt).then(function() {{
            var b = document.getElementById('btn-{key}');
            b.textContent = '✅ Copied!';
            b.classList.add('copied');
            setTimeout(function() {{
                b.textContent = '📋 Copy Email';
                b.classList.remove('copied');
            }}, 2200);
        }});
    ">📋 Copy Email</button>
    """, height=48)


# ── Main layout ──────────────────────────────────────────────────────────────
def create_streamlit_app(llm, portfolio, clean_text):
    
    # ── Sidebar Configuration ──
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 1.2rem 0 0.5rem 0;'>
            <div style='font-size:2.2rem;'>✉️</div>
            <div style='font-size:1.1rem; font-weight:700; color:#e2e8f0; margin-top:0.3rem;'>Cold Email AI</div>
            <div style='font-size:0.78rem; color:#4a5568; margin-top:0.2rem;'>Powered by Groq</div>
        </div>
        <hr style='border-color:rgba(255,255,255,0.07); margin:1rem 0;'>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section-title">👤 Sender Profile</div>', unsafe_allow_html=True)
        sender_name = st.text_input("Name", value="Hassan", key="name")
        sender_role = st.text_input("Role", value="Business Development Officer", key="role")
        sender_company = st.text_input("Company", value="Mentee Consulting", key="company")

        st.markdown('<hr style="border-color:rgba(255,255,255,0.06); margin-top:2rem;">', unsafe_allow_html=True)
        st.markdown('<div style="color:#2d3748; font-size:0.75rem; text-align:center;">Cold Email Generator v2.0</div>', unsafe_allow_html=True)


    # Hero banner
    st.markdown("""
    <div class="hero-banner">
        <p class="hero-title">✉️ Cold Email Generator</p>
        <p class="hero-subtitle">
            Paste any job posting URL · AI extracts the role · Writes a personalised outreach email instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # URL Input form area (Removed raw HTML wrappers that caused empty boxes)
    st.markdown('<div class="input-label">🔗 Job Posting URL</div>', unsafe_allow_html=True)
    
    url_input = st.text_input(
        label="url",
        placeholder="https://jobs.lever.co/company/job-id  OR  https://boards.greenhouse.io/...",
        label_visibility="collapsed",
    )
    col_btn, col_spacer = st.columns([1, 4])
    with col_btn:
        submit_button = st.button("⚡ Generate Email", use_container_width=True)

    # Progress steps row (static, lights up via placeholders below)
    steps_placeholder = st.empty()

    def render_steps(active=0, done_up_to=-1):
        labels = ["🌐 Scraping URL", "🔍 Extracting Job", "🧩 Matching Portfolio", "✍️ Writing Email"]
        chips = []
        for i, label in enumerate(labels):
            if i < done_up_to:
                cls = "done"
            elif i == active:
                cls = "active"
            else:
                cls = ""
            chips.append(f'<span class="step-chip {cls}">{label}</span>')
            if i < len(labels) - 1:
                chips.append('<span class="step-arrow">›</span>')
        steps_placeholder.markdown(
            f'<div class="steps-row">{"".join(chips)}</div>',
            unsafe_allow_html=True,
        )

    if submit_button:
        if not url_input.strip():
            st.markdown("""
            <div class="error-card">⚠️ Please enter a job posting URL before generating.</div>
            """, unsafe_allow_html=True)
        else:
            try:
                # Step 1 – Scrape
                render_steps(active=0)
                with st.spinner("🌐 Scraping the job posting…"):
                    loader = WebBaseLoader([url_input])
                    data = clean_text(loader.load().pop().page_content)

                # Step 2 – Extract
                render_steps(active=1, done_up_to=1)
                with st.spinner("🔍 Extracting job details…"):
                    portfolio.load_portfolio()
                    jobs = llm.extract_jobs(data)

                # Step 3 – Match portfolio
                render_steps(active=2, done_up_to=2)
                with st.spinner("🧩 Matching your portfolio…"):
                    results = []
                    for job in jobs:
                        skills = job.get("skills", [])
                        portfolio_urls = portfolio.query_links(skills)
                        results.append((job, portfolio_urls))

                # Step 4 – Generate emails
                render_steps(active=3, done_up_to=3)
                with st.spinner("✍️ Writing professional cold emails…"):
                    emails = []
                    for job, portfolio_urls in results:
                        email = llm.write_email(job, portfolio_urls, sender_name, sender_role, sender_company)
                        emails.append((job, email))

                # All done → mark all steps green
                steps_placeholder.markdown("""
                <div class="steps-row">
                  <span class="step-chip done">🌐 Scraping URL</span>
                  <span class="step-arrow">›</span>
                  <span class="step-chip done">🔍 Extracting Job</span>
                  <span class="step-arrow">›</span>
                  <span class="step-chip done">🧩 Matching Portfolio</span>
                  <span class="step-arrow">›</span>
                  <span class="step-chip done">✍️ Writing Email</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style='
                    background:rgba(72,187,120,0.1);
                    border:1px solid rgba(72,187,120,0.35);
                    border-radius:10px;
                    padding:0.75rem 1.2rem;
                    color:#48bb78;
                    font-size:0.9rem;
                    margin-bottom:1.5rem;'>
                    ✅ Done! Generated <b>{len(emails)}</b> cold email{"s" if len(emails)>1 else ""}.
                </div>
                """, unsafe_allow_html=True)

                # Render each email as a card
                for idx, (job, email) in enumerate(emails, start=1):
                    role = job.get("role", "Role")
                    st.markdown(f"""
                    <div class="email-card">
                        <div class="email-card-header">
                            <span class="email-number">#{idx}</span>
                            <span class="role-badge">💼 {role}</span>
                        </div>
                        <div class="email-body">{email}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    copy_button(email, key=f"email_{idx}")

            except Exception as e:
                render_steps(active=0)
                st.markdown(f"""
                <div class="error-card">
                    ❌ <div><b>An error occurred:</b><br><span style="font-size:0.85rem; opacity:0.85;">{e}</span></div>
                </div>
                """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        Built with ❤️ using Streamlit · LangChain · Groq · ChromaDB
    </div>
    """, unsafe_allow_html=True)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio(file_path="./sample_portfolio.csv")
    create_streamlit_app(chain, portfolio, clean_text)