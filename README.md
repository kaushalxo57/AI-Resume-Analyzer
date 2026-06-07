# AI Resume Analyzer 👹

A premium Applicant Tracking System (ATS) resume auditor built using Python and Streamlit. The application features a custom, high-end interface styled in **Japanese Cyber Minimalism**—featuring a black luxury aesthetic, sharp editorial typography, and accent-red indicators.

This project is built to showcase production-ready engineering and is ideal for showcasing on portfolios (GitHub, LinkedIn).

---

## ⚡ Features
1. **PDF Resume Parsing**: Automatically extracts text from uploaded PDF files (including multi-page documents).
2. **Hybrid Analysis Engine**:
   - **Local NLP Heuristics (Offline)**: Compares resume and job description using TF-IDF Vectorization, Cosine Similarity, case-insensitive Regex skills extraction, and stopword-filtered keyword matching.
   - **AI-Enhanced Deep Analysis (Gemini)**: Upgrade analysis quality dynamically by pasting your Google Gemini API Key in the sidebar. Performs advanced semantic auditing.
3. **ATS Match Scoring**: Displays an alignment score percentage along with classification badges (`Poor`, `Average`, `Strong`).
4. **Core Technical Skills Extraction**: Identifies 19 predefined industry skills and displays them in minimalist tags.
5. **Missing Keywords Auditing**: Finds the top 10 important terms in the job description missing from the candidate's resume.
6. **Role Match Prediction**: Predicts candidate's primary matching role and maps secondary alternatives.
7. **Resume Health Check**: Evaluates length, formatting, and structural checks, displaying a health index out of 100.
8. **Actionable Suggestions**: Provides clear, prioritized, and practical suggestions for improvement.
9. **Interactive PDF Report Download**: Generates a professional, beautifully formatted PDF report of the findings on the fly using `reportlab`.

---

## 🎨 Design Direction (Japanese Cyber Minimalism)
- **Theme**: Minimalist black background (`#000000` / `#0A0A0A`) with sharp crimson accents (`#FF3B30`).
- **Typography**: Editorial headings using **Space Grotesk** and clear body copy using **Inter**.
- **UX Feel**: Clear borders, hover highlights, clean margins, and an absence of standard emojis or overly colorful dashboard widgets.

---

## 📁 Project Directory Structure
```text
AI-Resume-Analyzer/
├── app.py                     # Main Streamlit web application
├── requirements.txt           # Package dependencies
├── README.md                  # System documentation
├── assets/
│   └── style.css              # Custom cyber-minimalist CSS overrides
└── utils/
    ├── parser.py              # PDF parsing module (pypdf)
    ├── scorer.py              # Local TF-IDF & Gemini matcher
    ├── recommendations.py     # Local improvement suggester
    ├── resume_summary.py      # Local highlights summary builder
    ├── role_predictor.py      # Local role density classifier
    ├── health_analyzer.py     # Health criteria checklist auditor
    └── report_generator.py    # ReportLab PDF report builder
```

---

## ⚙️ Installation & Running Locally

### Prerequisites
- Python 3.10 or higher (Tested on Python 3.13)
- Pip package manager

### 1. Clone & Navigate
```bash
git clone <your-repository-url>
cd "AI Resume Analyzer"
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
If you wish to pre-load a Gemini API Key instead of entering it in the web interface, create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 5. Launch the Application
```bash
streamlit run app.py
```

The application will launch on `http://localhost:8501`.

---

## ☁️ Deployment
The application is pre-configured for instant deployment to **Streamlit Community Cloud** or other platforms like Hugging Face Spaces:
1. Push this directory to a public GitHub repository.
2. Visit [Streamlit Share](https://share.streamlit.io/) and log in with GitHub.
3. Link the repository, select `app.py` as the entrypoint, and deploy!
4. *(Optional)* Add your `GEMINI_API_KEY` under Streamlit Advanced Settings -> Secrets if you want it enabled by default for all users.
