
    
    

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


