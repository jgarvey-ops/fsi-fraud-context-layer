from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from context_service.config import settings
from context_service.fixture_store import FixtureStore
from context_service.state import runtime

app = FastAPI(title="Fraud Context Service", version="0.1.0")

store = FixtureStore(settings.fixtures_dir)
runtime.stream_injection_enabled = settings.stream_injection_default

SCRIPTED_ALERTS_PATH = Path("synthetic/scripted_alerts.yaml")


class InjectionBody(BaseModel):
    enabled: bool


class AuditTurnBody(BaseModel):
    session_id: str
    turn: int
    tool: str
    params_hash: str
    response_hash: str


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "mode": "trino" if settings.trino_host else "fixtures",
        "stream_injection_enabled": runtime.stream_injection_enabled,
    }


@app.get("/v1/cases/{case_id}")
def get_case(case_id: str) -> dict[str, Any]:
    case = next((c for c in store.cases() if c["case_id"] == case_id), None)
    if not case:
        raise HTTPException(status_code=404, detail="case not found")
    alerts = store.alerts_for_case(case_id)
    timeline = store.case_timeline(case_id)
    citations = [
        f"demobank.fraud.gold_cases(case_id={case_id})",
        f"demobank.fraud.silver_fraud_alerts(case_id={case_id})",
    ]
    return {
        "case": case,
        "alerts": alerts,
        "timeline": timeline,
        "citations": citations,
    }


@app.get("/v1/customers/{party_id}/history")
def customer_history(party_id: str, days: int = 90) -> dict[str, Any]:
    customer = store.customer(party_id)
    if not customer:
        raise HTTPException(status_code=404, detail="party not found")
    txns = store.transactions_for_party(party_id, limit=100)
    redacted = {**customer, "tax_id_token": "***"}
    return {
        "party_id": party_id,
        "window_days": days,
        "customer": redacted,
        "recent_transactions": txns,
        "citations": [f"demobank.fraud.silver_transactions(party_id={party_id})"],
    }


@app.get("/v1/stream/recent")
def stream_recent(limit: int = 20) -> dict[str, Any]:
    events = list(store.stream_events(limit=limit))
    if runtime.stream_injection_enabled:
        events = runtime.injected_events + events
    return {
        "stream_injection_enabled": runtime.stream_injection_enabled,
        "events": events[:limit],
        "citations": ["demobank.fraud.silver_stream_events"],
    }


@app.post("/v1/admin/stream/injection")
def set_injection(body: InjectionBody) -> dict[str, Any]:
    runtime.stream_injection_enabled = body.enabled
    if body.enabled:
        runtime.injected_events = _load_scripted_injection_events()
    else:
        runtime.injected_events = []
    return {"stream_injection_enabled": runtime.stream_injection_enabled, "injected_count": len(runtime.injected_events)}


@app.post("/v1/audit/turn")
def audit_turn(body: AuditTurnBody) -> dict[str, str]:
    # Phase 4: append to Iceberg context_agent_audit via Trino/batch writer
    return {"status": "accepted", "session_id": body.session_id}


def _load_scripted_injection_events() -> list[dict[str, Any]]:
    if not SCRIPTED_ALERTS_PATH.is_file():
        return []
    data = yaml.safe_load(SCRIPTED_ALERTS_PATH.read_text(encoding="utf-8")) or {}
    events: list[dict[str, Any]] = []
    for item in data.get("injection", []):
        events.append(
            {
                "event_id": item.get("alert_id", "inject-unknown"),
                "stream_type": "scripted_alert",
                "case_id": item.get("case_id"),
                "typology": item.get("typology"),
                "severity": item.get("severity"),
                "narrative": item.get("narrative"),
                "event_time": "2025-10-14T23:00:00Z",
            }
        )
    return events
