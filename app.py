import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Interface
st.set_page_config(page_title="HMM Serviços - Perícia Psicossocial", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo Avançado COPSOQ III - Perícia Judicial")
st.markdown("---")

with st.sidebar:
    st.header("📋 Identificação")
    empresa = st.text_input("Empresa Avaliada:", "Ex: Ilda Monetti")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função/Cargo:")
    st.divider()
    st.info("HMM Serviços - Engenharia de Segurança e Perícias")

escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 2. Formulário Ampliado (Unindo o anterior com o novo)
with st.form("form_pericia_v3"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Demandas e Ritmo")
        p1 = st.radio("O ritmo de trabalho é intenso/rápido?", list(escala.keys()), index=2)
        p2 = st.radio("As tarefas são emocionalmente desgastantes?", list(escala.keys()), index=2)
        
        st.markdown("#### 🛠️ Autonomia e Controle")
        p3 = st.radio("Você tem influência sobre como faz seu trabalho?", list(escala.keys()), index=2)
        p4 = st.radio("O seu trabalho permite aprender coisas novas?", list(escala.keys()), index=2)

        st.markdown("#### 🔒 Insegurança e Significado")
        p9 = st.radio("Você tem receio de ser demitido em breve?", list(escala.keys()), index=2)
        p10 = st.radio("Você sente que seu trabalho é importante?", list(escala.keys()), index=2)

    with col2:
        st.markdown("#### 🤝 Suporte e Liderança")
        p5 = st.radio("Recebe apoio técnico/emocional da chefia?", list(escala.keys()), index=2)
        p6 = st.radio("Há um clima de colaboração entre colegas?", list(escala.keys()), index=2)
        
        st.markdown("#### ⚠️ Saúde e Estresse")
        p7 = st.radio("Sente-se tenso ou estressado ultimamente?", list(escala.keys()), index=2)
        p8 = st.radio("O trabalho interfere na sua qualidade de sono?", list(escala.keys()), index=2)

    submit = st.form_submit_button("Registrar Avaliação Técnica")

# 3. Cálculo e Gravação (Append na Página1)
if submit:
    # Médias para o Radar
    v_demanda = (escala[p1] + escala[p2]) / 2
    v_controle = (escala[p3] + escala[p4]) / 2
    v_suporte = (escala[p5] + escala[p6]) / 2
    v_saude = (escala[p7] + escala[p8]) / 2
    v_inseguranca = escala[p9]
    v_significado = escala[p10]
    
    st.session_state.df_radar = pd.DataFrame([
        {'Dimensão': 'Demanda', 'Score': v_demanda},
        {'Dimensão': 'Controle', 'Score': v_controle},
        {'Dimensão': 'Suporte', 'Score': v_suporte},
        {'Dimensão': 'Saúde', 'Score': v_saude},
        {'Dimensão': 'Insegurança', 'Score': v_inseguranca},
        {'Dimensão': 'Significado', 'Score': v_significado}
    ])

    try:
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor, "Funcao": funcao,
            "Demanda": v_demanda, "Controle": v_controle, 
            "Suporte": v_suporte, "Saude": v_saude,
            "Inseguranca": v_inseguranca, "Significado": v_significado
        }])
        
        # Lê a base e anexa o novo registro
        df_base = conn.read(worksheet="Página1")
        df_final = pd.concat([df_base, nova_linha], ignore_index=True)
        conn.update(worksheet="Página1", data=df_final)
        
        st.success(f"✅ Laudo de {funcao} registrado com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro na gravação: {e}")

# 4. Área do Perito
if st.session_state.df_radar is not None:
    st.markdown("---")
    with st.expander("🔐 Área de Análise (Acesso com Senha)"):
        senha = st.text_input("Senha Pericial:", type="password", key="final_pass")
        if senha == "1234":
            st.subheader(f"📊 Resultado Técnico: {funcao}")
            fig = px.line_polar(st.session_state.df_radar, r='Score', theta='Dimensão', 
                               line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)
            
            # Parecer técnico automático
            if v_demanda > 70 and v_controle < 40:
                st.error("🚩 **RISCO CRÍTICO:** Alta demanda e baixo controle. Ambiente patogênico (Modelo de Karasek).")
            else:
                st.info("✅ **ESTÁVEL:** Indicadores não sugerem risco crítico imediato.")
