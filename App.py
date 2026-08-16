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
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ESTILIZAÇÃO CSS CUSTOMIZADA (SESSÕES EM BLOCOS)
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
        .nav-links {
            display: flex;
            gap: 25px;
            font-size: 14px;
            color: #94a3b8;
        }
        .nav-link-active {
            color: #38bdf8;
            border-bottom: 2px solid #38bdf8;
            padding-bottom: 4px;
            font-weight: 600;
        }

        /* Blocos Escuros Isolados por Sessão (Exatamente como nos riscos da imagem) */
        .dark-card {
            background-color: #121824;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
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
            margin-bottom: 15px;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BARRA DE NAVEGAÇÃO SUPERIOR
# ==========================================
st.markdown("""
    <div class="top-navbar">
        <div class="nav-brand">
            <span>🌐 ECODATA PERFORMANCE</span>
        </div>
        <div class="nav-links">
            <span class="nav-link-active">📊 Visão Geral</span>
            <span>🎯 Campanhas</span>
            <span>👥 Leads</span>
            <span>📄 Relatórios</span>
            <span>⚙️ Configurações</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. FILTRO DE DATA E STATUS DA INFRA
# ==========================================
col_filter, col_status = st.columns([3, 1])

with col_filter:
    st.markdown("<span style='color: #94a3b8; font-size: 13px;'>Filtro de Data:</span> &nbsp;&nbsp; `[ Últimos 30 Dias ▾ ]`", unsafe_allow_html=True)

with col_status:
    st.markdown("<div style='text-align: right;'><span class='status-badge'>🟢 ONLINE - API ATIVA</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. BLOCO DE MÉTRICAS SUPERIORES (Investimento, Faturamento, ROAS, Leads)
# ==========================================
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
            <div class="metric-title">[LEADS GUALIFICADOS]</div>
            <div class="metric-value">452</div>
            <div class="metric-sub-green">Texa conv. 4.2%</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. SESSÃO 1: CRESCIMENTO DE VENDAS VS. GASTO (Bloco 1)
# ==========================================
st.markdown('<div class="dark-card">', unsafe_allow_html=True)
st.markdown('<div class="block-header">CRESCIMENTO DE VENDAS VS. GASTO</div>', unsafe_allow_html=True)

df_grafico = pd.DataFrame({
    'Dia': ['00:00h', '01:00h', '16:00h', '17:00h', '18:00h', '19:00h', '20:00h', '23:00h', '30 dias'],
    'Vendas': [1000, 2200, 3800, 4100, 5600, 6000, 5200, 7100, 1400],
    'Gasto': [200, 800, 1000, 2500, 3200, 5800, 4500, 3200, 1300]
})

fig = px.line(df_grafico, x='Dia', y=['Vendas', 'Gasto'], markers=True)
fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    height=260,
    legend=dict(orientation="h", y=1.15, x=0)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 7. SESSÃO 2: TABELA DE PERFORMANCE POR CAMPANHA (Bloco 2)
# ==========================================
st.markdown('<div class="dark-card">', unsafe_allow_html=True)
st.markdown('<div class="block-header">TABELA: PERFORMANCE POR CAMPANHA (Deep Dive)</div>', unsafe_allow_html=True)

df_campanhas = pd.DataFrame({
    'Campanha': ['Campanha A', 'Campanha B'],
    'Gasto': ['R$ 500', 'R$ 500'],
    'Cliques': [120, 120],
    'CPA Real': ['R$ 15,20', 'R$ 15,20'],
    'Status': ['🟢 ATIVA', '🟢 ATIVA'],
    'Ações': ['[Pausar] [Otimizar]', '[Pausar] [Otimizar]']
})

st.dataframe(df_campanhas, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. SESSÃO 3: STATUS DA INFRAESTRUTURA TÉCNICA (Bloco 3)
# ==========================================
st.markdown('<div class="dark-card">', unsafe_allow_html=True)
st.markdown('<div class="block-header">STATUS DA INFRAESTRUTURA TÉCNICA</div>', unsafe_allow_html=True)

col_infra1, col_infra2 = st.columns(2)
with col_infra1:
    st.markdown("✅ Pizel Meta Server-Side: <span style='color: #22c55e;'>Sincronizado</span> (Último log: 2s atrás)", unsafe_allow_html=True)
    st.markdown("✅ API de Conversão Google: <span style='color: #22c55e;'>OK</span>", unsafe_allow_html=True)

with col_infra2:
    st.markdown("✅ Rastreamento de Leads: <span style='color: #22c55e;'>100%</span> (Sem perdas por adblockers)", unsafe_allow_html=True)
    st.markdown("✅ Webhook Vendas: <span style='color: #22c55e;'>OK</span>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
