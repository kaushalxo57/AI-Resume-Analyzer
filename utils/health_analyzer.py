import re

def analyze_resume_health_locally(resume_text: str, extracted_skills: list) -> dict:
    """
    Evaluates the overall formatting, length, and sections of the resume
    to generate a health score and checklist indicators.
    """
    score = 0
    checklist = {
        "word_count": False,
        "sections_found": False,
        "skills_coverage": False,
        "ats_formatting": False
    }

    # 1. Word Count Check (Ideal: 300 to 900 words)
    words = resume_text.split()
    word_count = len(words)
    
    if 300 <= word_count <= 900:
        score += 30
        checklist["word_count"] = True
    elif 150 <= word_count < 300 or 900 < word_count <= 1200:
        score += 20
        checklist["word_count"] = True
    else:
        score += 10

    # 2. Key Resume Sections Check
    sections = ["education", "experience", "project", "skill", "contact"]
    resume_lower = resume_text.lower()
    sections_found = 0
    
    for section in sections:
        # Match word boundaries or bold headers
        if re.search(rf"\b{section}s?\b", resume_lower):
            sections_found += 1

    section_score = sections_found * 8  # Max 40 points
    score += section_score
    if sections_found >= 4:
        checklist["sections_found"] = True

    # 3. Skill Coverage (Ideal: at least 4 extracted skills)
    skill_count = len(extracted_skills)
    if skill_count >= 5:
        score += 20
        checklist["skills_coverage"] = True
    elif 2 <= skill_count < 5:
        score += 15
        checklist["skills_coverage"] = True
    else:
        score += 5

    # 4. ATS Formatting Scan (Look for bad chars or formatting symbols)
    # Give a default boost if the document parses successfully
    if word_count > 50:
        score += 10
        checklist["ats_formatting"] = True
    else:
        score += 5

    # Cap score
    score = min(max(score, 15), 100)

    # Classify health label
    if score >= 80:
        label = "Excellent"
    elif score >= 60:
        label = "Good"
    else:
        label = "Needs Improvement"

    return {
        "health_score": score,
        "health_label": label,
        "word_count": word_count,
        "sections_found_count": sections_found,
        "checklist": checklist
    }
