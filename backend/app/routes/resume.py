import logging
import os
import uuid
from datetime import datetime, timezone

from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app.extensions import get_db
from app.services.resume_parser_service import ResumeParserService
from app.utils.responses import success, error
from app.utils.validators import to_object_id

logger = logging.getLogger("skillgap")
resume_bp = Blueprint("resume", __name__, url_prefix="/api/resume")

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def _allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_RESUME_EXTENSIONS"]


@resume_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_resume():
    if "file" not in request.files:
        return error("No file provided", 422)

    file = request.files["file"]

    if not file or file.filename == "":
        return error("No file selected", 422)

    filename = secure_filename(file.filename)

    if not filename or not _allowed_file(filename):
        return error("Only PDF and DOCX files are allowed", 422)

    if file.mimetype not in ALLOWED_MIME_TYPES:
        return error("Invalid file type detected", 422)

    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    try:
        parser = ResumeParserService(db)
        text = parser.extract_text(file.stream, filename)
        detected_skills = parser.detect_skills(text)
    except ValueError as e:
        return error(str(e), 422)
    except Exception:
        logger.exception("Unexpected error parsing resume for user %s", user_id)
        return error("Failed to process the uploaded resume", 500)

    # Persist only metadata + detected skills — never raw resume content or logs of it
    now = datetime.now(timezone.utc)
    resume_record = {
        "user_id": user_id,
        "original_filename": filename,
        "detected_skills": detected_skills,
        "uploaded_at": now,
    }
    db.resumes.insert_one(resume_record)

    logger.info("Resume uploaded and parsed for user %s (%d skills detected)",
                user_id, len(detected_skills))

    return success(
        {"detected_skills": detected_skills, "filename": filename},
        "Resume processed successfully",
    )
