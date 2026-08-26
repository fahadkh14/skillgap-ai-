from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.extensions import get_db
from app.utils.responses import success, error
from app.utils.validators import serialize_doc, to_object_id, is_valid_object_id

job_roles_bp = Blueprint("job_roles", __name__, url_prefix="/api/job-roles")


@job_roles_bp.route("", methods=["GET"])
@jwt_required()
def list_job_roles():
    db = get_db()
    roles = list(db.job_roles.find({}, {"name": 1, "description": 1, "skills": 1}).sort("name", 1))
    return success(serialize_doc(roles), "Job roles retrieved")


@job_roles_bp.route("/<role_id>", methods=["GET"])
@jwt_required()
def get_job_role(role_id):
    if not is_valid_object_id(role_id):
        return error("Invalid job role id", 422)

    db = get_db()
    role = db.job_roles.find_one({"_id": to_object_id(role_id)})
    if not role:
        return error("Job role not found", 404)

    return success(serialize_doc(role), "Job role retrieved")
