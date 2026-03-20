import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES DE ENGENHARIA E CONEXÃO
st.set_page_config(page_title="HMM Serviços - Gestão Psicossocial", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("Programa de Avaliação de Riscos Psicossociais (COPSOQ III)")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.caption("🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Coleta de Dados (Ficha)", "🔐 Painel de Gestão e Relatórios"])

# --- ABA 1: COLETA (5 ITENS DE DEMANDA CONFORME FICHA) ---
with tab1:
    st.subheader("📋 Identificação da Unidade")
    c_id1, c_id2, c_id3 = st.columns([2, 1, 1])
    with c_id1: empresa = st.text_input("Empresa:", placeholder="Nome do Cliente")
    with c_id2: setor = st.text_input("Setor:", placeholder="Ex: Produção")
    with c_id3: funcao = st.text_input("Função:", placeholder="Ex: Operador")
    
    escala_freq = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_v22_1"):
        st.markdown("#### QUESTIONÁRIO DE DIAGNÓSTICO ORGANIZACIONAL")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 1. EXIGÊNCIAS (DEMANDAS)")
            p1_1 = st.radio("1.1 Você tem que trabalhar muito rápido?", list(escala_freq.keys()), index=None)
            p1_2 = st.radio("1.2 O seu trabalho é emocionalmente desgastante?", list(escala_freq.keys()), index=None)
            p1_3 = st.radio("1.3 O volume de trabalho é excessivo para o tempo?", list(escala_freq.keys()), index=None)
            p1_4 = st.radio("1.4 Você lida com prazos muito apertados?", list(escala_freq.keys()), index=None)
            p1_5 = st.radio("1.5 O trabalho exige esforço intenso (físico/mental)?", list(escala_freq.keys()), index=None)
            
            st.markdown("### 2. INFLUÊNCIA E DESENVOLVIMENTO (CONTROLE)")
            p2_1 = st.radio("2.1 Tem influência sobre as decisões no trabalho?", list(escala_freq.keys()), index=None)
            p2_2 = st.radio("2.2 Tem oportunidade de aprender coisas novas?", list(escala_freq.keys()), index=None)
            
        with col2:
            st.markdown("### 3. RELAÇÕES E SUPORTE SOCIAL")
            p3_1 = st.radio("3.1 O superior imediato apoia você quando precisa?", list(escala_freq.keys()), index=None)
            p3_2 = st.radio("3.2 Há um bom espírito de cooperação entre colegas?", list(escala_freq.keys()), index=None)
            
            st.markdown("### 4. BEM-ESTAR E SEGURANÇA")
            p4_1 = st.radio("4.1 Sente-se tenso ou estressado ultimamente?", list(escala_freq.keys()), index=
