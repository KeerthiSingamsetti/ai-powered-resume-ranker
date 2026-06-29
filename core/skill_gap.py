"""
skill_gap.py
────────────
Feature 2: Skill Gap Analyzer
Extracts skills from JD and each resume, then shows what's missing.
"""

import re
from typing import List, Set, Dict

# ── Master skill vocabulary ────────────────────────────────────────────────────
# Extend this list freely — it covers common tech + soft skills.
SKILL_VOCAB: Set[str] = {
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "ruby", "php", "swift", "kotlin", "scala", "r", "matlab",
    # Web
    "html", "css", "react", "angular", "vue", "nextjs", "nodejs", "express",
    "django", "flask", "fastapi", "spring", "laravel",
    # Data / ML
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "matplotlib", "seaborn", "plotly", "tableau", "power bi",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "cassandra", "sqlite", "firebase",
    # Cloud / DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "ci/cd",
    "terraform", "ansible", "git", "github", "gitlab", "linux",
    # Data Engineering
    "spark", "hadoop", "kafka", "airflow", "dbt", "etl",
    # Soft skills
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "project management", "agile", "scrum",
    # Other tech
    "api", "rest", "graphql", "microservices", "llm", "openai", "claude",
    "langchain", "vector database", "prompt engineering",
}


def _normalize(text: str) -> str:
    return text.lower().strip()


def extract_skills(text: str) -> Set[str]:
    """Return set of skills found in the given text."""
    text_lower = _normalize(text)
    found = set()
    for skill in SKILL_VOCAB:
        # Use word-boundary match to avoid substring false positives
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def analyze_skill_gap(resume_text: str, jd_text: str) -> Dict:
    """
    Returns:
        {
            "jd_skills":      set of skills required by JD,
            "resume_skills":  set of skills found in resume,
            "matched":        skills present in both,
            "missing":        skills in JD but not in resume,
            "extra":          skills in resume but not in JD (bonus),
            "match_pct":      percentage of JD skills matched,
        }
    """
    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    matched = jd_skills & resume_skills
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills

    match_pct = (len(matched) / len(jd_skills) * 100) if jd_skills else 0.0

    return {
        "jd_skills": jd_skills,
        "resume_skills": resume_skills,
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "match_pct": round(match_pct, 1),
    }
