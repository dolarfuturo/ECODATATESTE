import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para modo Wide (estilo profissional)
st.set_page_config(page_title="EcoData Performance", layout="wide")

st.title("📊 EcoData Performance Dashboard")

# --- Dados Fictícios para Teste ---
data = {
    'Dia': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
    'Vendas': [1200, 1500, 1800, 1400, 2200, 2500, 2100],
    'Gasto': [500, 600, 550, 700, 800, 900, 750]
}
df = pd.DataFrame(data)

# --- Top Metrics (Cartões de métricas) ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Investimento", "R$ 15.400,00", "+12%")
c2.metric("Faturamento", "R$ 48.200,00", "+8%")
c3.metric("ROAS", "3.13x", "Meta: 2.5x")
c4.metric("Leads", "452", "Taxa: 4.2%")

st.markdown("---")

# --- Gráfico ---
st.subheader("📈 Crescimento de Vendas vs. Gasto")
fig = px.line(df, x='Dia', y=['Vendas', 'Gasto'], markers=True)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# --- Tabela de Campanhas ---
st.subheader("🎯 Tabela de Performance")
df_campanhas = pd.DataFrame({
    'Campanha': ['Campanha A', 'Campanha B', 'Campanha C'],
    'Gasto': [500, 300, 100],
    'Status': ['🟢 ATIVA', '🟢 ATIVA', '🔴 PAUSADA']
})
st.dataframe(df_campanhas, use_container_width=True)

# --- Status da Infraestrutura ---
st.markdown("---")
st.subheader("🛠️ Status da Infraestrutura (Server-Side)")
col_a, col_b, col_c = st.columns(3)
col_a.success("API Meta: Online")
col_b.success("API Google: Online")
col_c.success("Rastreamento: Ativo")

