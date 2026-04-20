
  
    
    

    create  table
      "swifthub"."main"."fct_transactions__dbt_tmp"
  
    as (
      

SELECT
    *
FROM "swifthub"."main"."stg_transactions"
    );
  
  