
    

    create  table
      "pipeline"."main"."consumo_tempo_conciliacao__dbt_tmp"
  
    
    as (
      -- GRÃO: uma linha por solicitação FINALIZADA com as cinco etapas válidas.
-- Wide table: adequada para responder diretamente à pergunta principal.
--
-- Métrica derivada:
-- tempo_total_conciliacao_dias = data_finalizacao - data_entrada
with etapas as (
    select *
    from "pipeline"."main"."stg_historico_etapas"
    where data_inicio is not null
      and data_fim is not null
      and data_fim >= data_inicio
    qualify row_number() over (
        partition by id_solicitacao, etapa, data_inicio, data_fim
        order by id_solicitacao
    ) = 1
),
solicitacoes as (
    select *
    from "pipeline"."main"."stg_solicitacoes"
    where id_solicitacao is not null
      and protocolo is not null
      and data_entrada is not null
      and status = 'FINALIZADA'
),
base as (
    select
        s.id_solicitacao,
        s.protocolo,
        h.tipo_conflito,
        s.data_entrada,
        max(h.data_fim) as data_finalizacao,
        strftime(s.data_entrada, '%Y-%m') as periodo_entrada,
        datediff('day', s.data_entrada, max(h.data_fim)) as tempo_total_conciliacao_dias
    from solicitacoes s
    join etapas h using (id_solicitacao)
    group by 1,2,3,4
    having count(distinct h.etapa) = 5
)
select *
from base
where data_finalizacao >= data_entrada
    );
    
  