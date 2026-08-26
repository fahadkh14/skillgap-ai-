"""
Shared pytest fixtures for the SkillGap AI backend test suite.

Tests use mongomock to fully isolate database state per test run without
requiring a live MongoDB instance. If mongomock is unavailable, install it
with: pip install mongomock
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("FLASK_ENV", "testing")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/skillgap_test")
os.environ.setdefault("MONGO_DB_NAME", "skillgap_test")


@pytest.fixture()
def app():
    import mongomock
    from app import create_app
    from app.config import Config
    import app.extensions as extensions_module

    class TestConfig(Config):
        TESTING = True
        DEBUG = True

    flask_app = create_app(TestConfig)

    # Swap the real MongoClient for an in-memory mongomock client
    mock_client = mongomock.MongoClient()
    extensions_module._mongo_client = mock_client
    extensions_module._db = mock_client[TestConfig.MONGO_DB_NAME]

    # Seed minimal job role + skill catalog data needed by tests
    db = extensions_module._db
    db.job_roles.insert_one({
        "name": "DevOps Engineer",
        "description": "Test role",
        "skills": [
            {"name": "Linux", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "Docker", "required": True, "weight": 10, "minimum_proficiency": "Intermediate"},
            {"name": "Kubernetes", "required": True, "weight": 15, "minimum_proficiency": "Intermediate"},
        ],
    })

    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def registered_user(client):
    resp = client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123",
        "confirm_password": "TestPass123",
    })
    data = resp.get_json()
    token = data["data"]["access_token"]
    return {"token": token, "user_id": data["data"]["user"]["id"]}


@pytest.fixture()
def auth_headers(registered_user):
    return {"Authorization": f"Bearer {registered_user['token']}"}
