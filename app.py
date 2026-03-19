import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações
st.set_page_config(page_title="HMM Serviços - Perícia 3.0", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicialização de Memória
if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Avaliação Psicossocial Avançada - COPSOQ III")
st.markdown("---")

# 2. Sidebar
with st.sidebar:
    st.header("📋 Dados Técnicos")
    empresa = st.text_input("Empresa:", "Nome da Empresa")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função:")
    st.divider()
    st.info("HMM Serviços - Itapetininga/SP")

escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário
with st.form("form_final_v3"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Demandas e Ritmo")
        p1 = st.radio("Ritmo de trabalho intenso?", list(escala.keys()), index=2)
        p2 = st.radio("Tarefas emocionalmente desgastantes?", list(escala.keys()), index=2)
        st.markdown("#### 🛠️ Controle e Autonomia")
        p3 = st.radio("Influência sobre as decisões?", list(escala.keys()), index=2)
        p4 = st.radio("Trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
    with c2:
        st.markdown("#### 🤝 Suporte e Liderança")
        p5 = st.radio("Apoio da chefia quando precisa?", list(escala.keys()), index=2)
        p6 = st.radio("Colaboração entre colegas?", list(escala.keys()), index=2)
        st.markdown("#### ⚠️ Saúde e Insegurança")
        p7 = st.radio("Sente-se tenso ou estressado?", list(escala.keys()), index=2)
        p9 = st.radio("Receio de ser demitido?", list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Registrar e Empilhar Dados")

# 4. Lógica de Gravação Segura
if submit:
    v_dem = (escala[p1] + escala[p2]) / 2
    v_con = (escala[p3] + escala[p4]) / 2
    v_sup = (escala[p5] + escala[p6]) / 2
    v_sau = escala[p7]
    v_ins = escala[p9]
    
    # Prepara o Radar
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
            "Saude": v_sau, "Inseguranca": v_ins, "Significado": 50 # Valor padrão para manter a estrutura
        }])
        
        # Lê apenas para garantir o append no final
        df_atual = conn.read(worksheet="Página1")
        df_novo = pd.concat([df_atual, nova_linha], ignore_index=True)
        conn.update(worksheet="Página1", data=df_novo)
        
        st.success(f"✅ Avaliação de {funcao} empilhada com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro: {e}")

# 5. Área do Perito
if st.session_state.df_radar is not None:
    st.markdown("---")
    with st.expander("🔐 Análise do Perito"):
        senha = st.text_input("Senha:", type="password")
        if senha == "1234":
            fig = px.line_polar(st.session_state.df_radar, r='Score', theta='Dimensão', line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)
