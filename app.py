import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Expert COPSOQ III - Perícia", layout="wide")

st.title("📊 Avaliação Psicossocial Completa - COPSOQ III")
st.markdown("---")

# Configurações de Identificação
with st.sidebar:
    st.header("📋 Dados da Avaliação")
    empresa = st.text_input("Empresa Sob Avaliação:", "Minha Empresa")
    setor = st.selectbox("Setor:", ["Produção", "Logística", "Administrativo", "Operacional", "Vendas"])
    st.info("Este questionário é anônimo conforme a LGPD.")

# Definição das Dimensões e Perguntas (Versão Média)
# Escala: Sempre(100), Frequentemente(75), Às vezes(50), Raramente(25), Nunca(0)
escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

st.subheader(f"Questionário: {setor}")

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

    submit = st.form_submit_button("Finalizar e Gerar Gráfico")

if submit:
    # Cálculo das médias por dimensão
    dados = {
        'Exigências': (escala[p1] + escala[p2]) / 2,
        'Autonomia': (escala[p3] + escala[p4]) / 2,
        'Liderança': (escala[p5] + escala[p6]) / 2,
        'Estresse/Saúde': (escala[p7] + escala[p8]) / 2
    }
    
    df = pd.DataFrame(list(dados.items()), columns=['Dimensão', 'Pontuação'])

    # Exibição do Gráfico de Radar
    st.success("Cálculos realizados com sucesso!")
    
    fig = px.line_polar(df, r='Pontuação', theta='Dimensão', line_close=True, range_r=[0,100])
    fig.update_traces(fill='toself', line_color='red')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Alerta de Risco para o Perito
    st.warning("**Análise de Risco:** Valores acima de 75 nas áreas de 'Exigências' ou 'Estresse' indicam alta probabilidade de nexo causal para doenças ocupacionais.")
