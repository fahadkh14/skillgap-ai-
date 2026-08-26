from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import get_db
from app.utils.responses import success
from app.utils.validators import serialize_doc, to_object_id

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("", methods=["GET"])
@jwt_required()
def get_dashboard():
    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    latest_analysis = db.analyses.find_one({"user_id": user_id}, sort=[("created_at", -1)])
    total_skills = db.skills.count_documents({"user_id": user_id})

    matched_count = len(latest_analysis.get("matched_skills", [])) if latest_analysis else 0
    partial_count = len(latest_analysis.get("partial_skills", [])) if latest_analysis else 0
    missing_count = len(latest_analysis.get("missing_skills", [])) if latest_analysis else 0
    readiness_score = latest_analysis.get("readiness_score", 0) if latest_analysis else 0

    roadmap = None
    if latest_analysis:
        roadmap = db.roadmaps.find_one({
            "user_id": user_id,
            "job_role_id": latest_analysis["job_role_id"],
        })
    learning_progress = roadmap.get("overall_progress", 0) if roadmap else 0

    top_gaps = []
    if latest_analysis:
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        combined = list(latest_analysis.get("missing_skills", [])) + list(latest_analysis.get("partial_skills", []))
        combined.sort(key=lambda s: priority_order.get(s.get("priority", "Low"), 9))
        top_gaps = combined[:5]

    recent_analyses = list(
        db.analyses.find(
            {"user_id": user_id},
            {"job_role_name": 1, "readiness_score": 1, "created_at": 1},
        ).sort("created_at", -1).limit(5)
    )

    data = {
        "job_readiness": readiness_score,
        "total_skills": total_skills,
        "matched_skills": matched_count,
        "partial_skills": partial_count,
        "missing_skills": missing_count,
        "learning_progress": learning_progress,
        "top_skill_gaps": serialize_doc(top_gaps),
        "recent_analyses": serialize_doc(recent_analyses),
        "current_target_role": latest_analysis.get("job_role_name") if latest_analysis else None,
    }

    return success(data, "Dashboard data retrieved")
