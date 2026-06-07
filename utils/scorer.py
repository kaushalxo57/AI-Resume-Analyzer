import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
import json
import logging

logger = logging.getLogger(__name__)

# Predefined list of skills and their regexes for local matching
SKILL_PATTERNS = {
    "Python": r"\bpython\b",
    "SQL": r"\bsql\b",
    "Pandas": r"\bpandas\b",
    "NumPy": r"\bnumpy\b",
    "Machine Learning": r"\bmachine\s+learning\b|\bml\b",
    "Scikit-Learn": r"\bscikit-learn\b|\bsci-kit\s+learn\b|\bsklearn\b",
    "Streamlit": r"\bstreamlit\b",
    "Git": r"\bgit\b",
    "GitHub": r"\bgithub\b",
    "Excel": r"\bexcel\b",
    "Power BI": r"\bpower\s*bi\b",
    "Tableau": r"\btableau\b",
    "HTML": r"\bhtml\b",
    "CSS": r"\bcss\b",
    "JavaScript": r"\bjavascript\b|\bjs\b",
    "Java": r"\bjava\b",
    "C++": r"\bc\+\+\b",
    "Data Analytics": r"\bdata\s+analytics\b|\bdata\s+analysis\b",
    "Data Visualization": r"\bdata\s+visualisation\b|\bdata\s+visualization\b",
    "Docker": r"\bdocker\b",
    "Kubernetes": r"\bkubernetes\b|\bk8s\b",
    "AWS": r"\baws\b|\bamazon\s+web\s+services\b",
    "React": r"\breact\b|\breact\.js\b|\breactjs\b",
    "Node.js": r"\bnode\.js\b|\bnodejs\b",
    "TypeScript": r"\btypescript\b|\bts\b",
    "NoSQL": r"\bnosql\b|\bmongodb\b|\bredis\b",
    "CI/CD": r"\bci/cd\b|\bjenkins\b|\bgithub\s+actions\b",
    "Terraform": r"\bterraform\b"
}

STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could',
    'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here',
    'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in',
    'into', 'is', 'isnt', 'it', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor',
    'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'shan', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that',
    'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd',
    'theyll', 'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was',
    'wasnt', 'we', 'wed', 'well', 'were', 'weve', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres',
    'which', 'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd',
    'youll', 'youre', 'youve', 'your', 'yours', 'yourself', 'yourselves', 'will', 'skills', 'experience', 'requirements',
    'like', 'modern', 'portfolio', 'apis', 'logic', 'thought', 'degree', 'candidate', 'role', 'team', 'work', 'working',
    'plus', 'strong', 'good', 'knowledge', 'relevant', 'ability', 'years', 'technologies', 'tools', 'frameworks',
    'certifications', 'software', 'development', 'engineering', 'systems', 'solutions', 'building', 'designing',
    'implementing', 'developing', 'design', 'management', 'support', 'collaboration', 'collaborative', 'collaborate',
    'communication', 'communicating', 'expert', 'expertise', 'hands-on', 'high-performance', 'performance', 'scalable',
    'scalability', 'clean', 'standard', 'standards', 'best', 'practices'
}

def extract_skills_locally(text: str) -> list:
    """Extracts predefined skills from text based on regex matching."""
    extracted = []
    text_lower = text.lower()
    for skill, pattern in SKILL_PATTERNS.items():
        if re.search(pattern, text_lower):
            extracted.append(skill)
    return extracted

def extract_missing_keywords_locally(resume_text: str, job_desc: str) -> list:
    """
    Identifies terms in the job description that are missing from the resume,
    excluding stopwords and short symbols, limited to the top 10 keywords.
    """
    # Tokenize and clean text helper
    def clean_tokens(text):
        text = re.sub(r'[^\w\s\+\-]', ' ', text.lower())
        tokens = text.split()
        return [t for t in tokens if len(t) > 2 and t not in STOPWORDS and not t.isdigit()]

    jd_tokens = clean_tokens(job_desc)
    resume_tokens_set = set(clean_tokens(resume_text))

    # Frequency analysis of JD tokens to find important keywords
    freq = {}
    for token in jd_tokens:
        if token not in resume_tokens_set:
            freq[token] = freq.get(token, 0) + 1

    # Sort by frequency descending and format cleanly (capitalize)
    sorted_missing = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top_missing = [item[0].capitalize() for item in sorted_missing[:10]]
    
    # Map back special capitalizations if needed (e.g. aws -> AWS, docker -> Docker)
    special_cases = {
        "Aws": "AWS", "Docker": "Docker", "Kubernetes": "Kubernetes", "Sql": "SQL", "Api": "API",
        "Python": "Python", "Tableau": "Tableau", "Git": "Git", "Github": "GitHub", "Excel": "Excel"
    }
    top_missing = [special_cases.get(word, word) for word in top_missing]
    return top_missing

def calculate_local_score(resume_text: str, job_desc: str) -> dict:
    """
    Calculates a blended match score based on TF-IDF cosine similarity
    and matching keywords.
    """
    if not resume_text.strip() or not job_desc.strip():
        return {"score": 0, "classification": "Poor"}

    # 1. Cosine similarity of TF-IDF vectors
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc])
        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except Exception:
        cos_sim = 0.0

    # 2. Key term overlap percentage
    def get_terms(text):
        words = re.sub(r'[^\w\s\+\-]', ' ', text.lower()).split()
        return set([w for w in words if len(w) > 2 and w not in STOPWORDS])

    resume_terms = get_terms(resume_text)
    jd_terms = get_terms(job_desc)
    
    overlap = 0.0
    if jd_terms:
        matching = resume_terms.intersection(jd_terms)
        overlap = len(matching) / len(jd_terms)

    # Blended match score out of 100
    # Giving TF-IDF 40% weight and Keyword overlap 60% weight for stability
    score_percentage = int((cos_sim * 0.4 + overlap * 0.6) * 100)
    score_percentage = min(max(score_percentage, 5), 98) # Keep within realistic limits [5, 98]

    # Classification
    if score_percentage <= 40:
        classification = "Poor"
    elif score_percentage <= 70:
        classification = "Average"
    else:
        classification = "Strong"

    return {
        "score": score_percentage,
        "classification": classification
    }

def analyze_with_gemini(api_key: str, resume_text: str, job_desc: str) -> dict:
    """
    Invokes the Google Gemini API to analyze the resume vs. job description,
    returning structured JSON data matching the dashboard sections.
    """
    try:
        genai.configure(api_key=api_key)
        # Use gemini-2.5-flash as the standard, fast, and modern model
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""
You are an expert Applicant Tracking System (ATS) auditor. Analyze the following Resume text against the Job Description.

Resume Text:
{resume_text}

Job Description Text:
{job_desc}

Provide your response strictly in valid JSON format with the following keys and data types. Do not include markdown code block formatting (such as ```json) or any explanation outside the JSON.

JSON Structure:
{{
  "score": int, // 0 to 100 match score
  "classification": string, // "Poor" (0-40), "Average" (41-70), or "Strong" (71-100)
  "skills_extracted": [string], // List of skills found on the resume (focus on Python, SQL, Pandas, NumPy, Machine Learning, Scikit-Learn, Streamlit, Git, GitHub, Excel, Power BI, Tableau, HTML, CSS, JavaScript, Java, C++, Data Analytics, Data Visualization)
  "missing_keywords": [string], // Top 10 critical missing technical keywords from job description. ONLY include specific technologies, tools, frameworks, certifications, and technical skills. DO NOT include generic words like "Modern", "APIs", "Logic", "Degree", "Like", "Portfolio", "Thought", "Experience", or verbs.
  "professional_summary": [string], // 3 to 5 clear, high-impact bullet highlights of the candidate's profile
  "role_predictions": {{
    "best_match": string, // E.g., "Data Analyst" or "Python Developer"
    "alternative_matches": [string] // 2-3 other suitable titles
  }},
  "health_analysis": {{
    "health_score": int, // Resume structure health score 0 to 100
    "health_label": string // "Excellent", "Good", or "Needs Improvement"
  }},
  "improvement_suggestions": [string] // 4-5 prioritized, highly actionable improvement recommendations
}}
"""
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean any markdown code blocks if the model mistakenly outputs them
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                lines = lines[1:-1]
            text = "\n".join(lines).strip()
            
        result = json.loads(text)
        return result
    except Exception as e:
        logger.error(f"Error during Gemini API analysis: {e}")
        # Return fallback flag to prompt calling code to run local heuristics
        return {"error": str(e)}
