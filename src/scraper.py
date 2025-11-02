import requests
import json
import time
import os
from utils import safe_request, ensure_directories

PROJECTS = ["HADOOP", "SPARK", "KAFKA"]
BASE_URL = "https://issues.apache.org/jira/rest/api/2/search"
HEADERS = {"Accept": "application/json"}
OUTPUT_FILE = "data/raw_issues.jsonl"
CHECKPOINT_FILE = "checkpoints/last_checkpoint.json"

ensure_directories(["data", "checkpoints"])

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)
    return {project: 0 for project in PROJECTS}

def save_checkpoint(checkpoint):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f)

def fetch_issues(project, start_at):
    params = {
        "jql": f"project={project}",
        "startAt": start_at,
        "maxResults": 50,
        "fields": "summary,description,status,priority,reporter,assignee,comment,created,updated,labels"
    }
    response = safe_request(BASE_URL, headers=HEADERS, params=params)
    if response:
        return response.json()
    return {"issues": []}

def save_issue(issue):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(issue, ensure_ascii=False) + "\n")

def run_scraper():
    checkpoint = load_checkpoint()
    for project in PROJECTS:
        start_at = checkpoint.get(project, 0)
        while True:
            data = fetch_issues(project, start_at)
            issues = data.get("issues", [])
            if not issues:
                break
            for issue in issues:
                save_issue(issue)
            start_at += len(issues)
            checkpoint[project] = start_at
            save_checkpoint(checkpoint)
            time.sleep(1)

if __name__ == "__main__":
    run_scraper()
