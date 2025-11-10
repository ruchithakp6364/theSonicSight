import json, os, requests

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = os.getenv("CI_PROJECT_ID")

def read_metrics(path="metrics/val_metrics.json"):
    if not os.path.exists(path):
        return 0.0
    with open(path, "r") as f:
        data = json.load(f)
    return data.get("accuracy", 0.0)

def create_issue(acc):
    url = f"https://gitlab.com/api/v4/projects/{PROJECT_ID}/issues"
    headers = {"PRIVATE-TOKEN": GITLAB_TOKEN}
    title = f"🚨 Accuracy drop detected ({acc*100:.2f}%)"
    desc = f"Model performance below threshold. Suggest retraining with new dataset or tuning learning rate."
    requests.post(url, headers=headers, data={"title": title, "description": desc})

if __name__ == "__main__":
    acc = read_metrics()
    print("Current model accuracy:", acc)
    if acc < float(os.getenv("MODEL_ACC_THRESHOLD", 0.85)):
        create_issue(acc)
        print("⚠️ Issue created: model needs retraining")
    else:
        print("✅ Accuracy within safe range")
