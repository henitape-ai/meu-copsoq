import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Página
st.set_page_config(page_title="Expert COPSOQ III - Pericia", layout="wide")

# Inicializa a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Interface e Título
st.title("📊 Sistema de Avaliação Psicossocial - COPSOQ III")
st.markdown("---")

# Barra Lateral para Identificação
with st.sidebar:
    st.header("📋 Identificação da Perícia")
    empresa = st.text_input("Empresa Sob Avaliação:", "Minha Empresa")
    setor = st.selectbox("Setor:", ["Produção", "Logística", "Administrativo", "Operacional", "Vendas"])
    st.divider()
    st.info("Este questionário coleta dados técnicos para análise de nexo causal.")

# Definição da Escala Likert (0 a 100)
escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

st.subheader(f"Questionário Técnico - Setor: {setor}")

# 3. Formulário de Coleta para o Trabalhador
with st.form("form_copsoq"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. Exigências e Ritmo")
        p1 = st.radio("Você precisa trabalhar muito rápido?", list(escala.keys()), index=2)
        p2 = st.radio("O trabalho é distribuído de forma desigual?", list(escala.keys()), index=2)
        st.markdown("#### 2. Influência e Desenvolvimento")
        p3 = st.radio("Você tem influência sobre as decisões do seu trabalho?", list(escala.keys()), index=2)
        p4 = st.radio("O seu trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
    with col2:
        st.markdown("#### 3. Liderança e Apoio")
        p5 = st.radio("O seu superior imediato planeja bem o trabalho?", list(escala.keys()), index=2)
        p6 = st.radio("Você recebe ajuda e apoio de seus colegas?", list(escala.keys()), index=2)
        st.markdown("#### 4. Saúde e Bem-estar")
        p7 = st.radio("Sente-se tenso ou estressado ultimamente?", list(escala.keys()), index=2)
        p8 = st.radio("O trabalho afeta sua vida familiar/pessoal?", list(escala.keys()), index=2)
    submit = st.form_submit_button("Finalizar Avaliação")

# 4. Lógica de Processamento e Gravação
if submit:
    dados_calculados = {
        'Exigências': (escala[p1] + escala[p2]) / 2,
        'Autonomia': (escala[p3] + escala[p4]) / 2,
        'Liderança': (escala[p5] + escala[p6]) / 2,
        'Saúde': (escala[p7] + escala[p8]) / 2
    }
    df_grafico = pd.DataFrame(list(dados_calculados.items()), columns=['Dimensão', 'Pontuação'])

    try:
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa,
            "Setor": setor,
            "Exigencias": dados_calculados['Exigências'],
            "Autonomia": dados_calculados['Autonomia'],
            "Liderança": dados_calculados['Liderança'],
            "Saude": dados_calculados['Saúde']
        }])
        conn.create(data=nova_linha)
        st.success("✅ Avaliação enviada com sucesso! Obrigado pela colaboração.")
        st.balloons()
    except Exception as e:
        st.error(f"Erro técnico na gravação: {e}")

    st.markdown("---")

    # 5. ÁREA RESTRITA DO PERITO
    with st.expander("🔐 Área do Perito (Acesso Restrito)"):
        # A linha abaixo foi corrigida para evitar o SyntaxError
        senha_perito = st.text_input("Digite a senha:", type="password", key="perito_key")
        
        if senha_perito == "1234":
            st.subheader(f"📊 Análise de Risco - {empresa}")
            fig = px.line_polar(df_grafico, r='Pontuação', theta='Dimensão', line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='blue')
            st.plotly_chart(fig, use_container_width=True)
            
            if dados_calculados['Saúde'] > 70 or dados_calculados['Exigências'] > 70:
                alerta = "🚩 **ALTO RISCO:** Pontuação elevada (Nexo Causal Provável)."
            else:
                alerta = "✅ **RISCO CONTROLADO:** Dimensões dentro da normalidade."
            
            st.info(f"**Parecer Prévio:** {alerta}")
        elif senha_perito != "":
            st.error("Senha incorreta.")
