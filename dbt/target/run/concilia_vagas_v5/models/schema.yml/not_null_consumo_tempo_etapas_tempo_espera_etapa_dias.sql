
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select tempo_espera_etapa_dias
from "pipeline"."main"."consumo_tempo_etapas"
where tempo_espera_etapa_dias is null



  
  
      
    ) dbt_internal_test