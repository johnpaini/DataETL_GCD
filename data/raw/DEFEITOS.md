# solicitacoes.csv — massa controlada

30 linhas sintéticas, sendo 11 com defeitos intencionais.

## Defeitos

| Linha | Defeito |
|---:|---|
| 2 | protocolo vazio |
| 3 | status ambíguo: `EM ANALISE` |
| 4 | status ambíguo em minúsculas e com acento: `em análise` |
| 5 | data de criação inválida |
| 6 | aceite com valor fora do domínio: `talvez` |
| 7 | identificador ausente |
| 8 | data de atualização ausente |
| 9 | status fora do domínio: `STATUS_INVALIDO` |
| 10 | protocolo duplicado |
| 11 | data em formato inconsistente e inválida |
| 12 | aceite vazio |

## Regra ambígua

`EM_ANALISE`, `EM ANALISE` e `em análise` devem ser avaliados pela Silver e normalizados para `EM_ANALISE`, com a regra documentada e validada pelo responsável de negócio.

Todos os dados são sintéticos.
