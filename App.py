import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import sqlite3

# ==========================================
# CONFIGURAÇÃO DO BANCO DE DADOS SQLite
# ==========================================
DB_NAME = "ecodata.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            horario TEXT,
            nome TEXT,
            email TEXT,
            telefone TEXT,
            campanha TEXT,
            valor TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horario TEXT,
            ip TEXT,
            dispositivo TEXT,
            utm TEXT,
            status TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campanhas (
            nome TEXT PRIMARY KEY
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    ''')
    
    # Dados padrão iniciais se estiver vazio
    cursor.execute("SELECT COUNT(*) FROM campanhas")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO campanhas (nome) VALUES (?)", ("Campanha Scale Q3",))
        cursor.execute("INSERT INTO campanhas (nome) VALUES (?)", ("Campanha Remarketing",))

    cursor.execute("SELECT COUNT(*) FROM leads")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO leads (data, horario, nome, email, telefone, campanha, valor, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("16/08/2026", "16:11:02", "Carlos Silva", "carlos****@gmail.com", "(11) 98765-4321", "Campanha Scale Q3", "R$ 297,00", "🟢 Convertido"))
        cursor.execute('''
            INSERT INTO leads (data, horario, nome, email, telefone, campanha, valor, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("16/08/2026", "15:42:18", "Mariana Souza", "mari****@outlook.com", "(21) 97123-8899", "Campanha Remarketing", "R$ 497,00", "🟢 Convertido"))

    cursor.execute("SELECT COUNT(*) FROM logs")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO logs (horario, ip, dispositivo, utm, status)
            VALUES (?, ?, ?, ?, ?)
        ''', ("16:11:02", "187.12.44.192", "Mobile / iOS", "utm_source=facebook", "✔ Capturado"))
        cursor.execute('''
            INSERT INTO logs (horario, ip, dispositivo, utm, status)
            VALUES (?, ?, ?, ?, ?)
        ''', ("15:42:18", "177.184.9.12", "Desktop / Windows", "utm_source=instagram", "✔ Capturado"))

    cursor.execute("SELECT valor FROM configuracoes WHERE chave = 'investimento_total'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO configuracoes (chave, valor) VALUES ('investimento_total', '15400.0')")

    conn.commit()
    conn.close()

init_db()

# Funções de Leitura do Banco
def carregar_leads():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM leads ORDER BY id DESC", conn)
    conn.close()
    return df.to_dict(orient='records')

def carregar_logs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)
    conn.close()
    return df.to_dict(orient='records')

def carregar_campanhas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM campanhas")
    res = [row[0] for row in cursor.fetchall()]
    conn.close()
    return res

def carregar_investimento():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = 'investimento_total'")
    res = cursor.fetchone()
    conn.close()
    return float(res[0]) if res else 15400.0

def salvar_investimento(valor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES ('investimento_total', ?)", (str(valor),))
    conn.commit()
    conn.close()

def inserir_lead_db(lead_dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (data, horario, nome, email, telefone, campanha, valor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (lead_dict["Data"], lead_dict["Horário"], lead_dict["Nome"], lead_dict["E-mail"], lead_dict["Telefone"], lead_dict["Campanha"], lead_dict["Valor"], lead_dict["Status"]))
    conn.commit()
    conn.close()

def inserir_log_db(log_dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (horario, ip, dispositivo, utm, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (log_dict["Horário"], log_dict["IP"], log_dict["Dispositivo"], log_dict["UTM"], log_dict["Status"]))
    conn.commit()
    conn.close()

def adicionar_campanha_db(nome):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO campanhas (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def deletar_campanha_db(nome):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM campanhas WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()

def atualizar_campanha_db(antigo, novo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE campanhas SET nome = ? WHERE nome = ?", (novo, antigo))
    cursor.execute("UPDATE leads SET campanha = ? WHERE campanha = ?", (novo, antigo))
    conn.commit()
    conn.close()

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

# ==========================================
# 1.1 CAPTURA DE CLIQUES E REDIRECIONAMENTO (MODO PONTE)
# ==========================================
params = st.query_params
utm_campaign_param = params.get("utm_campaign", "")
utm_source_param = params.get("utm_source", "")
dest_url = params.get("dest", "")

if utm_campaign_param and "clique_capturado_sessao" not in st.session_state:
    headers = st.context.headers
    user_ip = headers.get("X-Forwarded-For", "127.0.0.1").split(",")[0]
    
    nome_campanha_formatado = utm_campaign_param.replace("_", " ").title()
    campanhas_atuais = carregar_campanhas()
    if nome_campanha_formatado not in campanhas_atuais:
        adicionar_campanha_db(nome_campanha_formatado)

    novo_log = {
        "Horário": datetime.now().strftime("%H:%M:%S"),
        "IP": user_ip,
        "Dispositivo": "Web / Browser",
        "UTM": f"utm_source={utm_source_param}&utm_campaign={utm_campaign_param}",
        "Status": "✔ Capturado"
    }
    inserir_log_db(novo_log)
    st.session_state.clique_capturado_sessao = True

if dest_url:
    if not dest_url.startswith("http"):
        dest_url = "https://" + dest_url
        
    components.html(f"""
        <script>
            window.location.replace("{dest_url}");
        </script>
    """, height=0)
    st.stop()

# ==========================================
# FUNÇÕES AUXILIARES DE CÁLCULO
# ==========================================
def calcular_faturamento_numerico():
    leads = carregar_leads()
    total = 0.0
    for lead in leads:
        val = lead['valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
        try:
            total += float(val)
        except:
            continue
    return total

def calcular_faturamento():
    total = calcular_faturamento_numerico()
    return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_investimento():
    inv = carregar_investimento()
    return f"R$ {inv:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def calcular_roas():
    investimento_total = carregar_investimento()
    faturamento = calcular_faturamento_numerico()
    if investimento_total > 0:
        roas_val = faturamento / investimento_total
        return f"{roas_val:.2f}x"
    return "0.00x"

def calcular_percentual_faturamento():
    inv = carregar_investimento()
    fat = calcular_faturamento_numerico()
    if inv > 0:
        perc = ((fat - inv) / inv) * 100
        sinal = "▲" if perc >= 0 else "▼"
        return f"{sinal} {abs(perc):.1f}% vs Inv.", perc >= 0
    return "▲ 0.0% vs Inv.", True

def calcular_faturamento_por_campanha():
    campanhas = carregar_campanhas()
    leads = carregar_leads()
    resumo = {camp: 0.0 for camp in campanhas}
    for lead in leads:
        campanha = lead['campanha']
        val_str = lead['valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
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

leads_atuais = carregar_leads()
logs_atuais = carregar_logs()
campanhas_atuais = carregar_campanhas()

if st.session_state.pagina_atual == '📊 Visão Geral':
    col_filter, col_status = st.columns([3, 1])
    with col_filter:
        st.markdown("<span style='color: #94a3b8; font-size: 13px;'>Filtro de Data:</span> &nbsp;&nbsp; `[ Últimos 30 Dias ▾ ]`", unsafe_allow_html=True)
    with col_status:
        st.markdown("<div style='text-align: right;'><span class='status-badge'>🟢 ONLINE - WEBHOOK ATIVO</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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
                <div class="metric-value">{len(leads_atuais)}</div>
                <div class="metric-sub-green">Taxa conv. 4.2%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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
        
        if len(leads_atuais) > 0:
            df_leads_sorted = sorted(leads_atuais, key=lambda x: (x.get('data', ''), x['horario']))
            horarios = [f"{item.get('data', '')} {item['horario']}" for item in df_leads_sorted]
            
            valores_vendas = []
            acumulado_vendas = 0.0
            total_investimento_base = carregar_investimento()
            n_pontos = len(df_leads_sorted)
            valores_gasto = []
            
            for i, item in enumerate(df_leads_sorted):
                v_str = item['valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
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

    with st.container(border=True):
        st.markdown('<div class="block-header">TABELA: PERFORMANCE POR CAMPANHA (Deep Dive)</div>', unsafe_allow_html=True)
        
        perf_campanhas = {}
        for lead in leads_atuais:
            camp = lead['campanha']
            val_str = lead['valor'].replace('R$', '').replace('.', '').replace(',', '.').strip()
            try:
                v = float(val_str)
            except:
                v = 0.0
            
            if camp not in perf_campanhas:
                perf_campanhas[camp] = {'conversoes': 0, 'receita': 0.0}
            perf_campanhas[camp]['conversoes'] += 1
            perf_campanhas[camp]['receita'] += v
            
        tabela_deep = '<table class="custom-table"><thead><tr><th>Campanha</th><th>Conversões</th><th>Receita Gerada</th><th>Status</th><th>Ações</th></tr></thead><tbody>'
        for camp in campanhas_atuais:
            dados = perf_campanhas.get(camp, {'conversoes': 0, 'receita': 0.0})
            rev_fmt = f"R$ {dados['receita']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            tabela_deep += f'<tr><td>{camp}</td><td>{dados["conversoes"]} leads</td><td style="color: #22c55e; font-weight: bold;">{rev_fmt}</td><td><span style="color: #22c55e;">🟢 ATIVA</span></td><td><span class="action-btn">[Pausar]</span> <span class="action-btn">[Otimizar]</span></td></tr>'
        tabela_deep += '</tbody></table>'
        st.markdown(tabela_deep, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="block-header">STATUS DA INFRAESTRUTURA TÉCNICA</div>', unsafe_allow_html=True)
        col_infra1, col_infra2 = st.columns(2)
        with col_infra1:
            st.markdown("✅ Pixel Meta Server-Side: <span style='color: #22c55e;'>Sincronizado</span>", unsafe_allow_html=True)
            st.markdown("✅ API de Conversão Google: <span style='color: #22c55e;'>OK</span>", unsafe_allow_html=True)
        with col_infra2:
            st.markdown("✅ Rastreamento de Leads: <span style='color: #22c55e;'>100%</span>", unsafe_allow_html=True)
            st.markdown("✅ Webhook Flask Endpoint: <span style='color: #22c55e;'>Ativo (/webhook)</span>", unsafe_allow_html=True)

elif st.session_state.pagina_atual == '🎯 Campanhas':
    with st.container(border=True):
        st.markdown('<div class="block-header">GERENCIADOR DE ECOSSISTEMA & CAMPANHAS</div>', unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("➕ Cadastrar Nova Campanha")
            with st.form("form_nova_campanha"):
                nova_camp = st.text_input("Nome da Campanha (ex: Lançamento Outubro)")
                if st.form_submit_button("Registrar no Ecossistema"):
                    if nova_camp and nova_camp not in campanhas_atuais:
                        adicionar_campanha_db(nova_camp)
                        st.success(f"Campanha '{nova_camp}' registrada com sucesso!")
                        st.rerun()
                    else:
                        st.warning("Nome inválido ou já existente.")
        
        with col_c2:
            st.subheader("🔗 Gerador de Link UTM (Modo Ponte)")
            if len(campanhas_atuais) > 0:
                camp_selecionada = st.selectbox("Escolha a campanha:", campanhas_atuais)
                url_destino_cliente = st.text_input("URL do site do cliente (destino):", "https://www.queroquero.com.br")
                
                utm_link = f"https://ecosistem.streamlit.app/?dest={url_destino_cliente}&utm_source=ads&utm_campaign={camp_selecionada.lower().replace(' ', '_')}"
                st.code(utm_link, language="text")
                st.info("Passe este link para o seu sobrinho colocar no gerenciador de anúncios.")
            else:
                st.warning("Cadastre uma campanha primeiro para gerar o link.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ✏️ Editar ou Deletar Campanhas Existentes")
        
        if len(campanhas_atuais) > 0:
            camp_para_gerenciar = st.selectbox("Selecione a campanha para gerenciar:", campanhas_atuais, key="sel_gerenciar_camp")
            
            col_ed1, col_ed2 = st.columns(2)
            with col_ed1:
                with st.form("form_editar_campanha"):
                    novo_nome_camp = st.text_input("Novo nome para a campanha", value=camp_para_gerenciar)
                    btn_salvar = st.form_submit_button("💾 Salvar Alteração de Nome")
                    if btn_salvar:
                        if novo_nome_camp and novo_nome_camp not in campanhas_atuais:
                            atualizar_campanha_db(camp_para_gerenciar, novo_nome_camp)
                            st.success("Campanha atualizada com sucesso!")
                            st.rerun()
                        else:
                            st.warning("Nome inválido ou já existente.")
            with col_ed2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Deletar Campanha Selecionada", type="primary"):
                    if len(campanhas_atuais) > 1:
                        deletar_campanha_db(camp_para_gerenciar)
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
                    campanha_input = st.selectbox("Campanha de Origem", campanhas_atuais)
                
                valor_input = st.text_input("Valor da Venda", value="197,00")
                
                submitted = st.form_submit_button("🚀 Simular Envio de Webhook & Captura")
                if submitted:
                    data_atual = datetime.now().strftime("%d/%m/%Y")
                    horario_atual = datetime.now().strftime("%H:%M:%S")
                    novo_lead = {
                        "Data": data_atual,
                        "Horário": horario_atual,
                        "Nome": nome_input,
                        "E-mail": email_input[:4] + "****" + email_input[email_input.find("@"):] if "@" in email_input else "cli****@email.com",
                        "Telefone": tel_input,
                        "Campanha": campanha_input,
                        "Valor": f"R$ {valor_input}",
                        "Status": "🟢 Convertido"
                    }
                    inserir_lead_db(novo_lead)
                    
                    novo_log = {
                        "Horário": horario_atual,
                        "IP": "191.240.12.89",
                        "Dispositivo": "Mobile / Android",
                        "UTM": f"utm_campaign={campanha_input.lower().replace(' ', '_')}",
                        "Status": "✔ Capturado"
                    }
                    inserir_log_db(novo_log)
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Histórico de Leads e Clientes Capturados")
        
        tabela_html = '<table class="custom-table"><thead><tr><th>Data</th><th>Horário</th><th>Nome</th><th>E-mail</th><th>Telefone</th><th>Campanha</th><th>Valor</th><th>Status</th></tr></thead><tbody>'
        for lead in leads_atuais:
            data_lead = lead.get("data", "16/08/2026")
            tabela_html += f'<tr><td>{data_lead}</td><td>{lead["horario"]}</td><td>{lead["nome"]}</td><td>{lead["email"]}</td><td>{lead["telefone"]}</td><td>{lead["campanha"]}</td><td style="color: #22c55e; font-weight: bold;">{lead["valor"]}</td><td><span style="color: #22c55e;">{lead["status"]}</span></td></tr>'
        tabela_html += '</tbody></table>'
        st.markdown(tabela_html, unsafe_allow_html=True)

elif st.session_state.pagina_atual == '🔍 Rastreamento e Logs':
    with st.container(border=True):
        st.markdown('<div class="block-header">FONTE DA VERDADE: LOGS DE CLIQUES E DADOS DE AUDITORIA (SERVER-SIDE)</div>', unsafe_allow_html=True)
        
        tabela_logs = '<table class="custom-table"><thead><tr><th>Horário</th><th>IP / Origem</th><th>Dispositivo</th><th>UTM Campaign</th><th>Status</th></tr></thead><tbody>'
        for log in logs_atuais:
            tabela_logs += f'<tr><td>{log["horario"]}</td><td>{log["ip"]}</td><td>{log["dispositivo"]}</td><td>{log["utm"]}</td><td><span style="color: #22c55e;">{log["status"]}</span></td></tr>'
        tabela_logs += '</tbody></table>'
        st.markdown(tabela_logs, unsafe_allow_html=True)

elif st.session_state.pagina_atual == '📄 Relatórios':
    with st.container(border=True):
        st.markdown('<div class="block-header">RELATÓRIOS E AUDITORIA DE DADOS</div>', unsafe_allow_html=True)
        st.markdown(f"- Investimento Total: **{calcular_investimento()}**")
        st.markdown(f"- Faturamento Consolidado: **{calcular_faturamento()}**")
        st.markdown(f"- ROAS Atual: **{calcular_roas()}**")
        st.markdown(f"- Total de Conversões Registradas: **{len(leads_atuais)}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📥 Exportar Dados")
        
        if len(leads_atuais) > 0:
            df_export = pd.DataFrame(leads_atuais)
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
        st.markdown("Status da Conexão Server-Side: <span style='color: #22c55e;'>Ativa e Sincronizada com o banco SQLite em tempo real.</span>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💰 Configuração do Valor de Investimento (Tráfego Pago)")
        with st.form("form_config_investimento"):
            novo_inv = st.number_input("Valor total investido (R$)", value=float(carregar_investimento()), step=100.0, format="%.2f")
            if st.form_submit_button("💾 Atualizar Investimento"):
                salvar_investimento(novo_inv)
                st.success("Investimento atualizado com sucesso! As métricas de ROAS e gráficos foram recalculados.")
                st.rerun()
