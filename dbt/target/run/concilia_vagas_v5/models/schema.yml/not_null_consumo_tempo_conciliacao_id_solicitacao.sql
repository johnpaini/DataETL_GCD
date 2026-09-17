
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select id_solicitacao
from "pipeline"."main"."consumo_tempo_conciliacao"
where id_solicitacao is null



  
  
      
    ) dbt_internal_test