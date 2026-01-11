import google.generativeai as genai
import json
import time

def analyze_resume_with_ai(resume_text, jd_text, api_key):
    if not api_key:
        return {"error": "API Key missing"}

    genai.configure(api_key=api_key)
    
    # Use the stable alias which usually has better free tier limits
    model = genai.GenerativeModel('models/gemini-flash-latest')

    prompt = f"""
    Act as an expert ATS (Applicant Tracking System).
    
    JOB DESCRIPTION:
    {jd_text}

    RESUME TEXT:
    {resume_text}

    TASK:
    1. Identify all technical skills in the JD and Resume.
    2. Calculate a Match Score (0-100).
    3. List MATCHED vs MISSING skills.
    4. Provide specific feedback.

    OUTPUT FORMAT (Strict JSON):
    {{
        "match_score": 75,
        "jd_skills": ["Skill A", "Skill B"],
        "resume_skills": ["Skill A"],
        "missing_skills": ["Skill B"],
        "summary_feedback": "Feedback here."
    }}
    """

    # RETRY LOGIC (Try 3 times before failing)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            json_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(json_text)
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                # If rate limited, wait 5 seconds and try again
                time.sleep(5)
                continue
            else:
                # If it's a real error (like 404 or Auth), stop immediately
                return {"error": f"AI Error: {error_msg}"}
    
    return {"error": "Server is busy. Please try again in a minute."}