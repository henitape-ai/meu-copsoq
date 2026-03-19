import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Página
st.set_page_config(page_title="Expert COPSOQ III - HMM Serviços", layout="wide")

# Inicializa a conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa a memória para o gráfico não sumir
if 'df_grafico' not in st.session_state:
    st.session_state.df_grafico = None
if 'dados_pericia' not in st.session_state:
    st.session_state.dados_pericia = None

st.title("📊 Avaliação Psicossocial Avançada - COPSOQ III")
st.markdown("---")

# 2. Identificação (Barra Lateral)
with st.sidebar:
    st.header("📋 Dados da Perícia")
    empresa = st.text_input("Empresa Avaliada:", "Ilda Monetti")
    setor = st.text_input("Setor:", "Paleto")
    funcao = st.text_input("Função/Cargo:", "Costureira")
    st.divider()
    st.info("HMM Serviços - Engenharia e Perícias Judiciais")

# Escala Likert
escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

st.subheader(f"Questionário de Campo - Função: {funcao}")

# 3. Formulário de Coleta
with st.form("form_copsoq_estavel"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. Exigências e Ritmo")
        p1 = st.radio("Você precisa trabalhar muito rápido?", list(escala.keys()), index=2)
        p2 = st.radio("O trabalho é distribuído de forma desigual?", list(escala.keys()), index=2)
        st.markdown("#### 2. Autonomia e Influência")
        p3 = st.radio("Você tem influência sobre as decisões?", list(escala.keys()), index=2)
        p4 = st.radio("O trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
        st.markdown("#### 3. Insegurança e Significado")
        p9 = st.radio("Tem receio de ser demitido?", list(escala.keys()), index=2)
        p10 = st.radio("Seu trabalho é importante?", list(escala.keys()), index=2)

    with col2:
        st.markdown("#### 4. Liderança e Apoio")
        p5 = st.radio("Superior planeja bem?", list(escala.keys()), index=2)
        p6 = st.radio("Recebe ajuda dos colegas?", list(escala.keys()), index=2)
        st.markdown("#### 5. Saúde e Estresse")
        p7 = st.radio("Sente-se tenso ou estressado?", list(escala.keys()), index=2)
        p8 = st.radio("Afeta sua vida pessoal?", list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Finalizar e Gravar Dados")

# 4. Lógica de Gravação (Modo Append)
if submit:
    dados = {
        'Exigências': (escala[p1] + escala[p2]) / 2,
        'Autonomia': (escala[p3] + escala[p4]) / 2,
        'Liderança': (escala[p5] + escala[p6]) / 2,
        'Saúde': (escala[p7] + escala[p8]) / 2,
        'Insegurança': escala[p9],
        'Significado': escala[p10]
    }
    st.session_state.df_grafico = pd.DataFrame(list(dados.items()), columns=['Dimensão', 'Pontuação'])
    st.session_state.dados_pericia = dados

    try:
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor, "Funcao": funcao,
            "Exigencias": dados['Exigências'], "Autonomia": dados['Autonomia'],
            "Liderança": dados['Liderança'], "Saude": dados['Saúde'],
            "Inseguranca": dados['Insegurança'], "Significado": dados['Significado']
        }])
        
        # Lê os dados da Página1 e adiciona a nova linha no fim
        df_existente = conn.read(worksheet="Página1")
        df_atualizado = pd.concat([df_existente, nova_linha], ignore_index=True)
        conn.update(worksheet="Página1", data=df_atualizado)
        
        st.success(f"✅ Avaliação de {funcao} registrada na Página1!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro na gravação: {e}. Renomeie sua aba para 'Página1'.")

# 5. ÁREA RESTRITA DO PERITO
if st.session_state.df_grafico is not None:
    st.markdown("---")
    with st.expander("🔐 Visualizar Análise Técnica"):
        senha = st.text_input("Senha:", type="password", key="auth_hmm_2026")
        if senha == "1234":
            st.subheader(f"📊 Laudo Técnico: {funcao} - {empresa}")
            fig = px.line_polar(st.session_state.df_grafico, r='Pontuação', theta='Dimensão', 
                               line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='blue')
            st.plotly_chart(fig, use_container_width=True)
            
            d_finais = st.session_state.dados_pericia
            resumo = "🚩 ALTO RISCO" if d_finais['Exigências'] > 75 or d_finais['Saúde'] > 75 else "✅ NORMAL"
            st.info(f"**Parecer:** {resumo} | Saúde: {d_finais['Saúde']} | Exigências: {d_finais['Exigências']}")
        elif senha != "":
            st.error("Senha incorreta.")
