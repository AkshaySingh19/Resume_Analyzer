import spacy
from spacy.lang.en import English

# 1️⃣ Define the loader function FIRST
def load_skill_extractor(pattern_path="data/skills.jsonl"):
    """
    Dynamically builds a Spacy NLP pipeline that looks for skills
    defined in the external JSONL file.
    """
    nlp = English()
    # Add the EntityRuler pipe (this handles the matching)
    ruler = nlp.add_pipe("entity_ruler")
    
    # Load patterns from external file
    try:
        ruler.from_disk(pattern_path)
    except Exception as e:
        print(f"⚠️ Warning: Could not load skill patterns from {pattern_path}. {e}")
        
    return nlp

# 2️⃣ Initialize the NLP model (Global variable)
# This works now because the function is defined above ↑
nlp = load_skill_extractor()

# 3️⃣ Define the Normalization Database (Map abbreviations to full names)
SKILL_DB = {
    "ml": "Machine Learning",
    "ai": "Artificial Intelligence",
    "nlp": "Natural Language Processing",
    "js": "JavaScript",
    "ts": "TypeScript",
    "aws": "Amazon Web Services",
    "gcp": "Google Cloud Platform",
    "rag": "Retrieval-Augmented Generation",
    "llm": "Large Language Models",
    "react": "React.js",
    "reactjs": "React.js",
    "vue": "Vue.js",
    "node": "Node.js",
    "mysql": "SQL",        # Map specific SQLs to generic SQL if JD asks for generic
    "postgresql": "SQL",
    "postgres": "SQL"
}

# 4️⃣ Define the extraction function
def extract_skills(text):
    """
    Extracts skills and normalizes them (e.g., 'ML' -> 'Machine Learning').
    """
    if not text:
        return []

    doc = nlp(text)
    skills = set()
    
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            # Clean the text
            clean_skill = ent.text.strip()
            
            # Check if it's an abbreviation in our DB
            if clean_skill.lower() in SKILL_DB:
                standard_skill = SKILL_DB[clean_skill.lower()]
                skills.add(standard_skill)
            else:
                # Otherwise, just add the skill as is (Capitalized)
                skills.add(clean_skill.title())
            
    return sorted(list(skills))