def test_add_skill(client, auth_headers):
    resp = client.post(
        "/api/skills",
        json={
            "skill_name": "Docker",
            "proficiency": "Intermediate",
            "years_of_experience": 1.5,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 201
    assert resp.get_json()["data"]["skill_name"] == "Docker"


def test_add_duplicate_skill_rejected(client, auth_headers):
    payload = {
        "skill_name": "Linux",
        "proficiency": "Beginner",
        "years_of_experience": 1,
    }
    client.post("/api/skills", json=payload, headers=auth_headers)
    resp = client.post("/api/skills", json=payload, headers=auth_headers)
    assert resp.status_code == 409


def test_list_skills(client, auth_headers):
    client.post(
        "/api/skills",
        json={"skill_name": "Git", "proficiency": "Advanced", "years_of_experience": 2},
        headers=auth_headers,
    )
    resp = client.get("/api/skills", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.get_json()["data"]) >= 1


def test_delete_skill(client, auth_headers):
    add_resp = client.post(
        "/api/skills",
        json={
            "skill_name": "AWS",
            "proficiency": "Beginner",
            "years_of_experience": 0.5,
        },
        headers=auth_headers,
    )
    skill_id = add_resp.get_json()["data"]["id"]
    del_resp = client.delete(f"/api/skills/{skill_id}", headers=auth_headers)
    assert del_resp.status_code == 200

    list_resp = client.get("/api/skills", headers=auth_headers)
    names = [s["skill_name"] for s in list_resp.get_json()["data"]]
    assert "AWS" not in names
