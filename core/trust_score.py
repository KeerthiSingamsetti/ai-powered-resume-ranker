"""
trust_score.py
──────────────
Feature 3: Trust Score — Auth + Red Flag Detector
Detects fake experience claims, job gaps, job hopping.
Score: 0 – 100 (higher = more trustworthy)
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple

from dateutil import parser as date_parser


# ── Patterns ───────────────────────────────────────────────────────────────────

# e.g., "Jan 2020 – Mar 2022", "2019 - 2021", "2020–Present"
DATE_RANGE_PATTERN = re.compile(
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{4}|\d{4})"
    r"\s*[-–—to]+\s*"
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{4}|\d{4}|Present|present|Current|current|Now|now)",
    re.IGNORECASE,
)

GRADUATION_PATTERN = re.compile(
    r"(?:graduated?|batch|class\s+of|degree\s+in|b\.?tech|m\.?tech|b\.?e|m\.?e|"
    r"b\.?sc|m\.?sc|mba|phd|bachelor|master)[^\n]{0,40}(\d{4})",
    re.IGNORECASE,
)

EXPERIENCE_CLAIM_PATTERN = re.compile(
    r"(\d+)\s*\+?\s*years?\s+(?:of\s+)?(?:experience|exp)",
    re.IGNORECASE,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _parse_year_month(raw: str) -> datetime:
    """Convert a raw date string to a datetime object."""
    raw = raw.strip()
    if raw.lower() in {"present", "current", "now"}:
        return datetime.now()
    try:
        return date_parser.parse(raw, default=datetime(datetime.now().year, 1, 1))
    except Exception:
        try:
            return datetime(int(raw), 6, 1)  # mid-year if only year given
        except Exception:
            return None


def _extract_date_ranges(text: str) -> List[Tuple[datetime, datetime]]:
    """Return list of (start, end) datetime pairs from text."""
    ranges = []
    for match in DATE_RANGE_PATTERN.finditer(text):
        start = _parse_year_month(match.group(1))
        end = _parse_year_month(match.group(2))
        if start and end and start <= end:
            ranges.append((start, end))
    ranges.sort(key=lambda x: x[0])
    return ranges


def _graduation_year(text: str):
    """Extract the most likely graduation year."""
    matches = GRADUATION_PATTERN.findall(text)
    if matches:
        years = [int(y) for y in matches if y.isdigit()]
        if years:
            return min(years)
    return None


def _claimed_experience_years(text: str):
    """Extract claimed years of experience from text."""
    matches = EXPERIENCE_CLAIM_PATTERN.findall(text)
    if matches:
        return max(int(y) for y in matches)
    return None


def _detect_job_gaps(ranges: List[Tuple[datetime, datetime]]) -> List[float]:
    """Return list of gaps (in months) between consecutive jobs."""
    gaps = []
    for i in range(1, len(ranges)):
        gap_days = (ranges[i][0] - ranges[i - 1][1]).days
        if gap_days > 90:  # > 3 months = gap
            gaps.append(round(gap_days / 30.44, 1))
    return gaps


def _detect_job_hopping(ranges: List[Tuple[datetime, datetime]]) -> int:
    """Return count of jobs held for < 12 months."""
    short = 0
    for start, end in ranges:
        months = (end - start).days / 30.44
        if months < 12:
            short += 1
    return short


# ── Main scorer ────────────────────────────────────────────────────────────────

def compute_trust_score(resume_text: str) -> Dict:
    """
    Analyse resume text and return a trust analysis dict:
    {
        "score":          int 0-100,
        "red_flags":      list of str,
        "positives":      list of str,
        "graduation_year": int | None,
        "claimed_exp":    int | None,
        "actual_exp_years": float,
        "job_gaps":       list of float (months),
        "short_tenures":  int,
    }
    """
    red_flags: List[str] = []
    positives: List[str] = []
    score = 100  # start perfect, deduct for issues

    date_ranges = _extract_date_ranges(resume_text)
    grad_year = _graduation_year(resume_text)
    claimed_exp = _claimed_experience_years(resume_text)

    # ── Actual experience ──────────────────────────────────────────────────────
    if date_ranges:
        earliest = date_ranges[0][0]
        latest = max(e for _, e in date_ranges)
        actual_exp_years = round((latest - earliest).days / 365.25, 1)
    else:
        actual_exp_years = 0.0

    # ── Fake experience check ──────────────────────────────────────────────────
    if claimed_exp and grad_year:
        current_year = datetime.now().year
        max_possible_exp = current_year - grad_year
        if claimed_exp > max_possible_exp + 1:
            red_flags.append(
                f"⚠️ Claims {claimed_exp} yrs experience but graduated in "
                f"{grad_year} (max possible ≈ {max_possible_exp} yrs)"
            )
            score -= 30
    elif claimed_exp and actual_exp_years > 0:
        if claimed_exp > actual_exp_years + 2:
            red_flags.append(
                f"⚠️ Claims {claimed_exp} yrs but date ranges show only "
                f"≈{actual_exp_years} yrs"
            )
            score -= 20

    # ── Job gaps ───────────────────────────────────────────────────────────────
    job_gaps = _detect_job_gaps(date_ranges)
    for gap in job_gaps:
        if gap >= 6:
            red_flags.append(f"📅 Unexplained job gap of ≈{gap:.0f} months")
            score -= 10
        elif gap >= 3:
            red_flags.append(f"📅 Short gap of ≈{gap:.0f} months")
            score -= 5

    # ── Job hopping ────────────────────────────────────────────────────────────
    short_tenures = _detect_job_hopping(date_ranges)
    if short_tenures >= 3:
        red_flags.append(f"🔁 Job hopping: {short_tenures} roles lasted < 12 months")
        score -= 15
    elif short_tenures == 2:
        red_flags.append(f"🔁 {short_tenures} roles lasted < 12 months")
        score -= 7

    # ── Positives ──────────────────────────────────────────────────────────────
    if not red_flags:
        positives.append("✅ No experience inconsistencies detected")
    if not job_gaps:
        positives.append("✅ Continuous employment history")
    if short_tenures == 0 and date_ranges:
        positives.append("✅ Stable job tenure across roles")

    score = max(0, min(100, score))

    return {
        "score": score,
        "red_flags": red_flags,
        "positives": positives,
        "graduation_year": grad_year,
        "claimed_exp": claimed_exp,
        "actual_exp_years": actual_exp_years,
        "job_gaps": job_gaps,
        "short_tenures": short_tenures,
    }
