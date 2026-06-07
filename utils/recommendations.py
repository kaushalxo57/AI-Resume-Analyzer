def generate_local_suggestions(score: int, missing_keywords: list, extracted_skills: list) -> list:
    """
    Generates actionable, prioritized improvement recommendations for the resume
    based on local scoring and analysis.
    """
    suggestions = []

    # Recommendation 1: Word Count / Density
    if len(extracted_skills) < 5:
        suggestions.append("Enrich your skills profile by adding specific technologies and workflows mentioned in the target role.")
    else:
        suggestions.append("Reorganize your technical section using clean bullet points and distinct categories for improved readability.")

    # Recommendation 2: Missing Keywords Actionable Item
    if missing_keywords:
        top_missing_str = ", ".join(missing_keywords[:3])
        suggestions.append(f"Incorporate missing core industry keywords: <b>{top_missing_str}</b> within your professional experience descriptions.")
    else:
        suggestions.append("Tailor your professional highlights to reflect the exact vocabulary and keywords used in the job description.")

    # Recommendation 3: Match Score based suggestion
    if score < 40:
        suggestions.append("Structure your bullet points using the <b>X-Y-Z formula</b>: 'Accomplished [X] as measured by [Y], by doing [Z]' to show clear business impact.")
    elif score < 70:
        suggestions.append("Quantify your project outcomes. Use metrics, percentages, and dollar amounts where possible to illustrate your contributions.")
    else:
        suggestions.append("Ensure your GitHub portfolio and active project links are highly visible near the header of your document.")

    # Recommendation 4: Missing technical competencies checklist
    missing_tech = [k for k in ["SQL", "Python", "Git", "Tableau", "Excel"] if k not in extracted_skills]
    if missing_tech:
        suggestions.append(f"Highlight foundational developer utilities such as <b>{', '.join(missing_tech[:2])}</b> if you possess exposure to them.")
    else:
        suggestions.append("Emphasize automation, pipeline scalability, or leadership contributions in your most recent project descriptions.")

    # Recommendation 5: General Formatting Standard
    suggestions.append("Optimize formatting for ATS: Avoid tables, images, text boxes, and complex multi-column grid layouts which confuse scanners.")

    return suggestions
