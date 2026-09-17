-- PERGUNTA COMPLEMENTAR:
-- Em qual etapa está concentrado o maior tempo médio de espera?
select
    etapa,
    count(*) as quantidade_ocorrencias,
    round(avg(tempo_espera_etapa_dias), 2) as tempo_medio_espera_dias,
    sum(tempo_espera_etapa_dias) as tempo_total_dias
from consumo_tempo_etapas
group by etapa
order by tempo_medio_espera_dias desc;
