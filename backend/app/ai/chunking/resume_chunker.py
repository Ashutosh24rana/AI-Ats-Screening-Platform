import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

SECTION_HINTS = {
    "experience": ["work experience", "professional experience", "employment", "work history", "experience", "career"],
    "education": ["education", "academic", "degree", "university", "college"],
    "skills": ["technical skills", "skills", "technologies", "competencies"],
    "projects": ["projects", "portfolio", "open source"],
    "summary": ["summary", "objective", "profile", "about"],
}


def _build_heading_pattern(hints: list[str]) -> re.Pattern:
    # longest hint first so "work experience" wins over "experience"
    ordered = sorted(hints, key=len, reverse=True)
    escaped = [re.escape(h) for h in ordered]
    # heading must be the whole line (allow trailing colon)
    pattern = r"^\s*(?:" + "|".join(escaped) + r")\s*:?\s*$"
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE)


_SECTION_PATTERNS: dict[str, re.Pattern] = {
    section: _build_heading_pattern(hints) for section, hints in SECTION_HINTS.items()
}


def _find_section_boundaries(text: str) -> list[tuple[str, int, int]]:
    """Return sorted list of (section, heading_start, heading_end) for every heading line found."""
    hits: list[tuple[str, int, int]] = []
    for section, pattern in _SECTION_PATTERNS.items():
        for m in pattern.finditer(text):
            hits.append((section, m.start(), m.end()))
    # prefer longer heading when two hints start at same offset (e.g. "work experience" vs "experience")
    hits.sort(key=lambda x: (x[1], -(x[2] - x[1])))
    deduped: list[tuple[str, int, int]] = []
    seen_starts: set[int] = set()
    for section, s, e in hits:
        if s not in seen_starts:
            deduped.append((section, s, e))
            seen_starts.add(s)
    deduped.sort(key=lambda x: x[1])
    return deduped


class ResumeChunker:
    """Detect sections → split each section → tag chunks with section metadata."""

    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 120):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def split(self, text: str, metadata: dict | None = None) -> list[Document]:
        base_metadata = dict(metadata or {})
        boundaries = _find_section_boundaries(text)

        # No headings found → fallback to old blind splitter (single "other" section)
        if not boundaries:
            chunks = self.splitter.create_documents([text])
            return [Document(page_content=c.page_content, metadata={**base_metadata, "section": "other", "chunk_index": i}) for i, c in enumerate(chunks)]

        documents: list[Document] = []
        chunk_index = 0

        # Content before first heading → treat as summary/header
        first_start = boundaries[0][1]
        preface = text[:first_start].strip()
        if preface:
            for c in self.splitter.create_documents([preface]):
                documents.append(Document(page_content=c.page_content, metadata={**base_metadata, "section": "summary", "chunk_index": chunk_index}))
                chunk_index += 1

        # Each heading's content = from heading_end to next heading_start
        for idx, (section, _, heading_end) in enumerate(boundaries):
            next_start = boundaries[idx + 1][1] if idx + 1 < len(boundaries) else len(text)
            section_text = text[heading_end:next_start].strip()
            if not section_text:
                continue
            for c in self.splitter.create_documents([section_text]):
                documents.append(Document(page_content=c.page_content, metadata={**base_metadata, "section": section, "chunk_index": chunk_index}))
                chunk_index += 1

        # Edge: headings found but all sections empty (e.g. only headings) → fallback
        if not documents:
            chunks = self.splitter.create_documents([text])
            return [Document(page_content=c.page_content, metadata={**base_metadata, "section": "other", "chunk_index": i}) for i, c in enumerate(chunks)]

        return documents
