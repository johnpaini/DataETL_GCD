-- GRÃO: uma linha por solicitação.
--
-- Regra de precedência:
-- 1. A fonte ORIGINAL é a fonte principal.
-- 2. A fonte COMPLEMENTAR_SINTETICA somente adiciona solicitações
--    cujo id ainda não existe na fonte ORIGINAL.
--
-- Dessa forma, uma solicitação presente nas duas fontes não é duplicada
-- e os dados da fonte principal são preservados.
--
-- Normalização de status:
-- `EM_ANALISE` e `EM_ANÁLISE` representam o mesmo status.
-- A representação canônica adotada no staging é `EM_ANALISE`.

with original as (

    select
        try_cast(id as integer) as id_solicitacao,
        protocolo,
        case
            when upper(trim(status)) = 'EM_ANÁLISE' then 'EM_ANALISE'
            else upper(trim(status))
        end as status,
        aceiteInstrucoes as aceite_instrucoes,
        try_cast(dataCriacao as timestamp) as data_entrada,
        try_cast(dataAtualizacao as timestamp) as data_atualizacao,
        'ORIGINAL' as origem_fonte
    from "pipeline"."main"."raw_solicitacoes"

),

complementar as (

    select
        try_cast(id as integer) as id_solicitacao,
        protocolo,
        case
        when replace(upper(trim(status)), ' ', '_') in (
            'EM_ANALISE',
            'EM_ANÁLISE'
        ) then 'EM_ANALISE'
        else upper(trim(status))
        end as status,
        aceiteInstrucoes as aceite_instrucoes,
        try_cast(dataCriacao as timestamp) as data_entrada,
        try_cast(dataAtualizacao as timestamp) as data_atualizacao,
        'COMPLEMENTAR_SINTETICA' as origem_fonte
    from "pipeline"."main"."raw_solicitacoes_complementares"

),

complementar_sem_original as (

    select c.*
    from complementar c
    where not exists (
        select 1
        from original o
        where o.id_solicitacao = c.id_solicitacao
    )

)

select *
from original

union all

select *
from complementar_sem_original