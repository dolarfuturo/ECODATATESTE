import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

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

if 'passo_simulacao' not in st.session_state:
    st.session_state.passo_simulacao = 'feed'

if 'investimento_total' not in st.session_state:
    st.session_state.investimento_total = 15400.0

if 'campanhas_cadastradas' not in st.session_state:
    st.session_state.campanhas_cadastradas = ["Campanha Scale Q3", "Campanha Remarketing"]

if 'leads_data' not in st.session_state:
    st.session_state.leads_data = [
        {
            "Data": "16/08/2026",
            "Horário": "16:11:02",
            "Nome": "Carlos Silva",
            "E-mail": "carlos****@gmail.com",
            "Telefone": "(11) 98765-4321",
            "Campanha": "Campanha Scale Q3",
            "Valor": "R$ 297,00",
            "Status": "🟢 Convertido"
        },
        {
            "Data": "16/08/2026",
            "Horário": "15:42:18",
            "Nome": "Mariana Souza",
            "E-mail": "mari****@outlook.com",
            "Telefone": "(21) 97123-8899",
            "Campanha": "Campanha Remarketing",
            "Valor": "R$ 497,00",
            "Status": "🟢 Convertido"
        }
    ]

if 'logs_data' not in st.session_state:
    st.session_state.logs_data = [
        {
            "Horário": "16:11:02",
            "IP": "187.12.44.192",
            "Dispositivo": "Mobile / iOS",
            "UTM": "utm_source=facebook",
            "Status": "✔ Capturado"
        },
        {
            "Horário": "15:42:18",
            "IP": "177.184.9.12",
            "Dispositivo": "Desktop / Windows",
            "UTM": "utm_source=instagram",
            "Status": "✔ Capturado"
        }
    ]

# ==========================================
# FUNÇÕES AUXILIARES DE CÁLCULO
# ==========================================
def calcular_faturamento_numerico():
    total = 0.0
    for lead in st.session_state.leads_data:
        val = lead['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            total += float(val)
        except:
            continue
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
    if investimento_total > 0:
        roas_val = faturamento / investimento_total
        return f"{roas_val:.2f}x"
    return "0.00x"

def calcular_percentual_faturamento():
    inv = st.session_state.investimento_total
    fat = calcular_faturamento_numerico()
    if inv > 0:
        perc = ((fat - inv) / inv) * 100
        sinal = "▲" if perc >= 0 else "▼"
        return f"{sinal} {abs(perc):.1f}% vs Inv.", perc >= 0
    return "▲ 0.0% vs Inv.", True

def calcular_faturamento_por_campanha():
    resumo = {camp: 0.0 for camp in st.session_state.campanhas_cadastradas}
    for lead in st.session_state.leads_data:
        campanha = lead['Campanha']
        val_str = lead['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            val = float(val_str)
        except:
            val = 0.0
        
        if campanha in resumo:
            resumo[campanha] += val
        else:
            resumo[campanha] = val
    return resumo

# ==========================================
# 2. ESTILIZAÇÃO CSS CUSTOMIZADA
# ==========================================
st.markdown("""
    <style>
        .stApp { background-color: #0a0e17; color: #ffffff; }
        .top-navbar { display: flex; justify-content: space-between; align-items: center; background-color: #0f172a; padding: 12px 20px; border-bottom: 1px solid #1e293b; border-radius: 8px; margin-bottom: 20px; }
        .nav-brand { font-weight: bold; font-size: 16px; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
        [data-testid="stHorizontalBlock"] button { background-color: transparent !important; border: none !important; color: #94a3b8 !important; font-size: 13px !important; font-weight: 500 !important; text-align: left !important; padding: 4px 6px !important; box-shadow: none !important; }
        [data-testid="stHorizontalBlock"] button:hover { color: #38bdf8 !important; }
        [data-testid="stVerticalBlockBorderWrapper"] { background-color: #121824 !important; border: 1px solid #1e293b !important; border-radius: 12px !important; padding: 20px !important; margin-bottom: 20px !important; }
        .metric-box { background-color: #121824; border: 1px solid #1e293b; border-radius: 10px; padding: 16px; }
        .metric-title { font-size: 11px; color: #64748b; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
        .metric-value { font-size: 24px; font-weight: bold; color: #ffffff; margin-top: 6px; margin-bottom: 4px; }
        .metric-sub-green { font-size: 12px; color: #22c55e; font-weight: 500; }
        .metric-sub-red { font-size: 12px; color: #ef4444; font-weight: 500; }
        .metric-sub-gray { font-size: 12px; color: #94a3b8; }
        .status-badge { background-color: #052e16; border: 1px solid #15803d; color: #22c55e; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .block-header { font-size: 14px; font-weight: 700; color: #f8fafc; letter-spacing: 0.5px; margin-bottom: 12px; text-transform: uppercase; }
        .custom-table { width: 100%; border-collapse: collapse; color: #ffffff; font-size: 13px; }
        .custom-table th { text-align: left; padding: 10px 12px; color: #64748b; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid #1e293b; }
        .custom-table td { padding: 12px; border-bottom: 1px solid #1e293b; color: #f8fafc; }
        .action-btn { color: #38bdf8; cursor: pointer; font-weight: 500; margin-right: 8px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BARRA DE NAVEGAÇÃO SUPERIOR INTERATIVA
# ==========================================
st.markdown('<div class="top-navbar">', unsafe_allow_html=True)
nav_col1, nav_col2 = st.columns([2, 7]) # Ajustado para 7 colunas no menu

with nav_col1:
    st.markdown('<div class="nav-brand"><span>🌐 ECODATA PERFORMANCE</span></div>', unsafe_allow_html=True)

with nav_col2:
    b1, b2, b3, b4, b5, b6, b7 = st.columns(7)
    with b1:
        if st.button("📊 Visão"): st.session_state.pagina_atual = '📊 Visão Geral'
    with b2:
        if st.button("🎯 Camp"): st.session_state.pagina_atual = '🎯 Campanhas'
    with b3:
        if st.button("👥 Leads"): st.session_state.pagina_atual = '👥 Leads'
    with b4:
        if st.button("🔍 Logs"): st.session_state.pagina_atual = '🔍 Rastreamento e Logs'
    with b5:
        if st.button("📱 Sim. Ads"): st.session_state.pagina_atual = '📱 Simular Anúncio'
    with b6:
        if st.button("📄 Relat"): st.session_state.pagina_atual = '📄 Relatórios'
    with b7:
        if st.button("⚙️ Config"): st.session_state.pagina_atual = '⚙️ Configurações'

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. CONTEÚDO DINÂMICO
# ==========================================

if st.session_state.pagina_atual == '📊 Visão Geral':
    # ... (Seu código existente da Visão Geral permanece igual)
    col_filter, col_status = st.columns([3, 1])
    with col_filter: st.markdown("<span style='color: #94a3b8; font-size: 13px;'>Filtro de Data:</span> &nbsp;&nbsp; `[ Últimos 30 Dias ▾ ]`", unsafe_allow_html=True)
    with col_status: st.markdown("<div style='text-align: right;'><span class='status-badge'>🟢 ONLINE - API ATIVA</span></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    txt_perc_fat, eh_positivo_fat = calcular_percentual_faturamento()
    classe_sub_fat = "metric-sub-green" if eh_positivo_fat else "metric-sub-red"

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-box"><div class="metric-title">[INVESTIMENTO]</div><div class="metric-value">{calcular_investimento()}</div><div class="metric-sub-green">Atualizado</div></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box"><div class="metric-title">[FATURAMENTO]</div><div class="metric-value">{calcular_faturamento()}</div><div class="{classe_sub_fat}">{txt_perc_fat}</div></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box"><div class="metric-title">[ROAS]</div><div class="metric-value">{calcular_roas()}</div><div class="metric-sub-gray">(Meta: 2.5x)</div></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-box"><div class="metric-title">[LEADS QUALIFICADOS]</div><div class="metric-value">{len(st.session_state.leads_data)}</div><div class="metric-sub-green">Taxa conv. 4.2%</div></div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="block-header">FATURAMENTO POR CAMPANHA</div>', unsafe_allow_html=True)
        resumo_campanha = calcular_faturamento_por_campanha()
        tabela_camp = '<table class="custom-table"><thead><tr><th>Campanha</th><th>Receita Gerada</th></tr></thead><tbody>'
        for camp, valor in resumo_campanha.items():
            valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tabela_camp += f'<tr><td>{camp}</td><td style="color: #22c55e; font-weight: bold;">{valor_formatado}</td></tr>'
        tabela_camp += '</tbody></table>'
        st.markdown(tabela_camp, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="block-header">EVOLUÇÃO EM DUAS LINHAS: FATURAMENTO VS. INVESTIMENTO</div>', unsafe_allow_html=True)
        if len(st.session_state.leads_data) > 0:
            df_leads_sorted = sorted(st.session_state.leads_data, key=lambda x: (x.get('Data', ''), x['Horário']))
            horarios = [f"{item.get('Data', '')} {item['Horário']}" for item in df_leads_sorted]
            valores_vendas, acumulado_vendas = [], 0.0
            total_investimento_base, n_pontos = st.session_state.investimento_total, len(df_leads_sorted)
            valores_gasto = []
            for i, item in enumerate(df_leads_sorted):
                val = float(item['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip())
                acumulado_vendas += val
                valores_vendas.append(acumulado_vendas)
                valores_gasto.append(total_investimento_base * ((i + 1) / n_pontos))
            df_grafico = pd.DataFrame({'Data/Horário': horarios, 'Faturamento': valores_vendas, 'Investimento': valores_gasto})
            fig = px.line(df_grafico, x='Data/Horário', y=['Faturamento', 'Investimento'], markers=True)
        else:
            fig = px.line()
        fig.update_layout(template="plotly_dark", plot_bgcolor="#121824", paper_bgcolor="#121824", margin=dict(l=10, r=10, t=10, b=10), height=260, legend=dict(orientation="h", y=1.15, x=0))
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.pagina_atual == '📱 Simular Anúncio':
    with st.container(border=True):
        if st.session_state.passo_simulacao == 'feed':
            st.markdown('<div class="block-header">📱 FEED DE ANÚNCIOS (SIMULAÇÃO)</div>', unsafe_allow_html=True)
            st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; max-width: 400px; margin: auto; border: 1px solid #334155;">
                    <div style="color: #64748b; font-size: 12px; margin-bottom: 10px;">PATROCINADO • EcoData Performance</div>
                    <div style="background-color: #334155; height: 200px; display: flex; align-items: center; justify-content: center; color: #94a3b8; border-radius: 5px;">Imagem do Anúncio</div>
                    <h3 style="margin-top: 15px; color: white;">Transforme seus dados em lucro!</h3>
                    <p style="font-size: 14px; color: #cbd5e1;">Descubra como otimizar seu ROI com nossa ferramenta avançada de rastreamento.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("👉 SAIBA MAIS (Clicar no Anúncio)"):
                st.session_state.passo_simulacao = 'landing_page'
                st.rerun()

        elif st.session_state.passo_simulacao == 'landing_page':
            st.markdown('<div class="block-header">🌐 LANDING PAGE (DESTINO)</div>', unsafe_allow_html=True)
            st.info("Você clicou no anúncio! Aqui estaria sua página de vendas real.")
            st.subheader("🛒 Oferta Especial: Ecodata Pro")
            st.write("Valor da conversão: R$ 297,00")
            if st.button("✅ COMPRAR AGORA"):
                # Simula captura
                novo_lead = {
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Horário": datetime.now().strftime("%H:%M:%S"),
                    "Nome": "Cliente Simulado",
                    "E-mail": "cliente.teste@mail.com",
                    "Telefone": "(00) 99999-9999",
                    "Campanha": st.session_state.campanhas_cadastradas[0],
                    "Valor": "R$ 297,00",
                    "Status": "🟢 Convertido"
                }
                st.session_state.leads_data.insert(0, novo_lead)
                st.success("Compra realizada com sucesso! O painel foi atualizado.")
                if st.button("⬅️ Voltar ao feed"):
                    st.session_state.passo_simulacao = 'feed'
                    st.rerun()

elif st.session_state.pagina_atual == '🎯 Campanhas':
    # ... (Seu código existente de Campanhas)
    with st.container(border=True):
        st.markdown('<div class="block-header">GERENCIADOR DE ECOSSISTEMA & CAMPANHAS</div>', unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.subheader("➕ Cadastrar Nova Campanha")
            with st.form("form_nova_campanha"):
                nova_camp = st.text_input("Nome da Campanha")
                if st.form_submit_button("Registrar"):
                    if nova_camp and nova_camp not in st.session_state.campanhas_cadastradas:
                        st.session_state.campanhas_cadastradas.append(nova_camp)
                        st.rerun()
        with col_c2:
            st.subheader("🔗 Gerador de Link UTM")
            if len(st.session_state.campanhas_cadastradas) > 0:
                camp_selecionada = st.selectbox("Escolha a campanha:", st.session_state.campanhas_cadastradas)
                st.code(f"https://seu-dominio.com.br/?utm_source=ads&utm_campaign={camp_selecionada.lower().replace(' ', '_')}", language="text")

elif st.session_state.pagina_atual == '👥 Leads':
    # ... (Seu código existente de Leads)
    with st.container(border=True):
        st.markdown('<div class="block-header">📋 Histórico de Leads</div>', unsafe_allow_html=True)
        tabela_html = '<table class="custom-table"><thead><tr><th>Data</th><th>Horário</th><th>Nome</th><th>Valor</th><th>Status</th></tr></thead><tbody>'
        for lead in st.session_state.leads_data:
            tabela_html += f'<tr><td>{lead["Data"]}</td><td>{lead["Horário"]}</td><td>{lead["Nome"]}</td><td style="color: #22c55e;">{lead["Valor"]}</td><td>{lead["Status"]}</td></tr>'
        tabela_html += '</tbody></table>'
        st.markdown(tabela_html, unsafe_allow_html=True)

elif st.session_state.pagina_atual == '🔍 Rastreamento e Logs':
    # ... (Seu código existente de Logs)
    with st.container(border=True):
        st.markdown('<div class="block-header">LOGS DE AUDITORIA (SERVER-SIDE)</div>', unsafe_allow_html=True)
        tabela_logs = '<table class="custom-table"><thead><tr><th>Horário</th><th>UTM</th><th>Status</th></tr></thead><tbody>'
        for log in st.session_state.logs_data:
            tabela_logs += f'<tr><td>{log["Horário"]}</td><td>{log["UTM"]}</td><td>{log["Status"]}</td></tr>'
        tabela_logs += '</tbody></table>'
        st.markdown(tabela_logs, unsafe_allow_html=True)

elif st.session_state.pagina_atual == '📄 Relatórios':
    # ... (Seu código existente de Relatórios)
    with st.container(border=True):
        st.markdown('<div class="block-header">RELATÓRIOS E EXPORTAÇÃO</div>', unsafe_allow_html=True)
        st.markdown(f"- Investimento: {calcular_investimento()} | Faturamento: {calcular_faturamento()} | ROAS: {calcular_roas()}")

elif st.session_state.pagina_atual == '⚙️ Configurações':
    # ... (Seu código existente de Configurações)
    with st.container(border=True):
        st.markdown('<div class="block-header">CONFIGURAÇÕES</div>', unsafe_allow_html=True)
        with st.form("form_config_investimento"):
            novo_inv = st.number_input("Valor total investido (R$)", value=float(st.session_state.investimento_total), step=100.0)
            if st.form_submit_button("💾 Atualizar Investimento"):
                st.session_state.investimento_total = novo_inv
                st.rerun()
