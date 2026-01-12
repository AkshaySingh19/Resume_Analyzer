import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# -------------------- LOAD ENV --------------------
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

# -------------------- FUNCTIONS --------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an ATS (Applicant Tracking System).

Analyze the resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:
1. Resume Match Percentage
2. Key Strengths
3. Missing Skills
"""

    response = model.generate_content(prompt)
    return response.text


# 🔥 NEW FEATURE: INTERVIEW QUESTION GENERATOR
def generate_interview_questions(resume_text, job_description):
    prompt = f"""
You are an AI technical interviewer.

Using the candidate resume and job description below, generate interview questions.

Resume:
{resume_text}

Job Description:
{job_description}

Generate:
1. 3 skill-based technical questions
2. 2 project-based questions
3. 2 gap-based questions (skills missing or weak)
4. 2 scenario-based problem-solving questions

Rules:
- Questions must be concise
- Role-specific
- No explanations
- Use bullet points
"""

    response = model.generate_content(prompt)
    return response.text


# -------------------- UI --------------------
st.title("📄 AI Resume Analyzer with Interview Intelligence")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

# -------------------- ANALYZE BUTTON --------------------
if st.button("Analyze Resume"):
    if uploaded_file is None or job_description.strip() == "":
        st.warning("Please upload a resume and provide a job description.")
    else:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            analysis_result = analyze_resume(resume_text, job_description)

        st.subheader("📊 ATS Analysis Result")
        st.write(analysis_result)

        # Store for later use
        st.session_state["resume_text"] = resume_text
        st.session_state["job_description"] = job_description


# -------------------- INTERVIEW QUESTIONS --------------------
if "resume_text" in st.session_state and "job_description" in st.session_state:
    st.markdown("---")
    st.subheader("🧠 AI-Suggested Interview Questions")

    if st.button("Generate Interview Questions"):
        with st.spinner("Generating tailored interview questions..."):
            questions = generate_interview_questions(
                st.session_state["resume_text"],
                st.session_state["job_description"]
            )

        st.markdown(questions)
