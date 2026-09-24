from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Concilia Vagas",
    page_icon="📊",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "pipeline.duckdb"

st.title("📊 Concilia Vagas")
st.subheader("Análise do volume e do tempo de conciliação de vagas")
st.caption(
    "A análise de tempo considera somente solicitações finalizadas "
    "com histórico temporal válido e etapa FINALIZAÇÃO registrada."
)

con = duckdb.connect(str(DB_PATH), read_only=True)

df_tempo = con.sql("SELECT * FROM consumo_tempo_conciliacao").df()
df_etapas = con.sql("SELECT * FROM consumo_tempo_etapas").df()
df_volume = con.sql("SELECT * FROM consumo_volume_solicitacoes").df()
df_cobertura = con.sql("SELECT * FROM consumo_cobertura_historico").df()

con.close()

if not df_tempo.empty:
    df_tempo["data_entrada"] = pd.to_datetime(df_tempo["data_entrada"])
    df_tempo["data_finalizacao"] = pd.to_datetime(df_tempo["data_finalizacao"])

if not df_volume.empty:
    df_volume["periodo_entrada"] = df_volume["periodo_entrada"].astype(str)

st.sidebar.header("🔎 Filtros")

if not df_tempo.empty:
    tipos = sorted(df_tempo["tipo_conflito"].dropna().unique().tolist())
    tipos_selecionados = st.sidebar.multiselect(
        "Tipo de conflito",
        options=tipos,
        default=tipos,
    )
    df_filtrado = df_tempo[
        df_tempo["tipo_conflito"].isin(tipos_selecionados)
    ].copy()
else:
    tipos_selecionados = []
    df_filtrado = df_tempo.copy()

total_finalizadas = 0
total_analisadas = 0
cobertura = 0.0

if not df_cobertura.empty:
    total_finalizadas = int(df_cobertura.iloc[0]["total_finalizadas"])
    total_analisadas = int(df_cobertura.iloc[0]["total_analisadas"])
    cobertura = float(df_cobertura.iloc[0]["cobertura_historico_percentual"])

tempo_medio = (
    float(df_filtrado["tempo_total_conciliacao_dias"].mean())
    if not df_filtrado.empty else 0.0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Solicitações finalizadas", f"{total_finalizadas:,}".replace(",", "."))
with col2:
    st.metric("Solicitações analisadas", f"{total_analisadas:,}".replace(",", "."))
with col3:
    st.metric("Cobertura do histórico", f"{cobertura:.1f}%")
with col4:
    st.metric("Tempo médio analisado", f"{tempo_medio:.1f} dias")

if total_finalizadas > total_analisadas:
    st.info(
        f"ℹ️ Existem {total_finalizadas} solicitações com status FINALIZADA, "
        f"mas somente {total_analisadas} possuem histórico temporal válido "
        f"para o cálculo do tempo de conciliação."
    )

st.divider()

# VOLUME
col_volume, col_status = st.columns(2)

with col_volume:
    st.subheader("📈 Volume por período")
    if not df_volume.empty:
        volume_periodo = (
            df_volume.groupby("periodo_entrada", as_index=False)
            ["quantidade_solicitacoes"].sum()
            .sort_values("periodo_entrada")
            .set_index("periodo_entrada")
            .rename(columns={"quantidade_solicitacoes": "Solicitações"})
        )
        st.bar_chart(volume_periodo, width="stretch")
        if len(volume_periodo) == 1:
            st.caption(
                f"Os dados disponíveis nesta camada concentram o volume no período "
                f"{volume_periodo.index[0]}."
            )
    else:
        st.warning("Não há dados de volume disponíveis.")

with col_status:
    st.subheader("📊 Volume por período e status")
    if not df_volume.empty:
        volume_status = (
            df_volume.pivot_table(
                index="periodo_entrada",
                columns="status",
                values="quantidade_solicitacoes",
                aggfunc="sum",
                fill_value=0,
            )
            .sort_index()
        )
        nomes_status = {
            "EM_ANALISE": "Em análise",
            "EM_ANÁLISE": "Em análise",
            "FINALIZADA": "Finalizada",
            "REGISTRADA": "Registrada",
        }
        volume_status = volume_status.rename(columns=nomes_status)
        st.bar_chart(volume_status, width="stretch")
    else:
        st.warning("Não há dados de status disponíveis.")

st.divider()

# NOMES AMIGÁVEIS SOMENTE NA APRESENTAÇÃO
nomes_conflito = {
    "LONGE_DA_RESIDENCIA": "Longe da residência",
    "PROXIMA_DA_RESIDENCIA": "Próxima da residência",
    "NA_ESCOLA_DO_IRMAO": "Na escola do irmão",
    "NO_CAMINHO_DO_TRABALHO": "No caminho do trabalho",
    "PROXIMA_DO_TRABALHO": "Próxima do trabalho",
    "MESMA_REGIAO_DA_RESIDENCIA": "Mesma região da residência",
    "ACESSO_POR_TRANSPORTE_PUBLICO": "Transporte público",
    "OUTRO": "Outro",
}

nomes_etapa = {
    "RECEPCAO_TRIAGEM": "Recepção / triagem",
    "ANALISE": "Análise",
    "NEGOCIACAO": "Negociação",
    "VALIDACAO": "Validação",
    "FINALIZACAO": "Finalização",
}

# TEMPO
col_tipo, col_etapa = st.columns(2)

with col_tipo:
    st.subheader("⏱️ Tempo médio por tipo de conflito")

    if not df_filtrado.empty:
        tempo_tipo = (
            df_filtrado.groupby("tipo_conflito", as_index=False)
            ["tempo_total_conciliacao_dias"].mean()
            .sort_values("tempo_total_conciliacao_dias")
        )
        tempo_tipo["tempo_total_conciliacao_dias"] = (
            tempo_tipo["tempo_total_conciliacao_dias"].round(1)
        )
        tempo_tipo["tipo_exibicao"] = (
            tempo_tipo["tipo_conflito"]
            .map(nomes_conflito)
            .fillna(tempo_tipo["tipo_conflito"])
        )
        tempo_tipo_chart = tempo_tipo[["tipo_exibicao", "tempo_total_conciliacao_dias"]].rename(
            columns={"tipo_exibicao": "Tipo de conflito", "tempo_total_conciliacao_dias": "Dias"}
        )
        st.vega_lite_chart(
            tempo_tipo_chart,
            {
                "mark": {"type": "bar", "cornerRadiusEnd": 3},
                "encoding": {
                    "y": {"field": "Tipo de conflito", "type": "nominal", "sort": "-x", "title": None},
                    "x": {"field": "Dias", "type": "quantitative", "title": "Dias", "scale": {"zero": True}},
                    "tooltip": [
                        {"field": "Tipo de conflito", "type": "nominal", "title": "Tipo de conflito"},
                        {"field": "Dias", "type": "quantitative", "title": "Dias", "format": ".1f"},
                    ],
                },
                "height": 260,
            },
            use_container_width=True,
        )
    else:
        st.warning("Nenhuma solicitação corresponde aos filtros selecionados.")

with col_etapa:
    st.subheader("⏱️ Tempo médio por etapa")

    if not df_etapas.empty and not df_filtrado.empty:
        ids_validos = df_filtrado["id_solicitacao"].unique()
        etapas_filtradas = df_etapas[
            df_etapas["id_solicitacao"].isin(ids_validos)
        ].copy()

        if not etapas_filtradas.empty:
            tempo_etapas = (
                etapas_filtradas.groupby("etapa", as_index=False)
                ["tempo_espera_etapa_dias"].mean()
                .sort_values("tempo_espera_etapa_dias")
            )
            tempo_etapas["tempo_espera_etapa_dias"] = (
                tempo_etapas["tempo_espera_etapa_dias"].round(1)
            )
            tempo_etapas["etapa_exibicao"] = (
                tempo_etapas["etapa"]
                .map(nomes_etapa)
                .fillna(tempo_etapas["etapa"])
            )
            tempo_etapas_chart = (
                tempo_etapas.set_index("etapa_exibicao")
                [["tempo_espera_etapa_dias"]]
                .rename(columns={"tempo_espera_etapa_dias": "Dias"})
            )
            st.bar_chart(tempo_etapas_chart, width="stretch")

            etapa_maior_tempo = tempo_etapas.iloc[-1]
            etapa_maior_tempo_nome = nomes_etapa.get(
                etapa_maior_tempo["etapa"], etapa_maior_tempo["etapa"]
            )
            st.info(
                f"📌 Na amostra filtrada, a etapa com maior tempo médio "
                f"de permanência é **{etapa_maior_tempo_nome}**, "
                f"com aproximadamente "
                f"**{etapa_maior_tempo['tempo_espera_etapa_dias']:.1f} dias**."
            )
        else:
            st.warning("Não há histórico de etapas para os filtros selecionados.")
    else:
        st.warning("Não há dados suficientes para calcular o tempo por etapa.")

# TEMPO POR PERÍODO: só aparece se houver pelo menos dois períodos
if not df_filtrado.empty:
    tempo_periodo = (
        df_filtrado.groupby("periodo_entrada", as_index=False)
        ["tempo_total_conciliacao_dias"].mean()
        .sort_values("periodo_entrada")
    )
    tempo_periodo["tempo_total_conciliacao_dias"] = (
        tempo_periodo["tempo_total_conciliacao_dias"].round(1)
    )

    if len(tempo_periodo) > 1:
        st.divider()
        st.subheader("📅 Tempo médio por período de entrada")
        tempo_periodo_chart = (
            tempo_periodo.set_index("periodo_entrada")
            [["tempo_total_conciliacao_dias"]]
            .rename(columns={"tempo_total_conciliacao_dias": "Dias"})
        )
        st.line_chart(tempo_periodo_chart, width="stretch")

# TABELA
st.divider()
st.subheader("📋 Solicitações analisadas")

if not df_filtrado.empty:
    colunas_exibicao = [
        "id_solicitacao",
        "protocolo",
        "tipo_conflito",
        "data_entrada",
        "data_finalizacao",
        "periodo_entrada",
        "tempo_total_conciliacao_dias",
    ]

    tabela = df_filtrado[colunas_exibicao].copy()
    tabela = tabela.rename(
        columns={
            "id_solicitacao": "ID",
            "protocolo": "Protocolo",
            "tipo_conflito": "Tipo de conflito",
            "data_entrada": "Entrada",
            "data_finalizacao": "Finalização",
            "periodo_entrada": "Período",
            "tempo_total_conciliacao_dias": "Tempo total (dias)",
        }
    )

    tabela["Tipo de conflito"] = (
        tabela["Tipo de conflito"]
        .map(nomes_conflito)
        .fillna(tabela["Tipo de conflito"])
    )
    tabela["Entrada"] = tabela["Entrada"].dt.strftime("%d/%m/%Y %H:%M")
    tabela["Finalização"] = tabela["Finalização"].dt.strftime("%d/%m/%Y %H:%M")
    tabela["Tempo total (dias)"] = tabela["Tempo total (dias)"].round(1)

    st.dataframe(tabela, width="stretch", hide_index=True)
else:
    st.info("Nenhuma solicitação foi encontrada para os filtros selecionados.")

st.divider()

st.caption(
    "Nota metodológica: a camada de tempo utiliza somente solicitações "
    "FINALIZADA com histórico temporal válido. Como o histórico não "
    "possui uma etapa explícita de FINALIZACAO, a data de finalização "
    "utilizada corresponde ao maior data_fim disponível."
)
