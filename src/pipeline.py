dfrom pathlib import Path
import json
import pandas as pd
import duckdb
from deltalake import write_deltalake

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DB = ROOT / "data" / "pipeline.duckdb"
DELTA = ROOT / "data" / "delta"

def main():
    # INGESTÃO: captura e persistência; não há regra de negócio.
    solicitacoes = pd.read_csv(RAW / "solicitacoes.csv", dtype=str, keep_default_na=False)
    complementares = pd.read_csv(RAW / "solicitacoes_complementares.csv", dtype=str, keep_default_na=False)
    historico = pd.DataFrame(json.loads((RAW / "historico_etapas.json").read_text(encoding="utf-8")))

    con = duckdb.connect(str(DB))
    con.register("df_solicitacoes", solicitacoes)
    con.register("df_complementares", complementares)
    con.register("df_historico", historico)
    con.execute("CREATE OR REPLACE TABLE solicitacoes AS SELECT * FROM df_solicitacoes")
    con.execute("CREATE OR REPLACE TABLE solicitacoes_complementares AS SELECT * FROM df_complementares")
    con.execute("CREATE OR REPLACE TABLE historico_etapas AS SELECT * FROM df_historico")
    con.close()

    # Preservação/versionamento Delta das fontes capturadas.
    for nome, df in [
        ("solicitacoes", solicitacoes),
        ("solicitacoes_complementares", complementares),
        ("historico_etapas", historico),
    ]:
        path=DELTA/nome
        write_deltalake(str(path), df, mode="overwrite")
        write_deltalake(str(path), df, mode="overwrite")

    print("Ingestão concluída; versões Delta 0 e 1 geradas.")

if __name__ == "__main__":
    main()
