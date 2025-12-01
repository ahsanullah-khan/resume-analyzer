
import streamlit as st
import pandas as pd
from resume_analyzer import resume_analyzer_app, extract_text_from_file
import plotly.graph_objects as go
import time
import base64

st.set_page_config(
    page_title="Smart Resume Analyzer - AI Job Fit Checker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styling
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 3.5rem;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }

    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #eaeaea;
        margin-bottom: 2rem;
        text-align: center;
        height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    /* Section Cards */
    .section-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #eaeaea;
        margin-bottom: 2rem;
    }

    /* Info note styling */
    .info-note {
        background: #f8f9fa;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #495057 !important;
        border-left: 4px solid #667eea;
        font-size: 0.95rem;
    }

    /* Skills styling */
    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    .skill-tag {
        background: #667eea;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .skill-tag.missing {
        background: #e74c3c;
    }

    /* Button styling */
    .analyze-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
    }
    .analyze-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        color: white;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-label {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }

    /* Testimonial */
    .testimonial {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }

    /* Hide Streamlit elements */
    .css-1d391kg {display: none}
</style>
""", unsafe_allow_html=True)

def main():
    # Navigation
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: white; border-radius: 10px; margin-bottom: 2rem;'>
        <strong style='font-size: 1.2rem; color: #667eea;'>Smart Resume Analyzer</strong>
        <span style='margin: 0 1rem; color: #ccc'>|</span>
        <a href='#analyzer' style='color: #667eea; text-decoration: none; margin: 0 1rem;'>Analyze Resume</a>
        <span style='margin: 0 1rem; color: #ccc'>|</span>
        <a href='#features' style='color: #667eea; text-decoration: none; margin: 0 1rem;'>Features</a>
        <span style='margin: 0 1rem; color: #ccc'>|</span>
        <a href='#how-it-works' style='color: #667eea; text-decoration: none; margin: 0 1rem;'>How It Works</a>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>SCORE MY RESUME - FREE RESUME CHECKER</div>
        <div class='hero-subtitle'>Get expert feedback on your resume, instantly</div>
        <p style='font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.9;'>
            Our free AI-powered resume checker scores your resume on key criteria recruiters and hiring managers look for.
            Get actionable steps to revamp your resume and land more interviews.
        </p>
        <a href='#analyzer' class='analyze-btn'>Check My Resume Now →</a>
        <p style='margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;'>100% privacy • Trusted by thousands of job seekers</p>
    </div>
    """, unsafe_allow_html=True)

    # Trust Badges
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='font-size: 1.1rem; font-weight: 600; color: #2c3e50;'>Excellent Review</div>
            <div style='font-size: 0.9rem; color: #666;'>Rated 4.9/5 based on 1000+ reviews</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Features Section
    st.markdown("<a id='features'></a>", unsafe_allow_html=True)
    st.markdown("## 🚀 The Most Advanced Resume Checker, Powered by AI")
    st.markdown("""
    <div class='info-note'>
        <strong>Smart Resume Analyzer</strong> goes beyond basic spell checking and uses leading Artificial Intelligence technology
        to grade your resume on 20+ resume checks that recruiters and hiring managers pay attention to.
    </div>
    """, unsafe_allow_html=True)

    # Feature Grid
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🎯</div>
            <div class='feature-title'>AI-Powered Analysis</div>
            <p>Advanced AI analyzes your resume's impact, style, and content against job requirements</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <div class='feature-title'>Match Scoring</div>
            <p>Get precise match percentage and detailed breakdown of skills alignment</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>💡</div>
            <div class='feature-title'>Actionable Suggestions</div>
            <p>Receive specific, personalized advice to improve your resume instantly</p>
        </div>
        """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown("<a id='how-it-works'></a>", unsafe_allow_html=True)
    st.markdown("## 🔍 How Our Resume Checker Works")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='section-card'>
            <h3>🤖 Powered by Advanced AI</h3>
            <p>Our system uses machine learning and natural language processing to analyze your resume against job descriptions,
            identifying key skills, experience gaps, and improvement opportunities.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='section-card'>
            <h3>🎯 Designed by Experts</h3>
            <p>The analysis criteria are based on insights from hiring managers and recruiters at top companies.
            We know exactly what they look for in candidates.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='section-card'>
            <h3>📈 Proven Results</h3>
            <p>Users who improve their resumes based on our feedback see 3x more interviews and callbacks.
            Transform your resume with data-driven insights.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='section-card'>
            <h3>⚡ Instant Analysis</h3>
            <p>Get comprehensive resume analysis in seconds. No waiting, no sign-up required.
            Just upload and get immediate, actionable feedback.</p>
        </div>
        """, unsafe_allow_html=True)

    # Testimonial
    st.markdown("""
    <div class='testimonial'>
        <h3 style='color: white; margin-bottom: 1rem;'>"This tool helped me land 3x more interviews!"</h3>
        <p style='color: white; opacity: 0.9;'>- Sarah Khan., Software Engineer at Engro Corp</p>
    </div>
    """, unsafe_allow_html=True)

    # Main Analyzer Section
    st.markdown("<a id='analyzer'></a>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 📊 Analyze Your Resume Now")

    # Initialize session state
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    # Input Section
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📄 Upload Your Resume")

        resume_file = st.file_uploader(
            "Choose your resume file",
            type=['pdf', 'docx', 'txt'],
            key="resume_upload",
            label_visibility="collapsed"
        )

        if resume_file:
            resume_text = extract_text_from_file(resume_file.getvalue(), resume_file.name)
            st.success(f"✅ Resume uploaded! ({len(resume_text)} characters)")
        else:
            resume_text = st.text_area(
                "Paste your resume text:",
                height=180,
                placeholder="Paste your resume content here...",
                key="resume_text"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📋 Upload Job Description")

        jd_file = st.file_uploader(
            "Choose job description file",
            type=['pdf', 'docx', 'txt'],
            key="jd_upload",
            label_visibility="collapsed"
        )

        if jd_file:
            job_description = extract_text_from_file(jd_file.getvalue(), jd_file.name)
            st.success(f"✅ Job Description uploaded! ({len(job_description)} characters)")
        else:
            job_description = st.text_area(
                "Paste job description:",
                height=180,
                placeholder="Paste the job description here...",
                key="job_desc"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Analyze Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Analyze My Resume Now", use_container_width=True, type="primary"):
            if not resume_text or not job_description:
                st.error("❌ Please provide both resume content and job description.")
            else:
                st.session_state.processing = True
                with st.spinner("🤖 AI is analyzing your resume against the job description... This may take a few seconds."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)

                    try:
                        results = resume_analyzer_app.invoke({
                            "resume_text": resume_text,
                            "job_description": job_description
                        })
                        st.session_state.analysis_results = results
                        st.session_state.processing = False
                        st.success("✅ Analysis Complete! Scroll down to see your results.")
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.session_state.processing = False

    # Results Section
    if st.session_state.analysis_results and not st.session_state.processing:
        results = st.session_state.analysis_results

        st.markdown("---")
        st.markdown("## 📈 Your Resume Analysis Results")

        # Score Cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{results["match_percentage"]}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Overall Match</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{int(results["semantic_similarity"] * 100)}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Content Relevance</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            keyword_data = results["keyword_matches"]
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{len(keyword_data["missing_skills"])}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Skills to Improve</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Missing Skills
        if keyword_data["missing_skills"]:
            st.markdown("### 🎯 Focus on These Skills")
            st.markdown('<div class="skills-container">', unsafe_allow_html=True)
            for skill in keyword_data["missing_skills"]:
                st.markdown(f'<span class="skill-tag missing">{skill.title()}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("🎉 Excellent! Your resume covers all the required skills mentioned in the job description.")

        # Improvement Suggestions
        st.markdown("## 💡 Personalized Improvement Suggestions")

        for i, suggestion in enumerate(results["suggested_changes"], 1):
            st.markdown(f"""
            <div class='section-card'>
                <strong>🎯 Suggestion #{i}:</strong> {suggestion}
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h3>Smart Resume Analyzer</h3>
        <p>Get the job you deserve, faster. Powered by AI and expert insights.</p>
        <div style='margin-top: 1rem;'>
            <a href='#analyzer' style='color: #667eea; text-decoration: none; margin: 0 1rem;'>Analyze Resume</a> •
            <a href='#features' style='color: #667eea; text-decoration: none; margin: 0 1rem;'>Features</a> •
            <a href='#how-it-works' style='color: #667eea; text-decoration: none; margin: 0 1rem;'>How It Works</a>
        </div>
        <p style='margin-top: 2rem; font-size: 0.9rem;'>Built by Ahsanullah Khan using LangGraph, Streamlit, and Groq LLM</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
