def predict_roles_locally(extracted_skills: list) -> dict:
    """
    Predicts the best matching job roles and alternative matches
    based on the overlap density of actual extracted skills.
    """
    # Map roles to their key detectable skills (aligned with SKILL_PATTERNS)
    role_skill_maps = {
        "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Git", "GitHub", "Terraform", "CI/CD"],
        "Cloud Engineer": ["AWS", "Docker", "Kubernetes", "Terraform", "Git"],
        "Full Stack Developer": ["JavaScript", "TypeScript", "HTML", "CSS", "Python", "SQL", "Git", "GitHub", "React", "Node.js"],
        "Frontend Developer": ["JavaScript", "TypeScript", "HTML", "CSS", "React", "Git", "GitHub"],
        "Backend Developer": ["Python", "SQL", "Java", "C++", "Git", "GitHub", "Node.js", "NoSQL"],
        "Data Scientist": ["Python", "Pandas", "NumPy", "Machine Learning", "Scikit-Learn", "Data Visualization", "SQL"],
        "Data Engineer": ["Python", "SQL", "Pandas", "NumPy", "NoSQL", "Git"],
        "Data Analyst": ["SQL", "Excel", "Tableau", "Power BI", "Pandas", "Data Analytics", "Data Visualization"],
        "Business Analyst": ["Excel", "SQL", "Power BI", "Tableau", "Data Analytics"]
    }

    scores = {}
    extracted_set = {s.lower() for s in extracted_skills}
    
    # Calculate skill match counts for each role
    for role, key_skills in role_skill_maps.items():
        matched = [s for s in key_skills if s.lower() in extracted_set]
        scores[role] = len(matched)

    # Sort roles by match count descending
    sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Default outputs in case no skills are matched or all score zero
    if not extracted_skills or sorted_roles[0][1] == 0:
        return {
            "best_match": "Junior Software Engineer",
            "alternative_matches": ["Full Stack Developer", "Backend Developer"]
        }

    best_match = sorted_roles[0][0]
    
    # Alternative matches should have some skill overlap
    alternative_matches = [role for role, score in sorted_roles[1:] if score > 0]
    
    # Fill in standard alternatives if the list is empty or short
    fallbacks = ["Full Stack Developer", "Backend Developer", "Data Analyst", "DevOps Engineer"]
    for role in fallbacks:
        if len(alternative_matches) >= 2:
            break
        if role != best_match and role not in alternative_matches:
            alternative_matches.append(role)

    return {
        "best_match": best_match,
        "alternative_matches": alternative_matches[:2]
    }
