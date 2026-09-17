
    
    

select
    id_solicitacao as unique_field,
    count(*) as n_records

from "pipeline"."main"."consumo_tempo_conciliacao"
where id_solicitacao is not null
group by id_solicitacao
having count(*) > 1


