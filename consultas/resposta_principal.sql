-- PERGUNTA PRINCIPAL:
-- Quanto tempo, em média, uma solicitação leva da entrada à finalização,
-- considerando tipo de conflito e período de entrada?
select
    tipo_conflito,
    periodo_entrada,
    count(*) as quantidade_solicitacoes,
    round(avg(tempo_total_conciliacao_dias), 2) as tempo_medio_dias
from consumo_tempo_conciliacao
group by tipo_conflito, periodo_entrada
order by periodo_entrada, tipo_conflito;
