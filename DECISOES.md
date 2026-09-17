# DECISOES.md — V5 baseada na massa original

## 1. Arquitetura
FONTES → INGESTÃO → PRESERVAÇÃO DO BRUTO → TRANSFORMAÇÃO → CONSUMO → RESPOSTA.

## 2. Preservação da fonte original
O `solicitacoes.csv` enviado é mantido exatamente como recebido, inclusive defeitos.

## 3. Por que duas fontes complementares?
A fonte original não contém data de finalização, histórico de etapas nem tipo de conflito.
Também possui registros finalizados concentrados em janeiro.

Por isso:
- `solicitacoes_complementares.csv` adiciona casos sintéticos finalizados em vários meses;
- `historico_etapas.json` fornece as datas de início/fim das etapas e o tipo de conflito.

Isso torna os cortes pedidos pela pergunta respondíveis sem falsificar a semântica de `dataAtualizacao`.

## 4. Grão principal
`consumo_tempo_conciliacao`: uma linha por solicitação finalizada com histórico completo e válido.

## 5. Métrica principal
`tempo_total_conciliacao_dias = data_finalizacao - data_entrada`.

`data_finalizacao` é o fim da última etapa válida (`FINALIZACAO`), e não `dataAtualizacao`.

## 6. Grão de etapa
`consumo_tempo_etapas`: uma linha por solicitação e etapa válida.

`tempo_espera_etapa_dias = data_fim - data_inicio`.

## 7. Tipo de conflito
A dimensão é fornecida pelo histórico sintético complementar. Os valores são controlados para permitir o corte analítico solicitado.

## 8. Período de entrada
É derivado diretamente de `data_entrada`, no formato `YYYY-MM`.

## 9. Registros inválidos
Defeitos que impedem cálculo seguro são preservados na RAW e identificados na quarentena. Solicitações não finalizadas não são transformadas em “zero dias”.

## 10. Gargalo
“Maior tempo de espera” é operacionalizado como maior tempo médio de permanência observado por etapa. Isso não prova causalidade nem restrição de capacidade.
