
  
    
    

    create  table
      "swifthub"."main"."dim_users__dbt_tmp"
  
    as (
      

SELECT
    user_id,
    name AS user_name,
    gender,
    age,
    city,
    region,
    loyalty_tier,
    churn_risk_score
FROM "swifthub"."main"."stg_users"
    );
  
  