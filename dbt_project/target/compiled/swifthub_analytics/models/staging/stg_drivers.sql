

WITH raw_drivers AS (
    SELECT * FROM read_parquet('../data/production/drivers.parquet')
)

SELECT
    CAST(driver_id AS VARCHAR) AS driver_id,
    CAST(name AS VARCHAR) AS name,
    CAST(gender AS VARCHAR) AS gender,
    CAST(age AS INTEGER) AS age,
    CAST(city AS VARCHAR) AS city,
    CAST(vehicle_type AS VARCHAR) AS vehicle_type,
    CAST(rating AS DOUBLE) AS driver_rating
FROM raw_drivers