import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURAÇÃO GLOBAL E ESTADO INICIAL
# ==========================================
st.set_page_config(
    page_title="EcoData Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = '📊 Visão Geral'

if 'investimento_total' not in st.session_state:
    st.session_state.investimento_total = 15400.0

if 'campanhas_cadastradas' not in st.session_state:
    st.session_state.campanhas_cadastradas = ["Campanha Scale Q3", "Campanha Remarketing"]

if 'leads_data' not in st.session_state:
    st.session_state.leads_data = [
        {"Data": "16/08/2026", "Horário": "16:11:02", "Nome": "Carlos Silva", "E-mail": "carlos****@gmail.com", "Telefone": "(11) 98765-4321", "Campanha": "Campanha Scale Q3", "Valor": "R$ 297,00", "Status": "🟢 Convertido"},
        {"Data": "16/08/2026", "Horário": "15:42:18", "Nome": "Mariana Souza", "E-mail": "mari****@outlook.com", "Telefone": "(21) 97123-8899", "Campanha": "Campanha Remarketing", "Valor": "R$ 497,00", "Status": "🟢 Convertido"}
    ]

if 'logs_data' not in st.session_state:
    st.session_state.logs_data = [
        {"Horário": "16:11:02", "IP": "187.12.44.192", "Dispositivo": "Mobile / iOS", "UTM": "utm_source=facebook", "Status": "✔ Capturado"},
        {"Horário": "15:42:18", "IP": "177.184.9.12", "Dispositivo": "Desktop / Windows", "UTM": "utm_source=instagram", "Status": "✔ Capturado"}
    ]

# ==========================================
# 1.1. INTEGRAÇÃO TOTAL: WEBHHOOK E PONTE
# ==========================================
params = st.query_params

# 1. ESCUTADOR DE VENDAS (WEBHOOK RECEPTOR)
if params.get("evento") == "venda":
    valor_v = params.get("valor", "0,00")
    camp_v = params.get("campanha", "Geral").replace("_", " ")
    
    novo_lead_web = {
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Horário": datetime.now().strftime("%H:%M:%S"),
        "Nome": "Via Webhook (Venda)",
        "E-mail": "sistema@api.com",
        "Telefone": "N/A",
        "Campanha": camp_v,
        "Valor": f"R$ {valor_v}",
        "Status": "🟢 Convertido"
    }
    st.session_state.leads_data.insert(0, novo_lead_web)

# 2. CAPTURA DE CLIQUES (UTM)
utm_campaign_param = params.get("utm_campaign", "")
utm_source_param = params.get("utm_source", "")
dest_url = params.get("dest", "")

if utm_campaign_param and "clique_capturado_sessao" not in st.session_state:
    nome_campanha_formatado = utm_campaign_param.replace("_", " ").title()
    if nome_campanha_formatado not in st.session_state.campanhas_cadastradas:
        st.session_state.campanhas_cadastradas.append(nome_campanha_formatado)
    
    st.session_state.logs_data.insert(0, {
        "Horário": datetime.now().strftime("%H:%M:%S"),
        "IP": "API_LOG",
        "Dispositivo": "Server-Side",
        "UTM": f"utm_source={utm_source_param}&utm_campaign={utm_campaign_param}",
        "Status": "✔ Capturado"
    })
    st.session_state.clique_capturado_sessao = True

# 3. REDIRECIONAMENTO (MODO PONTE)
if dest_url:
    if not dest_url.startswith("http"): dest_url = "https://" + dest_url
    components.html(f'<script>window.location.replace("{dest_url}");</script>', height=0)
    st.stop()

# ==========================================
# FUNÇÕES AUXILIARES DE CÁLCULO
# ==========================================
def calcular_faturamento_numerico():
    total = 0.0
    for lead in st.session_state.leads_data:
        val = lead['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
        try: total += float(val)
        except: continue
    return total

def calcular_faturamento():
    total = calcular_faturamento_numerico()
    return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_investimento():
    inv = st.session_state.investimento_total
    return f"R$ {inv:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_roas():
    investimento_total = st.session_state.investimento_total
    faturamento = calcular_faturamento_numerico()
    return f"{faturamento / investimento_total:.2f}x" if investimento_total > 0 else "0.00x"

def calcular_percentual_faturamento():
    inv = st.session_state.investimento_total
    fat = calcular_faturamento_numerico()
    if inv > 0:
        perc = ((fat - inv) / inv) * 100
        return f"{'▲' if perc >= 0 else '▼'} {abs(perc):.1f}% vs Inv.", perc >= 0
    return "▲ 0.0% vs Inv.", True

def calcular_faturamento_por_campanha():
    resumo = {camp: 0.0 for camp in st.session_state.campanhas_cadastradas}
    for lead in st.session_state.leads_data:
        campanha = lead['Campanha']
        try: val = float(lead['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip())
        except: val = 0.0
        if campanha in resumo: resumo[campanha] += val
        else: resumo[campanha] = val
    return resumo

# ==========================================
# CSS E UI (MANTIDOS IGUAIS)
# ==========================================
st.markdown("""<style>
    .stApp { background-color: #0a0e17; color: #ffffff; }
    .top-navbar { display: flex; justify-content: space-between; align-items: center; background-color: #0f172a; padding: 12px 20px; border-bottom: 1px solid #1e293b; border-radius: 8px; margin-bottom: 20px; }
    .nav-brand { font-weight: bold; color: #38bdf8; }
    .metric-box { background-color: #121824; border: 1px solid #1e293b; border-radius: 10px; padding: 16px; }
    .metric-title { font-size: 11px; color: #64748b; font-weight: 700; text-transform: uppercase; }
    .metric-value { font-size: 24px; font-weight: bold; color: #ffffff; }
    .custom-table { width: 100%; border-collapse: collapse; color: #ffffff; font-size: 13px; }
    .custom-table th { text-align: left; padding: 10px; color: #64748b; border-bottom: 1px solid #1e293b; }
    .custom-table td { padding: 12px; border-bottom: 1px solid #1e293b; }
    .action-btn { color: #38bdf8; cursor: pointer; }
    .block-header { font-size: 14px; font-weight: 700; color: #f8fafc; letter-spacing: 0.5px; margin-bottom: 12px; text-transform: uppercase; }
</style>""", unsafe_allow_html=True)

# ==========================================
# 3. BARRA DE NAVEGAÇÃO
# ==========================================
st.markdown('<div class="top-navbar">', unsafe_allow_html=True)
nav_col1, nav_col2 = st.columns([2, 6])
with nav_col1: st.markdown('<div class="nav-brand">🌐 ECODATA PERFORMANCE</div>', unsafe_allow_html=True)
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
# 4. CONTEÚDO DINÂMICO
# ==========================================

if st.session_state.pagina_atual == '📊 Visão Geral':
    # (Dashboard omitido por brevidade de leitura, mas a lógica de processamento já está rodando no topo)
    txt_perc, ok = calcular_percentual_faturamento()
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="metric-box"><div class="metric-title">[INVESTIMENTO]</div><div class="metric-value">{calcular_investimento()}</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-box"><div class="metric-title">[FATURAMENTO]</div><div class="metric-value">{calcular_faturamento()}</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-box"><div class="metric-title">[ROAS]</div><div class="metric-value">{calcular_roas()}</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="metric-box"><div class="metric-title">[LEADS]</div><div class="metric-value">{len(st.session_state.leads_data)}</div></div>', unsafe_allow_html=True)
    
    # Exibir Tabela de Resumo atualizada com dados do webhook
    st.markdown('<div class="block-header">FATURAMENTO POR CAMPANHA</div>', unsafe_allow_html=True)
    resumo = calcular_faturamento_por_campanha()
    for camp, valor in resumo.items():
        st.write(f"{camp}: R$ {valor:,.2f}")

elif st.session_state.pagina_atual == '🎯 Campanhas':
    st.subheader("🔗 Link para Integração (Webhook de Vendas)")
    st.info("Para registrar uma venda via sistema, dispare um GET nesta URL:")
    st.code("https://ecosistem.streamlit.app/?evento=venda&valor=100,00&campanha=Campanha_Scale_Q3", language="text")

# (Demais páginas permanecem iguais...)
