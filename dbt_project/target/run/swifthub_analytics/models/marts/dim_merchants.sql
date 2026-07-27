
  
    
    

    create  table
      "swifthub"."main"."dim_merchants__dbt_tmp"
  
    as (
      

SELECT
    merchant_id,
    merchant_name,
    service_type,
    department,
    city,
    rating AS merchant_rating
FROM "swifthub"."main"."stg_merchants"
    );
  
  