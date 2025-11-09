import os, requests, openai

project_id = os.getenv("CI_PROJECT_ID")
token = os.getenv("GITLAB_TOKEN")
commit_msg = os.getenv("CI_COMMIT_MESSAGE", "No commit message provided")

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = f"""
You are GitLab's AI reviewer. The last commit message was:
'{commit_msg}'.
Suggest one meaningful code or architecture improvement in one short paragraph.
"""

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": prompt}]
)

suggestion = response["choices"][0]["message"]["content"]
print("AI Suggestion:", suggestion)

url = f"https://gitlab.com/api/v4/projects/{project_id}/issues"
headers = {"PRIVATE-TOKEN": token}
data = {"title": "🤖 AI Improvement Suggestion", "description": suggestion}

res = requests.post(url, headers=headers, data=data)
print("Issue created:", res.status_code)

    model="gpt-4o-mini",
    messages=[{"role": "system", "content": prompt}]
)

suggestion = response["choices"][0]["message"]["content"]
print("AI Suggestion:", suggestion)

url = f"https://gitlab.com/api/v4/projects/{project_id}/issues"
headers = {"PRIVATE-TOKEN": token}
data = {"title": "🤖 AI Improvement Suggestion", "description": suggestion}

res = requests.post(url, headers=headers, data=data)
print("Issue created:", res.status_code)
