
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    protocolo as unique_field,
    count(*) as n_records

from "pipeline"."main"."consumo_tempo_conciliacao"
where protocolo is not null
group by protocolo
having count(*) > 1



  
  
      
    ) dbt_internal_test