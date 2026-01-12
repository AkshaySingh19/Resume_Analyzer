# 📄 Resume Analyzer (GenAI Powered)

A **GenAI-powered Resume Analyzer** built using **Streamlit** and **Google Gemini**.  
The application compares a candidate’s resume with a job description and provides:

- 🧠 Candidate summary  
- ✅ Skills that match the job description  
- ⚠️ Skills that are missing  

Designed to mimic how an **ATS (Applicant Tracking System)** or **technical recruiter** evaluates resumes.

---

## 🚀 Features

- 📂 Upload resume in **PDF format**
- 📝 Paste any **job description**
- 🤖 AI-powered analysis using **Google Gemini**
- 📊 Clear, structured output:
  - Professional candidate summary
  - Matched skills
  - Missing skills
- 🌙 Clean dark UI
- 🔐 Secure API key handling via `.env`

---

## 🛠 Tech Stack

- **Frontend**: Streamlit  
- **AI Model**: Google Gemini (`models/gemini-flash-latest`)  
- **PDF Parsing**: PyPDF2  
- **Environment Management**: python-dotenv  

---

## 📁 Project Structure

Resume_Analyzer/
│
├── app.py # Streamlit application
├── requirements.txt # Python dependencies
├── .gitignore
│
└── src/
├── ai_analyzer.py # Gemini-based resume analysis logic
└── extract_text.py # PDF resume text extraction
