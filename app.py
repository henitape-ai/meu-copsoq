import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia - HMM Serviços
st.set_page_config(page_title="HMM Serviços - Perícia Avançada", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa estados de memória
if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos Ocupacionais")
st.markdown("---")

# 2. Sidebar de Identificação
with st.sidebar:
    st.header("📋 Dados da Perícia")
    empresa = st.text_input("Empresa:", "Empresa Exemplo")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função/Cargo:")
    st.divider()
    st.info("HMM Serviços - Itapetininga/SP")

escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário Técnico
with st.form("form_hmm_final"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Demandas e Ritmo")
        p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
        p2 = st.radio("O trabalho exige muito esforço emocional?", list(escala.keys()), index=2)
        st.markdown("#### 🛠️ Controle e Influência")
        p3 = st.radio("Você tem influência sobre as decisões do trabalho?", list(escala.keys()), index=2)
        p4 = st.radio("O trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
    with c2:
        st.markdown("#### 🤝 Suporte Social")
        p5 = st.radio("Recebe apoio da chefia quando precisa?", list(escala.keys()), index=2)
        p6 = st.radio("Os colegas ajudam uns aos outros?", list(escala.keys()), index=2)
        st.markdown("#### ⚠️ Saúde e Insegurança")
        p7 = st.radio("Sente-se tenso ou estressado ultimamente?", list(escala.keys()), index=2)
        p9 = st.radio("Tem receio de perder o emprego em breve?", list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Registrar Avaliação Técnica")

# 4. Lógica de Gravação (Tratamento de Sucesso Corrigido)
if submit:
    v_dem = (escala[p1] + escala[p2]) / 2
    v_con = (escala[p3] + escala[p4]) / 2
    v_sup = (escala[p5] + escala[p6]) / 2
    v_sau = escala[p7]
    v_ins = escala[p9]
    v_sig = 50 

    st.session_state.df_radar = pd.DataFrame([
        {'Dimensão': 'Demanda', 'Score': v_dem},
        {'Dimensão': 'Controle', 'Score': v_con},
        {'Dimensão': 'Suporte', 'Score': v_sup},
        {'Dimensão': 'Saúde', 'Score': v_sau},
        {'Dimensão': 'Insegurança', 'Score': v_ins}
    ])

    try:
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor, "Funcao": funcao,
            "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
            "Saude": v_sau, "Inseguranca": v_ins, "Significado": v_sig
        }])
        
        # Operação de Append
        df_base = conn.read(worksheet="Página1")
        df_final = pd.concat([df_base, nova_linha], ignore_index=True)
        conn.update(worksheet="Página1", data=df_final)
        
        # Mensagem de Sucesso (Ignora o objeto de resposta do Google)
        st.success(f"✅ Sucesso! Dados de {funcao} registrados na Página1.")
        st.balloons()
        
    except Exception as e:
        st.error(f"Erro Real na Gravação: {e}")
