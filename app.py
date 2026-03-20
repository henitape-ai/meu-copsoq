import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão HMM
st.set_page_config(page_title="HMM Serviços - Perícia 11.1", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Avaliação Psicossocial COPSOQ - HMM Serviços")
st.markdown("---")

# 2. Navegação por Abas
tab1, tab2 = st.tabs(["Coleta de Dados", "Painel de Análise e Laudo"])

# --- ABA 1: COLETA DE DADOS ---
with tab1:
    st.subheader("Identificação da Avaliação")
    
    c_id1, c_id2, c_id3 = st.columns([2, 1, 1])
    with c_id1: empresa = st.text_input("Empresa Avaliada:", "Nome da Empresa")
    with c_id2: setor = st.text_input("Setor:")
    with c_id3: funcao = st.text_input("Função/Cargo:")
    
    st.markdown("---")
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_coleta_v11"):
        st.markdown("#### QUESTIONÁRIO TÉCNICO (COPSOQ)")
        # Texto de anonimato menor que o título
        st.caption("🔒 Esta avaliação é anônima e sigilosa. Os dados são processados coletivamente para diagnóstico organizacional.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 1. DEMANDAS")
            p1 = st.radio("O RITMO DE TRABALHO É INTENSO?", list(escala.keys()), index=2)
            st.markdown("<br>", unsafe_allow_html=True)
            
            p2 = st.radio("AS TAREFAS SÃO EMOCIONALMENTE DESGASTANTES?", list(escala.keys()), index=2)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### 2. CONTROLE")
            p3 = st.radio("VOCÊ TEM INFLUÊNCIA SOBRE AS DECISÕES NO TRABALHO?", list(escala.keys()), index=2)
            st.markdown("<br>", unsafe_allow_html=True)
            
            p4 = st.radio("O TRABALHO PERMITE APRENDER NOVAS HABILIDADES?", list(escala.keys()), index=2)
            
        with col2:
            st.markdown("### 3. SUPORTE SOCIAL")
            p5 = st.radio("RECEBE APOIO DA CHEFIA QUANDO PRECISA?", list(escala.keys()), index=2)
            st.markdown("<br>", unsafe_allow_html=True)
            
            p6 = st.radio("HÁ COLABORAÇÃO ENTRE OS COLEGAS?", list(escala.keys()), index=2)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### 4. SAÚDE E INSEGURANÇA")
            p7 = st.radio("SENTE-SE TENSO OU ESTRESSADO ULTIMAMENTE?", list(escala.keys()), index=2)
            st.markdown("<br>", unsafe_allow_html=True)
            
            p9 = st.radio("TEM RECEIO DE SER DEMITIDO EM BREVE?", list(escala.keys()), index=2)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("FINALIZAR E GRAVAR DIAGNÓSTICO")

    if submit:
        v_dem = (escala[p1] + escala[p2]) / 2
        v_con = (escala[p3] + escala[p4]) / 2
        v_sup = (escala[p5] + escala[p6]) / 2
        v_sau, v_ins = escala[p7], escala[p9]

        classif = "Baixo Risco"
        if v_dem > 60 and v_con < 40: classif = "ALTO RISCO (Alta Tensão)"
        elif v_dem > 60 or v_sau > 60: classif = "Risco Moderado"

        try:
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                "Saude": v_sau, "Inseguranca": v_ins, "Significado": 50,
                "Classificacao_Risco": classif, 
                "Parecer_Tecnico": f"Avaliação em {setor}", 
                "Link_Grafico": ""
            }])
            df_b = conn.read(worksheet="Página1", ttl=0)
            conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
            st.success(f"DADOS DE {funcao.upper()} GRAVADOS COM SUCESSO!")
            st.balloons()
        except Exception as e:
            if "200" in str(e): st.success("DIAGNÓSTICO ENVIADO COM SUCESSO!")
            else: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE ANÁLISE E LAUDO ---
with tab2:
    st.subheader("Painel de Análise")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_v11")

    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    lista_emp = sorted(df['Empresa'].unique())
                    emp_sel = st.selectbox("1. SELECIONE A EMPRESA:", lista_emp)
                    df_emp = df[df['Empresa'] == emp_sel]
                with c_f2:
                    lista_set = sorted(df_emp['Setor'].unique())
                    set_sel = st.selectbox("2. SELECIONE O SETOR:", lista_set)
                    df_set = df_emp[df_emp['Setor'] == set_sel]

                m = df_set[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca']].mean()
                
                st.markdown(f"### 📊 DIAGNÓSTICO CONSOLIDADO: {set_sel.upper()}")
                col_radar, col_metrics = st.columns([2, 1])
                
                with col_radar:
                    radar_df = pd.DataFrame({'Eixo': m.index, 'Valor': m.values})
                    fig = px.line_polar(radar_df, r='Valor', theta='Eixo', line_close=True, range_r=[0,100])
                    fig.update_traces(fill='toself', line_color='red')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_metrics:
                    st.write("**MÉDIAS DO SETOR:**")
                    st.dataframe(m)
                    st.metric("AMOSTRA (N)", len(df_set))

                # Lógica de Relatório
                status = "ESTÁVEL"
                if m['Demanda'] > 60 and m['Controle'] < 40: status
