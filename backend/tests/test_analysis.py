def _get_devops_role_id(client, auth_headers):
    resp = client.get("/api/job-roles", headers=auth_headers)
    roles = resp.get_json()["data"]
    role = next(r for r in roles if r["name"] == "DevOps Engineer")
    return role["id"]


def test_analysis_calculation(client, auth_headers):
    # User has Linux (meets) and Docker at Beginner (below required Intermediate)
    client.post(
        "/api/skills",
        json={
            "skill_name": "Linux",
            "proficiency": "Intermediate",
            "years_of_experience": 1,
        },
        headers=auth_headers,
    )
    client.post(
        "/api/skills",
        json={
            "skill_name": "Docker",
            "proficiency": "Beginner",
            "years_of_experience": 0.5,
        },
        headers=auth_headers,
    )

    role_id = _get_devops_role_id(client, auth_headers)
    resp = client.post(
        "/api/analysis", json={"job_role_id": role_id}, headers=auth_headers
    )
    assert resp.status_code == 201
    data = resp.get_json()["data"]

    matched_names = [s["skill_name"] for s in data["matched_skills"]]
    partial_names = [s["skill_name"] for s in data["partial_skills"]]
    missing_names = [s["skill_name"] for s in data["missing_skills"]]

    assert "Linux" in matched_names
    assert "Docker" in partial_names
    assert "Kubernetes" in missing_names


def test_readiness_score_is_deterministic(client, auth_headers):
    client.post(
        "/api/skills",
        json={
            "skill_name": "Linux",
            "proficiency": "Intermediate",
            "years_of_experience": 1,
        },
        headers=auth_headers,
    )
    role_id = _get_devops_role_id(client, auth_headers)

    resp1 = client.post(
        "/api/analysis", json={"job_role_id": role_id}, headers=auth_headers
    )
    resp2 = client.post(
        "/api/analysis", json={"job_role_id": role_id}, headers=auth_headers
    )

    score1 = resp1.get_json()["data"]["readiness_score"]
    score2 = resp2.get_json()["data"]["readiness_score"]
    assert score1 == score2


def test_roadmap_generated_after_analysis(client, auth_headers):
    role_id = _get_devops_role_id(client, auth_headers)
    client.post("/api/analysis", json={"job_role_id": role_id}, headers=auth_headers)

    resp = client.get("/api/roadmap", headers=auth_headers)
    assert resp.status_code == 200
    roadmap = resp.get_json()["data"]
    assert roadmap is not None
    assert len(roadmap["items"]) > 0


def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code in (200, 503)
    assert "status" in resp.get_json()
