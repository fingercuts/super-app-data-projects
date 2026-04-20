# SwiftHub: Unified Analytics Platform for Super App Ecosystems

An end-to-end data platform simulating the complex analytics lifecycle of **SwiftHub**, a multi-service super app operating in the Indonesian market.

---

## Project Highlights

- **End-to-End Pipeline**: Unified data lifecycle from raw ingestion through DuckDB/dbt modeling to executive-level BI.
- **Real-time Engine**: Simulated Kafka broadcast and consumption layer for high-velocity transaction events.
- **Architectural Parity**: Implements a Kimball Star Schema (Fact + Dimensions) for optimized analytical performance.
- **Data Contracts**: Strict schema enforcement using Pydantic during the ingestion phase, ensuring high-fidelity data quality.
- **Technical Excellence**: Fully automated environment management via Makefile and cross-platform setup scripts.
- **Executive BI**: Multi-page Streamlit dashboard providing geospatial intelligence, fleet monitoring, and financial health metrics.

---

## Technical Stack

- **Languages**: Python (Pandas, Numpy, Pydantic), SQL
- **Workflow**: dbt (Data Build Tool)
- **Engine**: DuckDB (OLAP), FastAPI (Serving Layer)
- **Orchestration**: Vectorized Batch + Real-time Stream Emulation
- **Frontend**: Streamlit Executive Control Center
- **DevOps**: GitHub Actions CI, SQLFluff, Pytest, Docker

---

## Repository Structure

```text
data/
├── raw/            # Source CSV extracts
├── staging/        # Processed intermediate files
└── marts/          # Star schema tables (dbt output)

dbt_project/        # dbt models and schema tests
api/                # FastAPI application serving layer
dashboard/          # Streamlit executive overview
scripts/            # Real-time streaming and ingestion logic
tests/              # Pydantic validation and CI test suite
```

---

## Local Setup

The project provides a unified setup process for Windows environments.

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd super-app-data-projects
   ```

2. **Automated Setup**:
   Use the provided PowerShell script to initialize the environment, install dependencies, and configure dbt:
   ```powershell
   .\setup_env.ps1
   ```

3. **Manual Setup**:
   If you prefer manual configuration, use the Makefile:
   ```bash
   make install
   ```

---

## Data Pipeline Architecture

1. **Generation & Ingestion**: Vectorized Python scripts generate high-fidelity Super App data (Users, Drivers, Merchants, Transactions) with Indonesian locale specificity.
2. **Real-time Link**: A Kafka-inspired streaming layer simulates live transaction broadcasts.
3. **Transformation**: dbt transforms raw data into a Kimball Star Schema, enforcing data quality through automated tests.
4. **Serving**: A FastAPI layer provides recent transaction snapshots for operational monitoring.
5. **Insights**: The Streamlit dashboard serves as the final consumption layer for executive decision-making.

---

## Documentation

- [**Executive Summary**](EXECUTIVE_SUMMARY.md): Strategic overview and business impact analysis.
- [**Governance Guide**](docs/governance_guidelines.md): PII masking and data quality enforcement strategies.
- [**Insight Reference**](docs/insight_guidelines.md): Key Performance Indicator (KPI) definitions for Super App services.
- [**Forecasting Manual**](docs/forecasting_guide.md): Analysis of seasonal trends and Indonesian market dynamics.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.
