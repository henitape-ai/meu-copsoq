import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="HMM Serviços - Perícia Avançada", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_grafico' not in st.session_state:
    st.session_state.df_grafico = None

st.title("📊 Protocolo de Avaliação Psicossocial - HMM Serviços")
st.markdown("---")

with st.sidebar:
    st.header("📋 Dados Técnicos")
    empresa = st.text_input("Empresa:", "Nome da Empresa")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função:")
    st.info("Utilizando Metodologia COPSOQ III (Copenhagen Psychosocial Questionnaire)")

escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

with st.form("form_pericia_v2"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 1. Demandas de Trabalho")
        p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
        p2 = st.radio("As tarefas são emocionalmente desgastantes?", list(escala.keys()), index=2)
        
        st.markdown("#### 2. Controle e Desenvolvimento")
        p3 = st.radio("Você pode influenciar como o trabalho é feito?", list(escala.keys()), index=2)
        p4 = st.radio("O trabalho exige que você aprenda novas habilidades?", list(escala.keys()), index=2)

    with c2:
        st.markdown("#### 3. Suporte Social e Liderança")
        p5 = st.radio("Você recebe apoio técnico da chefia quando precisa?", list(escala.keys()), index=2)
        p6 = st.radio("Há um clima de colaboração entre os colegas?", list(escala.keys()), index=2)
        
        st.markdown("#### 4. Reações de Estresse")
        p7 = st.radio("Sente dificuldades para relaxar após o expediente?", list(escala.keys()), index=2)
        p8 = st.radio("O trabalho interfere na sua qualidade de sono?", list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Registrar Avaliação Técnica")

if submit:
    # Cálculo por Dimensões Técnicas
    demanda = (escala[p1] + escala[p2]) / 2
    controle = (escala[p3] + escala[p4]) / 2
    suporte = (escala[p5] + escala[p6]) / 2
    estresse = (escala[p7] + escala[p8]) / 2
    
    dados_dict = {'Demanda': demanda, 'Controle': controle, 'Suporte': suporte, 'Estresse': estresse}
    st.session_state.df_grafico = pd.DataFrame(list(dados_dict.items()), columns=['Dimensão', 'Pontuação'])

    try:
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor, "Funcao": funcao,
            "Demanda": demanda, "Controle": controle, "Suporte": suporte, "Estresse": estresse
        }])
        
        # Lógica de Append estável na Página1
        df_base = conn.read(worksheet="Página1")
        df_final = pd.concat([df_base, nova_linha], ignore_index=True)
        conn.update(worksheet="Página1", data=df_final)
        
        st.success("✅ Dados consolidados na Página1.")
    except Exception as e:
        st.error(f"Erro: {e}. Verifique o nome da aba 'Página1'.")

# Área do Perito
if st.session_state.df_grafico is not None:
    st.markdown("---")
    with st.expander("🔐 Análise de Risco (Exclusivo Perito)"):
        senha = st.text_input("Senha:", type="password")
        if senha == "1234":
            st.subheader("Gráfico de Dispersão de Risco")
            fig = px.line_polar(st.session_state.df_grafico, r='Pontuação', theta='Dimensão', line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)
