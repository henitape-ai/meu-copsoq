import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Expert COPSOQ III", layout="wide")

st.title("📊 Avaliação Psicossocial - Protocolo COPSOQ III")
st.sidebar.header("Configurações da Avaliação")

# 1. Cadastro Inicial
empresa = st.sidebar.text_input("Empresa:", "Empresa Exemplo")
setor = st.sidebar.selectbox("Setor:", ["Produção", "Administrativo", "Logística", "Vendas"])

# 2. Definição das Perguntas e Dimensões
perguntas = {
    "Exigências Quantitativas": "Você precisa trabalhar muito rápido?",
    "Influência": "Você tem influência sobre as decisões importantes no seu trabalho?",
    "Apoio Social": "Você recebe ajuda e apoio de seus colegas?",
    "Saúde/Estresse": "Com que frequência você se sentiu tenso ou estressado?"
}

escala = {
    "Sempre": 100,
    "Frequentemente": 75,
    "Às vezes": 50,
    "Raramente": 25,
    "Nunca": 0
}

# 3. Interface de Coleta
st.subheader(f"Questionário Anonimizado - Setor: {setor}")
respostas_usuario = {}

with st.form("form_copsoq"):
    for dimensao, pergunta in perguntas.items():
        respostas_usuario[dimensao] = st.radio(pergunta, list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Enviar Avaliação")

# 4. Processamento dos Resultados
if submit:
    # Converter respostas em pontos
    pontos = {d: escala[r] for d, r in respostas_usuario.items()}
    df_resultados = pd.DataFrame(list(pontos.items()), columns=['Dimensão', 'Pontuação'])

    st.success("Avaliação enviada com sucesso!")
    
    # Exibição do Gráfico de Radar/Barras
    st.divider()
    st.subheader(f"Análise de Risco: {empresa} - {setor}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line_polar(df_resultados, r='Pontuação', theta='Dimensão', line_close=True)
        fig.update_traces(fill='toself')
        st.plotly_chart(fig)

    with col2:
        st.write("**Interpretação Pericial:**")
        for d, p in pontos.items():
            status = "🔴 CRÍTICO" if p > 75 else "🟡 ALERTA" if p > 50 else "🟢 SEGURO"
            st.write(f"- {d}: **{p} pts** ({status})")

    # Botão para simular geração de Laudo
    st.button("📄 Gerar Relatório PDF para Perícia")