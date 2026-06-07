# AI Resume Analyzer

🔗 **Live Demo:** https://kaushal-ai-resume-analyzer.streamlit.app/

AI Resume Analyzer is a web application built with Python and Streamlit that helps job seekers evaluate how well their resume aligns with a target job description.

The application performs ATS-style analysis by comparing resume content against job requirements, identifying missing keywords, extracting technical skills, predicting suitable career roles, and providing actionable suggestions to improve resume quality.

This project was built to strengthen my skills in Python development, NLP, data processing, UI/UX design, and deploying production-ready applications.

---

## Features

### ATS Match Analysis

* Compare resumes against job descriptions
* Calculate ATS compatibility scores
* Classify resumes as Poor, Average, or Strong matches

### Resume Parsing

* Upload PDF resumes
* Support for multi-page documents
* Automatic text extraction

### Skill Detection

Extracts technical skills such as:

* Python
* SQL
* Pandas
* NumPy
* Machine Learning
* Git & GitHub
* Power BI
* Tableau
* HTML, CSS, JavaScript

### Missing Keyword Analysis

* Detect important keywords missing from the resume
* Improve ATS compatibility
* Highlight opportunities for optimization

### Role Prediction

Suggest suitable career paths based on detected skills:

* Data Analyst
* Python Developer
* Data Science Intern
* Business Analyst

### Resume Health Check

Evaluate:

* Resume length
* Skill coverage
* ATS readiness
* Overall resume quality

### Improvement Suggestions

Generate practical recommendations to improve resume strength and keyword coverage.

### PDF Report Export

Download a complete resume analysis report for future reference.

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Libraries

* Pandas
* NumPy
* Scikit-learn
* ReportLab
* PDF Processing Libraries
* Python-dotenv

### AI Integration

* Google Gemini API (Optional)
* Local NLP-based Analysis Engine

---

## Project Structure

```text
AI-Resume-Analyzer/

├── app.py
├── requirements.txt
├── README.md

├── assets/
│   └── style.css

├── utils/
│   ├── parser.py
│   ├── scorer.py
│   ├── recommendations.py
│   ├── resume_summary.py
│   ├── role_predictor.py
│   ├── health_analyzer.py
│   └── report_generator.py
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd AI-Resume-Analyzer
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## Future Enhancements

* Resume comparison across multiple versions
* Advanced ATS scoring algorithms
* Section-wise resume feedback
* Interview preparation suggestions
* Industry-specific resume recommendations
* Resume benchmarking system

---

## What I Learned

Through this project, I gained hands-on experience with:

* Python application development
* Streamlit dashboard design
* PDF text extraction
* Natural Language Processing (NLP)
* ATS-style resume analysis
* API integration
* UI/UX design principles
* Application deployment and project structuring

---

## Author

**Kaushal**

Aspiring Python Developer and Data Analytics Enthusiast passionate about building practical applications, exploring AI-driven solutions, and continuously improving through hands-on projects.
