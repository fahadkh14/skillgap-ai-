"""
RoadmapService
--------------
Builds a personalized, phased learning roadmap from the results of a
skill-gap analysis. Existing roadmap item progress is preserved across
re-generation so users don't lose their tracked progress.
"""
from datetime import datetime, timezone

DURATION_BY_PRIORITY = {
    "Critical": "3-4 weeks",
    "High": "2-3 weeks",
    "Medium": "1-2 weeks",
    "Low": "1 week",
}

DESCRIPTION_TEMPLATES = {
    "Critical": "This is a core requirement for the role — prioritize mastering it first.",
    "High": "An important skill that significantly impacts your readiness score.",
    "Medium": "A valuable skill to strengthen your overall profile.",
    "Low": "A nice-to-have that can be picked up once higher-priority gaps are closed.",
}

PRIORITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}


class RoadmapService:
    def __init__(self, db):
        self.db = db

    def generate(self, user_id, analysis):
        """
        Build (or refresh) the roadmap for a user based on the latest
        analysis document. Matched skills are marked Completed. Missing
        and partial skills become roadmap phases ordered by priority.
        """
        existing = self.db.roadmaps.find_one({
            "user_id": user_id,
            "job_role_id": analysis["job_role_id"],
        })
        existing_progress = {}
        if existing:
            for item in existing.get("items", []):
                existing_progress[item["skill"]] = {
                    "status": item.get("status", "Not Started"),
                    "progress": item.get("progress", 0),
                }

        items = []

        for matched in analysis.get("matched_skills", []):
            items.append({
                "skill": matched["skill_name"],
                "description": "You already meet the required proficiency for this skill.",
                "priority": "Completed",
                "estimated_duration": "-",
                "prerequisites": [],
                "status": "Completed",
                "progress": 100,
            })

        gap_skills = list(analysis.get("partial_skills", [])) + list(analysis.get("missing_skills", []))
        gap_skills.sort(key=lambda s: PRIORITY_ORDER.get(s.get("priority", "Low"), 9))

        for idx, gap in enumerate(gap_skills):
            name = gap["skill_name"]
            priority = gap.get("priority", "Medium")
            prev_state = existing_progress.get(name, {"status": "Not Started", "progress": 0})
            prerequisites = [gap_skills[idx - 1]["skill_name"]] if idx > 0 and priority == "Critical" else []
            items.append({
                "skill": name,
                "description": DESCRIPTION_TEMPLATES.get(priority, DESCRIPTION_TEMPLATES["Medium"]),
                "priority": priority,
                "estimated_duration": DURATION_BY_PRIORITY.get(priority, "1-2 weeks"),
                "prerequisites": prerequisites,
                "status": prev_state["status"],
                "progress": prev_state["progress"],
            })

        overall_progress = 0
        if items:
            overall_progress = round(sum(i["progress"] for i in items) / len(items))

        roadmap_doc = {
            "user_id": user_id,
            "job_role_id": analysis["job_role_id"],
            "job_role_name": analysis.get("job_role_name"),
            "items": items,
            "overall_progress": overall_progress,
            "updated_at": datetime.now(timezone.utc),
        }

        if existing:
            self.db.roadmaps.update_one({"_id": existing["_id"]}, {"$set": roadmap_doc})
            roadmap_doc["_id"] = existing["_id"]
        else:
            roadmap_doc["created_at"] = datetime.now(timezone.utc)
            result = self.db.roadmaps.insert_one(roadmap_doc)
            roadmap_doc["_id"] = result.inserted_id

        return roadmap_doc

    @staticmethod
    def recompute_overall_progress(items):
        if not items:
            return 0
        return round(sum(i.get("progress", 0) for i in items) / len(items))
