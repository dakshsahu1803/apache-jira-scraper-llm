import json
import csv
from tqdm import tqdm

INPUT = "data/cleaned_issues.jsonl"
OUTPUT = "data/cleaned_issues.csv"
FIELDNAMES = [
    "issue_id",
    "project",
    "title",
    "description",
    "status",
    "priority",
    "reporter",
    "assignee",
    "labels",
    "comments",
    "created",
    "updated",
    "derived_summary",
    "derived_classification",
    "derived_qa_question",
    "derived_qa_answer"
]

def join_list(v, limit=None):
    if not v:
        return ""
    if isinstance(v, list):
        if limit:
            return " || ".join(x.replace("\n"," ").strip() for x in v[:limit])
        return " || ".join(x.replace("\n"," ").strip() for x in v)
    return str(v)

with open(INPUT, "r", encoding="utf-8") as fin, open(OUTPUT, "w", encoding="utf-8", newline="") as fout:
    writer = csv.DictWriter(fout, fieldnames=FIELDNAMES)
    writer.writeheader()
    for line in tqdm(fin, desc="Exporting to CSV"):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except:
            continue
        row = {
            "issue_id": obj.get("issue_id",""),
            "project": obj.get("project",""),
            "title": obj.get("title",""),
            "description": obj.get("description",""),
            "status": obj.get("status",""),
            "priority": obj.get("priority",""),
            "reporter": obj.get("reporter",""),
            "assignee": obj.get("assignee",""),
            "labels": join_list(obj.get("labels",[])),
            "comments": join_list(obj.get("comments",[]), limit=5),
            "created": obj.get("created",""),
            "updated": obj.get("updated",""),
            "derived_summary": (obj.get("derived") or {}).get("summary",""),
            "derived_classification": (obj.get("derived") or {}).get("classification",""),
            "derived_qa_question": ((obj.get("derived") or {}).get("qa") or {}).get("question",""),
            "derived_qa_answer": ((obj.get("derived") or {}).get("qa") or {}).get("answer","")
        }
        writer.writerow(row)
print("CSV export completed:", OUTPUT)
