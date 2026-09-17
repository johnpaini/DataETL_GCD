
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        etapa as value_field,
        count(*) as n_records

    from "pipeline"."main"."stg_historico_etapas"
    group by etapa

)

select *
from all_values
where value_field not in (
    'RECEPCAO_TRIAGEM','ANALISE','NEGOCIACAO','VALIDACAO','FINALIZACAO'
)



  
  
      
    ) dbt_internal_test