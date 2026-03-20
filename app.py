import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia - HMM Serviços
st.set_page_config(page_title="HMM Serviços - Perícia 3.4", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos Ocupacionais")
st.markdown("---")

# 2. Sidebar de Identificação
with st.sidebar:
    st.header("📋 Dados Técnicos")
    empresa = st.text_input("Empresa:", "Nome da Empresa")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função:")
    st.divider()
    st.info("HMM Serviços - Itapetininga/SP")

escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário Técnico
with st.form("form_final_perito"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Demandas")
        p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
        p2 = st.radio("As tarefas são emocionalmente desgastantes?", list(escala.keys()), index=2)
        st.markdown("#### 🛠️ Controle")
        p3 = st.radio("Você pode influenciar no seu trabalho?", list(escala.keys()), index=2)
        p4 = st.radio("O trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
    with c2:
        st.markdown("#### 🤝 Suporte")
        p5 = st.radio("Recebe apoio da chefia?", list(escala.keys()), index=2)
        p6 = st.radio("Há colaboração entre os colegas?", list(escala.keys()), index=2)
        st.markdown("#### ⚠️ Saúde e Insegurança")
        p7 = st.radio("Sente-se estressado ultimamente?", list(escala.keys()), index=2)
        p9 = st.radio("Tem medo de perder o emprego?", list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Registrar na Planilha")

# 4. Lógica de Gravação Segura (Sem Cache)
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
        # Prepara a linha (10 colunas idênticas ao cabeçalho da Página1)
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor, "Funcao": funcao,
            "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
            "Saude": v_sau, "Inseguranca": v_ins, "Significado": v_sig
        }])
        
        # Lê a Página1 forçando a atualização em tempo real (ttl=0)
        df_base = conn.read(worksheet="Página1", ttl=0)
        
        # Concatena e Atualiza
        df_final = pd.concat([df_base, nova_linha], ignore_index=True)
        conn.update(worksheet="Página1", data=df_final)
        
        st.success(f"✅ Avaliação de {funcao} gravada com sucesso!")
        st.balloons()
        
    except Exception as e:
        if "200" in str(e):
            st.success("✅ Dados enviados com sucesso (Resposta 200)!")
            st.balloons()
        else:
            st.error(f"Erro Real na Gravação: {e}")

# 5. Área do Perito
if st.session_state.df_radar is not None:
    st.markdown("---")
    with st.expander("🔐 Área do Perito"):
        senha = st.text_input("Senha:", type="password", key="sec_2026")
        if senha == "1234":
            fig = px.line_polar(st.session_state.df_radar, r='Score', theta='Dimensão', line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)
