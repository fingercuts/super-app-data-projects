

SELECT
    date_trunc('day', CAST(date AS TIMESTAMP)) AS transaction_date,
    department,
    service_id,
    COUNT(transaction_id) as total_tx_volume,
    SUM(total_amount) as total_gross_revenue,
    AVG(total_amount) as average_basket_size
FROM "swifthub"."main"."stg_transactions"
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 5 DESC