
  
    
    

    create  table
      "swifthub"."main"."dim_merchants__dbt_tmp"
  
    as (
      

SELECT
    *
FROM "swifthub"."main"."stg_merchants"
    );
  
  