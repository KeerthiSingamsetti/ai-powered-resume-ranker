# AI-Powered Resume Ranker — HR Intelligence Platform

An intelligent resume screening and ranking platform that helps HR teams and recruiters cut through hundreds of resumes in minutes — not hours. Built using NLP, machine learning, and Generative AI to deliver fair, fast, and explainable candidate evaluation.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

##  Problem Statement

Recruiters spend an average of **6–8 seconds** scanning a single resume. For high-volume hiring, an HR team may receive **500+ resumes** per job posting — making manual screening inefficient, biased, and error-prone.

There's no single tool that can rank candidates, detect fake claims, identify red flags, visually compare top candidates, **and** auto-generate interview questions — all in one platform.

##  Project Goal

Build a one-stop AI-powered HR platform that automates resume screening using NLP, ranks candidates intelligently, detects suspicious claims, visualizes comparisons, and generates interview questions — reducing HR screening time by up to **80%** while improving hiring quality.

---

##  Core Features

| # | Feature | Description |
|---|---------|--------------|
| 01 | **Multi-Resume Ranking Engine** | Upload multiple PDF resumes + paste a Job Description. Extracts text, vectorizes using TF-IDF, and ranks all candidates by Cosine Similarity score with a leaderboard and match %. |
| 02 | **Skill Gap Analyzer** | Identifies which required skills from the JD are missing in each resume — e.g. *"Missing: Docker, Kubernetes, CI/CD"*. |
| 03 | **Trust Score (Auth + Red Flag Detector)** | Combines authenticity checks (e.g. inflated experience claims) with red-flag detection (employment gaps, frequent job switches, vague descriptions) into a single Trust Score out of 100. |
| 04 | **Radar Chart Comparison** | Visual spider chart comparing top 3 candidates across 6 dimensions: Technical Skills, Experience, Education, Soft Skills, ATS Score, and Trust Score (built with Plotly). |
| 05 | **JD Bias Detector** | Scans the Job Description for biased language (age bias, gender bias, exclusionary terms) to promote fair, inclusive hiring. |
| 06 | **AI Interview Question Generator** | Auto-generates 5 personalized, role-specific interview questions per candidate using the Anthropic Claude API — based on their actual resume content and the JD. |

---

##  Tech Stack

| Category | Tools / Libraries | Purpose |
|----------|-------------------|---------|
| Language | Python 3.10+ | Core development |
| NLP | SpaCy, NLTK, Scikit-learn | Text processing & TF-IDF vectorization |
| PDF Parsing | PyPDF2, pdfplumber | Extracting text from uploaded resumes |
| Frontend | Streamlit | Interactive web UI |
| Backend (optional) | Flask | API layer for scoring engine |
| Visualization | Plotly, Matplotlib | Radar charts & score graphs |
| Generative AI | Anthropic Claude API | Interview question generation |
| Dataset | Custom / Kaggle Resume Dataset | Sample resumes for testing |

---

##  Project Structure

```
ai-powered-resume-ranker/
│
├── app.py                  # Main Streamlit application
├── ui/
│   └── styles.py            # Custom CSS theme
├── modules/
│   ├── pdf_extractor.py     # PDF text extraction
│   ├── ranking_engine.py    # TF-IDF + Cosine Similarity ranking
│   ├── skill_gap.py         # Skill gap analysis
│   ├── trust_score.py       # Authenticity + red flag detection
│   ├── bias_detector.py     # JD bias detection
│   └── interview_gen.py     # Claude API interview question generator
├── data/
│   └── sample_resumes/      # Sample resumes for testing
├── requirements.txt
├── .gitignore
└── README.md
```

---

##  Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/KeerthiSingamsetti/ai-powered-resume-ranker.git
cd ai-powered-resume-ranker
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.streamlit/secrets.toml` file in the project root:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```
> ⚠️ Never commit this file — it's already excluded via `.gitignore`.

### 5. Run the app
```bash
streamlit run app.py
```

---

##  Usage

1. Upload multiple candidate resumes (PDF format)
2. Paste the Job Description
3. View the ranked leaderboard with match scores
4. Check each candidate's Skill Gap report and Trust Score
5. Compare top 3 candidates on the Radar Chart
6. Review the JD for bias flags before publishing
7. Select any candidate to generate tailored interview questions

---

##  Future Improvements

- Multi-language resume support
- ATS-style formatting score
- Export ranked results to CSV/PDF
- Integration with applicant tracking systems (ATS)

---
