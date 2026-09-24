# Concilia Vagas — Pipeline de Dados

Projeto acadêmico de engenharia e governança de dados desenvolvido para transformar dados heterogêneos de solicitações de conciliação em informações analíticas confiáveis, rastreáveis e reproduzíveis.

O projeto utiliza ingestão em Python, preservação do dado bruto, transformação com dbt e DuckDB, camada de consumo orientada à pergunta de negócio, testes de qualidade, documentação de linhagem e versionamento com Delta Lake.

---

## 1. Pergunta de negócio

A pergunta principal do projeto é:

> **Quanto tempo, em média, uma solicitação leva desde a entrada até a finalização da conciliação, considerando o tipo de conflito e o período de entrada?**

A análise também permite identificar:

- o volume de solicitações por período e status;
- a cobertura do histórico de etapas;
- o tempo médio de permanência em cada etapa;
- a etapa com maior tempo médio de permanência;
- o comportamento do tempo de conciliação por tipo de conflito e período.

---

## 2. Jornada dos dados

O fluxo do projeto é organizado da seguinte forma:

```text
FONTES
  ↓
INGESTÃO
  ↓
PRESERVAÇÃO RAW
  ↓
STAGING
  ↓
CONSUMO
  ↓
RESPOSTA / DASHBOARD
```

Cada camada possui uma responsabilidade específica:

### Fontes

Contêm os arquivos originais utilizados pelo projeto.

### Ingestão

Realizada em Python, com responsabilidade de ler e estruturar os arquivos de origem.

A ingestão não aplica regras de negócio.

### Preservação RAW

Mantém os dados recebidos das fontes sem alterações de conteúdo.

O objetivo é garantir rastreabilidade e permitir a comparação entre o dado original e as transformações realizadas posteriormente.

### Staging

Realiza a preparação dos dados para análise.

Nesta camada são aplicadas transformações determinísticas e documentadas, como:

- padronização de textos;
- normalização de categorias equivalentes;
- conversão de tipos;
- tratamento de datas;
- preparação dos campos utilizados pelas camadas analíticas.

O dado original permanece preservado no RAW.

Quando uma inconsistência pode ser corrigida de maneira segura e determinística, busca-se normalizar o registro para aproveitá-lo na análise.

Quando não é possível corrigir uma informação com segurança, o valor não é inventado ou alterado artificialmente. O registro continua preservado nas camadas anteriores e pode participar das análises que não dependam da informação inconsistente.

### Consumo

Contém tabelas orientadas às perguntas analíticas do projeto.

As regras necessárias para construção dos indicadores são aplicadas antes da resposta final, evitando que a consulta de negócio precise acessar diretamente as fontes ou reproduzir regras de transformação.

### Resposta / Dashboard

A resposta final é obtida exclusivamente a partir da camada de consumo.

O projeto também possui um dashboard desenvolvido em Streamlit para exploração dos principais indicadores.

O dashboard não consulta diretamente os dados RAW.

---

## 3. Fontes de dados

O projeto utiliza diferentes formatos de entrada:

### Solicitações

```text
data/raw/solicitacoes.csv
```

Contém os registros principais das solicitações.

### Solicitações complementares

```text
data/raw/solicitacoes_complementares.csv
```

Fonte complementar utilizada para enriquecer a massa sintética do projeto acadêmico, incluindo registros e períodos necessários para demonstrar a análise.

### Histórico de etapas

```text
data/raw/historico_etapas.json
```

Contém o histórico temporal das etapas pelas quais as solicitações passaram.

O uso de mais de um formato de entrada demonstra o tratamento de fontes heterogêneas durante a ingestão.

> **Observação:** os dados utilizados no projeto são sintéticos/anônimos e destinados exclusivamente ao contexto acadêmico.

---

## 4. Arquitetura

A arquitetura simplificada do projeto é:

```text
                  ┌─────────────────────┐
                  │       FONTES        │
                  │ CSV / JSON          │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │      INGESTÃO       │
                  │      Python         │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   PRESERVAÇÃO RAW   │
                  │ Dado original       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │      STAGING        │
                  │ dbt + DuckDB        │
                  │                     │
                  │ Normalização        │
                  │ Tipagem             │
                  │ Tratamento de datas │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │      CONSUMO        │
                  │ Métricas e respostas│
                  └──────────┬──────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │     RESPOSTA / DASHBOARD    │
              │ SQL + Streamlit             │
              └──────────────────────────────┘
```

---

## 5. Tecnologias utilizadas

- Python 3.11+
- dbt Core
- DuckDB
- SQL
- Delta Lake
- biblioteca `deltalake`
- Streamlit
- Git

O projeto utiliza Delta Lake por meio da biblioteca `deltalake` e **não utiliza Apache Spark**.

---

## 6. Estrutura do projeto

A estrutura principal é organizada da seguinte forma:

```text
concilia-vagas/
│
├── data/
│   ├── raw/
│   │   ├── solicitacoes.csv
│   │   ├── solicitacoes_complementares.csv
│   │   └── historico_etapas.json
│   │
│   └── delta/
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── consumo/
│   │
│   ├── schema.yml
│   └── dbt_project.yml
│
├── src/
│   └── pipeline.py
│
├── consultas/
│   ├── executar_respostas.py
│   └── delta_time_travel.py
│
├── docs/
│
├── app.py
├── DECISOES.md
└── README.md
```

---

## 7. Modelagem e regras principais

### 7.1 Histórico de etapas

O histórico representa as etapas pelas quais uma solicitação passou.

As etapas esperadas para uma solicitação completa são:

```text
RECEPCAO_TRIAGEM
        ↓
ANALISE
        ↓
NEGOCIACAO
        ↓
VALIDACAO
        ↓
FINALIZACAO
```

A camada de staging padroniza os nomes das etapas e categorias antes que os dados sejam utilizados nas métricas.

---

## 8. Normalização dos dados

Uma das decisões centrais do projeto é priorizar o aproveitamento dos dados.

Exemplo de normalização:

```text
DISTANTE_DA_RESIDENCIA
          ↓
LONGE_DA_RESIDENCIA
```

A correção é realizada na camada de transformação, enquanto o valor original permanece preservado no RAW.

O mesmo princípio é aplicado a variações de texto e categorias equivalentes quando existe uma regra determinística para sua padronização.

A estratégia adotada é:

> **aproveitar o máximo possível dos dados sem criar informações que não estejam presentes na fonte.**

---

## 9. Métricas

### 9.1 Tempo total de conciliação

O tempo total é calculado entre:

```text
data_entrada
      ↓
data_finalizacao
```

A `data_finalizacao` utilizada pela métrica corresponde ao campo:

```text
data_fim
```

da etapa:

```text
FINALIZACAO
```

O tempo é calculado em dias.

---

### 9.2 Tempo por etapa

Para cada etapa válida:

```text
tempo_espera_etapa_dias =
    data_fim - data_inicio
```

Isso permite comparar a permanência média das solicitações em cada etapa do processo.

---

## 10. Critérios para cálculo do tempo total

Nem toda solicitação finalizada necessariamente possui histórico suficiente para calcular o tempo total com segurança.

Para participar da métrica de tempo de conciliação, a solicitação deve:

1. possuir status `FINALIZADA`;
2. possuir `id_solicitacao` válido;
3. possuir `protocolo` válido;
4. possuir `data_entrada` válida;
5. possuir histórico temporal válido;
6. possuir as cinco etapas esperadas:
   - `RECEPCAO_TRIAGEM`
   - `ANALISE`
   - `NEGOCIACAO`
   - `VALIDACAO`
   - `FINALIZACAO`;
7. possuir datas de início e fim válidas para as etapas utilizadas;
8. possuir `data_fim >= data_inicio`.

Solicitações que não atendem aos critérios necessários não são apagadas da origem.

Elas permanecem disponíveis nas camadas anteriores e podem ser utilizadas em análises que não dependam das informações ausentes ou inconsistentes.

Essa separação permite preservar os dados sem comprometer a confiabilidade da métrica.

---

## 11. Camada de consumo

A camada de consumo foi construída para responder perguntas específicas sem depender diretamente dos dados RAW.

### `consumo_tempo_conciliacao`

**Grão:** uma linha por solicitação finalizada com histórico completo e válido.

Utilizada para responder:

> Quanto tempo uma solicitação leva da entrada até a finalização?

Principais campos:

- `id_solicitacao`
- `protocolo`
- `tipo_conflito`
- `data_entrada`
- `data_finalizacao`
- `periodo_entrada`
- `tempo_total_conciliacao_dias`

### `consumo_tempo_etapas`

**Grão:** uma linha por solicitação e etapa válida.

Utilizada para analisar:

> Em qual etapa as solicitações permanecem por mais tempo?

Principais campos:

- `id_solicitacao`
- `protocolo`
- `tipo_conflito`
- `etapa`
- `data_inicio`
- `data_fim`
- `tempo_espera_etapa_dias`

### `consumo_volume_solicitacoes`

**Grão:** uma linha por período de entrada e status.

Utilizada para acompanhar o volume de solicitações ao longo do tempo.

Principais campos:

- `periodo_entrada`
- `status`
- `quantidade_solicitacoes`

### `consumo_cobertura_historico`

**Grão:** uma linha com os indicadores de cobertura do histórico.

Permite comparar:

- total de solicitações finalizadas;
- total de solicitações analisadas;
- percentual de cobertura do histórico.

---

## 12. Resposta final

A consulta final responde à pergunta principal exclusivamente a partir da camada de consumo:

```sql
select
    tipo_conflito,
    periodo_entrada,
    count(*) as quantidade_solicitacoes,
    round(avg(tempo_total_conciliacao_dias), 2) as tempo_medio_dias
from consumo_tempo_conciliacao
group by
    tipo_conflito,
    periodo_entrada
order by
    periodo_entrada,
    tipo_conflito;
```

A consulta final não acessa:

- arquivos RAW;
- tabelas de staging;
- fontes originais.

As regras de elegibilidade da métrica já foram tratadas na camada de consumo.

Dessa forma, a consulta final permanece simples e orientada à pergunta de negócio.

---

## 13. Dashboard

O projeto possui um dashboard em Streamlit executado por:

```bash
streamlit run app.py
```

O dashboard apresenta:

- total de solicitações finalizadas;
- total de solicitações analisadas;
- cobertura do histórico;
- tempo médio de conciliação;
- volume de solicitações por período;
- volume por período e status;
- tempo médio por tipo de conflito;
- tempo médio por etapa;
- evolução temporal do tempo médio;
- tabela das solicitações analisadas.

Também estão disponíveis filtros para exploração dos dados, incluindo:

- tipo de conflito;
- status;
- etapa;
- período de entrada.

### Regra importante

O dashboard não consulta diretamente o RAW.

As informações apresentadas são obtidas a partir das camadas preparadas do projeto.

---

## 14. Qualidade dos dados

A qualidade dos dados é tratada em diferentes pontos do pipeline.

### Preservação

O dado original é mantido no RAW.

### Normalização

Inconsistências que possuem correção determinística são tratadas nas transformações.

### Regras de elegibilidade

Métricas que dependem de informações completas utilizam somente os registros que atendem aos critérios necessários.

### Testes automatizados

O projeto possui testes dbt para verificar propriedades importantes dos dados.

Os testes utilizados incluem:

- `not_null`;
- `unique`;
- `accepted_values`.

Ao todo, o projeto possui **16 testes dbt**.

Esses testes ajudam a detectar problemas como:

- identificadores ausentes;
- protocolos duplicados;
- categorias fora do domínio esperado;
- inconsistências estruturais nos modelos.

---

## 15. dbt e linhagem

O dbt é responsável pelas transformações e pela organização das dependências entre os modelos.

A estrutura principal é:

```text
RAW
 ↓
STAGING
 ↓
CONSUMO
 ↓
RESPOSTA
```

A documentação e a linhagem dos modelos podem ser geradas com:

```bash
python -m dbt.cli.main docs generate --profiles-dir .
```

E visualizadas com:

```bash
python -m dbt.cli.main docs serve --profiles-dir .
```

A linhagem permite visualizar a origem dos dados e as dependências entre as transformações.

---

## 16. Delta Lake e versionamento

O projeto utiliza Delta Lake para demonstrar versionamento de dados.

A implementação utiliza a biblioteca:

```text
deltalake
```

sem necessidade de Apache Spark.

O objetivo é demonstrar:

- criação de uma tabela Delta;
- existência de múltiplas versões;
- consulta da versão atual;
- consulta de uma versão anterior;
- comparação entre versões.

A demonstração pode ser executada por:

```bash
python consultas/delta_time_travel.py
```

A funcionalidade de time travel permite recuperar uma versão anterior do conjunto de dados e comparar seu estado com a versão atual.

---

## 17. Execução do projeto

### 17.1 Instalação

Recomenda-se utilizar um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual conforme o sistema operacional e instale as dependências:

```bash
pip install -r requirements.txt
```

### 17.2 Executar a ingestão

Na raiz do projeto:

```bash
python -m src.pipeline
```

Essa etapa realiza a ingestão e preparação dos dados preservados no RAW.

### 17.3 Validar o ambiente dbt

Entre na pasta:

```bash
cd dbt
```

Execute:

```bash
python -m dbt.cli.main debug --profiles-dir .
```

### 17.4 Executar transformações e testes

Ainda dentro de `dbt/`:

```bash
python -m dbt.cli.main build --profiles-dir .
```

O comando executa os modelos e os testes definidos no projeto.

O resultado esperado é uma execução sem falhas nos modelos e testes.

### 17.5 Gerar documentação

```bash
python -m dbt.cli.main docs generate --profiles-dir .
```

Para visualizar:

```bash
python -m dbt.cli.main docs serve --profiles-dir .
```

### 17.6 Executar as consultas de resposta

Volte para a raiz:

```bash
cd ..
```

Execute:

```bash
python consultas/executar_respostas.py
```

### 17.7 Executar demonstração de Delta Lake

```bash
python consultas/delta_time_travel.py
```

### 17.8 Executar o dashboard

Na raiz do projeto:

```bash
streamlit run app.py
```

---

## 18. Reprodutibilidade

O projeto foi estruturado para permitir a reconstrução do pipeline a partir dos dados de entrada e das definições versionadas.

O fluxo principal é:

```bash
python -m src.pipeline

cd dbt

python -m dbt.cli.main build --profiles-dir .
```

Depois, a aplicação pode ser executada com:

```bash
cd ..

streamlit run app.py
```

A separação entre ingestão, transformação, consumo e apresentação permite reproduzir as etapas de forma independente.

---

## 19. Decisões de arquitetura

As principais decisões do projeto estão documentadas em:

```text
DECISOES.md
```

O documento detalha, entre outros pontos:

- arquitetura das camadas;
- grão dos modelos;
- tratamento de dados inconsistentes;
- normalização de categorias;
- tratamento das etapas do histórico;
- critérios para cálculo do tempo de conciliação;
- tratamento de informações incompletas;
- uso de dados sintéticos;
- decisões relacionadas ao consumo.

---

## 20. Princípios adotados

O projeto segue alguns princípios centrais:

### 1. Preservar antes de transformar

O dado original é mantido no RAW.

### 2. Normalizar antes de descartar

Quando uma inconsistência pode ser corrigida de forma determinística, busca-se aproveitar o registro.

### 3. Não inventar informação

Quando não existe informação suficiente para corrigir um campo com segurança, o projeto não cria um valor artificial.

### 4. Separar transformação de resposta

As regras de preparação e elegibilidade são aplicadas nas camadas de transformação e consumo.

### 5. Responder a perguntas de negócio

A camada de consumo não é apenas uma cópia dos dados tratados. Ela organiza os dados de acordo com as perguntas que precisam ser respondidas.

### 6. Garantir rastreabilidade

O projeto mantém:

- dados RAW;
- modelos dbt;
- testes;
- documentação;
- linhagem;
- decisões arquiteturais;
- versionamento Delta Lake.

### 7. Manter a resposta reproduzível

A mesma sequência de ingestão e transformação deve produzir os mesmos resultados a partir da mesma massa de entrada.

---

## 21. Privacidade

Os dados utilizados no projeto são sintéticos ou anonimizados e não devem conter dados pessoais reais.

O projeto foi desenvolvido exclusivamente para fins acadêmicos.

---

## 22. Checklist do projeto

### Fontes e ingestão

- [x] Utilização de mais de um formato de fonte
- [x] Ingestão realizada em Python
- [x] Preservação dos dados RAW
- [x] Separação entre ingestão e transformação

### Transformação

- [x] Transformações realizadas com dbt
- [x] Padronização de categorias
- [x] Conversão e tratamento de datas
- [x] Regras documentadas
- [x] Modelos com grão definido

### Consumo

- [x] Camada de consumo orientada à pergunta de negócio
- [x] Métrica de tempo total
- [x] Métrica de tempo por etapa
- [x] Volume por período e status
- [x] Indicador de cobertura do histórico
- [x] Consulta final baseada somente na camada de consumo

### Qualidade

- [x] 16 testes dbt
- [x] `not_null`
- [x] `unique`
- [x] `accepted_values`

### Governança e rastreabilidade

- [x] Documentação de decisões
- [x] Linhagem dbt
- [x] Preservação do RAW
- [x] Versionamento com Delta Lake
- [x] Demonstração de time travel

### Apresentação

- [x] Dashboard Streamlit
- [x] Indicadores principais
- [x] Filtros
- [x] Visualizações analíticas
- [x] Dados sem acesso direto ao RAW pelo dashboard

### Documentação

- [x] README
- [x] DECISOES.md
- [x] Documentação dbt
- [x] Consultas de resposta
- [x] Demonstração de Delta Lake

---

## 23. Resultado esperado

Ao final da execução, o projeto deve permitir responder de forma reproduzível:

> **Quanto tempo, em média, uma solicitação leva da entrada até a finalização da conciliação, considerando o tipo de conflito e o período de entrada?**

Além disso, deve ser possível identificar:

- o volume de solicitações ao longo do tempo;
- a cobertura disponível do histórico;
- o tempo médio por tipo de conflito;
- o tempo médio por etapa;
- a etapa com maior tempo médio de permanência.

A principal entrega do projeto é transformar dados heterogêneos e imperfeitos em uma estrutura analítica **utilizável, rastreável e reproduzível**, preservando o dado original e deixando explícitos os critérios utilizados para cada métrica.
