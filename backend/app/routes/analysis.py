import logging

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import get_db
from app.services.skill_gap_service import SkillGapAnalysisService
from app.services.roadmap_service import RoadmapService
from app.utils.responses import success, error
from app.utils.validators import serialize_doc, to_object_id, is_valid_object_id

logger = logging.getLogger("skillgap")
analysis_bp = Blueprint("analysis", __name__, url_prefix="/api/analysis")


@analysis_bp.route("", methods=["POST"])
@jwt_required()
def run_analysis():
    data = request.get_json(silent=True) or {}
    job_role_id = data.get("job_role_id")

    if not job_role_id or not is_valid_object_id(job_role_id):
        return error("A valid job_role_id is required", 422)

    db = get_db()
    user_id = to_object_id(get_jwt_identity())
    job_role_obj_id = to_object_id(job_role_id)

    service = SkillGapAnalysisService(db)
    try:
        analysis_doc = service.analyze(user_id, job_role_obj_id)
    except ValueError as e:
        return error(str(e), 404)

    result = db.analyses.insert_one(analysis_doc)
    analysis_doc["_id"] = result.inserted_id

    roadmap_service = RoadmapService(db)
    roadmap_service.generate(user_id, analysis_doc)

    logger.info("Analysis run for user %s against role %s -> score %s",
                user_id, job_role_id, analysis_doc["readiness_score"])

    return success(serialize_doc(analysis_doc), "Analysis completed successfully", 201)


@analysis_bp.route("", methods=["GET"])
@jwt_required()
def list_analyses():
    db = get_db()
    user_id = to_object_id(get_jwt_identity())
    analyses = list(
        db.analyses.find({"user_id": user_id}).sort("created_at", -1)
    )
    return success(serialize_doc(analyses), "Analysis history retrieved")


@analysis_bp.route("/<analysis_id>", methods=["GET"])
@jwt_required()
def get_analysis(analysis_id):
    if not is_valid_object_id(analysis_id):
        return error("Invalid analysis id", 422)

    db = get_db()
    user_id = to_object_id(get_jwt_identity())
    analysis = db.analyses.find_one({"_id": to_object_id(analysis_id), "user_id": user_id})

    if not analysis:
        return error("Analysis not found", 404)

    return success(serialize_doc(analysis), "Analysis retrieved")
