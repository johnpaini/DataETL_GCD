
    

    create  table
      "pipeline"."main"."consumo_tempo_etapas__dbt_tmp"
  
    
    as (
      -- GRÃO: uma linha por solicitação e etapa válida.
-- Permite identificar a etapa com maior tempo médio de permanência.
select
    s.id_solicitacao,
    s.protocolo,
    h.tipo_conflito,
    s.data_entrada,
    h.etapa,
    h.data_inicio,
    h.data_fim,
    datediff('day', h.data_inicio, h.data_fim) as tempo_espera_etapa_dias
from "pipeline"."main"."stg_solicitacoes" s
join "pipeline"."main"."stg_historico_etapas" h using (id_solicitacao)
where s.status = 'FINALIZADA'
  and s.id_solicitacao is not null
  and s.protocolo is not null
  and s.data_entrada is not null
  and h.data_inicio is not null
  and h.data_fim is not null
  and h.data_fim >= h.data_inicio
qualify row_number() over (
    partition by h.id_solicitacao, h.etapa, h.data_inicio, h.data_fim
    order by h.id_solicitacao
) = 1
    );
    
  