# CDE Spark jobs

Submit from a CDE project in `jgarv-cdp-env` after uploading `synthetic/out/full` to S3.

| Job | File | Schedule |
|-----|------|----------|
| Historic load | `load_historic.py` | On demand |
| Stream micro-batch | `microbatch_stream.py` | Every 5 minutes |
| Silver merge | `silver_merge.py` | Chain after micro-batch |

Environment variables (CDE):

- `SYNTHETIC_S3_PREFIX` — e.g. `s3://bucket/synthetic/fraud/`
- `ICEBERG_CATALOG` — `demobank`
- `ICEBERG_SCHEMA` — `fraud`

Job bodies are stubs until Iceberg Spark extensions are configured for your CDP version.
