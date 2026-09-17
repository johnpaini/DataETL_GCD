
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    id_solicitacao as unique_field,
    count(*) as n_records

from "pipeline"."main"."consumo_tempo_conciliacao"
where id_solicitacao is not null
group by id_solicitacao
having count(*) > 1



  
  
      
    ) dbt_internal_test