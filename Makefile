.PHONY: install tests batch dbt stream

# Install all dependencies
install:
	pip install -r requirements.txt
	pip install dbt-duckdb==1.7.2 pre-commit
	pre-commit install

# Run local pytest validations (Tests our Pydantic contracts)
test:
	pytest tests/ -v

# Run the Vectorized Data Generator
batch:
	python scripts/generate_all.py

# Run Git Hygiene validation
pre-commit:
	pre-commit run --all-files

# Run the Data Build Tool Local DuckDB Aggregation
dbt-run:
	cd dbt_project && dbt run

# Stand up the Local Airflow and Kafka Cluster
cluster-up:
	docker-compose up -d

# Spin down the cluster safely
cluster-down:
	docker-compose down

# Start broadcasting live streams locally
stream:
	python scripts/stream_realtime.py

# Intercept live streams
consume:
	python scripts/consume_realtime.py
