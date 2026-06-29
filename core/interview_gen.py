"""
interview_gen.py
────────────────
Feature 6: AI Interview Question Generator
Uses Anthropic Claude API to generate 5 personalized interview questions.
"""

import os
from typing import List, Dict


def generate_interview_questions(
    candidate_name: str,
    resume_text: str,
    job_description: str,
    missing_skills: List[str],
    api_key: str,
) -> Dict:
    """
    Calls Claude to generate 5 personalized interview questions.
    Returns {"questions": [...], "error": None | str}
    """
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        missing_str = ", ".join(sorted(missing_skills)[:8]) if missing_skills else "None identified"

        prompt = f"""You are an expert HR interviewer. 
        
Candidate: {candidate_name}
Job Description Summary: {job_description[:800]}
Missing Skills from Resume: {missing_str}

Resume Excerpt:
{resume_text[:1200]}

Generate exactly 5 personalized interview questions for this candidate. 
- 2 questions probing their claimed experience
- 2 questions exploring the missing skills (if any)
- 1 situational/behavioral question relevant to the role

Format your output STRICTLY as:
Q1. [question]
Q2. [question]
Q3. [question]
Q4. [question]
Q5. [question]

No extra text before or after. Be specific, professional, and concise."""

        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        questions = _parse_questions(raw)

        return {"questions": questions, "error": None, "raw": raw}

    except ImportError:
        return {"questions": [], "error": "Anthropic package not installed. Run: pip install anthropic"}
    except Exception as e:
        return {"questions": [], "error": str(e), "raw": ""}


def _parse_questions(raw_text: str) -> List[str]:
    """Extract Q1–Q5 from Claude's response."""
    import re
    pattern = re.compile(r"Q\d+\.\s*(.+?)(?=Q\d+\.|$)", re.DOTALL)
    matches = pattern.findall(raw_text)
    questions = [q.strip() for q in matches if q.strip()]
    # Fallback: split by newline if pattern fails
    if not questions:
        questions = [line.strip() for line in raw_text.splitlines() if line.strip()]
    return questions[:5]
