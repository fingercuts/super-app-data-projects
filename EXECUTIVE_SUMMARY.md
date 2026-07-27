# SwiftHub: Executive Summary

## What This Project Is

SwiftHub is an end-to-end data platform built around a fictional Indonesian super app (think Gojek or Grab). It simulates the full analytics lifecycle: generating realistic transaction data across ride-hailing, food delivery, and fintech (QRIS payments), validating it, transforming it into a star schema, and serving it through a FastAPI endpoint and Streamlit dashboard.

The goal was to build something that looks and feels like a real data platform, not just a tutorial project.

## The Architecture

```
generate data --> Pydantic validation --> DLQ (bad data) --> dbt transforms --> star schema --> FastAPI --> Streamlit
```

| Piece | What It Does |
|-------|-------------|
| Data generators | Python scripts that create realistic user, driver, merchant, and transaction data |
| Pydantic contracts | Validates every record before it enters the pipeline. Bad data goes to a DLQ |
| dbt + DuckDB | Transforms raw data into a Kimball star schema (dim_users, dim_drivers, dim_merchants, fact_daily_revenue, fct_transactions) |
| FastAPI | REST endpoints for querying recent transactions and user profiles |
| Streamlit | 4-page dashboard: executive overview, geospatial intelligence, fleet operations, data SLA |
| SLA Tracker | Logs validation results to SQLite so you can track data quality over time |

## Data Quality Approach

Instead of letting bad data slip through, every record is validated against a Pydantic contract at ingestion. Records that fail go to a Dead Letter Queue (DLQ) — they're not lost, just quarantined for review. The SLA tracker logs pass/fail rates so you can see how clean the data is over time.

dbt adds another layer with automated schema tests (unique keys, not_null, accepted values).

## Things I Had to Figure Out

- **CPU throttling**: The streaming simulation was burning 100% CPU. Switched to vectorized batch writes with sleep cycles to throttle to ~50 events/sec.
- **Currency formatting**: Streamlit doesn't natively handle Indonesian Rupiah. Wrote custom formatting helpers in `utils_i18n.py`.
- **dbt portability**: Hardcoded paths broke on different machines. Switched to dbt `vars` and it works everywhere.
- **SQLite for SLA tracking**: Fine for local dev, but would need Postgres or Prometheus in production.

## What's Next

- Migrate SLA tracker to Postgres for cloud deployment
- Add Apache Airflow for production orchestration
- Integrate Great Expectations for advanced data quality
- Connect to real Kafka instead of the local simulation
- Deploy to GCP (terraform config is ready)

## Repo

https://github.com/adespc/super-app-data-projects
MIT License
