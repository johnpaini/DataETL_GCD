# DECISOES.md — Concilia Vagas

## 1. Objetivo do documento

Este documento registra as principais decisões de arquitetura, modelagem, qualidade e interpretação adotadas no projeto **Concilia Vagas**.

O objetivo é deixar explícito **o que o pipeline considera dado válido para cada análise**, quais transformações são realizadas e quais informações são preservadas para rastreabilidade.

O projeto utiliza dados fictícios/sintéticos para fins acadêmicos.

---

## 2. Pergunta de negócio

A pergunta principal do projeto é:

> **Quanto tempo, em média, uma solicitação de conciliação de vagas leva desde a data de entrada até a sua finalização, considerando o tipo de conflito e o período de entrada, e em qual etapa do processo está concentrado o maior tempo de espera?**

A resposta é construída a partir de métricas derivadas pelo pipeline:

- tempo total de conciliação;
- tempo de permanência em cada etapa;
- quantidade de solicitações;
- recortes por tipo de conflito;
- recortes por período de entrada.

As métricas de tempo não existem prontas nas fontes: são calculadas a partir das datas disponíveis.

---

## 3. Arquitetura adotada

A arquitetura segue o fluxo:

```text
FONTES
  ↓
INGESTÃO
  ↓
RAW
  ↓
STAGING
  ↓
CONSUMO
  ↓
RESPOSTA / DASHBOARD
```

### RAW

A camada RAW representa a preservação dos dados de origem.

A regra adotada é:

> **O dado bruto não deve ser alterado para corrigir problemas de qualidade.**

Correções, padronizações e interpretações pertencem às camadas de transformação.

Isso permite manter rastreabilidade entre o dado recebido e o dado utilizado nas análises.

### STAGING

A camada STAGING realiza a preparação técnica dos dados, incluindo:

- conversão de tipos;
- tratamento de datas;
- padronização textual;
- normalização de valores;
- aplicação das regras necessárias para tornar os dados utilizáveis pelos modelos seguintes.

STAGING não deve ser confundida com a camada de resposta de negócio.

### CONSUMO

A camada de consumo contém tabelas preparadas para perguntas analíticas específicas.

A consulta final e o dashboard não devem acessar diretamente os dados RAW.

---

## 4. Fontes e formatos

O projeto utiliza fontes em formatos diferentes:

### Solicitações

```text
data/raw/solicitacoes.csv
```

Representa a fonte original de solicitações.

### Solicitações complementares

```text
data/raw/solicitacoes_complementares.csv
```

É uma fonte sintética complementar, utilizada para ampliar a massa disponível para a demonstração acadêmica.

### Histórico das etapas

```text
data/raw/historico_etapas.json
```

Representa o histórico temporal das etapas das solicitações.

Os dados complementares são sintéticos e não devem ser interpretados como dados reais.

---

## 5. Regra de precedência entre fontes

Quando uma solicitação aparece na fonte original e também na fonte complementar, a fonte **ORIGINAL tem precedência**.

A fonte complementar somente adiciona uma solicitação quando seu `id_solicitacao` ainda não existe na fonte original.

A regra é:

```text
ORIGINAL
   │
   ├── id já existente ──→ mantém ORIGINAL
   │
   └── id inexistente ───→ aceita COMPLEMENTAR
```

Essa decisão evita duplicação de solicitações e preserva a fonte principal.

A regra é implementada no modelo `stg_solicitacoes`.

---

## 6. Grão dos principais modelos

O grão deve ser explícito para evitar interpretações incorretas dos resultados.

### `stg_solicitacoes`

**Grão:** uma linha por solicitação.

### `stg_historico_etapas`

**Grão:** uma linha por ocorrência de etapa de uma solicitação.

Esse modelo representa o histórico e não determina, sozinho, se uma solicitação deve ser considerada finalizada para a métrica de tempo total.

### `consumo_tempo_etapas`

**Grão:** uma linha por solicitação e etapa válida.

Permite calcular o tempo de permanência em cada etapa.

### `consumo_tempo_conciliacao`

**Grão:** uma linha por solicitação FINALIZADA com histórico temporal completo e válido.

Esse é o modelo utilizado para a principal métrica de tempo total.

### `consumo_volume_solicitacoes`

**Grão:** uma linha por período de entrada e status.

Esse modelo permite analisar volume sem exigir que a solicitação possua histórico completo.

### `consumo_cobertura_historico`

**Grão:** uma única linha com indicadores de cobertura do histórico.

---

## 7. Definição de solicitação analisável para tempo total

Uma solicitação pode existir no sistema e estar com status `FINALIZADA`, mas isso não significa automaticamente que ela possa ser utilizada no cálculo do tempo total.

Para entrar em `consumo_tempo_conciliacao`, a solicitação precisa:

1. estar com status `FINALIZADA`;
2. possuir `id_solicitacao` válido;
3. possuir protocolo;
4. possuir `data_entrada`;
5. possuir histórico temporal válido;
6. possuir as cinco etapas esperadas;
7. possuir a etapa `FINALIZACAO`;
8. possuir datas de início e fim válidas nas etapas utilizadas;
9. não possuir `data_fim` anterior à `data_inicio`.

As cinco etapas esperadas são:

```text
RECEPCAO_TRIAGEM
ANALISE
NEGOCIACAO
VALIDACAO
FINALIZACAO
```

Essa regra evita calcular uma duração total com histórico incompleto.

---

## 8. Definição da data de finalização

A data de finalização utilizada na métrica principal é:

```text
data_fim da etapa FINALIZACAO
```

Essa definição é mais explícita do que simplesmente utilizar a maior data encontrada no histórico.

A métrica de tempo total é:

```text
tempo_total_conciliacao_dias
=
data_finalizacao - data_entrada
```

---

## 9. Tempo de permanência nas etapas

Para `consumo_tempo_etapas`, o tempo de permanência é calculado como:

```text
data_fim - data_inicio
```

em dias.

Somente registros com datas válidas são utilizados para esse cálculo.

Também é excluído o caso em que:

```text
data_fim < data_inicio
```

pois isso representaria uma inconsistência temporal para a métrica.

---

## 10. Padronização de `tipo_conflito`

Os textos recebidos das fontes são padronizados na camada de staging.

Um caso específico documentado é:

```text
DISTANTE_DA_RESIDENCIA
        ↓
LONGE_DA_RESIDENCIA
```

A padronização é feita na transformação, mantendo o valor original preservado na camada RAW.

Essa decisão evita tratar duas grafias semanticamente equivalentes como categorias diferentes na análise.

---

## 11. Valores ambíguos e regras de domínio

### `REDE_INTERNET`

O valor `REDE_INTERNET` aparece nos dados do histórico e é mantido como categoria própria.

Não é feita uma interpretação adicional para convertê-lo em outra categoria, pois o dado da fonte já fornece uma classificação explícita.

A apresentação pode utilizar um nome amigável, mas a categoria técnica permanece padronizada no modelo.

### Valores não reconhecidos

Valores de domínio não devem ser silenciosamente convertidos para outra categoria.

Quando uma regra de domínio é necessária, ela deve ser documentada no modelo correspondente e validada por testes.

---

## 12. Registros incompletos ou inválidos

O projeto adota o princípio:

> **Não apagar o dado de origem para resolver um problema de qualidade.**

Assim, um registro incompleto pode permanecer disponível nas camadas anteriores mesmo que não possa participar de determinada métrica.

Exemplos:

- solicitação finalizada sem histórico completo;
- etapa sem `data_inicio`;
- etapa sem `data_fim`;
- intervalo temporal inválido;
- solicitação sem campos necessários para uma determinada análise.

Esses casos não devem produzir artificialmente uma duração de conciliação.

---

## 13. Quarentena — decisão atual

Neste momento, o projeto **não possui uma camada física de quarentena implementada como tabela/modelo separado**.

O tratamento efetivamente adotado é:

```text
RAW preserva o registro
        ↓
STAGING padroniza
        ↓
qualidade é validada
        ↓
registro incompleto pode ser excluído
da MÉTRICA específica
        ↓
dados válidos seguem para CONSUMO
```

Portanto, não se deve afirmar que existe uma tabela `quarentena` caso ela não esteja presente no pipeline.

A decisão atual pode ser descrita como:

> **retenção no RAW + exclusão controlada das métricas que exigem maior qualidade temporal.**

Essa abordagem mantém rastreabilidade e evita contaminar os indicadores com registros que não possuem informação suficiente.

Uma futura camada física de quarentena poderá ser adicionada caso seja necessário registrar, de forma estruturada, o motivo da rejeição de cada registro. Essa evolução não faz parte da decisão atual.

---

## 14. Testes de qualidade

A qualidade é verificada também por testes do dbt.

São utilizados diferentes tipos de testes, incluindo:

- `not_null`;
- `unique`;
- `accepted_values`.

Os testes ajudam a detectar problemas como:

- identificadores ausentes;
- duplicidades;
- valores fora do domínio esperado;
- campos obrigatórios ausentes.

Os testes são um mecanismo de detecção de qualidade; eles não substituem a preservação do RAW nem as regras explícitas de transformação.

---

## 15. Camada de consumo e responsabilidade das regras

As regras de negócio utilizadas para construir as métricas ficam nos modelos de consumo.

A consulta final deve ser simples e orientada à pergunta:

```text
CONSUMO
  ↓
agregação
  ↓
resposta
```

A consulta final não deve reimplementar regras de qualidade que já foram definidas nos modelos anteriores.

Também não deve acessar diretamente o RAW.

---

## 16. Volume e cobertura do histórico

A massa sintética utilizada na demonstração foi ampliada para permitir uma análise mais representativa do processo.

A configuração atual foi construída para possuir solicitações finalizadas tanto com histórico completo quanto com histórico incompleto.

Isso é intencional: permite demonstrar que:

```text
total de FINALIZADAS
        ≠
total analisado no tempo
```

O indicador `cobertura_historico_percentual` explicita essa diferença.

A existência de solicitações finalizadas sem histórico completo não é tratada como motivo para apagar a solicitação. Elas continuam disponíveis nas camadas anteriores e podem participar de análises que não dependam do histórico completo.

---

## 17. Dashboard

O dashboard Streamlit utiliza as camadas preparadas pelo pipeline.

As consultas principais são realizadas sobre:

```text
consumo_tempo_conciliacao
consumo_tempo_etapas
consumo_volume_solicitacoes
consumo_cobertura_historico
```

O dashboard também utiliza `stg_solicitacoes` para filtros e informações de solicitação.

A apresentação utiliza nomes amigáveis somente na interface, sem alterar os valores técnicos armazenados nos modelos.

---

## 18. Delta Lake e versionamento

O projeto utiliza Delta Lake para demonstrar versionamento e Time Travel.

A decisão é utilizar a biblioteca Python `deltalake`, sem Spark.

A demonstração deve evidenciar:

1. uma versão atual;
2. uma versão anterior;
3. uma consulta equivalente nas duas versões;
4. a diferença entre os resultados.

O objetivo é demonstrar que uma alteração nos dados não elimina a possibilidade de consultar uma versão anterior da tabela.

---

## 19. Rastreabilidade e linhagem

A linhagem esperada é:

```text
FONTES
  ↓
RAW
  ↓
STAGING
  ↓
CONSUMO
  ↓
RESPOSTA
```

O dbt é utilizado para documentar as dependências entre modelos.

A camada RAW permanece como referência do dado de origem, enquanto STAGING e CONSUMO concentram as transformações e regras necessárias para a análise.

---

## 20. Princípios adotados

As decisões do projeto podem ser resumidas nos seguintes princípios:

1. **Preservar o dado bruto.**
2. **Não corrigir o RAW.**
3. **Documentar transformações no dbt.**
4. **Declarar o grão dos modelos.**
5. **Não calcular métricas com histórico temporal insuficiente.**
6. **Manter registros incompletos disponíveis para rastreabilidade.**
7. **Separar regras de transformação da consulta final.**
8. **Evitar que o dashboard consulte diretamente o RAW.**
9. **Validar qualidade com testes automatizados.**
10. **Manter os dados sintéticos claramente identificados como material acadêmico.**

---

## 21. Resumo das decisões

| Tema | Decisão |
|---|---|
| Dado bruto | Preservado sem correção |
| Fonte original x complementar | Original tem precedência |
| Grão de solicitação | Uma linha por solicitação |
| Grão de histórico | Uma linha por ocorrência de etapa |
| Tempo total | `data_finalizacao - data_entrada` |
| Data de finalização | `data_fim` da etapa `FINALIZACAO` |
| Etapas esperadas | 5 etapas do fluxo definido |
| Histórico incompleto | Não participa da métrica de tempo total |
| Dado inválido | Não é apagado do RAW |
| Quarentena física | Não implementada atualmente |
| Tratamento de qualidade | Testes + filtros controlados nas métricas |
| Dashboard | Consulta staging/consumo, não RAW |
| Dados complementares | Sintéticos, para fins acadêmicos |
| Versionamento | Delta Lake com Time Travel |

---

## 22. Observação final

Este documento descreve o comportamento efetivamente adotado pelo projeto e deve ser atualizado caso novas camadas ou regras sejam implementadas.

Em particular, caso uma camada física de quarentena seja criada posteriormente, a seção **13. Quarentena — decisão atual** deverá ser revisada para descrever sua estrutura, motivo da rejeição, retenção e fluxo de reprocessamento.
