.PHONY: test generate-fixtures generate run-context lint

VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

$(VENV)/bin/python:
	python3 -m venv $(VENV)
	$(PIP) install -U pip

install: $(VENV)/bin/python
	$(PIP) install -e "./synthetic/generator[dev]" -e "./context-service[dev]"
	$(PIP) install -r demo-ui/requirements.txt

test: install
	$(PYTHON) -m pytest synthetic/generator/tests context-service/tests -q

generate-fixtures: install
	GENERATOR_SCALE=small $(PYTHON) -m fraud_synthetic generate --out synthetic/out/fixtures-run

generate: install
	$(PYTHON) -m fraud_synthetic generate --out synthetic/out/full --scale $(or $(SCALE),medium)

run-context: install
	$(PYTHON) -m uvicorn context_service.main:app --app-dir context-service/src --host $${CONTEXT_SERVICE_HOST:-0.0.0.0} --port $${CONTEXT_SERVICE_PORT:-8080} --reload

lint: install
	$(PYTHON) -m ruff check synthetic/generator context-service/src
