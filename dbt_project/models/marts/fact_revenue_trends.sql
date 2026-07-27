{{ config(materialized='table') }}

-- Revenue trend analysis by day, department, and service
-- Includes rolling averages and growth calculations

SELECT
    date_trunc('day', t.date) AS transaction_date,
    t.department,
    t.service_id,
    COUNT(*) AS transaction_count,
    SUM(t.quantity) AS total_items,
    SUM(t.base_amount) AS gross_revenue,
    SUM(t.discounted_amount) AS total_discounts,
    SUM(t.total_amount) AS net_revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_transaction_value,
    ROUND(
        AVG(SUM(t.total_amount)) OVER (
            PARTITION BY t.department
            ORDER BY date_trunc('day', t.date)
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS revenue_7d_moving_avg,
    CASE
        WHEN LAG(SUM(t.total_amount)) OVER (
            PARTITION BY t.department ORDER BY date_trunc('day', t.date)
        ) > 0 THEN ROUND(
            (SUM(t.total_amount) - LAG(SUM(t.total_amount)) OVER (
                PARTITION BY t.department ORDER BY date_trunc('day', t.date)
            )) * 100.0 / LAG(SUM(t.total_amount)) OVER (
                PARTITION BY t.department ORDER BY date_trunc('day', t.date)
            ), 2
        )
        ELSE NULL
    END AS day_over_day_change_pct
FROM {{ ref('stg_transactions') }} t
GROUP BY date_trunc('day', t.date), t.department, t.service_id
ORDER BY transaction_date, t.department
