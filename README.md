# FSI Fraud Context Layer

Governed **context layer** for financial-crime investigation agents on **Cloudera Public Cloud (AWS)**. Synthetic historic customer data plus **CDE micro-batch** simulated streaming, queried via **Trino** (`demobank.fraud.silver_*`), exposed through a **Context Service** and **single open-weight agent** on **Cloudera AI**.

This repository is **separate** from model-governance demo apps.

## Documentation

| Doc | Purpose |
|-----|---------|
| [Design spec](docs/superpowers/specs/2026-10-21-fsi-fraud-context-layer-design.md) | Architecture, data model, security |
| [Implementation plan](docs/superpowers/plans/2026-10-21-fsi-fraud-context-layer.md) | Phased build checklist |
| [CDP greenfield setup](docs/cdp-greenfield-setup.md) | `jgarv-cdp-env` in `us-east-2`, Trino enablement |
| [Demo script](docs/demo-script.md) | Analyst walkthrough + stream toggle |

## Quick start (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e "./synthetic/generator[dev]" -e "./context-service[dev]"
make generate-fixtures   # small CI-sized pack under synthetic/out/
make test
make run-context         # FastAPI on :8080 (Trino optional)
```

## Repository layout

```
synthetic/generator/     # Historic + replay ledger generator
synthetic/fixtures/      # Committed samples for tests
cde/jobs/                # Spark jobs for CDP (historic load, micro-batch)
context-service/         # FastAPI context API (runs on Cloudera AI)
agent/                   # CAI tool definitions + deploy notes
demo-ui/                 # Streamlit demo shell (toggle + chat)
```

## Target CDP environment

- **Name:** `jgarv-cdp-env`
- **Region:** `us-east-2`
- **Stream cadence:** 5 minutes (CDE micro-batch)
- **Naming:** `demobank.fraud.silver_*` Iceberg tables via Trino catalog `demobank`, schema `fraud`
