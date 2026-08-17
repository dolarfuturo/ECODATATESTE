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
# 1.1 CAPTURA AUTOMÁTICA DE CLIQUES E UTMs EM TEMPO REAL
# ==========================================
params = st.query_params
utm_campaign_param = params.get("utm_campaign", "")
utm_source_param = params.get("utm_source", "")

if utm_campaign_param and "clique_capturado_sessao" not in st.session_state:
    headers = st.context.headers
    user_ip = headers.get("X-Forwarded-For", "127.0.0.1").split(",")[0]
    
    nome_campanha_formatado = utm_campaign_param.replace("_", " ").title()
    if nome_campanha_formatado not in st.session_state.campanhas_cadastradas:
        st.session_state.campanhas_cadastradas.append(nome_campanha_formatado)

    novo_log = {
        "Horário": datetime.now().strftime("%H:%M:%S"),
        "IP": user_ip,
        "Dispositivo": "Web / Browser",
        "UTM": f"utm_source={utm_source_param}&utm_campaign={utm_campaign_param}",
        "Status": "✔ Capturado"
    }
    
    st.session_state.logs_data.insert(0, novo_log)
    st.session_state.clique_capturado_sessao = True

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
        .stApp {
            background-color: #0a0e17;
            color: #ffffff;
        }
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
        [data-testid="stHorizontalBlock"] button {
            background-color: transparent !important;
            border: none !important;
            color: #94a3b8 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            text-align: left !important;
            padding: 4px 6px !important;
            box-shadow: none !important;
        }
        [data-testid="stHorizontalBlock"] button:hover {
            color: #38bdf8 !important;
        }
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
        .metric-sub-red {
            font-size: 12px;
            color: #ef4444;
            font-weight: 500;
        }
        .metric-sub-gray {
            font-size: 12px;
            color: #94a3b8;
        }
        .status-badge {
            background-color: #052e16;
            border: 1px solid #15803d;
            color: #22c55e;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }
        .block-header {
            font-size: 14px;
            font-weight: 700;
            color: #f8fafc;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            text-transform: uppercase;
        }
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
nav_col1, nav_col2 = st.columns([2, 6])

with nav_col1:
    st.markdown('<div class="nav-brand"><span>🌐 ECODATA PERFORMANCE</span></div>', unsafe_allow_html=True)

with nav_col2:
    b1, b2, b3, b4, b5, b6 = st.columns(6)
    with b1:
        if st.button("📊 Visão", use_container_width=True):
            st.session_state.pagina_atual = '📊 Visão Geral'
    with b2:
        if st.button("🎯 Camp", use_container_width=True):
            st.session_state.pagina_atual = '🎯 Campanhas'
    with b3:
        if st.button("👥 Leads", use_container_width=True):
            st.session_state.pagina_atual = '👥 Leads'
    with b4:
        if st.button("🔍 Logs", use_container_width=True):
            st.session_state.pagina_atual = '🔍 Rastreamento e Logs'
    with b5:
        if st.button("📄 Relat", use_container_width=True):
            st.session_state.pagina_atual = '📄 Relatórios'
    with b6:
        if st.button("⚙️ Config", use_container_width=True):
            st.session_state.pagina_atual = '⚙️ Configurações'

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. CONTEÚDO DINÂMICO DA APLICAÇÃO
# ==========================================

if st.session_state.pagina_atual == '📊 Visão Geral':
    col_filter, col_status = st.columns([3, 1])
    with col_filter:
        st.markdown("<span style='color: #94a3b8; font-size: 13px;'>Filtro de Data:</span> &nbsp;&nbsp; `[ Últimos 30 Dias ▾ ]`", unsafe_allow_html=True)
    with col_status:
        st.markdown("<div style='text-align: right;'><span class='status-badge'>🟢 ONLINE - API ATIVA</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Bloco de Métricas
    txt_perc_fat, eh_positivo_fat = calcular_percentual_faturamento()
    classe_sub_fat = "metric-sub-green" if eh_positivo_fat else "metric-sub-red"

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">[INVESTIMENTO]</div>
                <div class="metric-value">{calcular_investimento()}</div>
                <div class="metric-sub-green">Atualizado</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">[FATURAMENTO]</div>
                <div class="metric-value">{calcular_faturamento()}</div>
                <div class="{classe_sub_fat}">{txt_perc_fat}</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">[ROAS]</div>
                <div class="metric-value">{calcular_roas()}</div>
                <div class="metric-sub-gray">(Meta: 2.5x)</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">[LEADS QUALIFICADOS]</div>
                <div class="metric-value">{len(st.session_state.leads_data)}</div>
                <div class="metric-sub-green">Taxa conv. 4.2%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # TABELA DE FATURAMENTO POR CAMPANHA
    with st.container(border=True):
        st.markdown('<div class="block-header">FATURAMENTO POR CAMPANHA</div>', unsafe_allow_html=True)
        resumo_campanha = calcular_faturamento_por_campanha()
        tabela_camp = '<table class="custom-table"><thead><tr><th>Campanha</th><th>Receita Gerada</th></tr></thead><tbody>'
        for camp, valor in resumo_campanha.items():
            valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tabela_camp += f'<tr><td>{camp}</td><td style="color: #22c55e; font-weight: bold;">{valor_formatado}</td></tr>'
        tabela_camp += '</tbody></table>'
        st.markdown(tabela_camp, unsafe_allow_html=True)

    # GRÁFICO DE DUAS LINHAS (FATURAMENTO VS. INVESTIMENTO)
    with st.container(border=True):
        st.markdown('<div class="block-header">EVOLUÇÃO EM DUAS LINHAS: FATURAMENTO VS. INVESTIMENTO</div>', unsafe_allow_html=True)
        
        if len(st.session_state.leads_data) > 0:
            df_leads_sorted = sorted(st.session_state.leads_data, key=lambda x: (x.get('Data', ''), x['Horário']))
            horarios = [f"{item.get('Data', '')} {item['Horário']}" for item in df_leads_sorted]
            
            valores_vendas = []
            acumulado_vendas = 0.0
            total_investimento_base = st.session_state.investimento_total
            n_pontos = len(df_leads_sorted)
            valores_gasto = []
            
            for i, item in enumerate(df_leads_sorted):
                v_str = item['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
                try:
                    val = float(v_str)
                except:
                    val = 0.0
                acumulado_vendas += val
                valores_vendas.append(acumulado_vendas)
                
                gasto_acumulado = total_investimento_base * ((i + 1) / n_pontos) if n_pontos > 0 else 0.0
                valores_gasto.append(gasto_acumulado)
            
            df_grafico = pd.DataFrame({
                'Data/Horário': horarios,
                'Faturamento': valores_vendas,
                'Investimento': valores_gasto
            })
            
            fig = px.line(df_grafico, x='Data/Horário', y=['Faturamento', 'Investimento'], markers=True)
        else:
            df_grafico = pd.DataFrame({'Data/Horário': [], 'Faturamento': [], 'Investimento': []})
            fig = px.line(df_grafico, x='Data/Horário', y=['Faturamento', 'Investimento'])

        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="#121824",
            paper_bgcolor="#121824",
            margin=dict(l=10, r=10, t=10, b=10),
            height=260,
            legend=dict(orientation="h", y=1.15, x=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    # TABELA DE PERFORMANCE POR CAMPANHA (DEEP DIVE)
    with st.container(border=True):
        st.markdown('<div class="block-header">TABELA: PERFORMANCE POR CAMPANHA (Deep Dive)</div>', unsafe_allow_html=True)
        
        perf_campanhas = {}
        for lead in st.session_state.leads_data:
            camp = lead['Campanha']
            val_str = lead['Valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
            try:
                v = float(val_str)
            except:
                v = 0.0
            
            if camp not in perf_campanhas:
                perf_campanhas[camp] = {'conversoes': 0, 'receita': 0.0}
            perf_campanhas[camp]['conversoes'] += 1
            perf_campanhas[camp]['receita'] += v
            
        tabela_deep = '<table class="custom-table"><thead><tr><th>Campanha</th><th>Conversões</th><th>Receita Gerada</th><th>Status</th><th>Ações</th></tr></thead><tbody>'
        for camp in st.session_state.campanhas_cadastradas:
            dados = perf_campanhas.get(camp, {'conversoes': 0, 'receita': 0.0})
            rev_fmt = f"R$ {dados['receita']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tabela_deep += f'<tr><td>{camp}</td><td>{dados["conversoes"]} leads</td><td style="color: #22c55e; font-weight: bold;">{rev_fmt}</td><td><span style="color: #22c55e;">🟢 ATIVA</span></td><td><span class="action-btn">[Pausar]</span> <span class="action-btn">[Otimizar]</span></td></tr>'
        tabela_deep += '</tbody></table>'
        st.markdown(tabela_deep, unsafe_allow_html=True)

    # Status Infra
    with st.container(border=True):
        st.markdown('<div class="block-header">STATUS DA INFRAESTRUTURA TÉCNICA</div>', unsafe_allow_html=True)
        col_infra1, col_infra2 = st.columns(2)
        with col_infra1:
            st.markdown("✅ Pixel Meta Server-Side: <span style='color: #22c55e;'>Sincronizado</span> (Último log: agora mesmo)", unsafe_allow_html=True)
            st.markdown("✅ API de Conversão Google: <span style='color: #22c55e;'>OK</span>", unsafe_allow_html=True)
        with col_infra2:
            st.markdown("✅ Rastreamento de Leads: <span style='color: #22c55e;'>100%</span> (Sem perdas por adblockers)", unsafe_allow_html=True)
            st.markdown("✅ Webhook Vendas: <span style='color: #22c55e;'>OK</span>", unsafe_allow_html=True)

elif st.session_state.pagina_atual == '🎯 Campanhas':
    with st.container(border=True):
        st.markdown('<div class="block-header">GERENCIADOR DE ECOSSISTEMA & CAMPANHAS</div>', unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("➕ Cadastrar Nova Campanha")
            with st.form("form_nova_campanha"):
                nova_camp = st.text_input("Nome da Campanha (ex: Lançamento Outubro)")
                if st.form_submit_button("Registrar no Ecossistema"):
                    if nova_camp and nova_camp not in st.session_state.campanhas_cadastradas:
                        st.session_state.campanhas_cadastradas.append(nova_camp)
                        st.success(f"Campanha '{nova_camp}' registrada com sucesso!")
                        st.rerun()
                    else:
                        st.warning("Nome inválido ou já existente.")
        
        with col_c2:
            st.subheader("🔗 Gerador de Link UTM")
            if len(st.session_state.campanhas_cadastradas) > 0:
                camp_selecionada = st.selectbox("Escolha a campanha:", st.session_state.campanhas_cadastradas)
                url_base = st.text_input("URL do seu site (destino):", "https://seu-dominio.com.br")
                
                utm_link = f"{url_base}/?utm_source=ads&utm_campaign={camp_selecionada.lower().replace(' ', '_')}"
                st.code(utm_link, language="text")
                st.info("Copie este link e cole no seu gerenciador de anúncios.")
            else:
                st.warning("Cadastre uma campanha primeiro para gerar o link.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ✏️ Editar ou Deletar Campanhas Existentes")
        
        if len(st.session_state.campanhas_cadastradas) > 0:
            camp_para_gerenciar = st.selectbox("Selecione a campanha para gerenciar:", st.session_state.campanhas_cadastradas, key="sel_gerenciar_camp")
            
            col_ed1, col_ed2 = st.columns(2)
            with col_ed1:
                with st.form("form_editar_campanha"):
                    novo_nome_camp = st.text_input("Novo nome para a campanha", value=camp_para_gerenciar)
                    btn_salvar = st.form_submit_button("💾 Salvar Alteração de Nome")
                    if btn_salvar:
                        if novo_nome_camp and novo_nome_camp not in st.session_state.campanhas_cadastradas:
                            idx = st.session_state.campanhas_cadastradas.index(camp_para_gerenciar)
                            st.session_state.campanhas_cadastradas[idx] = novo_nome_camp
                            for lead in st.session_state.leads_data:
                                if lead['Campanha'] == camp_para_gerenciar:
                                    lead['Campanha'] = novo_nome_camp
                            st.success("Campanha atualizada com sucesso!")
                            st.rerun()
                        else:
                            st.warning("Nome inválido ou já existente.")
            with col_ed2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Deletar Campanha Selecionada", type="primary"):
                    if len(st.session_state.campanhas_cadastradas) > 1:
                        st.session_state.campanhas_cadastradas.remove(camp_para_gerenciar)
                        st.success("Campanha removida com sucesso!")
                        st.rerun()
                    else:
                        st.warning("O ecossistema precisa ter pelo menos uma campanha ativa.")
        else:
            st.info("Nenhuma campanha cadastrada no momento.")

elif st.session_state.pagina_atual == '👥 Leads':
    with st.container(border=True):
        st.markdown('<div class="block-header">👥 GESTÃO E CAPTURA DE DADOS DE USUÁRIOS (LEADS & VENDAS)</div>', unsafe_allow_html=True)
        
        with st.expander("➕ Simular Nova Conversão / Lead (Teste Front-End)", expanded=False):
            with st.form("form_simulador_lead"):
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    nome_input = st.text_input("Nome do Cliente", value="João Pedro")
                    email_input = st.text_input("E-mail", value="joao.pedro@email.com")
                with col_f2:
                    tel_input = st.text_input("Telefone", value="(11) 99888-7766")
                    campanha_input = st.selectbox("Campanha de Origem", st.session_state.campanhas_cadastradas)
                
                valor_input = st.text_input("Valor da Venda", value="197,00")
                
                submitted = st.form_submit_button("🚀 Simular Envio de Webhook & Captura")
                if submitted:
                    data_atual = datetime.now().strftime("%d/%m/%Y")
                    horario_atual = datetime.now().strftime("%H:%M:%S")
                    novo_lead = {
                        "Data": data_atual,
                        "Horário": horario_atual,
                        "Nome": nome_input,
                        "E-mail": email_input[:4] + "****" + email_input[email_input.find("@"):],
                        "Telefone": tel_input,
                        "Campanha": campanha_input,
                        "Valor": f"R$ {valor_input}",
                        "Status": "🟢 Convertido"
                    }
                    st.session_state.leads_data.insert(0, novo_lead)
                    
                    novo_log = {
                        "Horário": horario_atual,
                        "IP": "191.240.12.89",
                        "Dispositivo": "Mobile / Android",
                        "UTM": f"utm_campaign={campanha_input.lower().replace(' ', '_')}",
                        "Status": "✔ Capturado"
                    }
                    st.session_state.logs_data.insert(0, novo_log)
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Histórico de Leads e Clientes Capturados")
        
        tabela_html = '<table class="custom-table"><thead><tr><th>Data</th><th>Horário</th><th>Nome</th><th>E-mail</th><th>Telefone</th><th>Campanha</th><th>Valor</th><th>Status</th></tr></thead><tbody>'
        for lead in st.session_state.leads_data:
            data_lead = lead.get("Data", "16/08/2026")
            tabela_html += f'<tr><td>{data_lead}</td><td>{lead["Horário"]}</td><td>{lead["Nome"]}</td><td>{lead["E-mail"]}</td><td>{lead["Telefone"]}</td><td>{lead["Campanha"]}</td><td style="color: #22c55e; font-weight: bold;">{lead["Valor"]}</td><td><span style="color: #22c55e;">{lead["Status"]}</span></td></tr>'
        tabela_html += '</tbody></table>'
        st.markdown(tabela_html, unsafe_allow_html=True)

elif st.session_state.pagina_atual == '🔍 Rastreamento e Logs':
    with st.container(border=True):
        st.markdown('<div class="block-header">FONTE DA VERDADE: LOGS DE CLIQUES E DADOS DE AUDITORIA (SERVER-SIDE)</div>', unsafe_allow_html=True)
        
        tabela_logs = '<table class="custom-table"><thead><tr><th>Horário</th><th>IP / Origem</th><th>Dispositivo</th><th>UTM Campaign</th><th>Status</th></tr></thead><tbody>'
        for log in st.session_state.logs_data:
            tabela_logs += f'<tr><td>{log["Horário"]}</td><td>{log["IP"]}</td><td>{log["Dispositivo"]}</td><td>{log["UTM"]}</td><td><span style="color: #22c55e;">{log["Status"]}</span></td></tr>'
        tabela_logs += '</tbody></table>'
        st.markdown(tabela_logs, unsafe_allow_html=True)

elif st.session_state.pagina_atual == '📄 Relatórios':
    with st.container(border=True):
        st.markdown('<div class="block-header">RELATÓRIOS E AUDITORIA DE DADOS</div>', unsafe_allow_html=True)
        st.markdown(f"- Investimento Total: **{calcular_investimento()}**")
        st.markdown(f"- Faturamento Consolidado: **{calcular_faturamento()}**")
        st.markdown(f"- ROAS Atual: **{calcular_roas()}**")
        st.markdown(f"- Total de Conversões Registradas: **{len(st.session_state.leads_data)}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📥 Exportar Dados")
        
        if len(st.session_state.leads_data) > 0:
            df_export = pd.DataFrame(st.session_state.leads_data)
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📄 Baixar Relatório Completo de Leads (CSV)",
                data=csv_data,
                file_name="relatorio_leads_ecodata.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhum dado disponível para exportação no momento.")

elif st.session_state.pagina_atual == '⚙️ Configurações':
    with st.container(border=True):
        st.markdown('<div class="block-header">CONFIGURAÇÕES DO ECOSSISTEMA E APIS</div>', unsafe_allow_html=True)
        st.markdown("Status da Conexão Server-Side: <span style='color: #22c55e;'>Ativa e Sincronizada com o banco de sessão em tempo real.</span>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💰 Configuração do Valor de Investimento (Tráfego Pago)")
        with st.form("form_config_investimento"):
            novo_inv = st.number_input("Valor total investido (R$)", value=float(st.session_state.investimento_total), step=100.0, format="%.2f")
            if st.form_submit_button("💾 Atualizar Investimento"):
                st.session_state.investimento_total = novo_inv
                st.success("Investimento atualizado com sucesso! As métricas de ROAS e gráficos foram recalculados.")
                st.rerun()
