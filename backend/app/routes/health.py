from flask import Blueprint
from pymongo.errors import PyMongoError

from app.extensions import get_db

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health", methods=["GET"])
def health_check():
    db_status = "disconnected"
    status_code = 503
    try:
        db = get_db()
        db.command("ping")
        db_status = "connected"
        status_code = 200
    except PyMongoError:
        db_status = "disconnected"
    except RuntimeError:
        db_status = "disconnected"

    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
    }, status_code
