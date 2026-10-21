"""
CDE job: load synthetic historic JSONL from S3 into Iceberg demobank.fraud.silver_* / gold_*.

Wire Spark session + Iceberg catalog per CDP docs for jgarv-cdp-env before production use.
"""

from __future__ import annotations

import os
import sys


def main() -> None:
    prefix = os.environ.get("SYNTHETIC_S3_PREFIX")
    if not prefix:
        print("SYNTHETIC_S3_PREFIX required", file=sys.stderr)
        sys.exit(1)
    # TODO: spark.read.json(prefix + '/historic/*.jsonl').writeTo('demobank.fraud.silver_*')
    print(f"load_historic stub OK prefix={prefix}")


if __name__ == "__main__":
    main()
