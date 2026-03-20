import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES DE ENGENHARIA E CONEXÃO HMM
st.set_page_config(page_title="HMM Serviços - Gestão Psicossocial", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("Programa de Avaliação de Riscos Psicossociais (COPSOQ III)")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.caption("🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Coleta de Dados (Ficha)", "📊 Painel de Análise e Relatórios"])

# --- ABA 1: COLETA (5 ITENS DE DEMANDA CONFORME FICHA) ---
with tab1:
    st.subheader("📋 Identificação da Unidade")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: empresa = st.text_input("Empresa:", placeholder="Nome do Cliente")
    with c2: setor = st.text_input("Setor:", placeholder="Ex: Produção")
    with c3: funcao = st.text_input("Função:", placeholder="Ex: Operador")
    
    escala_freq = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_v22_5"):
        st.markdown("#### QUESTIONÁRIO DE DIAGNÓSTICO ORGANIZACIONAL")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 1. EXIGÊNCIAS (DEMANDAS)")
            p1_1 = st.radio("1.1 Você tem que trabalhar muito rápido?", list(escala_freq.keys()), index=None)
            p1_2 = st.radio("1.2 O seu trabalho é emocionalmente desgastante?", list(escala_freq.keys()), index=None)
            p1_3 = st.radio("1.3 O volume de trabalho é excessivo para o tempo?", list(escala_freq.keys()), index=None)
            p1_4 = st.radio("1.4 Você lida com prazos muito apertados?", list(escala_freq.keys()), index=None)
            p1_5 = st.radio("1.5 O trabalho exige esforço intenso?", list(escala_freq.keys()), index=None)
            st.markdown("### 2. INFLUÊNCIA (CONTROLE)")
            p2_1 = st.radio("2.1 Tem influência sobre as decisões no trabalho?", list(escala_freq.keys()), index=None)
            p2_2 = st.radio("2.2 Tem oportunidade de aprender coisas novas?", list(escala_freq.keys()), index=None)
        with col2:
            st.markdown("### 3. SUPORTE SOCIAL")
            p3_1 = st.radio("3.1 O superior imediato apoia você?", list(escala_freq.keys()), index=None)
            p3_2 = st.radio("3.2 Há cooperação entre os colegas?", list(escala_freq.keys()), index=None)
            st.markdown("### 4. BEM-ESTAR")
            p4_1 = st.radio("4.1 Sente-se tenso ou estressado?", list(escala_freq.keys()), index=None)
            p4_2 = st.radio("4.2 Preocupado com estabilidade no emprego?", list(escala_freq.keys()), index=None)
            st.markdown("### 5. AMBIENTE ÉTICO")
            p5_1 = st.radio("5.1 Exposto a humilhação ou assédio moral?", list(escala_freq.keys()), index=None)
            p5_2 = st.radio("5.2 Exposto a assédio sexual?", list(escala_freq.keys()), index=None)
        
        if st.form_submit_button("GRAVAR RESPOSTAS"):
            respostas = [p1_1, p1_2, p1_3, p1_4, p1_5, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2]
            if None in respostas or not empresa or not setor:
                st.error("⚠️ Responda todas as questões.")
            else:
                try:
                    v_dem = (escala_freq[p1_1]+escala_freq[p1_2]+escala_freq[p1_3]+escala_freq[p1_4]+escala_freq[p1_5])/5
                    v_con = (escala_freq[p2_1]+escala_freq[p2_2])/2
                    v_sup = (escala_freq[p3_1]+escala_freq[p3_2])/2
                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": empresa.strip(), "Setor": setor.strip(), "Funcao": funcao.strip(),
                        "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup,
                        "Saude": escala_freq[p4_1], "Inseguranca": escala_freq[p4_2],
                        "Assedio_Moral": escala_freq[p5_1], "Assedio_
