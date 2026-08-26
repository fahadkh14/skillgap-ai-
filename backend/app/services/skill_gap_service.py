"""
SkillGapAnalysisService
------------------------
Compares a user's skills against a target job role's required skills and
produces a deterministic, explainable job-readiness score along with
matched / partial / missing skill breakdowns and priority ranking.

The algorithm is intentionally simple and transparent (no randomness):

    matched skill  -> 100% of its weight
    partial skill  -> 50% of its weight
    missing skill  -> 0% of its weight

    readiness_score = round(100 * sum(earned_weight) / sum(total_weight))
"""
from datetime import datetime, timezone
from app.utils.validators import PROFICIENCY_RANK


def _proficiency_rank(name):
    return PROFICIENCY_RANK.get(name, 0)


def _priority_for(required, weight, gap_ranks):
    """
    Determine Critical/High/Medium/Low priority for a missing/partial skill.

    required   -> bool, whether the skill is required for the role
    weight     -> int, importance weight assigned to the skill (1-15 typical)
    gap_ranks  -> int, proficiency levels short of the minimum requirement
                  (0 for fully missing skills is treated as max gap = 4)
    """
    score = 0
    score += 3 if required else 0
    score += min(weight, 15) / 5  # 0-3 points
    score += min(gap_ranks, 4)     # 0-4 points

    if score >= 7:
        return "Critical"
    if score >= 5:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"


class SkillGapAnalysisService:
    def __init__(self, db):
        self.db = db

    def analyze(self, user_id, job_role_id):
        """
        Run the full analysis for a user against a job role.
        Returns a dict ready to be inserted into the `analyses` collection
        (minus _id / created_at, which the caller/route can attach).
        """
        job_role = self.db.job_roles.find_one({"_id": job_role_id})
        if not job_role:
            raise ValueError("Job role not found")

        user_skills_cursor = self.db.skills.find({"user_id": user_id})
        user_skill_map = {
            s["skill_name"].strip().lower(): s for s in user_skills_cursor
        }

        matched_skills = []
        partial_skills = []
        missing_skills = []

        total_weight = 0
        earned_weight = 0

        for req in job_role.get("skills", []):
            req_name = req["name"]
            req_key = req_name.strip().lower()
            weight = req.get("weight", 5)
            required = req.get("required", True)
            min_prof = req.get("minimum_proficiency", "Beginner")
            min_rank = _proficiency_rank(min_prof)

            total_weight += weight

            user_skill = user_skill_map.get(req_key)

            if user_skill is None:
                gap_ranks = 4  # fully missing -> maximum gap
                priority = _priority_for(required, weight, gap_ranks)
                missing_skills.append({
                    "skill_name": req_name,
                    "required": required,
                    "weight": weight,
                    "minimum_proficiency": min_prof,
                    "priority": priority,
                })
                continue

            user_rank = _proficiency_rank(user_skill.get("proficiency", "Beginner"))

            if user_rank >= min_rank:
                earned_weight += weight
                matched_skills.append({
                    "skill_name": req_name,
                    "required": required,
                    "weight": weight,
                    "user_proficiency": user_skill.get("proficiency"),
                    "minimum_proficiency": min_prof,
                })
            else:
                earned_weight += weight * 0.5
                gap_ranks = max(min_rank - user_rank, 1)
                priority = _priority_for(required, weight, gap_ranks)
                partial_skills.append({
                    "skill_name": req_name,
                    "required": required,
                    "weight": weight,
                    "user_proficiency": user_skill.get("proficiency"),
                    "minimum_proficiency": min_prof,
                    "priority": priority,
                })

        if total_weight == 0:
            readiness_score = 0
        else:
            readiness_score = round(100 * earned_weight / total_weight)

        # Sort missing/partial by priority severity for convenience
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        missing_skills.sort(key=lambda s: priority_order.get(s["priority"], 9))
        partial_skills.sort(key=lambda s: priority_order.get(s["priority"], 9))

        return {
            "user_id": user_id,
            "job_role_id": job_role_id,
            "job_role_name": job_role.get("name"),
            "readiness_score": readiness_score,
            "matched_skills": matched_skills,
            "partial_skills": partial_skills,
            "missing_skills": missing_skills,
            "total_weight": total_weight,
            "earned_weight": earned_weight,
            "created_at": datetime.now(timezone.utc),
        }
