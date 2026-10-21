# Demo script — fraud investigation agent

**Duration:** ~15 minutes  
**Persona:** L2 financial crime analyst  
**Environment:** `jgarv-cdp-env`, Context Service + Streamlit on Cloudera AI

## Before you start

1. CDE historic load completed; micro-batch schedule active (5 min).
2. Context Service healthy (`GET /health`).
3. Streamlit UI open; **Stream injection** = **Off** for first half.

## Act 1 — Case dossier (historic context)

1. Open case **`CASE-001`** (retail CNP velocity).
2. Ask the agent: *“Summarize this case and the customer’s 90-day payment pattern.”*
3. Show **citations**: `demobank.fraud.silver_transactions`, `silver_fraud_alerts`.
4. Point to **masked** fields (no full PAN/SSN).

## Act 2 — Entity graph (mixed FSI)

1. Switch to **`CASE-003`** (SMB mule / beneficiary cluster).
2. Ask: *“Which linked parties share beneficiaries in the last 90 days?”*
3. Highlight `silver_entity_links` and governed SQL template (no free-form SQL from the model).

## Act 3 — Simulated stream (toggle on)

1. In Streamlit, set **Stream injection** = **On** (calls `POST /v1/admin/stream/injection`).
2. Wait for one micro-batch cycle (~5 min) or trigger job manually in CDE for rehearsal.
3. Open **`CASE-002`**; ask: *“Any new alerts since the case opened?”*
4. Show new row in `silver_fraud_alerts` / `silver_stream_events` tied to scripted manifest.

## Act 4 — Audit

1. Show `context_agent_audit` (via Trino or admin export).
2. Closing line: *“Historic and streaming context share one governed lakehouse; the agent never holds lake credentials.”*

## Fallback (no Trino)

Context Service runs in **fixture mode** using `synthetic/fixtures/` — same script, note “offline rehearsal.”
