-- GRÃO: uma linha por ocorrência que impede o cálculo seguro.
select id_solicitacao, 'ID_INVALIDO' as motivo
from "pipeline"."main"."stg_solicitacoes"
where id_solicitacao is null

union all
select id_solicitacao, 'PROTOCOLO_VAZIO'
from "pipeline"."main"."stg_solicitacoes"
where protocolo is null

union all
select id_solicitacao, 'DATA_ENTRADA_INVALIDA'
from "pipeline"."main"."stg_solicitacoes"
where data_entrada is null

union all
select id_solicitacao, 'SOLICITACAO_NAO_FINALIZADA'
from "pipeline"."main"."stg_solicitacoes"
where status <> 'FINALIZADA'

union all
select id_solicitacao, 'DATA_ETAPA_INVALIDA'
from "pipeline"."main"."stg_historico_etapas"
where data_inicio is null or data_fim is null

union all
select id_solicitacao, 'DATA_FIM_ANTES_INICIO'
from "pipeline"."main"."stg_historico_etapas"
where data_inicio is not null
  and data_fim is not null
  and data_fim < data_inicio

union all
select id_solicitacao, 'ETAPA_DUPLICADA'
from (
    select id_solicitacao, etapa, data_inicio, data_fim,
           count(*) over(partition by id_solicitacao, etapa, data_inicio, data_fim) as qtd
    from "pipeline"."main"."stg_historico_etapas"
) x
where qtd > 1