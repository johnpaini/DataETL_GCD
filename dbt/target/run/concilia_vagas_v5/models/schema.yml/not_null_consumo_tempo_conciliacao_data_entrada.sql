
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select data_entrada
from "pipeline"."main"."consumo_tempo_conciliacao"
where data_entrada is null



  
  
      
    ) dbt_internal_test