import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão HMM
st.set_page_config(page_title="HMM Serviços - Perícia 9.0", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa estado para o radar de visualização rápida
if 'radar_preview' not in st.session_state:
    st.session_state.radar_preview = None

st.title("📊 Protocolo COPSOQ III - HMM Serviços")
st.markdown("---")

# 2. Navegação por Abas (Otimizado para Mobile)
tab1, tab2 = st.tabs(["📝 Coleta de Dados", "🔐 Painel de Análise e Laudo"])

# --- ABA 1: COLETA DE DADOS EM CAMPO ---
with tab1:
    st.subheader("📋 Identificação da Perícia")
    
    # Identificação visível no celular (Corpo Principal)
    c_id1, c_id2, c_id3 = st.columns([2, 1, 1])
    with c_id1: empresa = st.text_input("Empresa Avaliada:", "Nome da Empresa")
    with c_id2: setor = st.text_input("Setor:")
    with c_id3: funcao = st.text_input("Função/Cargo:")
    
    st.markdown("---")
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_coleta_hmm"):
        st.markdown("#### 📝 Questionário Técnico")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📈 Demandas**")
            p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
            p2 = st.radio("Tarefas emocionalmente desgastantes?", list(escala.keys()), index=2)
            st.markdown("**🛠️ Controle**")
            p3 = st.radio("Tem influência sobre as decisões?", list(escala.keys()), index=2)
            p4 = st.radio("O trabalho permite aprender novas habilidades?", list(escala.keys()), index=2)
        with col2:
            st.markdown("**🤝 Suporte Social**")
            p5 = st.radio("Recebe apoio da chefia quando precisa?", list(escala.keys()), index=2)
            p6 = st.radio("Há colaboração entre os colegas?", list(escala.keys()), index=2)
            st.markdown("**⚠️ Saúde e Insegurança**")
            p7 = st.radio("Sente-se tenso ou estressado?", list(escala.keys()), index=2)
            p9 = st.radio("Tem receio de ser demitido em breve?", list(escala.keys()), index=2)
        
        submit = st.form_submit_button("Finalizar e Gravar na Planilha")

    if submit:
        # Cálculos Técnicos
        v_dem = (escala[p1] + escala[p2]) / 2
        v_con = (escala[p3] + escala[p4]) / 2
        v_sup = (escala[p5] + escala[p6]) / 2
        v_sau, v_ins = escala[p7], escala[p9]

        # Diagnóstico para a Planilha
        classif = "Baixo Risco"
        if v_dem > 60 and v_con < 40: classif = "ALTO RISCO (Alta Tensão)"
        elif v_dem > 60 or v_sau > 60: classif = "Risco Moderado"

        try:
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                "Saude": v_sau, "Inseguranca": v_ins, "Significado": 50,
                "Classificacao_Risco": classif, "Parecer_Tecnico": f"Avaliação de {funcao}", "Link_Grafico": ""
            }])
            df_b = conn.read(worksheet="Página1", ttl=0)
            conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
            st.success(f"✅ Dados de {funcao} registrados com sucesso!")
            st.balloons()
        except Exception as e:
            if "200" in str(e): st.success("✅ Enviado (API 200)")
            else: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE ANÁLISE E LAUDO TÉCNICO ---
with tab2:
    st.subheader("🔐 Painel de Análise e Laudo Técnico")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_final")

    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                # Filtros Hierárquicos
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    lista_emp = sorted(df['Empresa'].unique())
                    emp_sel = st.selectbox("1. Selecione a Empresa:", lista_emp)
                    df_emp = df[df['Empresa'] == emp_sel]
                with c_f2:
                    lista_set = sorted(df_emp['Setor'].unique())
                    set_sel = st.selectbox("2. Selecione o Setor:", lista_set)
                    df_set = df_emp[df_emp['Setor'] == set_sel]

                # Cálculos de Média do Setor selecionado
                m = df_set[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca']].mean()
                
                # Visualização Gráfica
                st.markdown(f"### 📊 Diagnóstico do Setor: {set_sel}")
                col_radar, col_metrics = st.columns([2, 1])
                
                with col_radar:
                    radar_df = pd.DataFrame({'Eixo': m.index, 'Valor': m.values})
                    fig = px.line_polar(radar_df, r='Valor', theta='Eixo', line_close=True, range_r=[0,100])
                    fig.update_traces(fill='toself', line_color='red')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_metrics:
