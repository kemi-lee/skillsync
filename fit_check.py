import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
MODEL = "claude-sonnet-5-5"
def load_resume():
    path = Path(__file__).parent / "resume.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def ask_claude(prompt, max_tokens=1500):
    client = Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text = ""
    for block in message.content:
        if block.type == "text":
            text += block.text
    return text.strip()


def check_fit(posting, skills):
    prompt = f"""You are a career coach. Compare the job posting to the candidate's skills.

Job posting:
{posting}

Candidate skills:
{skills}

Rules:
- Only list concrete skills, tools, languages or technologies (for example "Python", "SQL", "CI/CD"). Do not list degrees, years of experience, or soft skills.
- Use short names, 1 to 3 words each.
- If the posting names few concrete skills, say so in the summary instead of inventing requirements.

Reply with ONLY a JSON object, no other text, with these keys:
- "matched": list of required skills the candidate has
- "missing": list of required skills the candidate lacks
- "strong_fit": true or false
- "summary": one or two sentences explaining the verdict
- "enough_detail": true if the posting names at least 3 concrete skills or technologies, otherwise false
"""
    text = ask_claude(prompt)
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def make_plan(missing):
    skills_text = ", ".join(missing)
    prompt = f"""Create a short learning plan for someone who wants to learn: {skills_text}.
For each skill, give 2 or 3 bullet points and one small first step.
Plain text, under 200 words."""
    return ask_claude(prompt)


if __name__ == "__main__":
    posting = "Junior Python developer. Required: Python, Flask, SQL, Git, REST APIs. Nice to have: Docker."
    skills = load_resume()

    result = check_fit(posting, skills)
    print("Strong fit:", "Yes" if result["strong_fit"] else "Not yet")
    print(result["summary"])
    print("Matched:", ", ".join(result["matched"]))
    print("Missing:", ", ".join(result["missing"]))

    if result["missing"]:
        answer = input("\nWant a short plan to learn the missing skills? (yes/no): ")
        if answer.strip().lower().startswith("y"):
            print()
            print(make_plan(result["missing"]))