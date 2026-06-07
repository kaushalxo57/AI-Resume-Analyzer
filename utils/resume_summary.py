import re

def generate_local_summary(resume_text: str, extracted_skills: list) -> list:
    """
    Generates 3 to 4 clear, high-impact bullet highlights summarizing the candidate's profile.
    Uses regex rules to look for degrees, experience, and top skills.
    Ensures a natural, human-written tone and avoids forbidden jargon.
    """
    highlights = []
    resume_lower = resume_text.lower()

    # 1. Degree/Education Check
    degree_patterns = [
        (r'\bcomputer\s+science\b', "Computer Science education"),
        (r'\b(b\s*\.?\s*s\b|bachelor|btech|b\.tech|b\.e\.)', "Bachelor's degree"),
        (r'\b(m\s*\.?\s*s\b|master|mtech|m\.tech|m\.b\.a\.)', "Master's level degree"),
        (r'\bphd|ph\.d\b', "Doctoral or advanced research degree")
    ]
    
    edu_match = None
    for pattern, description in degree_patterns:
        if re.search(pattern, resume_lower):
            edu_match = description
            break
            
    if edu_match:
        highlights.append(f"Academic background includes a {edu_match.lower()}.")
    else:
        highlights.append("Practical experience built through engineering coursework and training.")

    # 2. Key Tech Skills Check
    if extracted_skills:
        top_skills = extracted_skills[:4]
        skills_str = ", ".join(top_skills)
        highlights.append(f"Practical skill set includes hands-on experience with: <b>{skills_str}</b>.")
    else:
        highlights.append("Broad technical background supporting developer toolkits and general scripting.")

    # 3. Experience & Workflow Indicators
    experience_indicators = []
    if "git" in resume_lower or "github" in resume_lower:
        experience_indicators.append("Experience working with version control and collaborative software projects.")
    if "pandas" in resume_lower or "numpy" in resume_lower or "machine learning" in resume_lower:
        experience_indicators.append("Capable of executing data processing, data analysis, and modeling pipelines.")
    if "sql" in resume_lower or "database" in resume_lower:
        experience_indicators.append("Skill set covers structured database queries and database schema design.")

    if experience_indicators:
        highlights.append(experience_indicators[0])
    else:
        highlights.append("Adaptable technical background capable of aligning with custom project standards.")

    # 4. Project/Impact Indicator
    if re.search(r'\b(led|managed|developed|created|built|designed|implemented)\b', resume_lower):
        highlights.append("History of successfully building and deploying software features.")
    else:
        highlights.append("Strong problem-solving focus aimed at supporting engineering challenges.")

    return highlights
