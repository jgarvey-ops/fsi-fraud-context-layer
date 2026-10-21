from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


class FixtureStore:
    def __init__(self, historic_dir: Path) -> None:
        self.historic_dir = historic_dir

    def cases(self) -> list[dict[str, Any]]:
        return load_jsonl(self.historic_dir / "gold_cases.jsonl")

    def case_timeline(self, case_id: str) -> list[dict[str, Any]]:
        return [r for r in load_jsonl(self.historic_dir / "gold_case_timeline.jsonl") if r.get("case_id") == case_id]

    def alerts_for_case(self, case_id: str) -> list[dict[str, Any]]:
        return [r for r in load_jsonl(self.historic_dir / "silver_fraud_alerts.jsonl") if r.get("case_id") == case_id]

    def customer(self, party_id: str) -> dict[str, Any] | None:
        for row in load_jsonl(self.historic_dir / "silver_customers.jsonl"):
            if row.get("party_id") == party_id:
                return row
        return None

    def transactions_for_party(self, party_id: str, limit: int = 50) -> list[dict[str, Any]]:
        rows = [r for r in load_jsonl(self.historic_dir / "silver_transactions.jsonl") if r.get("party_id") == party_id]
        return rows[:limit]

    def stream_events(self, limit: int = 20) -> list[dict[str, Any]]:
        return load_jsonl(self.historic_dir / "silver_stream_events.jsonl")[:limit]
