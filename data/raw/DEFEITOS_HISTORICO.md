# Defeitos — historico_etapas.json

Esta fonte foi **gerada sinteticamente** para complementar a massa original.
A fonte CSV original não possui datas de início/fim das etapas necessárias
para calcular o tempo até finalização nem o tempo de permanência por etapa.

Defeitos intencionais:
1. Uma ocorrência de etapa está duplicada.
2. Uma `dataFim` está inválida.

Tratamento:
- RAW preserva os defeitos.
- A transformação deduplica ocorrências exatas para cálculo.
- Datas inválidas são encaminhadas à lógica de quarentena e não entram nas métricas.
