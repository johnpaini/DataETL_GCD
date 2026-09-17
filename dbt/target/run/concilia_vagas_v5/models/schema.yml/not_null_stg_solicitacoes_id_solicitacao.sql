
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select id_solicitacao
from "pipeline"."main"."stg_solicitacoes"
where id_solicitacao is null



  
  
      
    ) dbt_internal_test