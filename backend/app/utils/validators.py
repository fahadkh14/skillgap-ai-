import re
from bson import ObjectId
from bson.errors import InvalidId

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

VALID_PROFICIENCIES = ["Beginner", "Intermediate", "Advanced", "Expert"]
PROFICIENCY_RANK = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
VALID_EXPERIENCE_LEVELS = ["Student", "Fresher", "Junior", "Mid-Level", "Senior"]
VALID_ROADMAP_STATUSES = ["Not Started", "In Progress", "Completed"]


def is_valid_email(email):
    return bool(email) and bool(EMAIL_REGEX.match(email))


def is_valid_password(password):
    return bool(password) and len(password) >= 8


def is_valid_object_id(value):
    try:
        ObjectId(str(value))
        return True
    except (InvalidId, TypeError):
        return False


def to_object_id(value):
    return ObjectId(str(value))


def serialize_doc(doc):
    """Recursively convert ObjectId / datetime fields into JSON-safe values."""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if key == "_id":
                result["id"] = str(value)
            elif isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = serialize_doc(value)
            elif isinstance(value, list):
                result[key] = serialize_doc(value)
            elif hasattr(value, "isoformat"):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
    return doc
