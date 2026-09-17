from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "data" / "pipeline.duckdb"))

for nome in ["resposta_principal.sql", "resposta_gargalo.sql"]:
    print("\n===", nome, "===")
    sql = (ROOT / "consultas" / nome).read_text(encoding="utf-8")
    print(con.sql(sql).df().to_string(index=False))

con.close()
