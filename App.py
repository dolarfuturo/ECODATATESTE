import streamlit as st
import plotly.express as px
import pandas as pd

# ==========================================
# 1. CONFIGURAÇÃO GLOBAL DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="EcoData Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializar estado da página
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = '📊 Visão Geral'

# ==========================================
# 2. ESTILIZAÇÃO CSS CUSTOMIZADA (FORÇANDO FUNDO SÓLIDO EM TUDO)
# ==========================================
st.markdown("""
    <style>
        .stApp {
            background-color: #0a0e17;
            color: #ffffff;
        }
        
        /* Navbar Superior */
        .top-navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #0f172a;
            padding: 12px 20px;
            border-bottom: 1px solid #1e293b;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .nav-brand {
            font-weight: bold;
            font-size: 16px;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Estilização dos botões do menu superior */
        [data-testid="stHorizontalBlock"] button {
            background-color: transparent !important;
            border: none !important;
            color: #94a3b8 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-align: left !important;
            padding: 4px 8px !important;
            box-shadow: none !important;
        }
        [data-testid="stHorizontalBlock"] button:hover {
            color: #38bdf8 !important;
        }

        /* Forçar fundo #121824 em TODOS os contêineres e blocos internos */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #121824 !important;
            border: 1px solid #1e293b !important;
            border-radius: 12px !important;
            padding: 20px !important;
            margin-bottom: 20px !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] div,
        [data-testid="stVerticalBlockBorderWrapper"] section,
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"],
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"],
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stColumn"] {
            background-color: transparent !important;
        }

        /* Cartões de Métricas Superiores */
        .metric-box {
            background-color: #121824;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 16px;
        }
        .metric-title {
            font-size: 11px;
            color: #64748b;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 6px;
            margin-bottom: 4px;
        }
        .metric-sub-green {
            font-size: 12px;
            color: #22c55e;
            font-weight: 500;
        }
        .metric-sub-gray {
            font-size: 12px;
            color: #94a3b8;
        }

        /* Badge de Status Online */
        .status-badge {
            background-color: #052e16;
            border: 1px solid #15803d;
            color: #22c55e;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }

        /* Títulos Internos dos Blocos */
        .block-header {
            font-size: 14px;
            font-weight: 700;
            color: #f8fafc;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            text-transform: uppercase;
        }

        /* Estilização da Tabela Customizada */
        .custom-table {
            width: 100%;
            border-collapse: collapse;
            color: #ffffff;
            font-size: 13px;
        }
        .custom-table th {
            text-align: left;
            padding: 10px 12px;
            color: #64748b;
            font-size: 11px;
            text-transform: uppercase;
            border-bottom: 1px solid #1e293b;
        }
        .custom-table td {
            padding: 12px;
            border-bottom: 1px solid #1e293b;
            color: #f8fafc;
        }
        .action-btn {
            color: #38bdf8;
            cursor: pointer;
            font-weight: 500;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BARRA DE NAVEGAÇÃO SUPERIOR INTERATIVA
# ==========================================
st.markdown('<div class="top-navbar">', unsafe_allow_html=True)
nav_col1, nav_col2 = st.columns([2, 5])

with nav_col1:
    st.markdown('<div class="nav-brand"><span>🌐 ECODATA PERFORMANCE</span></div>', unsafe_allow_html=True)

with nav_col2:
    b1, b2, b3, b4, b5 = st.columns(5)
    with b1:
        if st.button("📊 Visão Geral", use_container_width=True):
            st.session_state.pagina_atual = '📊 Visão Geral'
    with b2:
        if st.button("🎯 Campanhas", use_container_width=True):
            st.session_state.pagina_atual = '🎯 Campanhas'
    with b3:
        if st.button("👥 Leads", use_container_width=True):
            st.session_state.pagina_atual = '👥 Leads'
    with b4:
        if st.button("📄 Relatórios", use_container_width=True):
            st.session_state.pagina_atual = '📄 Relatórios'
    with b5:
        if st.button("⚙️ Configurações", use_container_width=True):
            st.session_state.pagina_atual = '⚙️ Configurações'

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. CONTEÚDO DINÂMICO BASEADO NA PÁGINA SELECIONADA
# ==========================================

if st.session_state.pagina_atual == '📊 Visão Geral':
    # Filtro e Status
    col_filter, col_status = st.columns([3, 1])
    with col_filter:
        st.markdown("<span style='color: #94a3b8; font-size: 13px;'>Filtro de Data:</span> &nbsp;&nbsp; `[ Últimos 30 Dias ▾ ]`", unsafe_allow_html=True)
    with col_status:
        st.markdown("<div style='text-align: right;'><span class='status-badge'>🟢 ONLINE - API ATIVA</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bloco de Métricas Superiores
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
            <div class="metric-box">
                <div class="metric-title">[INVESTIMENTO]</div>
                <div class="metric-value">R$ 15.400,00</div>
                <div class="metric-sub-green">▲ 12%</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
            <div class="metric-box">
                <div class="metric-title">[FATURAMENTO]</div>
                <div class="metric-value">R$ 48.200,00</div>
                <div class="metric-sub-green">▲ 6%</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
            <div class="metric-box">
                <div class="metric-title">[ROAS]</div>
                <div class="metric-value">3.13x</div>
                <div class="metric-sub-gray">(Meta: 2.5x)</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
            <div class="metric-box">
                <div class="metric-title">[LEADS QUALIFICADOS]</div>
                <div class="metric-value">452</div>
                <div class="metric-sub-green">Taxa conv. 4.2%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Seção 1: Gráfico
    with st.container(border=True):
        st.markdown('<div class="block-header">CRESCIMENTO DE VENDAS VS. GASTO</div>', unsafe_allow_html=True)
        df_grafico = pd.DataFrame({
            'Dia': ['00:00h', '01:00h', '16:00h', '17:00h', '18:00h', '19:00h', '20:00h', '23:00h', '30 dias'],
            'Vendas': [1000, 2200, 3800, 4100, 5600, 6000, 5200, 7100, 1400],
            'Gasto': [200, 800, 1000, 2500, 3200, 5800, 4500, 3200, 1300]
        })
        fig = px.line(df_grafico, x='Dia', y=['Vendas', 'Gasto'], markers=True)
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="#121824",
            paper_bgcolor="#121824",
            margin=dict(l=10, r=10, t=10, b=10),
            height=260,
            legend=dict(orientation="h", y=1.15, x=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    # Seção 2: Tabela
    with st.container(border=True):
        st.markdown('<div class="block-header">TABELA: PERFORMANCE POR CAMPANHA (Deep Dive)</div>', unsafe_allow_html=True)
        st.markdown("""
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>Campanha</th>
                        <th>Gasto</th>
                        <th>Cliques</th>
                        <th>CPA Real</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Campanha A</td>
                        <td>R$ 500</td>
                        <td>120</td>
                        <td>R$ 15,20</td>
                        <td><span style="color: #22c55e;">🟢 ATIVA</span></td>
                        <td><span class="action-btn">[Pausar]</span> <span class="action-btn">[Otimizar]</span></td>
                    </tr>
                    <tr>
                        <td>Campanha B</td>
                        <td>R$ 500</td>
                        <td>120</td>
                        <td>R$ 15,20</td>
                        <td><span style="color: #22c55e;">🟢 ATIVA</span></td>
                        <td><span class="action-btn">[Pausar]</span> <span class="action-btn">[Otimizar]</span></td>
                    </tr>
                </tbody>
            </table>
        """, unsafe_allow_html=True)

    # Seção 3: Status da Infraestrutura
    with st.container(border=True):
        st.markdown('<div class="block-header">STATUS DA INFRAESTRUTURA TÉCNICA</div>', unsafe_allow_html=True)
        col_infra1, col_infra2 = st.columns(2)
        with col_infra1:
            st.markdown("✅ Pixel Meta Server-Side: <span style='color: #22c55e;'>Sincronizado</span> (Último log: 2s atrás)", unsafe_allow_html=True)
            st.markdown("✅ API de Conversão Google: <span style='color: #22c55e;'>OK</span>", unsafe_allow_html=True)
        with col_infra2:
            st.markdown("✅ Rastreamento de Leads: <span style='color: #22c55e;'>100%</span> (Sem perdas por adblockers)", unsafe_allow_html=True)
            st.markdown("✅ Webhook Vendas: <span style='color: #22c55e;'>OK</span>", unsafe_allow_html=True)

elif st.session_state.pagina_atual == '🎯 Campanhas':
    with st.container(border=True):
        st.markdown('<div class="block-header">GESTÃO AVANÇADA DE CAMPANHAS</div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Aqui você gerencia campanhas ativas, define orçamentos automatizados e otimiza o ROAS via Server-Side.</p>", unsafe_allow_html=True)
        st.markdown("### Campanhas em Execução", unsafe_allow_html=True)
        st.markdown("- **Campanha Scale Q3**: Investimento R$ 8.500,00 | Retorno R$ 28.100,00 | ROAS 3.3x")
        st.markdown("- **Campanha Remarketing**: Investimento R$ 3.500,00 | Retorno R$ 12.400,00 | ROAS 3.5x")

elif st.session_state.pagina_atual == '👥 Leads':
    with st.container(border=True):
        st.markdown('<div class="block-header">QUALIFICAÇÃO E FUNIL DE LEADS</div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Acompanhamento de leads capturados sem perdas por adblockers e pontuação de qualificação automática.</p>", unsafe_allow_html=True)
        st.markdown("- **Total de Leads Capturados**: 452")
        st.markdown("- **Leads Qualificados (API)**: 380")
        st.markdown("- **Taxa de Conversão do Funil**: 4.2%")

elif st.session_state.pagina_atual == '📄 Relatórios':
    with st.container(border=True):
        st.markdown('<div class="block-header">RELATÓRIOS E AUDITORIA DE DADOS</div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Geração de relatórios independentes baseados na fonte da verdade server-side.</p>", unsafe_allow_html=True)
        st.markdown("- 📥 Baixar Relatório Consolidado de Vendas (CSV)")
        st.markdown("- 📥 Exportar Logs de Auditoria de API (JSON)")

elif st.session_state.pagina_atual == '⚙️ Configurações':
    with st.container(border=True):
        st.markdown('<div class="block-header">CONFIGURAÇÕES DO ECOSSISTEMA E APIS</div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Gerenciamento de chaves de API, webhooks e integração com servidores de rastreamento.</p>", unsafe_allow_html=True)
        st.markdown("- **Token API Meta**: `EAAG...sh29` (Conectado)")
        st.markdown("- **Token API Google Ads**: `GGL...91a` (Conectado)")
        st.markdown("- **Endpoint Webhook**: `https://api.ecodata.io/v1/webhook`")
