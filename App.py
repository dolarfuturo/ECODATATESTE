import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para modo Wide (estilo profissional)
st.set_page_config(
    page_title="EcoData Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
        }
        .stMetric {
            background-color: #161b22;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #30363d;
        }
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL (Navegação) ---
st.sidebar.markdown("## 🧭 Navegação")
pagina = st.sidebar.radio(
    "Escolha a visualização:", 
    ["Visão Geral (Dashboard)", "Log de Cliques Detalhado"]
)

# --- FILTROS GLOBAIS (Topo da Sidebar) ---
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Filtros")
filtro_data = st.sidebar.selectbox(
    "Filtro de Data:", 
    ["Últimos 7 Dias", "Últimos 30 Dias", "Este Mês", "Personalizado"]
)

if pagina == "Visão Geral (Dashboard)":
    # Cabeçalho Principal com Status da Infraestrutura no Topo
    col_title, col_status = st.columns([3, 1])
    with col_title:
        st.title("📊 EcoData Performance Dashboard")
    with col_status:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("🟢 ONLINE - API ATIVA")

    st.markdown(f"*Período selecionado: **{filtro_data}***")
    st.markdown("---")

    # --- Dados Fictícios para Teste ---
    data = {
        'Dia': ['01 Jun', '05 Jun', '10 Jun', '15 Jun', '20 Jun', '25 Jun', '30 Jun'],
        'Vendas': [1200, 2300, 3500, 4200, 5600, 6800, 7900],
        'Gasto': [500, 800, 1100, 1400, 1200, 1500, 1650]
    }
    df = pd.DataFrame(data)

    # --- Top Metrics (Cartões de métricas) ---
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("INVESTIMENTO", "R$ 15.400,00", "▲ 12%")
    with c2:
        st.metric("FATURAMENTO", "R$ 48.200,00", "▲ 8%")
    with c3:
        st.metric("ROAS", "3.13x", "Meta: 2.5x")
    with c4:
        st.metric("LEADS QUALIFICADOS", "452", "Taxa: 4.2%")

    st.markdown("---")

    # --- Gráfico de Crescimento ---
    st.subheader("📈 Crescimento de Vendas vs. Gasto")
    fig = px.line(df, x='Dia', y=['Vendas', 'Gasto'], markers=True)
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Tabela de Campanhas ---
    st.subheader("🎯 Tabela: Performance por Campanha (Deep Dive)")
    df_campanhas = pd.DataFrame({
        'Campanha': ['Campanha A', 'Campanha B', 'Campanha C'],
        'Gasto': ['R$ 500,00', 'R$ 300,00', 'R$ 100,00'],
        'Cliques': [120, 95, 40],
        'CPA Real': ['R$ 15,20', 'R$ 18,50', 'R$ 12,00'],
        'Status': ['🟢 ATIVA', '🟢 ATIVA', '🔴 PAUSADA']
    })
    st.dataframe(df_campanhas, use_container_width=True)

    # --- Status da Infraestrutura Técnica ---
    st.markdown("---")
    st.subheader("🛠️ Status da Infraestrutura Técnica")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("✔ Pixel Meta Server-Side: Sincronizado (Último log: 2s atrás)")
        st.success("✔ API de Conversão Google: OK")
    with col_b:
        st.success("✔ Rastreamento de Leads: 100% (Sem perdas por adblockers)")
        st.success("✔ Webhook Vendas: OK")

elif pagina == "Log de Cliques Detalhado":
    st.title("🔍 Quem Clicou (Logs em Tempo Real)")
    st.write("Acompanhe cada acesso capturado pelo seu servidor antes do redirecionamento:")
    
    # --- Dados fictícios de quem clicou ---
    df_cliques = pd.DataFrame({
        'Horário': ['12:01:45', '12:05:12', '12:10:30', '12:15:02'],
        'IP do Usuário': ['192.168.1.15', '201.88.42.10', '177.22.10.5', '187.14.99.20'],
        'Origem': ['Instagram (Campanha A)', 'Google (Pesquisa)', 'Instagram (Campanha A)', 'Facebook (Campanha B)'],
        'Cliques': [1, 3, 1, 2]
    })
    
    st.dataframe(df_cliques, use_container_width=True)
    
    st.markdown("---")
    st.info("💡 No futuro, cada linha desta tabela será preenchida automaticamente pelas informações reais salvas no seu banco de dados.")
