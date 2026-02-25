import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================

st.set_page_config(page_title="Painel Kemparts", layout="wide")

st.image("LOGO_KEMPARTS_ALTA_DEFINICAO.png", width=250)

st.title("Painel Kemparts - Fevereiro 2026")

# =============================
# CARREGAR BASE DE DADOS
# =============================

df = pd.read_excel("BASE UNIFICADA SC X SP.xlsx")

# Ajustar tipos
df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
df["Custo"] = pd.to_numeric(df["Custo"], errors="coerce")
df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
df["DT Emissao"] = pd.to_datetime(df["DT Emissao"], errors="coerce")

# Remover vendedor KP
df = df[df["Vendedor 1"] != "KP"]

# =============================
# FILTROS LATERAIS
# =============================

st.sidebar.markdown("### 🔎 Filtros de Análise")

estado_filtro = st.sidebar.multiselect(
    "Estado",
    df["Estado"].dropna().unique(),
    placeholder="Selecione o estado"
)

vendedor_filtro = st.sidebar.multiselect(
    "Vendedor",
    df["Vendedor 1"].dropna().unique(),
    placeholder="Selecione o vendedor"
)

grupo_filtro = st.sidebar.multiselect(
    "Grupo",
    df["Nome Grupo"].dropna().unique(),
    placeholder="Selecione o grupo"
)

# =============================
# APLICAR FILTROS
# =============================

df_filtrado = df.copy()

if estado_filtro:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado_filtro)]

if vendedor_filtro:
    df_filtrado = df_filtrado[df_filtrado["Vendedor 1"].isin(vendedor_filtro)]

if grupo_filtro:
    df_filtrado = df_filtrado[df_filtrado["Nome Grupo"].isin(grupo_filtro)]



# =============================
# KPIs PRINCIPAIS
# =============================

meta_mensal = 3193147.61

faturamento_total = df_filtrado["Total"].sum()
custo_total = df_filtrado["Custo"].sum()
quantidade_total = df_filtrado["Quantidade"].sum()
total_pedidos = df_filtrado["Numero"].nunique()

margem = 0
if faturamento_total > 0:
    margem = ((faturamento_total - custo_total) / faturamento_total) * 100

ticket_medio = 0
if total_pedidos > 0:
    ticket_medio = faturamento_total / total_pedidos

atingimento_meta = 0
if meta_mensal > 0:
    atingimento_meta = (faturamento_total / meta_mensal) * 100

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🎯 Meta Mensal", f"R$ {meta_mensal:,.2f}")
col2.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")


col3.metric(
    "📊 % Atingido",
    f"{atingimento_meta:.2f}%",
    delta=f"{faturamento_total - meta_mensal:,.2f}"
)

col4.metric("📈 Margem (%)", f"{margem:.2f}%")
col5.metric("🛒 Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# =============================
# EVOLUÇÃO DO FATURAMENTO
# =============================

evolucao = (
    df_filtrado.groupby(df_filtrado["DT Emissao"].dt.date)["Total"]
    .sum()
    .reset_index()
)

fig_linha = px.line(
    evolucao,
    x="DT Emissao",
    y="Total",
    title="📈 Evolução do Faturamento Diário"
)

st.plotly_chart(fig_linha, use_container_width=True)

# =============================
# FATURAMENTO POR GRUPO
# =============================

grupo = (
    df_filtrado.groupby("Nome Grupo")["Total"]
    .sum()
    .reset_index()
    .sort_values(by="Total", ascending=False)
)

fig_grupo = px.bar(
    grupo,
    x="Total",
    y="Nome Grupo",
    orientation="h",
    title="📦 Faturamento por Grupo"
)

st.plotly_chart(fig_grupo, use_container_width=True)

# =============================
# FATURAMENTO POR ESTADO
# =============================

estado = (
    df_filtrado.groupby("Estado")["Total"]
    .sum()
    .reset_index()
)

fig_estado = px.bar(
    estado,
    x="Estado",
    y="Total",
    title="🗺 Faturamento por Estado"
)

st.plotly_chart(fig_estado, use_container_width=True)

# =============================
# FATURAMENTO POR VENDEDOR
# =============================

vendedor = (
    df_filtrado.groupby("Vendedor 1")["Total"]
    .sum()
    .reset_index()
    .sort_values(by="Total", ascending=False)
)

fig_vendedor = px.bar(
    vendedor,
    x="Total",
    y="Vendedor 1",
    orientation="h",
    title="👔 Faturamento por Vendedor"
)

st.plotly_chart(fig_vendedor, use_container_width=True)

# =============================
# RANKING TOP 3
# =============================

st.markdown("## 🏆 Ranking - Top 3 Vendedores")

top3 = vendedor.head(3)

if not top3.empty:
    melhor_vendedor = top3.iloc[0]

    st.success(
        f"🥇 Melhor Vendedor: {melhor_vendedor['Vendedor 1']} "
        f"com R$ {melhor_vendedor['Total']:,.2f}"
    )

st.dataframe(top3)

fig_top3 = px.bar(
    top3,
    x="Vendedor 1",
    y="Total",
    title="🏆 Top 3 Vendedores"
)

st.plotly_chart(fig_top3, use_container_width=True)
