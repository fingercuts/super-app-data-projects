{{ config(materialized='table') }}

-- Customer lifetime value estimation per user based on transaction history
-- Uses window functions to calculate cumulative spend, frequency, and recency

WITH user_metrics AS (
    SELECT
        t.user_id,
        u.name AS user_name,
        u.city,
        u.region,
        u.loyalty_tier,
        u.churn_risk_score,
        COUNT(DISTINCT t.transaction_id) AS total_transactions,
        SUM(t.total_amount) AS lifetime_value,
        ROUND(AVG(t.total_amount), 2) AS avg_order_value,
        MIN(t.date) AS first_transaction_date,
        MAX(t.date) AS last_transaction_date,
        DATEDIFF('day', MIN(t.date), MAX(t.date)) + 1 AS active_days,
        CASE
            WHEN DATEDIFF('day', MIN(t.date), MAX(t.date)) + 1 > 0
            THEN ROUND(CAST(COUNT(DISTINCT DATE(t.date)) AS DOUBLE) / (DATEDIFF('day', MIN(t.date), MAX(t.date)) + 1), 4)
            ELSE 0
        END AS purchase_frequency,
        DATEDIFF('day', MAX(t.date), '{{ var("end_date", "2024-12-31") }}') AS days_since_last_purchase
    FROM {{ ref('stg_transactions') }} t
    JOIN {{ ref('stg_users') }} u ON t.user_id = u.user_id
    GROUP BY t.user_id, u.name, u.city, u.region, u.loyalty_tier, u.churn_risk_score
)

SELECT
    *,
    CASE
        WHEN lifetime_value > quantile_cont(lifetime_value, 0.8) OVER () THEN 'High'
        WHEN lifetime_value > quantile_cont(lifetime_value, 0.5) OVER () THEN 'Medium'
        ELSE 'Low'
    END AS customer_segment
FROM user_metrics
