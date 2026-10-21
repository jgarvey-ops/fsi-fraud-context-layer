"""
CDE job (schedule: every 5 minutes): read next replay window from S3, append bronze_stream_raw.

When s3://.../control/stream_injection.json is true, prefer scripted windows from manifest.
"""

from __future__ import annotations

import os
import sys


def main() -> None:
    prefix = os.environ.get("SYNTHETIC_S3_PREFIX")
    if not prefix:
        print("SYNTHETIC_S3_PREFIX required", file=sys.stderr)
        sys.exit(1)
    # TODO: read bronze_ingest_checkpoint, load replay/win-*.jsonl, append bronze
    print(f"microbatch_stream stub OK prefix={prefix}")


if __name__ == "__main__":
    main()
