import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# ==========================================
# 1. INICIALIZAÇÃO E ESTADO GLOBAL
# ==========================================
st.set_page_config(page_title="EcoData Performance", layout="wide")

if 'campanhas_cadastradas' not in st.session_state:
    st.session_state.campanhas_cadastradas = ["Campanha Scale Q3", "Campanha Remarketing"]

if 'leads_data' not in st.session_state:
    st.session_state.leads_data = []

# (Restante das inicializações de session_state permanecem iguais...)

# ==========================================
# 2. ABA DE CAMPANHAS (GERAÇÃO DE LINK E CADASTRO)
# ==========================================
if st.session_state.pagina_atual == '🎯 Campanhas':
    st.markdown('<div class="block-header">GERENCIADOR DE ECOSSISTEMA</div>', unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("➕ Cadastrar Nova Campanha")
        with st.form("form_nova_campanha"):
            nova_camp = st.text_input("Nome da Campanha (ex: Lançamento Outubro)")
            if st.form_submit_button("Registrar no Ecossistema"):
                if nova_camp and nova_camp not in st.session_state.campanhas_cadastradas:
                    st.session_state.campanhas_cadastradas.append(nova_camp)
                    st.success(f"Campanha '{nova_camp}' registrada!")
                else:
                    st.warning("Nome inválido ou já existente.")
    
    with col_c2:
        st.subheader("🔗 Gerador de Link UTM")
        camp_selecionada = st.selectbox("Escolha a campanha para gerar o link:", st.session_state.campanhas_cadastradas)
        url_base = st.text_input("URL do seu site (destino):", "https://seu-dominio.com.br")
        
        # Lógica de criação do link
        utm_link = f"{url_base}/?utm_source=ads&utm_campaign={camp_selecionada.lower().replace(' ', '_')}"
        
        st.code(utm_link, language="text")
        st.info("Copie este link acima e cole no seu gerenciador de anúncios.")

# ==========================================
# 3. NO SIMULADOR DE LEADS (NA ABA LEADS)
# ==========================================
# Ao invés de hardcode, usamos a lista dinâmica:
# campanha_input = st.selectbox("Campanha de Origem", st.session_state.campanhas_cadastradas)

# ==========================================
# CÓDIGO AUXILIAR (FUNÇÕES)
# ==========================================
# Certifique-se de que a função calcular_faturamento_por_campanha use 
# a lista st.session_state.campanhas_cadastradas para iterar.
