import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão HMM
st.set_page_config(page_title="HMM Serviços - Protocolo COPSOQ III", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO INSTITUCIONAL ---
st.title("Avaliação de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia e Perícias")
st.caption("🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# 2. Navegação por Abas
tab1, tab2 = st.tabs(["📝 Coleta de Dados", "🔐 Painel de Análise"])

# --- ABA 1: COLETA DE DADOS (QUESTIONÁRIO OFICIAL) ---
with tab1:
    st.subheader("📋 Identificação da Avaliação")
    
    c_id1, c_id2, c_id3 = st.columns([2, 1, 1])
    with c_id1: empresa = st.text_input("Empresa Avaliada:", placeholder="Nome da Unidade/Cliente")
    with c_id2: setor = st.text_input("Setor:", placeholder="Ex: Oficina / Administrativo")
    with c_id3: funcao = st.text_input("Função/Cargo:", placeholder="Ex: Mecânico")
    
    st.markdown("---")
    
    # Escalas Oficiais COPSOQ III
    escala_freq = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}
    escala_int = {"Muito": 100, "Um pouco": 66, "Moderadamente": 33, "Nada": 0}

    with st.form("form_copsoq_oficial"):
        st.markdown("#### QUESTIONÁRIO TÉCNICO (BASEADO NO COPSOQ III)")
        st.caption("🔒 ESTA AVALIAÇÃO É ANÔNIMA E SIGILOSA. OS DADOS SÃO TRATADOS COLETIVAMENTE CONFORME LGPD.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 1. EXIGÊNCIAS (DEMANDAS)")
            p1 = st.radio("VOCÊ TEM QUE TRABALHAR MUITO RÁPIDO?", list(escala_freq.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p2 = st.radio("O SEU TRABALHO É EMOCIONALMENTE DESGASTANTE?", list(escala_freq.keys()), index=None)
            
            st.markdown("### 2. INFLUÊNCIA E DESENVOLVIMENTO (CONTROLE)")
            p3 = st.radio("VOCÊ TEM INFLUÊNCIA SOBRE AS DECISÕES RELATIVAS AO SEU TRABALHO?", list(escala_freq.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p4 = st.radio("O SEU TRABALHO DÁ OPORTUNIDADE DE APRENDER COISAS NOVAS?", list(escala_freq.keys()), index=None)
            
        with col2:
            st.markdown("### 3. RELAÇÕES SOCIAIS E LIDERANÇA (SUPORTE)")
            p5 = st.radio("O SEU SUPERIOR IMEDIATO APOIA VOCÊ QUANDO PRECISA?", list(escala_freq.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p6 = st.radio("EXISTE UM BOM ESPÍRITO DE COOPERAÇÃO ENTRE OS SEUS COLEGAS?", list(escala_freq.keys()), index=None)
            
            st.markdown("### 4. SAÚDE E INSEGURANÇA")
            p7 = st.radio("COM QUE FREQUÊNCIA VOCÊ SE SENTIU TENSO OU ESTRESSADO?", list(escala_freq.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p8 = st.radio("VOCÊ ESTÁ PREOCUPADO EM FICAR DESEMPREGADO?", list(escala_freq.keys()), index=None)

        st.markdown("---")
        st.markdown("### 5. COMPORTAMENTOS OFENSIVOS (CONDUTA ÉTICA)")
        st.warning("⚠️ Informe se você foi exposto a estas situações no ambiente de trabalho nos últimos 12 meses:")
        
        col3, col4 = st.columns(2)
        with col3:
            p9 = st.radio("VOCÊ FOI EXPOSTO A BULLYING, HUMILHAÇÃO OU ASSÉDIO MORAL?", list(escala_freq.keys()), index=None)
        with col4:
            p10 = st.radio("VOCÊ FOI EXPOSTO A ASSÉDIO SEXUAL (AVANÇOS OU INVESTIDAS INDESEJADAS)?", list(escala_freq.keys()), index=None)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("FINALIZAR E ENVIAR DIAGNÓSTICO")

    if submit:
        respostas = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
        if None in respostas or not empresa or not setor:
            st.error("⚠️ CAMPOS INCOMPLETOS: Por favor, responda todas as questões para garantir a validade do laudo.")
        else:
            # Cálculo dos Scores HMM conforme COPSOQ
            v_dem = (escala_freq[p1] + escala_freq[p2]) / 2
            v_con = (escala_freq[p3] + escala_freq[p4]) / 2
            v_sup = (escala_freq[p5] + escala_freq[p6]) / 2
            v_sau, v_ins = escala_freq[p7], escala_freq[p8]
            v_amor, v_asex = escala_freq[p9], escala_freq[p10]

            # Classificação de Risco Pericial
            classif = "Baixo Risco"
            if v_amor > 0 or v_asex > 0: classif = "ALERTA: Conduta Ofensiva"
            elif v_dem > 60 and v_con < 40: classif = "CRÍTICO: Alta Tensão"

            try:
                nova_linha = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                    "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                    "Saude": v_sau, "Inseguranca": v_ins, 
                    "Assedio_Moral": v_amor, "Assedio_Sexual": v_asex,
                    "Classificacao_Risco": classif, "Parecer_Tecnico": f"Protocolo COPSOQ III - {setor}", 
                    "Link_Grafico": ""
                }])
                df_b = conn.read(worksheet="Página1", ttl=0)
                conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                st.success(f"DADOS DE {funcao.upper()} PROCESSADOS COM SUCESSO!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro de Conexão: {e}")

    st.markdown("---")
    st.caption("© 2026 HMM Serviços - Engenharia e Perícias Judiciais. Protegido por Direitos Autorais.")

# --- ABA 2: PAINEL DE ANÁLISE ---
with tab2:
    st.subheader("🔐 Gestão de Riscos Psicossociais")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_v15")

    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    lista_emp = sorted(df['Empresa'].unique())
                    emp_sel = st.selectbox("Selecione a Empresa:", lista_emp, index=None, placeholder="Filtrar Cliente")
                with c_f2:
                    if emp_sel:
                        df_emp = df[df['Empresa'] == emp_sel]
                        lista_set = sorted(df_emp['Setor'].unique())
                        set_sel = st.selectbox("Selecione o Setor:", lista_set, index=None, placeholder="Filtrar Unidade")
                    else: set_sel = None

                if set_sel:
                    df_set = df_emp[df_emp['Setor'] == set_sel]
                    m = df_set[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca', 'Assedio_Moral', 'Assedio_Sexual']].mean()
                    
                    st.markdown(f"### 📊 Diagnóstico Setorial: {set_sel.upper()}")
                    
                    if m['Assedio_Moral'] > 0 or m['Assedio_Sexual'] > 0:
                        st.error("🚩 NEXO DE RISCO: Detectada incidência de comportamentos ofensivos/assédio.")

                    col_radar, col_metrics = st.columns([2, 1])
                    with col_radar:
                        radar_df = pd.DataFrame({'Eixo': m.index, 'Valor': m.values})
                        fig = px.line_polar(radar_df, r='Valor', theta='Eixo', line_close=True, range_r=[0,100])
                        fig.update_traces(fill='toself', line_color='blue')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col_metrics:
                        st.write("**MÉDIAS CALCULADAS:**")
                        st.dataframe(m)
                        st.metric("TOTAL DE AVALIAÇÕES", len(df_set))

                    relatorio = f"EMPRESA: {emp_sel.upper()}\nSETOR: {set_sel.upper()}\nSTATUS: {classif}\nMETODOLOGIA: COPSOQ III"
                    st.text_area("TEXTO PARA O LAUDO PERICIAL:", relatorio, height=200)
            else:
                st.warning("Banco de dados sem registros.")
        except Exception as e:
            st.error(f"Erro: {e}")
