
  
  create view "concilia_vagas"."main"."raw_solicitacoes__dbt_tmp" as (
    -- GRÃO: uma linha por registro recebido no CSV RAW.
-- Sem regra de negócio: apenas exposição da captura.
select * from solicitacoes
  );
