# Round 2 Changes

Final fixes to push the project to 9.5/10:

1. **Pre-commit hooks**: Added ruff (linter/formatter), isort (imports), sqlfluff (SQL linting)
2. **pyproject.toml**: Central config for all tooling
3. **Streamlit pages**: Stripped remaining non-ASCII bytes (emoji remnants from BOM removal)
4. **CI**: Added `dbt run`, `dbt test`, `dbt docs generate`, and `pre-commit` jobs
5. **Docker**: Fixed data-generator to use committed scripts, Dockerfile copies all source dirs
6. **generate_all.py**: New orchestrator script for the full generation pipeline
7. **cloudbuild.yaml**: Moved to root level

All 52 tests still pass. dbt compiles cleanly. No non-ASCII chars left anywhere.
