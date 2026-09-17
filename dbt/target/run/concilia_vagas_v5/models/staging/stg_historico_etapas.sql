
  
  create view "pipeline"."main"."stg_historico_etapas__dbt_tmp" as (
    -- GRÃO: uma linha por ocorrência de etapa.
-- Padroniza textos e converte datas; não define finalização.
select
    try_cast(idSolicitacao as integer) as id_solicitacao,
    upper(trim(tipoConflito)) as tipo_conflito,
    upper(trim(etapa)) as etapa,
    try_cast(dataInicio as timestamp) as data_inicio,
    try_cast(dataFim as timestamp) as data_fim
from "pipeline"."main"."raw_historico_etapas"
  );
