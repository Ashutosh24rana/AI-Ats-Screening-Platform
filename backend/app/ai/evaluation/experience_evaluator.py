import re

YEAR_PATTERNS = [
    re.compile(r"(\d{1,2})\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:professional\s+)?experience", re.IGNORECASE),
    re.compile(r"experience\s*[:\-]?\s*(\d{1,2})\+?\s*(?:years?|yrs?)", re.IGNORECASE),
    re.compile(r"over\s+(\d{1,2})\s+(?:years?|yrs?)", re.IGNORECASE),
]

DATE_RANGE_PATTERN = re.compile(r"(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|19\d{2}|present|current)", re.IGNORECASE)


class ExperienceEvaluator:
    """Estimates years of experience from resume text using regex heuristics."""

    def __init__(self, resume_text: str, current_year: int = 2026):
        self.text = resume_text
        self.current_year = current_year

    def estimate_years(self) -> int | None:
        for pattern in YEAR_PATTERNS:
            match = pattern.search(self.text)
            if match:
                return int(match.group(1))

        ranges = DATE_RANGE_PATTERN.findall(self.text)
        if not ranges:
            return None
        total_months = 0
        for start_str, end_str in ranges:
            try:
                start = int(start_str)
                end = self.current_year if end_str.lower() in ("present", "current") else int(end_str)
                if 1980 <= start <= self.current_year and start <= end <= self.current_year + 1:
                    total_months += (end - start) * 12
            except ValueError:
                continue
        # Overlapping jobs are common; cap the estimate at the span of earliest to latest.
        if total_months == 0:
            return None
        years = round(total_months / 12)
        # Deduplicate overlapping employment by capping at calendar span
        all_years = [int(s) for s, _ in ranges]
        earliest, latest = min(all_years), max(
            self.current_year if e.lower() in ("present", "current") else int(e) for _, e in ranges
        )
        span_years = max(years, latest - earliest)
        return min(span_years, 45)
