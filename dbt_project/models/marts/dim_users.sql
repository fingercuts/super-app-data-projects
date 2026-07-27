{{ config(materialized='table') }}

SELECT
    user_id,
    name AS user_name,
    gender,
    age,
    city,
    region,
    loyalty_tier,
    churn_risk_score
FROM {{ ref('stg_users') }}
