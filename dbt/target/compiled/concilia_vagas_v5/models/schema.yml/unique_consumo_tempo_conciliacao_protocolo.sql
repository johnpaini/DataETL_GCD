
    
    

select
    protocolo as unique_field,
    count(*) as n_records

from "pipeline"."main"."consumo_tempo_conciliacao"
where protocolo is not null
group by protocolo
having count(*) > 1


