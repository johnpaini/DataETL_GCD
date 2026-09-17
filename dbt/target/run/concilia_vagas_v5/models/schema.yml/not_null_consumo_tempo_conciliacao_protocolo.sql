
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select protocolo
from "pipeline"."main"."consumo_tempo_conciliacao"
where protocolo is null



  
  
      
    ) dbt_internal_test