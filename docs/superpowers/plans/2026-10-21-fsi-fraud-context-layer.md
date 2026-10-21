# FSI Fraud Context Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a Cloudera AI–hosted fraud investigation agent backed by a governed synthetic lakehouse context layer (`demobank.fraud.silver_*`) with CDE micro-batch stream simulation.

**Architecture:** Python generator → S3 → CDE Spark (historic + 5m micro-batch) → Iceberg → Trino ← Context Service (FastAPI on CAI) ← open-weight agent + Streamlit UI.

**Tech Stack:** Python 3.11+, FastAPI, PySpark (CDE), Trino client, Streamlit, Cloudera AI, CDP Public Cloud on AWS.

**Spec:** `docs/superpowers/specs/2026-10-21-fsi-fraud-context-layer-design.md`

## Global Constraints

- CDP environment: `jgarv-cdp-env`, region `us-east-2`, greenfield.
- Synthetic data only; medium scale (~5k customers, ~1M transactions / 90d) for full generate.
- Trino catalog `demobank`, schema `fraud`, table prefix `silver_*` / `gold_*` / `bronze_*` / `context_*`.
- Micro-batch interval: 5 minutes.
- Stream injection: admin API + Streamlit toggle.
- Public CDP APIs + replay fixtures; no VPC peering required for MVP.
- Open-weight models on Cloudera AI only.

---

## Phase 1 — Synthetic data & local Context Service

### Task 1: Generator package

**Files:** `synthetic/generator/`

- [x] Scaffold `fraud_synthetic` CLI (`generate`, scales `small|medium`)
- [x] Emit historic tables JSON/JSONL + replay windows + `scripted_alerts.yaml` merge hints
- [x] Unit tests for deterministic seed and demo case IDs
- [ ] `make generate SCALE=medium` and upload docs to S3 path in runbook

### Task 2: Context Service MVP

**Files:** `context-service/`

- [x] FastAPI `/health`, case + customer + stream routes
- [x] Fixture-backed mode when Trino env unset
- [x] Governed SQL template registry (stub)
- [x] `POST /v1/admin/stream/injection`
- [ ] Wire Trino client for live CDP
- [ ] OpenAPI parity test

### Task 3: Demo UI shell

**Files:** `demo-ui/app.py`

- [x] Streamlit: injection toggle calling admin API
- [ ] Chat panel wired to agent (Phase 4)

---

## Phase 2 — CDE jobs (CDP)

### Task 4: Historic load job

**Files:** `cde/jobs/load_historic.py`

- [ ] Read S3 historic prefix, write Iceberg `demobank.fraud.silver_*`, `gold_*`
- [ ] Manual smoke: row counts match generator manifest

### Task 5: Micro-batch stream + merge

**Files:** `cde/jobs/microbatch_stream.py`, `cde/jobs/silver_merge.py`

- [ ] Checkpoint table `bronze_ingest_checkpoint`
- [ ] Schedule every 5 minutes in CDE
- [ ] Honor injection flag file/object written by Context Service (S3 marker or DB)

---

## Phase 3 — CDP greenfield (`jgarv-cdp-env`)

**Files:** `docs/cdp-greenfield-setup.md`

- [ ] AWS + CDP console steps through Data Lake, SDX, CAI, CDE, Trino
- [ ] Smoke: Trino `SELECT` on `demobank.fraud.silver_customers`
- [ ] Deploy Context Service as CAI Workbench app
- [ ] Store CDP access key in workspace secrets

---

## Phase 4 — Agent on Cloudera AI

**Files:** `agent/tools.json`, `agent/README-cai-deploy.md`

- [ ] Register open-weight model
- [ ] Bind tools to Context Service base URL
- [ ] Demo script rehearsal with injection on/off

---

## Verification

```bash
make test
make generate-fixtures
make run-context
curl -s localhost:8080/v1/cases/CASE-002 | jq .
```
