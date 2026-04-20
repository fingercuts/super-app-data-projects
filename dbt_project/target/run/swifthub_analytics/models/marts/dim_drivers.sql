
  
    
    

    create  table
      "swifthub"."main"."dim_drivers__dbt_tmp"
  
    as (
      

SELECT
    *
FROM "swifthub"."main"."stg_drivers"
    );
  
  