import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CONFIGURAÇÃO GLOBAL DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="EcoData Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ESTILIZAÇÃO E COMPONENTES VISUAIS (CSS)
# ==========================================
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
        }
        /* Estilo customizado para os blocos/cards */
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MENU LATERAL E FILTROS GLOBAIS
# ==========================================
st.sidebar.markdown("## 🧭 Navegação")
pagina = st.sidebar.radio(
    "Escolha a visualização:", 
    ["Visão Geral (Dashboard)", "Log de Cliques Detalhado"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Filtros Globais")
filtro_data = st.sidebar.selectbox(
    "Período:", 
    ["Últimos 7 Dias", "Últimos 30 Dias", "Este Mês", "Personalizado"]
)

# ==========================================
# 4. VISÃO PRINCIPAL: DASHBOARD
# ==========================================
if pagina == "Visão Geral (Dashboard)":
    
    # --- BLOCO 0: CABEÇALHO ---
    col_title, col_status = st.columns([3, 1])
    with col_title:
        st.title("📊 EcoData Performance Dashboard")
    with col_status:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("🟢 ONLINE - API ATIVA")

    st.markdown("---")

    # --- BLOCO 1: TOP METRICS (Cartões Superiores) ---
    st.markdown("### 📌 Indicadores Gerais")
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

    # --- BLOCO 2: GRÁFICO (Isolado em um Card Escuro) ---
    with st.container(border=True):
        st.subheader("📈 Crescimento de Vendas vs. Gasto")
        st.markdown("<p style='color: gray; font-size: 14px;'>Evolução diária do capital investido frente ao retorno gerado.</p>", unsafe_allow_html=True)
        
        # Dados do Gráfico
        data_grafico = {
            'Dia': ['01 Jun', '05 Jun', '10 Jun', '15 Jun', '20 Jun', '25 Jun', '30 Jun'],
            'Vendas': [1200, 2300, 3500, 4200, 5600, 6800, 7900],
            'Gasto': [500, 800, 1100, 1400, 1200, 1500, 1650]
        }
        df_grafico = pd.DataFrame(data_grafico)

        fig = px.line(df_grafico, x='Dia', y=['Vendas', 'Gasto'], markers=True)
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", y=1.15, x=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BLOCO 3: TABELA DE PERFORMANCE (Isolado em um Card Escuro) ---
    with st.container(border=True):
        st.subheader("🎯 Tabela: Performance por Campanha (Deep Dive)")
        st.markdown("<p style='color: gray; font-size: 14px;'>Auditoria detalhada por canal e conjunto de anúncios.</p>", unsafe_allow_html=True)
        
        # Dados da Tabela
        df_campanhas = pd.DataFrame({
            'Campanha': ['Campanha A', 'Campanha B', 'Campanha C'],
            'Gasto': ['R$ 500,00', 'R$ 300,00', 'R$ 100,00'],
            'Cliques': [120, 95, 40],
            'CPA Real': ['R$ 15,20', 'R$ 18,50', 'R$ 12,00'],
            'Status': ['🟢 ATIVA', '🟢 ATIVA', '🔴 PAUSADA']
        })
        st.dataframe(df_campanhas, use_container_width=True)

    st.markdown("---")

    # --- BLOCO 4: STATUS DA INFRAESTRUTURA TÉCNICA ---
    st.subheader("🛠️ Status da Infraestrutura Técnica")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("✔ Pixel Meta Server-Side: Sincronizado (Último log: 2s atrás)")
        st.success("✔ API de Conversão Google: OK")
    with col_b:
        st.success("✔ Rastreamento de Leads: 100% (Sem perdas por adblockers)")
        st.success("✔ Webhook Vendas: OK")

# ==========================================
# 5. VISÃO SECUNDÁRIA: LOG DE CLIQUES
# ==========================================
elif pagina == "Log de Cliques Detalhado":
    st.title("🔍 Quem Clicou (Logs em Tempo Real)")
    st.write("Acompanhe cada acesso capturado pelo seu servidor antes do redirecionamento:")
    
    with st.container(border=True):
        df_cliques = pd.DataFrame({
            'Horário': ['12:01:45', '12:05:12', '12:10:30', '12:15:02'],
            'IP do Usuário': ['192.168.1.15', '201.88.42.10', '177.22.10.5', '187.14.99.20'],
            'Origem': ['Instagram (Campanha A)', 'Google (Pesquisa)', 'Instagram (Campanha A)', 'Facebook (Campanha B)'],
            'Cliques': [1, 3, 1, 2]
        })
        st.dataframe(df_cliques, use_container_width=True)
    
    st.markdown("---")
    st.info("💡 No futuro, cada linha desta tabela será preenchida automaticamente pelas informações reais salvas no seu banco de dados.")
