# Deploy on Cloudera AI (`jgarv-cdp-env`)

## Context Service

1. Create a Cloudera AI **Workbench** application from `context-service/`.
2. Start command:

```bash
pip install -e ./context-service
uvicorn context_service.main:app --host 0.0.0.0 --port 8080
```

3. Secrets: `TRINO_HOST`, `TRINO_USER`, `TRINO_PASSWORD`, `TRINO_CATALOG=demobank`, `TRINO_SCHEMA=fraud`.

## Demo UI (Streamlit)

```bash
pip install -r demo-ui/requirements.txt
streamlit run demo-ui/app.py
```

Set `CONTEXT_SERVICE_URL` to the Workbench app URL.

## Agent

1. Import `agent/tools.json` definitions into your CAI tool-calling project.
2. Point base URL to Context Service.
3. Use an open-weight instruct model (3B class) on CPU for demos.

## Stream injection

- API: `POST /v1/admin/stream/injection` with `{"enabled": true}`
- UI: Streamlit toggle (same API)
- CDE: sync `control/stream_injection.json` to S3 when implementing live micro-batch (Phase 2 task)
