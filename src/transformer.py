import json
import os
import hashlib
import re
from html import unescape
from tqdm import tqdm

RAW_FILE = "data/raw_issues.jsonl"
OUTPUT_FILE = "data/cleaned_issues.jsonl"
SEEN_FILE = "checkpoints/seen_hashes.json"
BATCH_WRITE = 500

def ensure_dirs():
    for d in ("data", "checkpoints"):
        if not os.path.exists(d):
            os.makedirs(d)

def strip_html(text):
    if not text:
        return ""
    t = unescape(text)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def first_n_sentences(text, n=2):
    if not text:
        return ""
    text = text.replace("\n", " ").strip()
    parts = re.split(r'(?<=[.!?])\s+', text)
    return " ".join(parts[:n]).strip()

def classify_text(title, description, labels):
    txt = (title + " " + description + " " + " ".join(labels)).lower()
    if any(k in txt for k in ("bug", "error", "exception", "nullpointer", "stacktrace")):
        return "Bug"
    if any(k in txt for k in ("feature", "enhancement", "add", "support")):
        return "Feature"
    if any(k in txt for k in ("doc", "documentation", "readme")):
        return "Documentation"
    if any(k in txt for k in ("performance", "slow", "optimiz", "latency")):
        return "Performance"
    return "Other"

def make_qa(title, summary):
    return {
        "question": f"What is the issue about: {title}".strip(),
        "answer": summary if summary else "No concise summary available."
    }

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r", encoding="utf-8") as f:
            try:
                return set(json.load(f))
            except:
                return set()
    return set()

def save_seen(seen_set):
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen_set), f)

def issue_hash(issue):
    key = issue.get("key", "")
    desc = (issue.get("fields", {}) or {}).get("description", "") or ""
    return hashlib.sha256((key + "|" + desc).encode("utf-8")).hexdigest()

def transform_issue(issue):
    fields = issue.get("fields", {}) or {}
    key = issue.get("key", "") or ""
    project = key.split("-")[0] if "-" in key else ""
    title = strip_html(fields.get("summary", "") or "")
    description = strip_html(fields.get("description", "") or "")
    comments_raw = fields.get("comment", {}).get("comments", []) or []
    comments = [strip_html(c.get("body", "") or "") for c in comments_raw]
    summary = first_n_sentences(description, 2) or first_n_sentences(" ".join(comments), 2)
    labels = fields.get("labels", []) or []
    classification = classify_text(title, description, labels)
    qa = make_qa(title, summary)
    return {
        "issue_id": key,
        "project": project,
        "title": title,
        "description": description,
        "status": (fields.get("status") or {}).get("name", ""),
        "priority": (fields.get("priority") or {}).get("name", ""),
        "reporter": (fields.get("reporter") or {}).get("displayName", ""),
        "assignee": (fields.get("assignee") or {}).get("displayName", ""),
        "labels": labels,
        "comments": comments,
        "created": fields.get("created", ""),
        "updated": fields.get("updated", ""),
        "derived": {
            "summary": summary,
            "classification": classification,
            "qa": qa
        }
    }

def transform_all():
    ensure_dirs()
    if not os.path.exists(RAW_FILE):
        return
    seen = load_seen()
    buffer = []
    written = 0
    with open(RAW_FILE, "r", encoding="utf-8") as fin:
        for line in tqdm(fin, desc="Transforming"):
            line = line.strip()
            if not line:
                continue
            try:
                issue = json.loads(line)
            except:
                continue
            h = issue_hash(issue)
            if h in seen:
                continue
            try:
                cleaned = transform_issue(issue)
            except:
                continue
            buffer.append(json.dumps(cleaned, ensure_ascii=False))
            seen.add(h)
            if len(buffer) >= BATCH_WRITE:
                with open(OUTPUT_FILE, "a", encoding="utf-8") as fo:
                    fo.write("\n".join(buffer) + "\n")
                written += len(buffer)
                buffer = []
        if buffer:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as fo:
                fo.write("\n".join(buffer) + "\n")
            written += len(buffer)
    save_seen(seen)
    return written

if __name__ == "__main__":
    transform_all()
