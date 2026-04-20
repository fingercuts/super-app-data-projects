

WITH raw_users AS (
    SELECT * FROM read_parquet('../data/production/users.parquet')
)

SELECT
    CAST(user_id AS VARCHAR) AS user_id,
    CAST(name AS VARCHAR) AS name,
    CAST(gender AS VARCHAR) AS gender,
    CAST(age AS INTEGER) AS age,
    CAST(city AS VARCHAR) AS city,
    CAST(region AS VARCHAR) AS region,
    CAST(loyalty_tier AS VARCHAR) AS loyalty_tier,
    CAST(churn_risk_score AS DOUBLE) AS churn_risk_score
FROM raw_users