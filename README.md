<div align="center">
<h1>📌 Apache Jira Scraper – Data Pipeline for LLM Training</h1>
<p>
<i>This project builds a fault-tolerant scraping and data transformation system that collects issue data from Apache Jira, processes it into a clean JSONL format, and prepares it for machine learning or LLM fine-tuning.</i>
</p>

<p>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3.9%252B-blue.svg" alt="Python 3.9+">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Status-Completed-green.svg" alt="Status: Completed">
<img src="https://www.google.com/search?q=https://img.shields.io/badge/License-MIT-purple.svg" alt="License: MIT">
</p>
</div>

<hr>
<h1> Data : https://drive.google.com/drive/folders/1kB5AzNMXvSELRAo1Xig01uCykfxGdJiP?usp=sharing</h1>
<h2>✅ 1. Features & Objectives</h2>

<table width="100%">
<tr>
<td valign="top" width="50%">
<strong>Core Pipeline Features:</strong>
<ul>
<li>✔ Scrape issues, comments, & metadata</li>
<li>✔ Resume scraping automatically (checkpoints)</li>
<li>✔ Handles API failures, retries, & timeouts</li>
<li>✔ Robust <code>HTTP 429</code> & <code>5xx</code> error handling</li>
<li>✔ Clean and modular code</li>
</ul>
</td>
<td valign="top" width="50%">
<strong>LLM-Ready Data:</strong>
<ul>
<li>✔ Transform raw data into structured JSONL</li>
<li>✔ Ideal for large datasets (<code>.jsonl</code>)</li>
<li>✔ Generates derived tasks:
<ul>
<li>Issue classification</li>
<li>Issue summarization</li>
<li>Question-Answer pair generation</li>
</ul>
</li>
</ul>
</td>
</tr>
</table>

<h2>📁 2. Project Structure</h2>

JIRA_SCRAPER/
├── src/
│   ├── scraper.py       # Scrapes Jira, handles pagination & checkpoints
│   ├── transformer.py   # Cleans, extracts, & structures data for LLM
│   ├── utils.py         # Retry logic, timeouts, HTTP 429/5xx handling
│   ├── export_to_csv.py # Converts cleaned JSONL → CSV (optional)
│   ├── data/            # (GitIgnored) Raw & cleaned data
│   │   ├── raw_issues.jsonl
│   │   └── cleaned_issues.jsonl
│   └── checkpoints/     # (GitIgnored) Stores progress
│       ├── last_checkpoint.json
│       └── seen_hashes.json
│
├── README.md            # This file
├── requirements.txt     # Project dependencies
└── .gitignore           # Tells Git what to ignore (data, venv, etc.)


<h2>🚀 3. Setup & Execution</h2>

<h3>Install & Run Locally</h3>

1. Clone the repository:

git clone [https://github.com/dakshsahu1803/jira-scraper.git](https://github.com/dakshsahu1803/jira-scraper.git)
cd jira-scraper


2. Create and activate a virtual environment:

# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


<h3>Run the Pipeline</h3>

1. Run Scraper (Fetch Raw Data):

cd src
python scraper.py


2. Run Transformer (Clean Data):

python transformer.py


3. (Optional) Export to CSV:

python export_to_csv.py


<h2>🏛️ 4. Architecture & Design</h2>

<h3>🔹 Workflow</h3>
<ol>
<li>Fetch Jira issues using the REST API (<code>scraper.py</code>).</li>
<li>Save raw data to <code>data/raw_issues.jsonl</code>.</li>
<li>Use <code>checkpoints/</code> to save progress and resume if interrupted.</li>
<li>Transform raw JSON into clean, structured JSONL (<code>transformer.py</code>).</li>
<li>Generate summaries, Q/A pairs, and classify issue types.</li>
<li>(Optional) Export the clean data to CSV for analysis.</li>
</ol>

<h3>🔹 Why JSONL?</h3>
<ul>
<li>✔ <strong>Memory-Efficient:</strong> Data is streamed line-by-line, preventing memory issues with large files.</li>
<li>✔ <strong>LLM-Ready:</strong> The ideal format for training models and using HuggingFace <code>datasets</code>.</li>
<li>✔ <strong>Robust:</strong> Easy to append and resume work without corrupting the entire file.</li>
</ul>

<h2>🛡️ 5. Edge Case Handling & Fault Tolerance</h2>

The system is designed to be robust and handle common real-world failures gracefully.

<table width="100%">
<thead>
<tr>
<th>Edge Case</th>
<th>Handling Method</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>HTTP 429 (Too Many Requests)</code></td>
<td>Automatic wait + retry with exponential backoff (via <code>utils.py</code>)</td>
</tr>
<tr>
<td><code>HTTP 5xx (Server errors)</code></td>
<td>Retry with a delay (up to 5 attempts)</td>
</tr>
<tr>
<td>Network Failure / Timeout</td>
<td><code>try/except</code> blocks with safe retries</td>
</tr>
<tr>
<td>Interrupted Execution (e.g., Ctrl+C)</td>
<td>Resumes from last checkpoint (<code>checkpoints/last_checkpoint.json</code>)</td>
</tr>
<tr>
<td>Duplicate Issues</td>
<td>Checked via SHA-256 hash (<code>checkpoints/seen_hashes.json</code>)</td>
</tr>
<tr>
<td>Empty or Malformed Data</td>
<td>Safely skipped with logging; does not crash the pipeline.</td>
</tr>
</tbody>
</table>

<h2>⚡ 6. Optimizations</h2>
<ul>
<li>✅ <strong>Batch Writes:</strong> Data is written to disk in batches, not per-issue, reducing I/O.</li>
<li>✅ <strong>Checkpoint Resuming:</strong> No need to restart from scratch on failure.</li>
<li>✅ <strong>Content Hashing:</strong> SHA-256 hashing skips already-processed issues.</li>
<li>✅ <strong>Modular Code:</strong> Clean, reusable functions in separate files.</li>
</ul>

<h2>📈 7. Future Improvements</h2>
<ul>
<li>🚀 Use <code>multithreading</code> / <code>asyncio</code> to speed up comment scraping.</li>
<li>🚀 Add Docker support (<code>Dockerfile</code>) for easy containerized deployment.</li>
<li>🚀 Add unit tests for the scraper and transformer modules.</li>
<li>🚀 Add a script to push the cleaned dataset directly to Hugging Face Datasets.</li>
<li>🚀 Add command-line arguments (using <code>argparse</code>) to pass project keys dynamically.</li>
</ul>

<h2>🙈 8. .gitignore</h2>
<p>This is the recommended content for your <code>.gitignore</code> file to keep the repository clean.</p>

# Python
venv/
__pycache__/
*.pyc

# Data & Checkpoints
data/
checkpoints/
*.jsonl
*.csv

# IDE
.idea/
.vscode/


<h2>👨‍💻 9. Authors</h2>
<p>
<strong>Developed by:</strong> <a href="https://www.google.com/search?q=https://github.com/dakshsahu1803">DAKSH SAHU</a>




<strong>Purpose:</strong> Assignment – Jira Issue Scraper & Data Preparation for LLMs




<strong>Mentors / Reviewers:</strong> Naman Bhalla
</p>
