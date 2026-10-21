from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fraud_synthetic.scales import ScaleProfile, SCALES

DEMO_CASES = [
    {
        "case_id": "CASE-001",
        "status": "open",
        "primary_party_id": "pty-retail-1001",
        "summary": "Retail CNP velocity — 6 authorizations in 12 minutes.",
    },
    {
        "case_id": "CASE-002",
        "status": "investigating",
        "primary_party_id": "pty-retail-2044",
        "summary": "ATO device fingerprint + wire attempt.",
    },
    {
        "case_id": "CASE-003",
        "status": "escalated",
        "primary_party_id": "pty-smb-3301",
        "summary": "SMB shared beneficiary cluster (mule typology demo).",
    },
]


def _ts(base: datetime, day_offset: int, minute: int = 0) -> str:
    dt = base + timedelta(days=day_offset, minutes=minute)
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def generate_pack(out_dir: Path, scale: str = "small", seed: int = 42) -> dict[str, Any]:
    profile = SCALES.get(scale)
    if profile is None:
        raise ValueError(f"Unknown scale {scale!r}; choose from {list(SCALES)}")

    rng = random.Random(seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    historic = out_dir / "historic"
    replay = out_dir / "replay"
    historic.mkdir(exist_ok=True)
    replay.mkdir(exist_ok=True)

    now = datetime(2025, 10, 14, 12, 0, 0, tzinfo=timezone.utc)
    start = now - timedelta(days=90)

    customers: list[dict[str, Any]] = []
    accounts: list[dict[str, Any]] = []
    entities: list[dict[str, Any]] = []
    entity_links: list[dict[str, Any]] = []

    for i in range(profile.n_customers):
        segment = "smb" if i % 5 == 0 else "retail"
        party_id = f"pty-{segment}-{i + 1:04d}"
        customers.append(
            {
                "party_id": party_id,
                "segment": segment,
                "risk_tier": rng.choice(["low", "medium", "high"]),
                "display_name": f"Synthetic {segment.title()} Customer {i + 1}",
                "tax_id_token": f"TIN-TOK-{rng.randint(10_000, 99_999)}",
            }
        )
        for acct_idx in range(1 if segment == "retail" else 2):
            accounts.append(
                {
                    "account_id": f"acct-{party_id}-{acct_idx + 1}",
                    "party_id": party_id,
                    "product": rng.choice(["card", "ach", "wire"]),
                    "pan_last4": f"{rng.randint(1000, 9999):04d}",
                }
            )

    for e in range(profile.n_entities):
        entity_id = f"ent-{e + 1:05d}"
        entities.append(
            {
                "entity_id": entity_id,
                "label": f"Synthetic Entity Cluster {e + 1}",
                "typology_hint": rng.choice(["mule", "ato", "cnp", "ach_fraud"]),
            }
        )
        link_count = rng.randint(1, 4)
        for _ in range(link_count):
            party = rng.choice(customers)
            entity_links.append(
                {
                    "entity_id": entity_id,
                    "party_id": party["party_id"],
                    "link_type": rng.choice(["beneficiary", "device", "counterparty"]),
                }
            )

    # Pin demo parties to stable IDs (indices 0..2)
    for idx, case in enumerate(DEMO_CASES):
        customers[idx]["party_id"] = case["primary_party_id"]

    transactions: list[dict[str, Any]] = []
    for t in range(profile.n_transactions):
        acct = rng.choice(accounts)
        day_offset = rng.randint(0, 89)
        transactions.append(
            {
                "txn_id": f"txn-{t + 1:08d}",
                "account_id": acct["account_id"],
                "party_id": acct["party_id"],
                "amount_usd": round(rng.uniform(5, 5000), 2),
                "channel": rng.choice(["card", "ach", "wire"]),
                "event_time": _ts(start, day_offset, rng.randint(0, 1439)),
            }
        )

    alerts: list[dict[str, Any]] = [
        {
            "alert_id": "frd-2025-10-14-001",
            "case_id": "CASE-001",
            "party_id": DEMO_CASES[0]["primary_party_id"],
            "typology": "card_not_present_velocity",
            "severity": "high",
            "score": 0.94,
            "event_time": _ts(now, 0, -30),
        },
        {
            "alert_id": "frd-2025-10-14-002",
            "case_id": "CASE-002",
            "party_id": DEMO_CASES[1]["primary_party_id"],
            "typology": "account_takeover_device",
            "severity": "medium",
            "score": 0.81,
            "event_time": _ts(now, 0, -120),
        },
        {
            "alert_id": "frd-2025-10-13-003",
            "case_id": "CASE-003",
            "party_id": DEMO_CASES[2]["primary_party_id"],
            "typology": "mule_network_graph",
            "severity": "high",
            "score": 0.97,
            "event_time": _ts(now, -1, 60),
        },
    ]

    case_rng = random.Random(seed + 99)
    cases = [
        {**case, "opened_at": _ts(now, -case_rng.randint(1, 5))} for case in DEMO_CASES
    ]

    timelines: list[dict[str, Any]] = []
    for case in cases:
        timelines.append(
            {
                "case_id": case["case_id"],
                "event_type": "case_opened",
                "detail": case["summary"],
                "event_time": case["opened_at"],
            }
        )

    _write_jsonl(historic / "silver_customers.jsonl", customers)
    _write_jsonl(historic / "silver_accounts.jsonl", accounts)
    _write_jsonl(historic / "silver_entities.jsonl", entities)
    _write_jsonl(historic / "silver_entity_links.jsonl", entity_links)
    _write_jsonl(historic / "silver_transactions.jsonl", transactions)
    _write_jsonl(historic / "silver_fraud_alerts.jsonl", alerts)
    _write_jsonl(historic / "gold_cases.jsonl", cases)
    _write_jsonl(historic / "gold_case_timeline.jsonl", timelines)

    manifest = {
        "scale": profile.name,
        "seed": seed,
        "generated_at": now.isoformat(),
        "counts": {
            "customers": len(customers),
            "accounts": len(accounts),
            "transactions": len(transactions),
            "replay_windows": profile.replay_windows,
        },
        "demo_cases": [c["case_id"] for c in DEMO_CASES],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    for w in range(profile.replay_windows):
        window_id = f"win-{w:05d}"
        events = []
        for e in range(profile.events_per_window):
            events.append(
                {
                    "event_id": f"str-{window_id}-{e}",
                    "stream_type": rng.choice(["auth", "login", "wire", "ach"]),
                    "party_id": rng.choice(customers)["party_id"],
                    "amount_usd": round(rng.uniform(10, 2000), 2),
                    "event_time": _ts(now, 0, w * 5 + e),
                }
            )
        _write_jsonl(replay / f"{window_id}.jsonl", events)

    return manifest


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
