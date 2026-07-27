{{ config(materialized='table') }}

SELECT
    merchant_id,
    merchant_name,
    service_type,
    department,
    city,
    rating AS merchant_rating
FROM {{ ref('stg_merchants') }}
