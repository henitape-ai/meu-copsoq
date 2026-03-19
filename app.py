import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações Iniciais
st.set_page_config(page_title="HMM Serviços - Perícia Avançada", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos Psicossociais")
st.markdown("---")

# 2. Identificação na Sidebar
with st.sidebar:
    st.header("📋 Dados do Periciado")
    empresa = st.text_input("Empresa:", "Empresa Exemplo")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função:")
    st.divider()
    st.info("HMM Serviços - Engenharia e Perícias Judiciais")

# Escala de Pontuação
escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário de Coleta
with st.form("form_hmm_final"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Demandas de Trabalho")
        p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
        p2 = st.radio("As tarefas são emocionalmente desgastantes?", list(escala.keys()), index=2)
        
        st.markdown("#### 🛠️ Controle e Influência")
        p3 = st.radio("Você tem influência sobre suas decisões?", list(escala.keys()), index=2)
        p4 = st.radio("O trabalho permite aprender coisas novas?", list(escala.keys()), index=2)

    with c2:
        st.markdown("#### 🤝 Suporte e Liderança")
        p5 = st.radio("Recebe apoio da chefia quando precisa?", list(escala.keys()), index=2)
        p6 = st.radio("Há colaboração entre os colegas?", list(escala.keys()), index=2)
        
        st.markdown("#### ⚠️ Saúde e Insegurança")
        p7 = st.radio("Sente-se tenso ou estressado?", list(escala.keys()), index=2)
        p9 = st.radio("Tem receio de ser demitido em breve?", list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Finalizar e Gravar Dados")

# 4. Processamento e Empilhamento (Append)
if submit:
    # Médias das Dimensões
    v_dem = (escala[p1] + escala[p2]) / 2
    v_con = (escala[p3] + escala[p4]) / 2
    v_sup = (escala[p5] + escala[p6]) / 2
    v_sau = escala[p7]
    v_ins = escala[p9]
    v_sig = 50 # Valor neutro para Significado
    
    st.session_state.df_radar = pd.DataFrame([
        {'Dimensão': 'Demanda', 'Score': v_dem},
        {'Dimensão': 'Controle', 'Score': v_con},
        {'Dimensão': 'Suporte', 'Score': v_sup},
        {'Dimensão': 'Saúde', 'Score': v_sau},
        {'Dimensão': 'Insegurança', 'Score': v_ins}
    ])

    try:
        # Cria a linha exatamente com os nomes das 10 colunas
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor, "Funcao": funcao,
            "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
            "Saude": v_sau, "Inseguranca": v_ins, "Significado": v_sig
        }])
        
        # Lê a aba fixa Página1
        df_base = conn.read(worksheet="Página1")
        # Concatena (Append)
        df_final = pd.concat([df_base, nova_linha], ignore_index=True)
        # Atualiza a aba
        conn.update(worksheet="Página1", data=df_final)
        
        st.success(f"✅ Avaliação de {funcao} registrada com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro na gravação: {e}. Certifique-se que a aba se chama 'Página1'.")

# 5. Área do Perito
if st.session_state.df_radar is not None:
    st.markdown("---")
    with st.expander("🔐 Área de Análise (Uso do Perito)"):
        senha = st.text_input("Senha Pericial:", type="password")
        if senha == "1234":
            st.subheader(f"📊 Laudo Técnico: {funcao} - {empresa}")
            fig = px.line_polar(st.session_state.df_radar, r='Score', theta='Dimensão', 
                               line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)
            
            # Parecer Técnico Automático
            if v_dem > 75 and v_con < 40:
                st.error("🚩 **RISCO ELEVADO:** Alta Demanda + Baixo Controle (Modelo de Karasek).")
            else:
                st.info("✅ **ESTÁVEL:** Indicadores dentro da normalidade.")
