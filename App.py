import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# ==========================================
# 1. FUNÇÕES AUXILIARES (LÓGICA)
# ==========================================
def formatar_moeda(valor):
    # Formata float para R$ X.XXX,XX
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_faturamento(lista_leads):
    total = 0.0
    for lead in lista_leads:
        # Remove "R$", "." e troca "," por "." para somar
        valor_limpo = lead['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            total += float(valor_limpo)
        except:
            pass
    return total

# ==========================================
# 2. CONFIGURAÇÃO GLOBAL
# ==========================================
st.set_page_config(
    page_title="EcoData Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = '📊 Visão Geral'

if 'leads_data' not in st.session_state:
    st.session_state.leads_data = [
        {"Horário": "16:11:02", "Nome": "Carlos Silva", "E-mail": "carlos****@gmail.com", "Telefone": "(11) 98765-4321", "Campanha": "Campanha Scale Q3", "Valor": "R$ 297,00", "Status": "🟢 Convertido"},
        {"Horário": "15:42:18", "Nome": "Mariana Souza", "E-mail": "mari****@outlook.com", "Telefone": "(21) 97123-8899", "Campanha": "Campanha Remarketing", "Valor": "R$ 497,00", "Status": "🟢 Convertido"}
    ]

# ==========================================
# 3. CSS CUSTOMIZADO
# ==========================================
st.markdown("""
    <style>
        .stApp { background-color: #0a0e17; color: #ffffff; }
        .top-navbar { display: flex; justify-content: space-between; align-items: center; background-color: #0f172a; padding: 12px 20px; border-bottom: 1px solid #1e293b; border-radius: 8px; margin-bottom: 20px; }
        .nav-brand { font-weight: bold; font-size: 16px; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
        [data-testid="stHorizontalBlock"] button { background-color: transparent !important; border: none !important; color: #94a3b8 !important; }
        [data-testid="stVerticalBlockBorderWrapper"] { background-color: #121824 !important; border: 1px solid #1e293b !important; border-radius: 12px !important; padding: 20px !important; }
        .metric-box { background-color: #121824; border: 1px solid #1e293b; border-radius: 10px; padding: 16px; }
        .metric-title { font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase; }
        .metric-value { font-size: 24px; font-weight: bold; color: #ffffff; margin-top: 6px; }
        .status-badge { background-color: #052e16; border: 1px solid #15803d; color: #22c55e; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .block-header { font-size: 14px; font-weight: 700; color: #f8fafc; margin-bottom: 12px; text-transform: uppercase; }
        .custom-table { width: 100%; border-collapse: collapse; color: #ffffff; font-size: 13px; }
        .custom-table th { text-align: left; padding: 10px 12px; color: #64748b; border-bottom: 1px solid #1e293b; }
        .custom-table td { padding: 12px; border-bottom: 1px solid #1e293b; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. NAVEGAÇÃO
# ==========================================
st.markdown('<div class="top-navbar">', unsafe_allow_html=True)
nav_col1, nav_col2 = st.columns([2, 6])
with nav_col1: st.markdown('<div class="nav-brand"><span>🌐 ECODATA PERFORMANCE</span></div>', unsafe_allow_html=True)
with nav_col2:
    b1, b2, b3, b4, b5, b6 = st.columns(6)
    if b1.button("📊 Visão"): st.session_state.pagina_atual = '📊 Visão Geral'
    if b2.button("🎯 Camp"): st.session_state.pagina_atual = '🎯 Campanhas'
    if b3.button("👥 Leads"): st.session_state.pagina_atual = '👥 Leads'
    if b4.button("🔍 Logs"): st.session_state.pagina_atual = '🔍 Rastreamento e Logs'
    if b5.button("📄 Relat"): st.session_state.pagina_atual = '📄 Relatórios'
    if b6.button("⚙️ Config"): st.session_state.pagina_atual = '⚙️ Configurações'
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. CONTEÚDO
# ==========================================
if st.session_state.pagina_atual == '📊 Visão Geral':
    # Calcular Faturamento Dinâmico
    faturamento_total = calcular_faturamento(st.session_state.leads_data)
    
    col_status = st.columns([1])[0]
    st.markdown("<div style='text-align: right;'><span class='status-badge'>🟢 ONLINE - API ATIVA</span></div>", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='metric-box'><div class='metric-title'>[INVESTIMENTO]</div><div class='metric-value'>R$ 15.400,00</div></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-box'><div class='metric-title'>[FATURAMENTO]</div><div class='metric-value'>{formatar_moeda(faturamento_total)}</div></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-box'><div class='metric-title'>[ROAS]</div><div class='metric-value'>{(faturamento_total/15400):.2f}x</div></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='metric-box'><div class='metric-title'>[LEADS]</div><div class='metric-value'>{len(st.session_state.leads_data)}</div></div>", unsafe_allow_html=True)

elif st.session_state.pagina_atual == '👥 Leads':
    with st.container(border=True):
        st.markdown('<div class="block-header">👥 GESTÃO E CAPTURA</div>', unsafe_allow_html=True)
        with st.expander("➕ Simular Nova Venda", expanded=False):
            with st.form("form_simulador"):
                n = st.text_input("Nome", "Cliente Novo")
                v = st.text_input("Valor", "197,00")
                if st.form_submit_button("🚀 Registrar Venda"):
                    st.session_state.leads_data.insert(0, {"Horário": datetime.now().strftime("%H:%M:%S"), "Nome": n, "E-mail": "cliente@teste.com", "Telefone": "00000", "Campanha": "Campanha Teste", "Valor": f"R$ {v}", "Status": "🟢 Convertido"})
                    st.rerun() # Atualiza a tela para refletir o valor somado

        tabela_html = '<table class="custom-table"><thead><tr><th>Horário</th><th>Nome</th><th>Valor</th><th>Status</th></tr></thead><tbody>'
        for lead in st.session_state.leads_data:
            tabela_html += f"<tr><td>{lead['Horário']}</td><td>{lead['Nome']}</td><td style='color: #22c55e;'>{lead['Valor']}</td><td>{lead['Status']}</td></tr>"
        st.markdown(tabela_html + "</tbody></table>", unsafe_allow_html=True)
