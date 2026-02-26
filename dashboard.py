import streamlit as st
import pandas as pd
import plotly.express as px

st.title("ATUALIZOU AGORA 🔥")

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================

st.set_page_config(page_title="Painel Kemparts", layout="wide")

st.image("LOGO_KEMPARTS_ALTA_DEFINICAO.png", width=250)

st.title("Relatório de Performance KP - Fevereiro 2026")

# =============================
# CARREGAR BASE DE DADOS
# =============================

df = pd.read_excel("BASE UNIFICADA SC X SP.xlsx")

df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
df["Custo"] = pd.to_numeric(df["Custo"], errors="coerce")
df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")
df["DT Emissao"] = pd.to_datetime(df["DT Emissao"], errors="coerce")

df = df[df["Vendedor 1"] != "KP"]

# =============================
# FILTROS
# =============================

st.sidebar.markdown("### 🔎 Filtros de Análise")

estado_filtro = st.sidebar.multiselect("Estado", df["Estado"].dropna().unique())
vendedor_filtro = st.sidebar.multiselect("Vendedor", df["Vendedor 1"].dropna().unique())
grupo_filtro = st.sidebar.multiselect("Grupo", df["Nome Grupo"].dropna().unique())

df_filtrado = df.copy()

if estado_filtro:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado_filtro)]

if vendedor_filtro:
    df_filtrado = df_filtrado[df_filtrado["Vendedor 1"].isin(vendedor_filtro)]

if grupo_filtro:
    df_filtrado = df_filtrado[df_filtrado["Nome Grupo"].isin(grupo_filtro)]

# =============================
# KPIs
# =============================

meta_mensal = 3193147.61

faturamento_total = df_filtrado["Total"].sum()
custo_total = df_filtrado["Custo"].sum()
total_pedidos = df_filtrado["Numero"].nunique()

margem = ((faturamento_total - custo_total) / faturamento_total) * 100 if faturamento_total > 0 else 0
ticket_medio = faturamento_total / total_pedidos if total_pedidos > 0 else 0
atingimento_meta = (faturamento_total / meta_mensal) * 100 if meta_mensal > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("🎯 Meta Mensal", f"R$ {meta_mensal:,.2f}")
col2.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
col3.metric("📊 % Atingido", f"{atingimento_meta:.2f}%")
col4.metric("📈 Margem (%)", f"{margem:.2f}%")
col5.metric("🛒 Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# =============================
# GRÁFICOS
# =============================

evolucao = df_filtrado.groupby(df_filtrado["DT Emissao"].dt.date)["Total"].sum().reset_index()

st.plotly_chart(px.line(evolucao, x="DT Emissao", y="Total"))

grupo = df_filtrado.groupby("Nome Grupo")["Total"].sum().reset_index()
st.plotly_chart(px.bar(grupo, x="Total", y="Nome Grupo", orientation="h"))

estado = df_filtrado.groupby("Estado")["Total"].sum().reset_index()
st.plotly_chart(px.bar(estado, x="Estado", y="Total"))

vendedor = df_filtrado.groupby("Vendedor 1")["Total"].sum().reset_index()
st.plotly_chart(px.bar(vendedor, x="Total", y="Vendedor 1", orientation="h"))