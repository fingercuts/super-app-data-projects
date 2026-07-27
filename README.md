# SwiftHub: Super-App Data Platform

End-to-end data platform simulating the analytics lifecycle of SwiftHub, a multi-service super app operating in the Indonesian market. Covers ride-hailing, food delivery, and fintech (QRIS payments).

## What This Is

A portfolio project that walks through the full data pipeline: generating realistic transaction data, validating it against strict contracts, transforming it with dbt into a star schema, serving it via FastAPI, and visualizing it in Streamlit.

Think of it as a mini-Gojek/Grab data stack, running locally.

## Tech Stack

- **Python** (Pandas, Numpy, Pydantic v2)
- **dbt + DuckDB** for transformations (Kimball star schema)
- **FastAPI** for the serving layer
- **Streamlit** for the dashboard (4 pages)
- **Pytest** for testing
- **Docker** for containerization
- **GitHub Actions** for CI

## Directory Layout

```
data/
  production/     # Processed parquet files (users, drivers, merchants, transactions)
  raw/            # Source data from generators
  sla_metrics.db  # SLA tracking database

dbt_project/      # All dbt stuff
  models/
    staging/      # Views over raw parquet files
    marts/        # Star schema tables (dim_*, fact_*)
  seeds/          # Static dimension tables (services, promotions)
  macros/         # Reusable SQL

api/              # FastAPI application
dashboard/        # Streamlit app
  pages/          # Individual dashboard pages

scripts/          # Data generation and streaming logic
  generate_entities.py       # Users, drivers, merchants
  generate_transactions.py   # Transaction records
  generate_dirty_data.py     # Intentionally bad data for DLQ testing
  generate_bulk.py           # Large-scale generator (not in git)
  stream_realtime.py         # Kafka-inspired streaming simulation
  sla_tracker.py             # Data quality tracking

tests/              # Pytest suite
terraform/          # GCP deployment config (reference only)
docs/               # Governance, forecasting, and insight docs
```

## Getting Started

### Local (recommended)

```bash
# Clone and install
git clone https://github.com/adespc/super-app-data-projects.git
cd super-app-data-projects
pip install -r requirements.txt
pip install dbt-duckdb==1.7.2

# Generate sample data
python scripts/generate_entities.py
python scripts/generate_transactions.py
python scripts/generate_dirty_data.py

# Transform with dbt
cd dbt_project
dbt run --vars '{"data_path": "../data/production"}'
dbt test

# Go back up and run the dashboard
cd ..
streamlit run dashboard/SwiftHub_Analytics.py
```

### Docker

```bash
docker-compose up --build
```

Dashboard at localhost:8501, API at localhost:8000.

### Makefile

```bash
make help          # list all targets
make pipeline      # generate data -> run dbt -> run tests
make generate-sample  # just the data
make dbt-full      # compile, run, test, docs
```

## Pipeline Overview

```
generate_entities.py  -->  parquet files
generate_transactions.py --> transactions + payments + locations
generate_dirty_data.py   --> DLQ (dead letter queue) for bad records

parquet files --> dbt staging views --> dbt marts (star schema)

star schema --> FastAPI (REST) --> Streamlit (dashboard)
```

## Data Quality

Data contracts are enforced at ingestion using Pydantic v2. Invalid records get routed to a DLQ instead of polluting the data models. The SLA tracker logs validation results to SQLite so you can see pass rates over time.

dbt also runs schema tests (unique, not_null, accepted_values) on every run.

## Engineering Decisions

### Why DuckDB over Postgres?
Wanted in-memory OLAP speed without running a database server. DuckDB reads parquet files directly, which is perfect for local development. Trade-off: no concurrent writes, but that's fine since transformations run sequentially.

### Why Pydantic v2 contracts?
Manual type checking is slow and error-prone when you have thousands of transactions from different services. Pydantic catches bad data at the gateway and routes it to the DLQ. Cost: more initial code, but prevents invalid entries from corrupting the warehouse.

### Why FastAPI?
The async event loop handles concurrent dashboard queries without much overhead. Simple REST endpoints for recent transactions and user profiles.

### Why Streamlit?
Quick to build, easy to share. Four pages: Executive Overview, Geospatial Intelligence, Fleet Operations, and Data SLA. Indonesian Rupiah formatting and bilingual support (EN/ID) built in.

## What I Learned

- **CPU throttling**: Simulating real-time Kafka broadcasts locally in Python hit 100% CPU. Fixed it with vectorized batch writes and dynamic sleep cycles (~50 events/sec).
- **SQLite for SLA tracking**: Works fine locally but wouldn't scale. In production, this should go to Prometheus or Datadog.
- **Currency formatting**: Streamlit doesn't natively format Indonesian Rupiah, so I wrote custom helpers in `utils_i18n.py`.
- **dbt path portability**: Hardcoded relative paths broke on different machines. Switched to dbt `vars` and it works everywhere now.

## Cloud Deployment

The `terraform/` directory has a reference GCP config (BigQuery, Cloud Run, GCS buckets). It's a starting point, not a finished deployment. To try it:

```bash
cd terraform
gcloud auth application-default login
terraform init
terraform plan -var="project_id=your-project-id"
```

## Tests

```bash
pytest tests/ -v
```

52 tests across 5 suites: API, validation, SLA tracking, integration, and streaming.

## Docs

- [Executive Summary](EXECUTIVE_SUMMARY.md)
- [Improvements Log](IMPROVEMENTS.md)
- [Improvements Round 2](IMPROVEMENTS_ROUND2.md)
- [Governance Guidelines](docs/governance_guidelines.md)
- [Insight Guidelines](docs/insight_guidelines.md)
- [Forecasting Guide](docs/forecasting_guide.md)

MIT License.
