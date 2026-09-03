import logging
from pymongo import MongoClient
from flask_jwt_extended import JWTManager

logger = logging.getLogger("skillgap")

jwt = JWTManager()

_mongo_client = None
_db = None


def init_mongo(app):
    """Initialize the global MongoDB client/database using app config."""
    global _mongo_client, _db
    _mongo_client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)
    _db = _mongo_client[app.config["MONGO_DB_NAME"]]
    return _db


def get_db():
    """Return the active MongoDB database handle."""
    if _db is None:
        raise RuntimeError(
            "MongoDB has not been initialized yet. Call init_mongo(app) first."
        )
    return _db


def get_client():
    if _mongo_client is None:
        raise RuntimeError("MongoDB client has not been initialized yet.")
    return _mongo_client
