"""CDE job: merge bronze_stream_raw into demobank.fraud.silver_stream_events (+ optional alerts)."""

from __future__ import annotations

import sys


def main() -> None:
    # TODO: idempotent merge on event_id
    print("silver_merge stub OK")


if __name__ == "__main__":
    main()
