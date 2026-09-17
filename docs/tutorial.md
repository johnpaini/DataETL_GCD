# Tutorial V5

## 1. Instalar

`python -m pip install -r requirements.txt`

## 2. Ingestão

`python -m src.pipeline`

Explique que o script captura CSV/JSON sem regras de negócio.

## 3. dbt

```bash
cd dbt
python -m dbt.cli.main debug --profiles-dir .
python -m dbt.cli.main build --profiles-dir .
python -m dbt.cli.main docs generate --profiles-dir .
cd ..
```

## 4. Resposta

`python consultas/executar_respostas.py`

Primeiro mostre a tabela por tipo e período; depois a tabela por etapa.

## 5. Delta

`python consultas/delta_time_travel.py`

Mostre histórico e versão 0.

## 6. Mensagem para o gestor

A resposta deve mostrar:
- tempo médio do processo;
- variação por tipo de conflito;
- variação por mês de entrada;
- etapa com maior permanência média.

Não diga que a etapa “causa” o atraso apenas com estes dados.
