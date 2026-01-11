from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_skills(resume_text, resume_skills, jd_skills, threshold=0.5):
    """
    Matches Resume skills to JD skills.
    1. Checks if JD skill is in Resume Text (Reverse Search).
    2. Checks Semantic Similarity.
    """
    matched_skills = set()
    missing_skills = set()
    
    resume_text_lower = resume_text.lower()

    for jd_skill in jd_skills:
        found = False
        
        # 1. Exact Match (Check if skill exists in full resume text)
        # We assume if the word exists, the user has the skill
        if f" {jd_skill.lower()} " in f" {resume_text_lower} ":
            matched_skills.add(jd_skill)
            found = True
        
        # 2. Semantic Match (If not found exactly, check similarity)
        elif resume_skills:
            jd_emb = model.encode([jd_skill])
            resume_emb = model.encode(resume_skills)
            scores = cosine_similarity(jd_emb, resume_emb)[0]
            
            if max(scores) >= threshold:
                matched_skills.add(jd_skill)
                found = True
        
        if not found:
            missing_skills.add(jd_skill)

    # Calculate Score
    if not jd_skills:
        score = 0
    else:
        score = (len(matched_skills) / len(jd_skills)) * 100

    return sorted(list(matched_skills)), sorted(list(missing_skills)), round(score, 2)