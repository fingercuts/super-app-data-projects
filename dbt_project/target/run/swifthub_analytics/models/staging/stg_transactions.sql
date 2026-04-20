
  
  create view "swifthub"."main"."stg_transactions__dbt_tmp" as (
    

WITH raw_transactions AS (
    SELECT * FROM read_parquet('../data/production/transactions.parquet')
)

SELECT
    CAST(transaction_id AS VARCHAR) AS transaction_id,
    CAST(date AS TIMESTAMP) AS transaction_timestamp,
    CAST(user_id AS VARCHAR) AS user_id,
    CAST(driver_id AS VARCHAR) AS driver_id,
    CAST(merchant_id AS VARCHAR) AS merchant_id,
    CAST(service_id AS VARCHAR) AS service_id,
    CAST(quantity AS INTEGER) AS quantity,
    CAST(base_amount AS DOUBLE) AS base_amount,
    CAST(discounted_amount AS DOUBLE) AS discounted_amount,
    CAST(total_amount AS DOUBLE) AS total_amount,
    CAST(payment_method AS VARCHAR) AS payment_method,
    CAST(department AS VARCHAR) AS department,
    CAST(city AS VARCHAR) AS city,
    CAST(region AS VARCHAR) AS region,
    CAST(promotion_id AS VARCHAR) AS promotion_id
FROM raw_transactions
  );
