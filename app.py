from flask import Flask, jsonify, request

from fit_check import check_fit, make_plan

app = Flask(__name__)


@app.route("/")
def home():
    return "SkillSync is running"


@app.route("/api/fit", methods=["POST"])
def fit():
    data = request.get_json(silent=True) or {}
    posting = data.get("posting", "").strip()
    skills = data.get("skills", "").strip()
    if not posting or not skills:
        return jsonify({"error": "Please provide both a job posting and your skills."}), 400
    return jsonify(check_fit(posting, skills))


@app.route("/api/plan", methods=["POST"])
def plan():
    data = request.get_json(silent=True) or {}
    missing = data.get("missing", [])
    if not missing:
        return jsonify({"error": "No missing skills provided."}), 400
    return jsonify({"plan": make_plan(missing)})