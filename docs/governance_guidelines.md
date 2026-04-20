# Data Governance & PII Framework

This document outlines the controls implemented in the SwiftHub Data Platform to manage sensitive information (PII) and ensure analytical utility while adhering to Indonesian data privacy standards.

## PII Masking Strategy
The project uses a custom dbt masking strategy and Pydantic validation to standardize how sensitive fields are handled.

| Category | Field(s) | Implementation | Rationale |
| :--- | :--- | :--- | :--- |
| **Identifiability** | User Name | Full Redaction (`****`) | Not required for aggregate analytical trends. |
| **Connectivity** | Email | Deterministic Hashing | Allows "blind joins" between datasets while preventing identity exposure. |
| **Geospatial** | Coordinate Detail | Precision Jittering | Preserves regional density patterns (Hotspots) while protecting exact home/office locations. |

## Access Control Layers
To support different business functions, we maintain a multi-layer view of the data:

### 1. Analytical Layer (Gold)
- **Audience**: BI dashboards, data analysts, executive stakeholders.
- **Exposure**: Contains only masked, hashed, and aggregated values.
- **Utility**: Suitable for large-scale trend analysis and KPI calculation.

### 2. Operational Layer (Silver)
- **Audience**: System administrators, data engineers.
- **Exposure**: Partially de-identified data used for debugging and reconciliation.

## Quality & Lineage
Governance is integrated into the pipeline flow:
1.  **Ingestion Validation**: Pydantic models flag invalid schema types and PII irregularities at the border.
2.  **Staging Cleanse**: dbt models apply masking logic immediately upon entry to the SQL warehouse.
3.  **Dead Letter Queue (DLQ)**: Records that fail data contract validation are isolated for audit without halting the production pipeline.
