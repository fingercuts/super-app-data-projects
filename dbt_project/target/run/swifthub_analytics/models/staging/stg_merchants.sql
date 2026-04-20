
  
  create view "swifthub"."main"."stg_merchants__dbt_tmp" as (
    

WITH raw_merchants AS (
    SELECT * FROM read_parquet('../data/production/merchants.parquet')
)

SELECT
    CAST(merchant_id AS VARCHAR) AS merchant_id,
    CAST(merchant_name AS VARCHAR) AS merchant_name,
    CAST(service_type AS VARCHAR) AS service_type,
    CAST(department AS VARCHAR) AS department,
    CAST(city AS VARCHAR) AS city,
    CAST(rating AS DOUBLE) AS merchant_rating
FROM raw_merchants
  );
