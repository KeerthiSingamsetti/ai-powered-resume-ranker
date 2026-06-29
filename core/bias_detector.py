"""
bias_detector.py
────────────────
Feature 5: JD Bias Detector
Scans a job description for biased language (age, gender, culture).
"""

import re
from typing import Dict, List, Tuple


# ── Bias lexicon ───────────────────────────────────────────────────────────────
# Each entry: (pattern_str, bias_category, severity, suggestion)
BIAS_RULES: List[Tuple[str, str, str, str]] = [
    # Age bias
    (r"\bdigital\s+native\b", "Age Bias", "HIGH",
     "Use 'proficient with digital tools' instead"),
    (r"\brecent\s+graduate\b", "Age Bias", "MEDIUM",
     "Use specific degree requirements rather than recency"),
    (r"\byoung\s+and?\s+energetic\b", "Age Bias", "HIGH",
     "Remove age-related descriptors"),
    (r"\b\d+\s*[-–]\s*\d+\s*years?\s+(?:of\s+)?experience\b", "Age Bias", "HIGH",
     "Use 'minimum X years experience' without upper bound"),
    (r"\bnative\s+speaker\b", "Age/Culture Bias", "MEDIUM",
     "Use 'proficient in English (or relevant language)'"),

    # Gender bias
    (r"\bhe\s+will\b|\bhe\s+should\b|\bhis\s+role\b", "Gender Bias", "HIGH",
     "Use gender-neutral 'they/their' or 'the candidate'"),
    (r"\bshe\s+will\b|\bshe\s+should\b|\bher\s+role\b", "Gender Bias", "HIGH",
     "Use gender-neutral language"),
    (r"\bmanpower\b", "Gender Bias", "MEDIUM",
     "Use 'workforce' or 'staff'"),
    (r"\bchairman\b", "Gender Bias", "LOW",
     "Use 'chairperson' or 'chair'"),
    (r"\bsalesman\b", "Gender Bias", "MEDIUM",
     "Use 'sales representative'"),
    (r"\bforefathers\b", "Gender Bias", "LOW",
     "Use 'predecessors' or 'founders'"),
    (r"\bninja\b|\brockstar\b|\bguru\b|\bwizard\b", "Exclusionary Language", "LOW",
     "Use neutral professional terms like 'expert' or 'specialist'"),
    (r"\bdominant\b", "Aggressive Language", "LOW",
     "Consider 'leading' or 'top-performing'"),
    (r"\baggressive\b", "Aggressive Language", "MEDIUM",
     "Use 'driven', 'motivated', or 'results-oriented'"),

    # Culture / origin bias
    (r"\bculture\s+fit\b", "Culture Bias", "MEDIUM",
     "Use 'culture add' to promote diversity"),
    (r"\bamerican\s+citizen\b|\bus\s+citizen\s+only\b", "Nationality Bias", "HIGH",
     "State work authorization requirements instead of citizenship"),

    # Disability
    (r"\bmust\s+be\s+able\s+to\s+lift\b", "Disability Bias", "MEDIUM",
     "Only include if truly essential for the role"),
]

_compiled_rules = [
    (re.compile(pat, re.IGNORECASE), cat, sev, sug)
    for pat, cat, sev, sug in BIAS_RULES
]


def detect_bias(jd_text: str) -> Dict:
    """
    Returns:
        {
            "findings":     list of {phrase, category, severity, suggestion, line},
            "severity_counts": {"HIGH": n, "MEDIUM": n, "LOW": n},
            "bias_free":    bool,
            "overall_risk": "LOW" | "MEDIUM" | "HIGH",
        }
    """
    findings = []
    lines = jd_text.splitlines()

    for lineno, line in enumerate(lines, start=1):
        for pattern, category, severity, suggestion in _compiled_rules:
            for match in pattern.finditer(line):
                findings.append({
                    "phrase": match.group(0),
                    "category": category,
                    "severity": severity,
                    "suggestion": suggestion,
                    "line": lineno,
                    "context": line.strip()[:120],
                })

    # Deduplicate by (phrase_lower, category)
    seen = set()
    unique_findings = []
    for f in findings:
        key = (f["phrase"].lower(), f["category"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in unique_findings:
        counts[f["severity"]] += 1

    if counts["HIGH"] >= 2:
        risk = "HIGH"
    elif counts["HIGH"] == 1 or counts["MEDIUM"] >= 2:
        risk = "MEDIUM"
    elif unique_findings:
        risk = "LOW"
    else:
        risk = "LOW"

    return {
        "findings": unique_findings,
        "severity_counts": counts,
        "bias_free": len(unique_findings) == 0,
        "overall_risk": risk,
    }
