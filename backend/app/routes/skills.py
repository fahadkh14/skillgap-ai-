from datetime import datetime, timezone

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import get_db
from app.utils.responses import success, error
from app.utils.validators import (
    serialize_doc, to_object_id, is_valid_object_id, VALID_PROFICIENCIES,
)

skills_bp = Blueprint("skills", __name__, url_prefix="/api/skills")


@skills_bp.route("", methods=["GET"])
@jwt_required()
def list_skills():
    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    search = request.args.get("search", "").strip()
    proficiency_filter = request.args.get("proficiency", "").strip()

    query = {"user_id": user_id}
    if search:
        query["skill_name"] = {"$regex": search, "$options": "i"}
    if proficiency_filter and proficiency_filter in VALID_PROFICIENCIES:
        query["proficiency"] = proficiency_filter

    skills = list(db.skills.find(query).sort("skill_name", 1))
    return success(serialize_doc(skills), "Skills retrieved")


@skills_bp.route("", methods=["POST"])
@jwt_required()
def add_skill():
    data = request.get_json(silent=True) or {}
    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    skill_name = (data.get("skill_name") or "").strip()
    proficiency = data.get("proficiency", "Beginner")
    years = data.get("years_of_experience", 0)

    if not skill_name:
        return error("Skill name is required", 422)
    if proficiency not in VALID_PROFICIENCIES:
        return error("Invalid proficiency level", 422)
    try:
        years = float(years)
        if years < 0:
            raise ValueError
    except (TypeError, ValueError):
        return error("Years of experience must be a non-negative number", 422)

    existing = db.skills.find_one({
        "user_id": user_id,
        "skill_name": {"$regex": f"^{skill_name}$", "$options": "i"},
    })
    if existing:
        return error("You already have this skill in your profile", 409)

    now = datetime.now(timezone.utc)
    doc = {
        "user_id": user_id,
        "skill_name": skill_name,
        "proficiency": proficiency,
        "years_of_experience": years,
        "created_at": now,
        "updated_at": now,
    }
    result = db.skills.insert_one(doc)
    doc["_id"] = result.inserted_id

    return success(serialize_doc(doc), "Skill added successfully", 201)


@skills_bp.route("/<skill_id>", methods=["PUT"])
@jwt_required()
def update_skill(skill_id):
    if not is_valid_object_id(skill_id):
        return error("Invalid skill id", 422)

    data = request.get_json(silent=True) or {}
    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    update_fields = {}
    if "proficiency" in data:
        if data["proficiency"] not in VALID_PROFICIENCIES:
            return error("Invalid proficiency level", 422)
        update_fields["proficiency"] = data["proficiency"]
    if "years_of_experience" in data:
        try:
            years = float(data["years_of_experience"])
            if years < 0:
                raise ValueError
            update_fields["years_of_experience"] = years
        except (TypeError, ValueError):
            return error("Years of experience must be a non-negative number", 422)
    if "skill_name" in data and data["skill_name"].strip():
        update_fields["skill_name"] = data["skill_name"].strip()

    if not update_fields:
        return error("No valid fields provided to update", 422)

    update_fields["updated_at"] = datetime.now(timezone.utc)

    result = db.skills.find_one_and_update(
        {"_id": to_object_id(skill_id), "user_id": user_id},
        {"$set": update_fields},
        return_document=True,
    )

    if not result:
        return error("Skill not found", 404)

    return success(serialize_doc(result), "Skill updated successfully")


@skills_bp.route("/<skill_id>", methods=["DELETE"])
@jwt_required()
def delete_skill(skill_id):
    if not is_valid_object_id(skill_id):
        return error("Invalid skill id", 422)

    db = get_db()
    user_id = to_object_id(get_jwt_identity())

    result = db.skills.delete_one({"_id": to_object_id(skill_id), "user_id": user_id})
    if result.deleted_count == 0:
        return error("Skill not found", 404)

    return success(message="Skill deleted successfully")
