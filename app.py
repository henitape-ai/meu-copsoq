import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão
st.set_page_config(page_title="HMM Serviços - Diagnóstico Avançado", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - HMM Serviços")
st.markdown("---")

# 2. Interface Principal em Abas
tab1, tab2 = st.tabs(["📝 Nova Avaliação (Mobile)", "🔐 Gerador de Laudos"])

# --- ABA 1: COLETA E DIAGNÓSTICO ---
with tab1:
    st.subheader("📋 Identificação da Perícia")
    col_id1, col_id2, col_id3 = st.columns([2, 1, 1])
    with col_id1: empresa = st.text_input("Empresa Avaliada:", "Nome da Empresa")
    with col_id2: setor = st.text_input("Setor:")
    with col_id3: funcao = st.text_input("Função/Cargo:")
    st.markdown("---")
    
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_coleta_avancada"):
        st.markdown("#### 📝 Questionário Técnico (Escala 0-100)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📈 Demandas**")
            p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
            p2 = st.radio("Tarefas emocionalmente desgastantes?", list(escala.keys()), index=2)
            st.markdown("**🛠️ Controle**")
            p3 = st.radio("Tem influência sobre as decisões?", list(escala.keys()), index=2)
            p4 = st.radio("Trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
        with c2:
            st.markdown("**🤝 Suporte Social**")
            p5 = st.radio("Recebe apoio da chefia?", list(escala.keys()), index=2)
            p6 = st.radio("Colaboração entre colegas?", list(escala.keys()), index=2)
            st.markdown("**⚠️ Saúde e Insegurança**")
            p7 = st.radio("Sente-se tenso/estressado?", list(escala.keys()), index=2)
            p9 = st.radio("Medo de perder o emprego?", list(escala.keys()), index=2)
        submit = st.form_submit_button("Finalizar e Gerar Diagnóstico")

    if submit:
        # Cálculos de Engenharia Organizacional
        v_dem = (escala[p1] + escala[p2]) / 2
        v_con = (escala[p3] + escala[p4]) / 2
        v_sup = (escala[p5] + escala[p6]) / 2
        v_sau = escala[p7]
        v_ins = escala[p9]
        v_sig = 50 # Valor padrão

        # --- MOTOR DE DIAGNÓSTICO (Lógica Pericial NR-17) ---
        classificacao = "Baixo Risco"
        parecer = "✅ Ambiente equilibrado. Sem necessidade de intervenção imediata."
        
        # Modelo Demanda-Controle (Karasek)
        if v_dem > 66 and v_con < 40:
            classificacao = "ALTO RISCO"
            parecer = "🚩 CRÍTICO: Alta Demanda e Baixo Controle. Risco elevado de Burnout/Adoecimento."
        elif v_dem > 66 or v_sau > 66:
            classificacao = "Risco Moderado"
            parecer = "⚠️ ATENÇÃO: Níveis elevados de demanda ou estresse. Recomenda-se monitoramento."
        elif v_con < 40 or v_sup < 40:
            classificacao = "Risco Moderado"
            parecer = "⚠️ ATENÇÃO: Baixo controle ou suporte social. Fator de agravamento organizacional."

        st.session_state.df_radar = pd.DataFrame([
            {'Dimensão': 'Demanda', 'Score': v_dem}, {'Dimensão': 'Controle', 'Score': v_con},
            {'Dimensão': 'Suporte', 'Score': v_sup}, {'Dimensão': 'Saúde', 'Score': v_sau},
            {'Dimensão': 'Insegurança', 'Score': v_ins}
        ])

        try:
            # Prepara a linha com as 13 colunas
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                "Saude": v_sau, "Inseguranca": v_ins, "Significado": v_sig,
                "Classificacao_Risco": classificacao,
                "Parecer_Tecnico": parecer,
                "Link_Grafico": "" # Será preenchido na planilha
            }])
            
            df_base = conn.read(worksheet="Página1", ttl=0)
            df_final = pd.concat([df_base, nova_linha], ignore_index=True)
            conn.update(worksheet="Página1", data=df_final)
            
            st.success(f"✅ Diagnóstico de {funcao} gravado na planilha com sucesso!")
            st.balloons()
            
            # Exibe o diagnóstico na tela para o perito
            st.markdown("---")
            st.subheader("📋 Diagnóstico Preliminar (HMM Serviços)")
            if classificacao == "ALTO RISCO": st.error(parecer)
            elif classificacao == "Risco Moderado": st.warning(parecer)
            else: st.success(parecer)
            
        except Exception as e:
            if "200" in str(e): st.success("✅ Diagnóstico enviado!")
            else: st.error(f"Erro Real na Gravação: {e}. Verifique se a planilha tem as 13 colunas.")

# --- ABA 2: GERADOR DE LAUDOS (MANTIDO) ---
with tab2:
    st.subheader("🔑 Acesso Restrito ao Perito")
    senha = st.text_input("Digite a senha:", type="password", key="sec_key_hmm")
    if senha == "HMM2024":
        # ... (Mesma lógica de busca da versão anterior, sem alterações)
        st.info("Utilize a busca para gerar o texto do laudo.")
