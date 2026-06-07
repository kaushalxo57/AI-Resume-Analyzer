# AI Resume Analyzer

A resume analysis tool built using Python and Streamlit that helps job seekers understand how well their resume matches a specific job description.

The application analyzes resumes using ATS-style matching, identifies missing keywords, extracts technical skills, predicts suitable roles, and generates improvement suggestions to help candidates improve their chances of getting shortlisted.

This project was built as part of my learning journey in Python, Data Analytics, NLP, and web application development.

---

## Features

### ATS Score Analysis

* Compares resume content with a target job description
* Generates an ATS compatibility score
* Classifies resumes as Poor, Average, or Strong matches

### Resume Parsing

* Upload resumes in PDF format
* Automatically extracts content from single or multi-page resumes

### Skill Extraction

Detects common technical skills such as:

* Python
* SQL
* Pandas
* NumPy
* Machine Learning
* Git
* GitHub
* Power BI
* Tableau
* HTML
* CSS
* JavaScript

### Missing Keyword Detection

* Identifies important keywords present in the job description but missing from the resume
* Helps improve ATS compatibility

### Role Prediction

Suggests suitable roles based on the detected skills, including:

* Data Analyst
* Python Developer
* Data Science Intern
* Business Analyst

### Resume Health Check

Evaluates:

* Resume length
* Skill coverage
* ATS readiness
* Overall resume quality

### Improvement Suggestions

Provides actionable recommendations to strengthen the resume and improve keyword coverage.

### PDF Report Export

Generate and download a complete analysis report.

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Libraries Used

* Pandas
* Scikit-learn
* PDF Processing
* ReportLab
* NumPy
* Python-dotenv

### AI Integration

* Google Gemini API (Optional)
* Local NLP-based analysis engine

---

## Project Structure

```text
AI-Resume-Analyzer/

├── app.py

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

├── requirements.txt

└── README.md
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

## Future Improvements

* Resume comparison between multiple versions
* Advanced ATS scoring model
* Resume section analysis
* Interview preparation suggestions
* Industry-specific recommendations
* Resume benchmarking

---

## What I Learned

Through this project I gained practical experience with:

* Python application development
* Streamlit dashboards
* PDF parsing
* NLP fundamentals
* ATS-style resume analysis
* UI/UX design
* API integration
* Project structuring and deployment

---

## Author

Built by Kaushal as part of my portfolio and continuous learning journey in Python, Data Analytics, and AI-powered applications.
