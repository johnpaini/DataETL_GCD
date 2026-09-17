# Dicionário

| Campo | Origem | Significado |
|---|---|---|
| id_solicitacao | CSV | Identificador |
| protocolo | CSV | Protocolo |
| data_entrada | CSV | Data de entrada |
| status | CSV | Situação da solicitação |
| tipo_conflito | JSON | Tipo do conflito |
| etapa | JSON | Etapa do processo |
| data_inicio | JSON | Início da etapa |
| data_fim | JSON | Fim da etapa |
| data_finalizacao | derivado | Maior data_fim válida |
| periodo_entrada | derivado | Mês da entrada |
| tempo_total_conciliacao_dias | derivado | Finalização menos entrada |
| tempo_espera_etapa_dias | derivado | Fim menos início da etapa |
