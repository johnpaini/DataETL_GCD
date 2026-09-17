
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select tempo_total_conciliacao_dias
from "pipeline"."main"."consumo_tempo_conciliacao"
where tempo_total_conciliacao_dias is null



  
  
      
    ) dbt_internal_test