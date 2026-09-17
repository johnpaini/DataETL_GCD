
  
  create view "pipeline"."main"."raw_historico_etapas__dbt_tmp" as (
    -- GRÃO: uma linha por ocorrência recebida no JSON RAW.
-- Sem regra de negócio: apenas exposição da captura.
select * from historico_etapas
  );
