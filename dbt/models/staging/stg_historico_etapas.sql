-- GRÃO: uma linha por ocorrência de etapa.
-- Padroniza textos e converte datas; não define finalização.

select

    try_cast(idSolicitacao as integer) as id_solicitacao,

    case
        when upper(trim(tipoConflito)) = 'DISTANTE_DA_RESIDENCIA'
            then 'LONGE_DA_RESIDENCIA'
        else upper(trim(tipoConflito))
    end as tipo_conflito,

    upper(trim(etapa)) as etapa,

    try_cast(dataInicio as timestamp) as data_inicio,

    try_cast(dataFim as timestamp) as data_fim

from {{ ref('raw_historico_etapas') }}