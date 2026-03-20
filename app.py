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

# --- ABA 1: COLETA ---
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
            p4_1 = st.radio("4.1 Sente-se tenso ou estressado ultimamente?", list(escala_freq.keys()), index=None)
            p4_2 = st.radio("4.2 Preocupado com a estabilidade no emprego?", list(escala_freq.keys()), index=None)
            
            st.markdown("### 5. AMBIENTE ÉTICO (ASSÉDIO)")
            p5_1 = st.radio("5.1 Exposto a humilhação ou assédio moral?", list(escala_freq.keys()), index=None)
            p5_2 = st.radio("5.2 Exposto a assédio sexual (investidas)?", list(escala_freq.keys()), index=None)
        
        if st.form_submit_button("GRAVAR RESPOSTAS"):
            respostas = [p1_1, p1_2, p1_3, p1_4, p1_5, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2]
            if None in respostas or not empresa or not setor:
                st.error("⚠️ Preencha todos os campos da ficha antes de enviar.")
            else:
                try:
                    v_dem = (escala_freq[p1_1]+escala_freq[p1_2]+escala_freq[p1_3]+escala_freq[p1_4]+escala_freq[p1_5])/5
                    v_con = (escala_freq[p2_1]+escala_freq[p2_2])/2
                    v_sup = (escala_freq[p3_1]+escala_freq[p3_2])/2
                    
                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                        "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup,
                        "Saude": escala_freq[p4_1], "Inseguranca": escala_freq[p4_2],
                        "Assedio_Moral": escala_freq[p5_1], "Assedio_Sexual": escala_freq[p5_2],
                        "Status": "Finalizado", "Metodo": "COPSOQ III"
                    }])
                    
                    df_base = conn.read(worksheet="Página1", ttl=0)
                    df_final = pd.concat([df_base, nova_linha], ignore_index=True)
                    conn.update(worksheet="Página1", data=df_final)
                    st.success("✅ DADOS ENVIADOS COM SUCESSO!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")

# --- ABA 2: PAINEL DE GESTÃO ---
with tab2:
    st.subheader("🔐 Área do Consultor - HMM Serviços")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_v22_1")

    if senha == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            emp_sel = st.selectbox("Selecione a Empresa:", sorted(df['Empresa'].unique()), index=None)
            
            if emp_sel:
                setores = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                set_sel = st.multiselect("Filtrar Setores:", setores)
                
                st.markdown("---")
                st.subheader("✍️ Análise e Conclusão")
                txt_padrao = ("Diagnóstico aponta perfil de [ALTA TENSÃO / ESTÁVEL]. "
                             "Foco recomendado em [CITAR FATOR].\n\n"
                             "RECOMENDAÇÕES:\n1. Ajuste NR-17;\n2. Treinamento liderança;\n3. Canal de Ética Lei 14.457/22.")
                conclusao = st.text_area("Edite a conclusão:", value=txt_padrao, height=200)

                if st.button("🚀 GERAR RELATÓRIO PARA WORD"):
                    setores_finais = set_sel if set_sel else setores
                    minuta = f"RELATÓRIO TÉCNICO DE GESTÃO PSICOSSOCIAL\nCLIENTE: {emp_sel.upper()}\nDATA: {datetime.now().strftime('%d/%m/%Y')}\n"
                    minuta += "="*60 + "\n\n"
                    
                    for s in setores_finais:
                        df_s = df[(df['Empresa'] == emp_sel) & (df['Setor'] == s)]
                        m = df_s[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca', 'Assedio_Moral', 'Assedio
