import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


def check_fit(posting, skills):
    prompt = f"""You are a career coach. Compare the job posting to the candidate's skills.

Job posting:
{posting}

Candidate skills:
{skills}

Reply with ONLY a JSON object, no other text, with these keys:
- "matched": list of required skills the candidate has
- "missing": list of required skills the candidate lacks
- "strong_fit": true or false
- "summary": one or two sentences explaining the verdict
"""
    message = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""
    for block in message.content:
        if block.type == "text":
            text += block.text

    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


if __name__ == "__main__":
    posting = "Junior Python developer. Required: Python, Flask, SQL, Git, REST APIs. Nice to have: Docker."
    skills = "Python, JavaScript, SQL, Git, PHP"
    print(json.dumps(check_fit(posting, skills), indent=2))