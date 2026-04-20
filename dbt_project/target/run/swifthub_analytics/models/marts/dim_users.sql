
  
    
    

    create  table
      "swifthub"."main"."dim_users__dbt_tmp"
  
    as (
      

SELECT
    *
FROM "swifthub"."main"."stg_users"
    );
  
  