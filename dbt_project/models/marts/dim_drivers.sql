{{ config(materialized='table') }}

SELECT
    driver_id,
    name AS driver_name,
    gender,
    age,
    city,
    vehicle_type,
    driver_rating,
    COUNT(*) OVER (PARTITION BY city) AS city_driver_count,
    AVG(driver_rating) OVER (PARTITION BY vehicle_type) AS vehicle_avg_rating
FROM {{ ref('stg_drivers') }}
