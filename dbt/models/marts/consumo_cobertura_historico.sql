-- GRÃO: uma linha com os indicadores de cobertura do histórico.

with finalizadas as (
    select count(*) as total_finalizadas
    from {{ ref('stg_solicitacoes') }}
    where status = 'FINALIZADA'
      and id_solicitacao is not null
),

analisadas as (
    select count(*) as total_analisadas
    from {{ ref('consumo_tempo_conciliacao') }}
)

select
    f.total_finalizadas,
    a.total_analisadas,
    round(
        100.0 * a.total_analisadas / nullif(f.total_finalizadas, 0),
        1
    ) as cobertura_historico_percentual
from finalizadas f
cross join analisadas a