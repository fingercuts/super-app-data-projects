.PHONY: install test batch dbt-run dbt-test dbt-docs dbt-full api dashboard stream consume cluster-up cluster-down generate-all generate-sample docker-build docker-run docker-clean pipeline help lint-sql lint-fix clean

# Default target
help: ## Show this help message
	@echo "SwiftHub Data Platform - Available Commands"
	@echo "=============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Install all dependencies
install: ## Install Python dependencies and set up pre-commit hooks
	pip install -r requirements.txt
	pip install dbt-duckdb==1.7.2 pre-commit
	pre-commit install

# Run local pytest validations (Tests our Pydantic contracts)
test: ## Run pytest validation suite
	pytest tests/ -v

# Run the Vectorized Data Generator (sample)
batch: ## Run sample data generation pipeline
	python scripts/generate_all.py

# Run full-scale data generation (requires generate_bulk.py)
generate-all: ## Run full-scale data generation
	python scripts/generate_bulk.py

# Generate only sample data (safe to run repeatedly)
generate-sample: ## Generate sample dataset for quick testing
	python scripts/generate_entities.py
	python scripts/generate_transactions.py
	python scripts/generate_dirty_data.py

# Run Git Hygiene validation
pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

# Run the Data Build Tool Local DuckDB Aggregation
dbt-run: ## Run dbt models to transform data
	cd dbt_project && dbt run --vars '{"data_path": "../data/production"}'

# Compile and validate dbt models (no execution)
dbt-compile: ## Compile dbt models for syntax validation
	cd dbt_project && dbt compile --vars '{"data_path": "../data/production"}'

# Run dbt tests (data quality checks)
dbt-test: ## Run dbt data quality tests
	cd dbt_project && dbt test --vars '{"data_path": "../data/production"}'

# Generate dbt documentation
dbt-docs: ## Generate dbt documentation site
	cd dbt_project && dbt docs generate && dbt docs serve

# Full dbt pipeline (compile + run + test + docs)
dbt-full: dbt-compile dbt-run dbt-test dbt-docs ## Run complete dbt pipeline

# Start FastAPI server
api: ## Start the FastAPI serving layer
	uvicorn api.main:app --reload --port 8000

# Start Streamlit dashboard
dashboard: ## Start the Streamlit executive dashboard
	streamlit run dashboard/SwiftHub_Analytics.py --server.port 8501 --server.address 0.0.0.0

# Run the realtime streaming simulator
stream: ## Start broadcasting live streams locally
	python scripts/stream_realtime.py

# Intercept live streams
consume: ## Consume live streams from Kafka
	python scripts/consume_realtime.py

# Stand up the Local Airflow and Kafka Cluster
cluster-up: ## Start Docker services (Kafka, Airflow, PostgreSQL)
	docker-compose up -d zookeeper kafka postgres

# Spin down the cluster safely
cluster-down: ## Stop and remove Docker services
	docker-compose down

# Full pipeline: generate data -> run dbt -> test
pipeline: generate-sample dbt-full ## Run the complete data pipeline

# Docker build and run
docker-build: ## Build the Docker image
	docker build -t swifthub:latest .

docker-run: ## Run the full stack with Docker
	docker-compose up --build

docker-clean: ## Clean Docker images and volumes
	docker-compose down -v
	docker system prune -f

# SQL linting
lint-sql: ## Lint SQL models with SQLFluff
	sqlfluff lint dbt_project/models/ --dialect duckdb

lint-fix: ## Auto-fix SQL linting issues
	sqlfluff fix dbt_project/models/ --dialect duckdb

# Clean generated artifacts
clean: ## Clean generated data, logs, and build artifacts
	rm -rf dbt_project/target
	rm -rf dbt_project/dbt_packages
	rm -rf dbt_project/logs
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	echo "Cleaned build artifacts and cache files."
