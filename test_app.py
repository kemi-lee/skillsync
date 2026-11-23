import app as app_module
from app import app


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"SkillSync is running" in response.data


def test_fit_requires_posting_and_skills():
    client = app.test_client()
    response = client.post("/api/fit", json={"posting": "", "skills": ""})
    assert response.status_code == 400


def test_fit_returns_result(monkeypatch):
    fake_result = {
        "matched": ["Python"],
        "missing": ["Flask"],
        "strong_fit": False,
        "summary": "Test summary",
    }
    monkeypatch.setattr(app_module, "check_fit", lambda posting, skills: fake_result)

    client = app.test_client()
    response = client.post(
        "/api/fit", json={"posting": "Python, Flask", "skills": "Python"}
    )
    assert response.status_code == 200
    assert response.get_json()["missing"] == ["Flask"]


def test_plan_requires_missing_skills():
    client = app.test_client()
    response = client.post("/api/plan", json={"missing": []})
    assert response.status_code == 400


def test_plan_returns_plan(monkeypatch):
    monkeypatch.setattr(app_module, "make_plan", lambda missing: "Fake plan")

    client = app.test_client()
    response = client.post("/api/plan", json={"missing": ["Flask"]})
    assert response.status_code == 200
    assert response.get_json()["plan"] == "Fake plan"

def test_fit_uses_saved_resume_when_no_skills(monkeypatch):
    seen = {}

    def fake_check_fit(posting, skills):
        seen["skills"] = skills
        return {"matched": [], "missing": [], "strong_fit": True, "summary": "ok"}

    monkeypatch.setattr(app_module, "load_resume", lambda: "My saved resume")
    monkeypatch.setattr(app_module, "check_fit", fake_check_fit)

    client = app.test_client()
    response = client.post("/api/fit", json={"posting": "Python job"})
    assert response.status_code == 200
    assert seen["skills"] == "My saved resume"