
  
  create view "pipeline"."main"."stg_solicitacoes__dbt_tmp" as (
    -- GRÃO: uma linha por solicitação capturada.
-- A união das duas fontes preserva o histórico original e adiciona a massa
-- complementar explicitamente sintética.
select
    try_cast(id as integer) as id_solicitacao,
    nullif(trim(protocolo), '') as protocolo,
    upper(replace(trim(status), ' ', '_')) as status,
    lower(trim(aceiteInstrucoes)) as aceite_instrucoes,
    try_cast(dataCriacao as timestamp) as data_entrada,
    try_cast(dataAtualizacao as timestamp) as data_atualizacao,
    'ORIGINAL' as origem_fonte
from "pipeline"."main"."raw_solicitacoes"

union all

select
    try_cast(id as integer) as id_solicitacao,
    nullif(trim(protocolo), '') as protocolo,
    upper(replace(trim(status), ' ', '_')) as status,
    lower(trim(aceiteInstrucoes)) as aceite_instrucoes,
    try_cast(dataCriacao as timestamp) as data_entrada,
    try_cast(dataAtualizacao as timestamp) as data_atualizacao,
    'COMPLEMENTAR_SINTETICA' as origem_fonte
from "pipeline"."main"."raw_solicitacoes_complementares"
  );
