📌 Apache Jira Scraper – Data Pipeline for LLM Training

This project builds a fault-tolerant scraping and data transformation system that collects issue data from Apache Jira, processes it into a clean JSONL format, and prepares it for machine learning or LLM fine-tuning.

✅ 1. Features & Objectives

✔ Scrape issues, comments, metadata (status, priority, reporter, assignee, tags etc.)
✔ Resume scraping automatically using checkpoints (no data loss)
✔ Handles API failures, retries, timeouts, HTTP 429 & 5xx errors
✔ Transform raw Jira data into a structured, LLM-ready JSONL corpus
✔ Adds derived tasks like:
  • Issue classification (Bug/Feature/Docs/Performance)
  • Issue summarization
  • Question-Answer pair generation
✔ Large datasets are stored in .jsonl instead of .csv to avoid memory issues
✔ Clean and modular code (scraper.py, transformer.py, utils.py)

✅ 2. Project Structure

JIRA_SCRAPER/
├── src/
│   ├── scraper.py          # Scrapes Jira issues, comments, handles pagination & checkpoints
│   ├── transformer.py      # Cleans, extracts, summarizes & structures data for LLM
│   ├── utils.py            # Retry logic, timeouts, HTTP 429/5xx handling
│   ├── export_to_csv.py    # Converts cleaned JSONL → CSV (optional for analysis)
│
├── data/                   # Raw & cleaned data (excluded from Git due to size)
│   ├── raw_issues.jsonl
│   ├── cleaned_issues.jsonl
│
├── checkpoints/            # Stores last progress & seen issue hashes
│   ├── last_checkpoint.json
│   ├── seen_hashes.json
│
├── README.md
├── requirements.txt
├── .gitignore

✅ 3. Setup Instructions
✅ Install & Run Locally
git clone https://github.com/dakshsahu1803/jira-scraper.git
cd jira-scraper

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

✅ Run Scraper (Fetch Raw Data)
cd src
python scraper.py
✅ Run Transformer (Clean Data)
python transformer.py
✅ (Optional) Export to CSV
python export_to_csv.py

✅ 4. Architecture & Design
🔹 Workflow

Fetch Jira issues using REST API

Save raw data to data/raw_issues.jsonl

Resume scraping using checkpoints & hashes

Transform raw JSON → Clean structured JSONL

Generate summaries, Q/A pairs, issue type classification

Export to CSV if required

🔹 Why JSONL?

✔ Memory-efficient (streamable line-by-line)
✔ Ideal for LLM training & HuggingFace datasets
✔ Easier to append and resume work

✅ 5. Edge Case Handling & Fault Tolerance
Edge Case	Handling Method
HTTP 429 (Too Many Requests)	Automatic wait + retry (exponential backoff)
HTTP 5xx (Server errors)	Retry with delay
Network failure / timeout	try/except + safe retries
Interrupted execution	Resumes via last_checkpoint.json
Duplicate issues	Checked via SHA-256 hash (seen_hashes.json)
Empty or malformed data	Ignored safely — no crash
API Rate Limits	Handled using safe_request() in utils.py
✅ 6. Optimizations

✅ Batch writes to disk instead of writing each issue
✅ Checkpoint-based resuming (no duplicates, no restart needed)
✅ SHA-256 content hashing to skip already processed issues
✅ Modular, reusable, readable codebase

✅ 7. Future Improvements

🚀 Use multithreading / asyncio to speed up scraping
🚀 Add Docker support (Dockerfile)
🚀 Add unit tests for scraper and transformer
🚀 Push cleaned dataset to Hugging Face Datasets
🚀 Add command-line arguments for custom projects

✅ 8. GitHub Guidelines (Important)
data/
checkpoints/
*.jsonl
*.csv
✅ 10. Authors

Developed by: DAKSH SAHU
Purpose: Assignment – Jira Issue Scraper & Data Preparation for LLMs
Mentors / Reviewers: Naman Bhalla.
