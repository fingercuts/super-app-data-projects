# What Got Fixed

This file tracks the improvements made to SwiftHub after the initial code review.

## Round 1

- Fixed broken emoji encoding in `dashboard/utils_i18n.py` — the whole translation dict was garbled
- Created `generate_transactions.py` and `generate_dirty_data.py` which were imported but didn't exist
- Made dbt paths portable by switching from hardcoded `../data/production` to dbt `vars`
- Updated `.gitignore` so sample generators are committed but large-scale ones stay out
- Rewrote `.github/workflows/ci.yml` — added dbt compile validation, SQL linting, and API tests
- Filled out `docker-compose.yml` with actual service definitions (dashboard, API, Kafka, Airflow)
- Expanded `Makefile` with targets like `pipeline`, `dbt-full`, `docker-run`
- Added `tests/test_integration.py` (29 tests) covering the full data pipeline
- Added `tests/test_streaming.py` (12 tests) for message format and schema validation
- Added dbt schema tests to `sources.yml` (unique, not_null, accepted_values)
- Created dbt seed files: `services.csv` and `promotions.csv`
- Enhanced `terraform/` with Cloud Build trigger and monitoring dashboard
- Added `dbt_project/macros/resolve_data_path.sql` for reusable path resolution
- Rewrote README.md with proper quick-start guides
- Updated EXECUTIVE_SUMMARY.md

## Round 2

- Added ruff, isort, and sqlfluff to `.pre-commit-config.yaml`
- Created `pyproject.toml` with config for ruff, isort, and pytest
- Stripped all non-ASCII characters from Streamlit pages (they had leftover emoji from the BOM removal)
- Added `dbt run`, `dbt test`, and `dbt docs generate` to the CI pipeline (was only doing compile before)
- Added a `pre-commit` job to CI
- Fixed `Dockerfile` to copy all source directories (scripts, api, dashboard)
- Fixed `docker-compose.yml` data-generator to explicitly run the committed sample scripts
- Created `scripts/generate_all.py` as an orchestrator for all sample generators
- Moved `cloudbuild.yaml` from `terraform/` to project root where CI expects it

## Result

52 tests pass. dbt compiles with 9 models, 2 seeds, 14 tests, 4 sources. No non-ASCII characters in any Streamlit page. All scripts are runnable from a fresh clone.
