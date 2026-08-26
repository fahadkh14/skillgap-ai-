from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import get_db
from app.utils.responses import success, error
from app.utils.validators import serialize_doc, to_object_id, VALID_EXPERIENCE_LEVELS

profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")

ALLOWED_FIELDS = [
    "full_name", "phone", "college", "education", "graduation_year",
    "experience_level", "current_role", "target_role", "bio",
]


@profile_bp.route("", methods=["GET"])
@jwt_required()
def get_profile():
    db = get_db()
    user_id = to_object_id(get_jwt_identity())
    profile = db.profiles.find_one({"user_id": user_id})
    if not profile:
        return error("Profile not found", 404)
    return success(serialize_doc(profile), "Profile retrieved")


@profile_bp.route("", methods=["PUT"])
@jwt_required()
def update_profile():
    data = request.get_json(silent=True) or {}
    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    if "experience_level" in data and data["experience_level"] not in VALID_EXPERIENCE_LEVELS:
        return error("Invalid experience level", 422)

    update_fields = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}
    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = db.profiles.find_one_and_update(
        {"user_id": user_id},
        {"$set": update_fields},
        return_document=True,
    )

    if not result:
        return error("Profile not found", 404)

    # Keep the user's display name in sync if full_name changed
    if "full_name" in update_fields:
        db.users.update_one({"_id": user_id}, {"$set": {"name": update_fields["full_name"]}})

    return success(serialize_doc(result), "Profile updated successfully")
