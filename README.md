# Concilia Vagas — V5 BASE ORIGINAL ADAPTADA

## Pergunta de negócio

> **Quanto tempo, em média, uma solicitação de conciliação de vagas leva desde a data de entrada até a sua finalização, considerando o tipo de conflito e o período de entrada, e em qual etapa do processo está concentrado o maior tempo de espera?**

## Base usada

A fonte original `data/raw/solicitacoes.csv` foi preservada integralmente.

Para tornar a pergunta tecnicamente respondível, foram acrescentadas duas fontes sintéticas:
- `solicitacoes_complementares.csv`: casos finalizados em vários meses;
- `historico_etapas.json`: datas de início/fim das etapas e tipo de conflito.

Essa complementação é necessária porque o CSV original não contém finalização, etapas ou tipo de conflito e os casos finalizados originais estão concentrados em janeiro.

## Fluxo

FONTES → INGESTÃO → RAW → TRANSFORMAÇÃO → CONSUMO → RESPOSTA

## Execução

```bash
python -m pip install -r requirements.txt
python -m src.pipeline

cd dbt
python -m dbt.cli.main debug --profiles-dir .
python -m dbt.cli.main build --profiles-dir .
python -m dbt.cli.main docs generate --profiles-dir .
cd ..

python consultas/executar_respostas.py
python consultas/delta_time_travel.py
```

## Métricas

Tempo total:
`data_finalizacao - data_entrada`

Tempo da etapa:
`data_fim - data_inicio`

## Regra de apresentação

A consulta final lê apenas a camada de consumo. Não consulta RAW e não cria regras de negócio no WHERE.

## Limitação

Os números das fontes complementares são sintéticos para a PoC acadêmica.
