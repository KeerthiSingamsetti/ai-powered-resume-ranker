"""
radar_chart.py
──────────────
Feature 4: Radar Chart Comparison
Plotly spider chart comparing top 3 candidates across 6 dimensions.
"""

import re
from typing import List, Dict, Optional

import plotly.graph_objects as go

from core.skill_gap import extract_skills, SKILL_VOCAB
from core.trust_score import compute_trust_score


# ── The 6 radar dimensions ─────────────────────────────────────────────────────
DIMENSIONS = [
    "Technical Skills",
    "Experience Depth",
    "Trust Score",
    "Skill Match %",
    "Certifications",
    "Soft Skills",
]

SOFT_SKILLS = {
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "project management", "agile", "scrum",
}

CERT_KEYWORDS = re.compile(
    r"\b(certified|certification|certificate|aws\s+certified|pmp|cpa|"
    r"cissp|ceh|google\s+cert|microsoft\s+cert|coursera|udemy|linkedin\s+learning)\b",
    re.IGNORECASE,
)

TECH_SKILLS = SKILL_VOCAB - SOFT_SKILLS


def _score_technical(text: str) -> float:
    skills = extract_skills(text) - SOFT_SKILLS
    return min(100.0, len(skills) * 6.0)


def _score_experience(text: str) -> float:
    """Rough proxy: years of experience mentioned."""
    matches = re.findall(r"(\d+)\s*\+?\s*years?", text, re.IGNORECASE)
    if matches:
        return min(100.0, max(int(y) for y in matches) * 10.0)
    return 30.0  # baseline


def _score_certifications(text: str) -> float:
    certs = CERT_KEYWORDS.findall(text)
    return min(100.0, len(certs) * 20.0)


def _score_soft_skills(text: str) -> float:
    soft = extract_skills(text) & SOFT_SKILLS
    return min(100.0, len(soft) * 15.0)


def build_candidate_dimensions(
    resume: Dict,          # {"name": str, "text": str, "match_score": float}
    trust_result: Dict,
) -> Dict:
    text = resume["text"]
    return {
        "name": resume["name"],
        "scores": [
            _score_technical(text),
            _score_experience(text),
            float(trust_result["score"]),
            float(resume.get("match_score", 0)),
            _score_certifications(text),
            _score_soft_skills(text),
        ],
    }


def create_radar_chart(candidates_data: List[Dict]) -> go.Figure:
    """
    candidates_data: list of {"name": str, "scores": [6 floats]}
    Returns a Plotly Figure (radar/spider chart).
    """
    dims = DIMENSIONS + [DIMENSIONS[0]]  # close the polygon

    COLORS = [
        "rgba(99, 102, 241, 0.85)",    # violet
        "rgba(236, 72, 153, 0.85)",    # pink
        "rgba(16, 185, 129, 0.85)",    # emerald
    ]

    fig = go.Figure()

    for i, candidate in enumerate(candidates_data[:3]):
        scores = candidate["scores"] + [candidate["scores"][0]]
        color = COLORS[i % len(COLORS)]
        fill_color = color.replace("0.85", "0.15")

        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=dims,
            fill="toself",
            fillcolor=fill_color,
            line=dict(color=color, width=2.5),
            name=candidate["name"],
            hovertemplate="%{theta}: <b>%{r:.1f}</b><extra>" + candidate["name"] + "</extra>",
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(15, 15, 30, 0.9)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#94a3b8", size=10),
                gridcolor="rgba(148, 163, 184, 0.2)",
                linecolor="rgba(148, 163, 184, 0.2)",
            ),
            angularaxis=dict(
                tickfont=dict(color="#e2e8f0", size=12),
                gridcolor="rgba(148, 163, 184, 0.15)",
                linecolor="rgba(148, 163, 184, 0.2)",
            ),
        ),
        paper_bgcolor="rgba(10, 10, 25, 0)",
        plot_bgcolor="rgba(10, 10, 25, 0)",
        legend=dict(
            font=dict(color="#e2e8f0", size=12),
            bgcolor="rgba(30, 30, 60, 0.8)",
            bordercolor="rgba(99, 102, 241, 0.4)",
            borderwidth=1,
        ),
        margin=dict(t=40, b=40, l=60, r=60),
        height=480,
    )

    return fig
