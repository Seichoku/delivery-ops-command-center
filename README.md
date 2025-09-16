# Delivery Ops Command Center

**Goal:** End-to-end data project that ingests public trip data, runs transforms & data quality checks, trains a simple model to flag late/abnormal trips, serves a scoring API, and visualizes insights on a dashboard.

## Quickstart
```bash
git clone <your_repo_url> && cd delivery-ops-command-center
python -m venv .venv
# macOS/Linux
. .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -U pip && pip install -r requirements.txt

# Run API
make run-api  # http://localhost:8000/health

# Run Dashboard
make run-app  # http://localhost:8501/
```
Status: Day 1 scaffold created: 2025-09-16
