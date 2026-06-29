"""
ranker.py
─────────
Feature 1: Multi-Resume Ranking Engine
TF-IDF + Cosine Similarity → ranked leaderboard with match %.
"""

import re
from typing import List, Dict, Tuple

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data (runs only once)
def _ensure_nltk_data():
    for resource in ["stopwords", "wordnet", "omw-1.4"]:
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, quiet=True)

_ensure_nltk_data()

_lemmatizer = WordNetLemmatizer()
_stop_words = set(stopwords.words("english"))

ABBREVIATIONS = {
    r"\bml\b": "machine learning",
    r"\bnlp\b": "natural language processing",
    r"\bai\b": "artificial intelligence",
    r"\bjs\b": "javascript",
    r"\bts\b": "typescript",
    r"\baws\b": "amazon web services",
    r"\bgcp\b": "google cloud platform",
    r"\bapi\b": "application programming interface",
    r"\bui\b": "user interface",
    r"\bux\b": "user experience",
    r"\bcicd\b": "continuous integration continuous deployment",
    r"\bci\s*/\s*cd\b": "continuous integration continuous deployment",
    r"\bjd\b": "job description",
    r"\bhr\b": "human resources",
}

def _preprocess(text: str) -> str:
    """Lowercase, expand abbreviations, remove noise, lemmatize."""
    text = text.lower()
    
    # Expand common abbreviations
    for pattern, expansion in ABBREVIATIONS.items():
        text = re.sub(pattern, expansion, text)
        
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = text.split()
    tokens = [_lemmatizer.lemmatize(t) for t in tokens if t not in _stop_words and len(t) > 1]
    return " ".join(tokens)


def rank_resumes(
    resumes: List[Dict],   # [{"name": str, "text": str}, ...]
    job_description: str,
) -> List[Dict]:
    """
    Returns list of dicts sorted by match_score descending.
    Each dict: {"rank", "name", "match_score", "text"}
    """
    if not resumes or not job_description.strip():
        return []

    jd_clean = _preprocess(job_description)
    resume_texts = [_preprocess(r["text"]) for r in resumes]

    corpus = [jd_clean] + resume_texts
    vectorizer = TfidfVectorizer(
    ngram_range=(1, 1),
    min_df=1,
    max_df=1.0,
    sublinear_tf=False
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)

    jd_vector = tfidf_matrix[0]
    resume_matrix = tfidf_matrix[1:]

    scores = cosine_similarity(jd_vector, resume_matrix)[0]

    results = []
    for i, resume in enumerate(resumes):
        results.append({
            "name": resume["name"],
            "match_score": round(float(scores[i]) * 100, 2),
            "text": resume["text"],
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    for idx, r in enumerate(results, start=1):
        r["rank"] = idx

    return results
