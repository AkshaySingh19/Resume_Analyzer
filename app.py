import streamlit as st
import os
from dotenv import load_dotenv
from src.extract_text import extract_text_from_pdf
from src.ai_analyzer import analyze_resume_with_ai

# Load env variables
load_dotenv()

st.set_page_config(page_title="GenAI Resume Analyzer", page_icon="🧠", layout="wide")

st.title("🧠 GenAI Resume Analyzer")
st.markdown("Fully powered by Google Gemini (No Regex/Hardcoding)")

# --- Sidebar ---
with st.sidebar:
    st.header("🔑 API Setup")
    env_key = os.getenv("GOOGLE_API_KEY")
    api_key = st.text_input("Gemini API Key", value=env_key or "", type="password")
    
    st.divider()
    st.header("📂 Upload")
    uploaded_file = st.file_uploader("Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Job Description", height=200)
    
    analyze_btn = st.button("Analyze with AI", type="primary")

# --- Main Logic ---
if analyze_btn:
    if not api_key:
        st.error("❌ Please enter your Google Gemini API Key.")
        st.stop()
        
    if uploaded_file and jd_text:
        with st.spinner("🤖 AI is reading your resume..."):
            
            # 1. Text Extraction
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # 2. AI Analysis (The RAG/GenAI Step)
            result = analyze_resume_with_ai(resume_text, jd_text, api_key)
            
            if "error" in result:
                st.error(f"AI Error: {result['error']}")
            else:
                # 3. Display Results
                score = result.get("match_score", 0)
                
                # Metrics
                st.divider()
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("AI Match Score", f"{score}%")
                    st.progress(score / 100)
                with col2:
                    st.info(f"💡 **AI Feedback:** {result.get('summary_feedback')}")

                # Skills Comparison
                st.divider()
                c1, c2 = st.columns(2)
                
                with c1:
                    st.subheader("✅ Matched Skills")
                    # Find intersection (This is logical matching, but AI already did the heavy lifting)
                    # For simplicity, we assume AI result['resume_skills'] covers it, 
                    # but let's show exactly what the AI said was missing vs present.
                    
                    # Calculate matched simply by checking what is NOT in missing
                    all_jd = set(result.get("jd_skills", []))
                    missing = set(result.get("missing_skills", []))
                    matched = list(all_jd - missing)
                    
                    for s in matched:
                        st.success(s)
                        
                with c2:
                    st.subheader("⚠️ Missing Skills")
                    for s in missing:
                        st.error(s)

                # Raw AI Data (Debug)
                with st.expander("🔍 See Raw AI Analysis"):
                    st.json(result)

    else:
        st.warning("Please upload a resume and paste a Job Description.")