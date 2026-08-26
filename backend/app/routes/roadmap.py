from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import get_db
from app.services.roadmap_service import RoadmapService
from app.utils.responses import success, error
from app.utils.validators import serialize_doc, to_object_id, is_valid_object_id, VALID_ROADMAP_STATUSES

roadmap_bp = Blueprint("roadmap", __name__, url_prefix="/api/roadmap")


@roadmap_bp.route("", methods=["GET"])
@jwt_required()
def get_roadmap():
    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    job_role_id = request.args.get("job_role_id")
    query = {"user_id": user_id}
    if job_role_id and is_valid_object_id(job_role_id):
        query["job_role_id"] = to_object_id(job_role_id)

    roadmap = db.roadmaps.find_one(query, sort=[("updated_at", -1)])
    if not roadmap:
        return success(None, "No roadmap has been generated yet")

    return success(serialize_doc(roadmap), "Roadmap retrieved")


@roadmap_bp.route("/<roadmap_id>", methods=["PUT"])
@jwt_required()
def update_roadmap_item(roadmap_id):
    """Update the status/progress of a single skill item within a roadmap."""
    if not is_valid_object_id(roadmap_id):
        return error("Invalid roadmap id", 422)

    data = request.get_json(silent=True) or {}
    skill_name = data.get("skill")
    status = data.get("status")
    progress = data.get("progress")

    if not skill_name:
        return error("skill is required", 422)
    if status is not None and status not in VALID_ROADMAP_STATUSES:
        return error("Invalid status value", 422)
    if progress is not None:
        try:
            progress = int(progress)
            if progress not in (0, 25, 50, 75, 100):
                raise ValueError
        except (TypeError, ValueError):
            return error("Progress must be one of 0, 25, 50, 75, 100", 422)

    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    roadmap = db.roadmaps.find_one({"_id": to_object_id(roadmap_id), "user_id": user_id})
    if not roadmap:
        return error("Roadmap not found", 404)

    items = roadmap.get("items", [])
    updated = False
    for item in items:
        if item["skill"] == skill_name:
            if status is not None:
                item["status"] = status
            if progress is not None:
                item["progress"] = progress
                if progress == 100:
                    item["status"] = "Completed"
                elif progress > 0 and item.get("status") == "Not Started":
                    item["status"] = "In Progress"
            updated = True
            break

    if not updated:
        return error("Skill not found in roadmap", 404)

    overall_progress = RoadmapService.recompute_overall_progress(items)

    db.roadmaps.update_one(
        {"_id": roadmap["_id"]},
        {"$set": {
            "items": items,
            "overall_progress": overall_progress,
            "updated_at": datetime.now(timezone.utc),
        }},
    )

    updated_roadmap = db.roadmaps.find_one({"_id": roadmap["_id"]})
    return success(serialize_doc(updated_roadmap), "Roadmap progress updated")
