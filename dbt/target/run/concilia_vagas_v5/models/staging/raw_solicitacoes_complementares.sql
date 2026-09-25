
  
  create view "pipeline"."main"."raw_solicitacoes_complementares__dbt_tmp" as (
    select * from solicitacoes_complementares
  );
