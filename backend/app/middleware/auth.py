from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.extensions import get_db
from app.utils.validators import to_object_id
from app.utils.responses import error


def require_auth(fn):
    """Decorator ensuring a valid JWT is present. Wraps flask_jwt_extended."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)

    return wrapper


def get_current_user():
    """Fetch the currently authenticated user document from MongoDB."""
    user_id = get_jwt_identity()
    if not user_id:
        return None
    db = get_db()
    return db.users.find_one({"_id": to_object_id(user_id)})
