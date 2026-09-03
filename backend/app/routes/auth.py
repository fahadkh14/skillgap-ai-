import logging
from datetime import datetime, timezone

import bcrypt
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from pymongo.errors import DuplicateKeyError

from app.extensions import get_db
from app.middleware.auth import get_current_user
from app.utils.responses import success, error
from app.utils.validators import is_valid_email, is_valid_password, serialize_doc

logger = logging.getLogger("skillgap")
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Simple in-memory blocklist for logged-out tokens (per-process).
# Suitable for a single-instance demo deployment.
_token_blocklist = set()


@auth_bp.record_once
def _setup(state):
    pass


def is_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in _token_blocklist


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    full_name = (data.get("full_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    confirm_password = data.get("confirm_password") or ""

    if not full_name:
        return error("Full name is required", 422)
    if not is_valid_email(email):
        return error("A valid email is required", 422)
    if not is_valid_password(password):
        return error("Password must be at least 8 characters long", 422)
    if password != confirm_password:
        return error("Passwords do not match", 422)

    db = get_db()

    if db.users.find_one({"email": email}):
        return error("An account with this email already exists", 409)

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    now = datetime.now(timezone.utc)

    user_doc = {
        "name": full_name,
        "email": email,
        "password_hash": password_hash,
        "created_at": now,
        "updated_at": now,
    }

    try:
        result = db.users.insert_one(user_doc)
    except DuplicateKeyError:
        return error("An account with this email already exists", 409)

    user_id = str(result.inserted_id)

    # Create an empty profile shell for the new user
    db.profiles.insert_one(
        {
            "user_id": result.inserted_id,
            "full_name": full_name,
            "email": email,
            "phone": "",
            "college": "",
            "education": "",
            "graduation_year": None,
            "experience_level": "Student",
            "current_role": "",
            "target_role": "",
            "bio": "",
            "created_at": now,
            "updated_at": now,
        }
    )

    logger.info("New user registered: %s", user_id)

    access_token = create_access_token(identity=user_id)
    return success(
        {
            "access_token": access_token,
            "user": {"id": user_id, "name": full_name, "email": email},
        },
        "Account created successfully",
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return error("Email and password are required", 422)

    db = get_db()
    user = db.users.find_one({"email": email})

    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user["password_hash"].encode("utf-8")
    ):
        logger.info("Failed login attempt for email: %s", email)
        return error("Invalid email or password", 401)

    user_id = str(user["_id"])
    access_token = create_access_token(identity=user_id)

    logger.info("User logged in: %s", user_id)

    return success(
        {
            "access_token": access_token,
            "user": {
                "id": user_id,
                "name": user.get("name"),
                "email": user.get("email"),
            },
        },
        "Login successful",
    )


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    _token_blocklist.add(jti)
    logger.info("User logged out: %s", get_jwt_identity())
    return success(message="Logged out successfully")


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = get_current_user()
    if not user:
        return error("User not found", 404)
    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    return success(serialize_doc(safe_user), "Current user retrieved")
