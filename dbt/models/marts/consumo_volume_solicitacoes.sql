-- GRÃO: uma linha por período de entrada e status.
--
-- Objetivo:
-- apresentar o volume de solicitações sem depender da existência
-- de histórico de etapas.

select
    strftime(data_entrada, '%Y-%m') as periodo_entrada,
    status,
    count(*) as quantidade_solicitacoes
from {{ ref('stg_solicitacoes') }}
where id_solicitacao is not null
  and data_entrada is not null
  and status in ('FINALIZADA', 'EM_ANALISE', 'REGISTRADA')
group by
    periodo_entrada,
    status
order by
    periodo_entrada,
    status