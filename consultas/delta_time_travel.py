from pathlib import Path
from deltalake import DeltaTable

ROOT = Path(__file__).resolve().parents[1]

for nome in ["solicitacoes", "historico_etapas"]:
    dt = DeltaTable(str(ROOT / "data" / "delta" / nome))
    print(f"\n=== {nome} ===")
    print("versão atual:", dt.version())
    print("histórico:")
    print(dt.history())
    if dt.version() >= 1:
        atual = dt.to_pandas()
        dt.load_as_version(0)
        anterior = dt.to_pandas()
        print("linhas versão 0:", len(anterior))
        print("linhas versão atual:", len(atual))
        print("time travel OK")
