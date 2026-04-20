
  
    
    

    create  table
      "swifthub"."main"."fact_daily_revenue__dbt_tmp"
  
    as (
      

WITH raw_transactions AS (
    -- DuckDB natively binds exactly to local massive parquet files
    SELECT *
    FROM read_parquet('../data/production/transactions.parquet')
)

SELECT
    date_trunc('day', CAST(date AS TIMESTAMP)) AS transaction_date,
    department,
    service_id,
    COUNT(transaction_id) as total_tx_volume,
    SUM(total_amount) as total_gross_revenue,
    AVG(total_amount) as average_basket_size
FROM raw_transactions
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 5 DESC
    );
  
  