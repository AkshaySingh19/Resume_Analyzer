import google.generativeai as genai

def configure_ai(api_key):
    try:
        if not api_key:
            return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error configuring AI: {e}")
        return None

def generate_suggestions(resume_text, missing_skills, jd_text, model):
    if not model:
        return "⚠️ AI Model not loaded. Please check your API Key."
    
    prompt = f"""
    Act as an expert Resume Writer.
    
    CONTEXT:
    The user has a resume but is missing these specific skills for a job: {missing_skills}.
    
    RESUME CONTENT:
    {resume_text[:2000]}
    
    JOB DESCRIPTION:
    {jd_text[:1000]}
    
    TASK:
    Based strictly on the user's existing projects and experience, suggest 3 specific bullet points they could add to their resume that would legitimately demonstrate some of the missing skills (or close alternatives).
    Do not invent false experience. Focus on how their existing work relates to the missing tools.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating suggestions: {e}"

def generate_interview_questions(resume_text, jd_text, model):
    if not model:
        return "⚠️ AI Model not loaded."

    prompt = f"""
    Act as a Technical Interviewer.
    Generate 3 tough technical interview questions based on the gap between this Resume and Job Description.
    
    RESUME: {resume_text[:1000]}
    JD: {jd_text[:1000]}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating questions: {e}"