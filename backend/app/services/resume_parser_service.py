"""
ResumeParserService
--------------------
Extracts plain text from an uploaded PDF or DOCX resume and detects
mentions of known catalog skills using word-boundary matching against
the skills collection. No resume content is persisted to the database
or logs — only the detected skill names are returned to the caller.
"""

import io
import logging
import re

from PyPDF2 import PdfReader
from docx import Document

logger = logging.getLogger("skillgap")


class ResumeParserService:
    def __init__(self, db):
        self.db = db

    def extract_text(self, file_stream, filename):
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext == "pdf":
            return self._extract_pdf_text(file_stream)
        if ext == "docx":
            return self._extract_docx_text(file_stream)
        raise ValueError("Unsupported file type")

    def _extract_pdf_text(self, file_stream):
        try:
            reader = PdfReader(file_stream)
            text_parts = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(text_parts)
        except Exception:
            logger.exception("Failed to parse PDF resume")
            raise ValueError("Could not read the PDF file. It may be corrupted.")

    def _extract_docx_text(self, file_stream):
        try:
            buffer = io.BytesIO(file_stream.read())
            doc = Document(buffer)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            logger.exception("Failed to parse DOCX resume")
            raise ValueError("Could not read the DOCX file. It may be corrupted.")

    def detect_skills(self, text):
        """Match extracted resume text against the known skills catalog."""
        if not text:
            return []

        catalog = list(self.db.skill_catalog.find({}, {"name": 1}))
        text_lower = text.lower()
        detected = []

        for entry in catalog:
            skill_name = entry["name"]
            pattern = r"\b" + re.escape(skill_name.lower()) + r"\b"
            if re.search(pattern, text_lower):
                detected.append(skill_name)

        return sorted(set(detected))
