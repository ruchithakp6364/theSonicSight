import os
import requests
from openai import OpenAI

# 🧠 Environment Variables
project_id = os.getenv("CI_PROJECT_ID")
token = os.getenv("GITLAB_TOKEN")
commit_msg = os.getenv("CI_COMMIT_MESSAGE", "No commit message provided")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🧠 AI Prompt
prompt = f"""
You are GitLab's AI reviewer. The last commit message was:
'{commit_msg}'.
Suggest one meaningful code or architecture improvement in one short paragraph.
"""

# 🤖 Get AI Suggestion
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": prompt}]
)

suggestion = response.choices[0].message.content
print("AI Suggestion:", suggestion)

# 🧾 Create GitLab Issue
url = f"https://gitlab.com/api/v4/projects/{project_id}/issues"
headers = {"PRIVATE-TOKEN": token}
data = {
    "title": "🤖 AI Improvement Suggestion",
    "description": suggestion
}

try:
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 201:
        print("✅ GitLab Issue created successfully!")
    else:
        print(f"⚠️ Failed to create issue: {res.status_code} - {res.text}")
except Exception as e:
    print("❌ Error creating issue:", e)