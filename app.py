import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Página
st.set_page_config(page_title="Expert COPSOQ III - HMM Serviços", layout="wide")

# Inicializa a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa o estado da sessão
if 'df_grafico' not in st.session_state:
    st.session_state.df_grafico = None

st.title("📊 Avaliação Psicossocial Avançada - COPSOQ III")
st.markdown("---")

# 2. Identificação Detalhada (Barra Lateral)
with st.sidebar:
    st.header("📋 Dados do Periciado")
    empresa = st.text_input("Empresa:", "Empresa Avaliada")
    setor = st.text_input("Setor:") # Mudado para texto livre para precisão
    funcao = st.text_input("Função/Cargo:") # Nova variável solicitada
    st.divider()
    st.info("HMM Serviços - Engenharia e Perícias Judiciais")

# Escala Likert
escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário de Coleta Ampliado
with st.form("form_copsoq_v2"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 1. Exigências e Ritmo")
        p1 = st.radio("Você precisa trabalhar muito rápido?", list(escala.keys()), index=2)
        p2 = st.radio("O trabalho é distribuído de forma desigual?", list(escala.keys()), index=2)
        
        st.markdown("#### 2. Autonomia e Influência")
        p3 = st.radio("Você tem influência sobre as decisões do seu trabalho?", list(escala.keys()), index=2)
        p4 = st.radio("O seu trabalho permite aprender coisas novas?", list(escala.keys()), index=2)

        st.markdown("#### 3. Insegurança no Trabalho") # Nova dimensão
        p9 = st.radio("Você tem receio de ser demitido em breve?", list(escala.keys()), index=2)

    with col2:
        st.markdown("#### 4. Liderança e Apoio Social")
        p5 = st.radio("O seu superior imediato planeja bem o trabalho?", list(escala.keys()), index=2)
        p6 = st.radio("Você recebe ajuda e apoio de seus colegas?", list(escala.keys()), index=2)
        
        st.markdown("#### 5. Saúde e Bem-estar")
        p7 = st.radio("Sente-se tenso ou estressado ultimamente?", list(escala.keys()), index=2)
        p8 = st.radio("O trabalho afeta sua vida familiar/pessoal?", list(escala.keys()), index=2)

        st.markdown("#### 6. Significado do Trabalho") # Nova dimensão
        p10 = st.radio("Você sente que o seu trabalho é importante?", list(escala.keys()), index=2)

    submit = st.form_submit_button("Finalizar e Gravar Avaliação")

# 4. Processamento e Gravação
if submit:
    # Cálculos das dimensões
    dados = {
        'Exigências': (escala[p1] + escala[p2]) / 2,
        'Autonomia': (escala[p3] + escala[p4]) / 2,
        'Liderança': (escala[p5] + escala[p6]) / 2,
        'Saúde': (escala[p7] + escala[p8]) / 2,
        'Insegurança': escala[p9],
        'Significado': escala[p10]
    }
    
    st.session_state.df_grafico = pd.DataFrame(list(dados.items()), columns=['Dimensão', 'Pontuação'])
    st.session_state.dados_finais = dados

    try:
        # Preparação da linha com 'Função'
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa,
            "Setor": setor,
            "Funcao": funcao, # Inserido na gravação
            "Exigencias": dados['Exigências'],
            "Autonomia": dados['Autonomia'],
            "Liderança": dados['Liderança'],
            "Saude": dados['Saúde'],
            "Inseguranca": dados['Insegurança']
        }])
        
        conn.create(data=nova_linha)
        st.success(f"✅ Avaliação de {funcao} enviada com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro na gravação: {e}")

# 5. ÁREA DO PERITO (Protegida)
if st.session_state.df_grafico is not None:
    st.markdown("---")
    with st.expander("🔐 Área do Perito (Análise Técnica)"):
        senha = st.text_input("Senha de Acesso:", type="password", key="sec_key")
        
        if senha == "1234":
            st.subheader(f"📊 Laudo Técnico: {funcao} - {empresa}")
            
            fig = px.line_polar(st.session_state.df_grafico, r='Pontuação', theta='Dimensão', 
                               line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)
            
            # Alerta de Nexo Causal
            d = st.session_state.dados_finais
            if d['Exigências'] > 70 and d['Autonomia'] < 40:
                st.error("🚩 **ALERTA DE NEXO:** Alta Exigência combinada com Baixa Autonomia (Modelo de Karasek) indica alto risco de adoecimento mental.")
            else:
                st.info("✅ Indicadores dentro da normalidade para esta função.")
