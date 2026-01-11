import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# -------------------- ENV & MODEL --------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-flash-latest")

# -------------------- UI STYLE --------------------
st.markdown("""
<style>
.stApp {
    background-color: #0f0f0f;
    color: #e5e7eb;
}
.section {
    background: #111827;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 24px;
}
h2, h3 {
    color: #f9fafb;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("📄 Resume Analyzer")
st.caption("Analyze resume against a job description")

# -------------------- RESUME UPLOAD --------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📂 Upload Resume (PDF only)")

uploaded_file = st.file_uploader("Choose a PDF resume", type=["pdf"])

resume_text = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        if page.extract_text():
            resume_text += page.extract_text()
    st.success("Resume uploaded successfully ✅")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- JOB DESCRIPTION --------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📝 Job Description")

job_description = st.text_area(
    "Paste job description here",
    height=220,
    placeholder="Required skills, responsibilities, experience..."
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ANALYZE BUTTON --------------------
analyze = st.button("🚀 Analyze Resume", use_container_width=True)

# -------------------- RESULT --------------------
if analyze:
    if not resume_text or not job_description:
        st.warning("⚠ Please upload a resume and enter a job description")
        st.stop()

    with st.spinner("🤖 Analyzing candidate profile..."):
        prompt = f"""
You are an ATS system and professional technical recruiter.

Your tasks:
1. Give a concise professional summary of the candidate.
2. List skills the candidate HAS that match the job description.
3. List skills the candidate is MISSING.

Resume:
{resume_text}

Job Description:
{job_description}

Return output with clear headings.
"""

        response = model.generate_content(prompt)
        result = response.text

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📊 Analysis Result")
    st.markdown(result)
    st.markdown("</div>", unsafe_allow_html=True)
