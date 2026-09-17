
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select tipo_conflito
from "pipeline"."main"."stg_historico_etapas"
where tipo_conflito is null



  
  
      
    ) dbt_internal_test