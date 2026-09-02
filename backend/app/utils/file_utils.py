import os
import re
import uuid
from dataclasses import dataclass

from fastapi import HTTPException, UploadFile, status

ALLOWED_EXTENSION = ".pdf"


@dataclass
class StoredFile:
    absolute_path: str
    url_path: str


def validate_pdf_upload(upload: UploadFile, max_size_mb: int) -> None:
    filename = upload.filename or ""
    if not filename.lower().endswith(ALLOWED_EXTENSION):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Only PDF resumes are accepted")
    if upload.content_type and upload.content_type not in ("application/pdf", "application/octet-stream", ""):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Only PDF resumes are accepted")


def safe_filename(filename: str) -> str:
    base = os.path.basename(filename)
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", base).strip("._") or "resume.pdf"
    return f"{uuid.uuid4().hex[:8]}_{name}"


def build_upload_path(upload_dir: str, candidate_id: str, stored_name: str) -> StoredFile:
    relative_dir = os.path.join(upload_dir, candidate_id)
    return StoredFile(
        absolute_path=os.path.abspath(os.path.join(relative_dir, stored_name)),
        url_path=f"/{relative_dir.replace(os.sep, '/')}/{stored_name}",
    )
