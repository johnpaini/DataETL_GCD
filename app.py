import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(
    page_title="Concilia Vagas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Concilia Vagas")
st.subheader("Análise do tempo de conciliação de vagas")

# ============================================================
# CONEXÃO
# ============================================================

con = duckdb.connect("data/pipeline.duckdb")

df = con.sql("""
    SELECT *
    FROM consumo_tempo_conciliacao
""").df()

df_etapas = con.sql("""
    SELECT *
    FROM consumo_tempo_etapas
""").df()

con.close()

# ============================================================
# TRATAMENTO DA DATA PARA VISUALIZAÇÃO
# ============================================================

df["data_entrada"] = pd.to_datetime(df["data_entrada"])

df["periodo_entrada"] = df["data_entrada"].dt.to_period("M").astype(str)

# ============================================================
# FILTROS
# ============================================================

st.sidebar.header("Filtros")

tipos = sorted(df["tipo_conflito"].dropna().unique())

tipo_selecionado = st.sidebar.multiselect(
    "Tipo de conflito",
    tipos,
    default=tipos
)

df_filtrado = df[
    df["tipo_conflito"].isin(tipo_selecionado)
]

# ============================================================
# INDICADORES
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Solicitações finalizadas",
        len(df_filtrado)
    )

with col2:
    st.metric(
        "Tempo médio",
        f"{df_filtrado['tempo_total_conciliacao_dias'].mean():.1f} dias"
    )

with col3:
    st.metric(
        "Maior tempo de conciliação",
        f"{df_filtrado['tempo_total_conciliacao_dias'].max():.0f} dias"
    )

st.divider()

# ============================================================
# GRÁFICO 1 - TEMPO MÉDIO POR TIPO DE CONFLITO
# ============================================================

st.subheader("⏱️ Tempo médio por tipo de conflito")

tempo_tipo = (
    df_filtrado
    .groupby("tipo_conflito", as_index=False)
    ["tempo_total_conciliacao_dias"]
    .mean()
    .sort_values("tempo_total_conciliacao_dias", ascending=False)
)

st.bar_chart(
    tempo_tipo.set_index("tipo_conflito")
)

# ============================================================
# GRÁFICO 2 - EVOLUÇÃO POR PERÍODO
# ============================================================

st.subheader("📅 Tempo médio por período de entrada")

tempo_periodo = (
    df_filtrado
    .groupby("periodo_entrada", as_index=False)
    ["tempo_total_conciliacao_dias"]
    .mean()
    .sort_values("periodo_entrada")
)

st.line_chart(
    tempo_periodo.set_index("periodo_entrada")
)

# ============================================================
# GRÁFICO 3 - TEMPO MÉDIO POR ETAPA
# ============================================================

st.subheader("🚦 Tempo médio por etapa do processo")

ids_validos = df_filtrado["id_solicitacao"].unique()

etapas_filtradas = df_etapas[
    df_etapas["id_solicitacao"].isin(ids_validos)
]

tempo_etapas = (
    etapas_filtradas
    .groupby("etapa", as_index=False)
    ["tempo_espera_etapa_dias"]
    .mean()
    .sort_values("tempo_espera_etapa_dias", ascending=False)
)

st.bar_chart(
    tempo_etapas.set_index("etapa")
)

# ============================================================
# DESTAQUE DA ETAPA COM MAIOR TEMPO
# ============================================================

if not tempo_etapas.empty:

    maior_etapa = tempo_etapas.iloc[0]

    st.info(
        f"📌 A etapa com maior tempo médio de permanência "
        f"é **{maior_etapa['etapa']}**, "
        f"com aproximadamente "
        f"**{maior_etapa['tempo_espera_etapa_dias']:.1f} dias**."
    )

# ============================================================
# DADOS DETALHADOS
# ============================================================

st.subheader("📋 Solicitações analisadas")

st.dataframe(
    df_filtrado,
    use_container_width=True
)