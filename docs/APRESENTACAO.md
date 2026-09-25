# Roteiro — 12 minutos

## 0–4 min
Pergunta de negócio, fontes e defeitos.

## 4–12 min
Executar:
1. `python -m src.pipeline`
2. `dbt build`
3. mostrar RAW → staging → consumo.

## 12–16 min
Mostrar:
- DAG;
- Delta/time travel;
- decisão sobre `dataAtualizacao` ≠ `dataFinalizacao`;

## 16–20 min
Executar as duas consultas e interpretar:
1. tempo total por tipo/período;
2. etapa com maior tempo médio.

## Frase-chave
“Na massa analisada, a etapa com maior tempo médio representa concentração de permanência; não é, isoladamente, prova de causalidade.”
