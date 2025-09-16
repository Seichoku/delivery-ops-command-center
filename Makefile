.PHONY: setup run-api run-app test lint format

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
run-api:
	. .venv/bin/activate && uvicorn api.main:app --reload --port 8000
run-app:
	. .venv/bin/activate && streamlit run app/dashboard.py --server.port 8501
test:
	. .venv/bin/activate && pytest -q
lint:
	. .venv/bin/activate && ruff check .
format:
	. .venv/bin/activate && black .
