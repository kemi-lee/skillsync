from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Say hello to SkillSync in one sentence."}
    ],
)

for block in message.content:
    if block.type == "text":
        print(block.text)