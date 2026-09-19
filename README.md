# Concilia Vagas — Pipeline de Dados

Pipeline acadêmico de **Gestão e Governança de Dados** desenvolvido para demonstrar a jornada completa dos dados:

**FONTES → INGESTÃO → PRESERVAÇÃO DO BRUTO → TRANSFORMAÇÃO → CONSUMO → RESPOSTA**

O projeto utiliza dados fictícios/sintéticos para demonstrar uma solução reproduzível de análise do tempo de conciliação de solicitações de vagas.

---

## 1. Pergunta de negócio

> **Quanto tempo, em média, uma solicitação de conciliação de vagas leva desde a data de entrada até a sua finalização, considerando o tipo de conflito e o período de entrada, e em qual etapa do processo está concentrado o maior tempo de espera?**

A pergunta é respondida por meio de:

- **tempo total de conciliação**;
- análise por **tipo de conflito**;
- análise por **período de entrada**;
- análise do **tempo médio de permanência em cada etapa**.

### Métricas derivadas

**Tempo total de conciliação**

```text
data_finalizacao - data_entrada
```

**Tempo de permanência na etapa**

```text
data_fim - data_inicio
```

Essas métricas são calculadas pelo pipeline e **não existem prontas nas fontes**.

---

## 2. Fontes de dados

O projeto utiliza fontes em formatos diferentes.

### Fonte 1 — Solicitações

```text
data/raw/solicitacoes.csv
```

Fonte original preservada sem alteração.

### Fonte 2 — Solicitações complementares

```text
data/raw/solicitacoes_complementares.csv
```

Dados sintéticos utilizados para complementar informações necessárias à análise, principalmente:

- datas de finalização;
- diferentes períodos de entrada;
- informações necessárias aos recortes da análise.

### Fonte 3 — Histórico das etapas

```text
data/raw/historico_etapas.json
```

Contém o histórico das etapas de cada solicitação, permitindo calcular o tempo de permanência em cada etapa.

> **Importante:** os dados complementares são sintéticos e foram utilizados exclusivamente para fins acadêmicos. Não são apresentados como dados reais.

---

## 3. Arquitetura do projeto

A solução utiliza uma arquitetura simplificada em camadas:

```text
                 FONTES
                   │
                   ▼
                INGESTÃO
                   │
                   ▼
             PRESERVAÇÃO RAW
                   │
                   ▼
                STAGING
              ┌────┴────┐
              ▼         ▼
         QUARENTENA   CONSUMO
                         │
                         ▼
                      RESPOSTA
```

### RAW

Preserva os dados conforme recebidos, incluindo eventuais defeitos.

### STAGING

Realiza:

- padronização;
- tipagem;
- tratamento de datas;
- normalização;
- tratamentos necessários para qualidade dos dados.

### QUARENTENA

Recebe registros que não podem participar da análise de forma confiável.

### CONSUMO

Contém os modelos preparados especificamente para responder à pergunta de negócio.

Principais modelos:

```text
consumo_tempo_conciliacao
consumo_tempo_etapas
```

---

## 4. Tecnologias utilizadas

- **Python 3.11+**
- **dbt Core**
- **DuckDB**
- **Delta Lake / deltalake**
- **SQL**
- **Git**

Não é necessário utilizar Spark.

---

## 5. Estrutura do projeto

A estrutura principal é:

```text
concilia-vagas/
│
├── data/
│   └── raw/
│       ├── solicitacoes.csv
│       ├── solicitacoes_complementares.csv
│       └── historico_etapas.json
│
├── src/
│   └── pipeline.py
│
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       ├── consumo/
│       ├── schema.yml
│       └── ...
│
├── consultas/
│   ├── resposta.sql
│   ├── executar_respostas.py
│   └── delta_time_travel.py
│
├── requirements.txt
├── README.md
└── DECISOES.md
```

---

## 6. Instalação

Abra o terminal na **raiz do projeto**.

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar no Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar dependências

```bash
python -m pip install -r requirements.txt
```

> O ambiente `.venv` é apenas o ambiente local de execução e **não deve ser versionado no Git**.

---

## 7. Execução do pipeline

Com o ambiente virtual ativado, execute:

```bash
python -m src.pipeline
```

Essa etapa realiza a ingestão e preparação dos dados necessários ao pipeline.

---

## 8. Validar o dbt

Entre na pasta do dbt:

```bash
cd dbt
```

Execute:

```bash
dbt build
```

O `dbt build` executa os modelos e testes definidos no projeto.

Ao final, os testes devem apresentar resultado de sucesso.

---

## 9. Gerar a documentação e DAG


```bash
dbt docs generate
```

Para abrir a documentação:

```bash
dbt docs serve
```

A documentação permite visualizar a **DAG e a linhagem dos dados**.


Depois volte para a raiz:

```bash
cd ..
```

---

## 10. Executar a resposta de negócio

Na raiz do projeto:

```bash
python consultas/executar_respostas.py
```

A consulta utiliza a **camada de consumo**, e não os dados RAW.

O resultado apresenta informações relacionadas a:

- tipo de conflito;
- período de entrada;
- quantidade de solicitações;
- tempo médio de conciliação;
- tempo médio das etapas.

---

## 11. Validar o Delta Lake

Execute:

```bash
python consultas/delta_time_travel.py
```

O objetivo é demonstrar que existem **duas ou mais versões da tabela Delta** e que é possível consultar uma versão anterior dos dados.

Durante a apresentação, deve ser demonstrado:

```text
Versão atual
     ↓
Consulta
     ↓
Resultado

Versão anterior
     ↓
Mesma consulta
     ↓
Resultado
```

Isso demonstra o recurso de **Time Travel**.

---

## 12. Exbir gráficos streamlit

```bash
streamlit run app.py
```
---

## 13. Testes de qualidade
O projeto possui testes definidos no `schema.yml`.

São utilizados diferentes tipos de validação, incluindo:

- `not_null`;
- `unique`;
- `accepted_values`;
- relacionamentos, quando aplicável.

Os testes verificam se os dados utilizados pela camada de consumo possuem qualidade suficiente para responder à pergunta de negócio.

---

## 14. Regras importantes

### Preservação do bruto

Os dados RAW não são alterados para corrigir problemas.

### Transformação

As regras de limpeza e padronização ficam nos modelos dbt.

### Consumo

A camada de consumo é construída especificamente para responder à pergunta de negócio.

### Consulta final

A consulta final:

- lê somente a camada de consumo;
- não acessa diretamente o RAW;
- não cria regras de negócio no `WHERE`.

### Reprodutibilidade

O pipeline deve conseguir ser reconstruído a partir das fontes.

---

## 15. Decisões de projeto

As principais decisões estão documentadas em:

```text
DECISOES.md
```

O documento explica:

1. **Arquitetura de armazenamento**
2. **Grão dos modelos**
3. **Tratamento de dado ambíguo**
4. **Destino dos registros inválidos**

---

## 16. Resultado esperado

Ao final da execução, o projeto deve permitir responder:

> **Quanto tempo uma solicitação de conciliação leva, em média, desde sua entrada até a finalização?**

E realizar os seguintes recortes:

```text
Tipo de conflito
        +
Período de entrada
        +
Etapa do processo
```

A análise complementar permite identificar **qual etapa apresenta o maior tempo médio de permanência**.

> Esse indicador representa o maior tempo médio observado entre as etapas. Ele não deve ser interpretado, isoladamente, como prova da causa do problema.

---

## 17. Dados e privacidade

Este projeto possui finalidade **exclusivamente acadêmica**.

Não devem ser utilizados dados pessoais reais no repositório.

As informações complementares utilizadas na PoC são **sintéticas/anônimas**.