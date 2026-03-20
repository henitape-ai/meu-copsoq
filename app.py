import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão HMM
st.set_page_config(page_title="HMM Serviços - Portal de Avaliação", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO INSTITUCIONAL ---
st.title("Avaliação Psicossocial - Riscos Psicossociais (COPSOQ)")
st.subheader("HMM Serviços")
st.caption("🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# 2. Navegação por Abas
tab1, tab2 = st.tabs(["📝 Coleta de Dados", "🔐 Painel de Análise e Resultados"])

# --- ABA 1: COLETA DE DADOS ---
with tab1:
    st.subheader("📋 Identificação da Avaliação")
    
    c_id1, c_id2, c_id3 = st.columns([2, 1, 1])
    with c_id1: empresa = st.text_input("Empresa Avaliada:", placeholder="Digite o nome da empresa")
    with c_id2: setor = st.text_input("Setor:", placeholder="Ex: Produção")
    with c_id3: funcao = st.text_input("Função/Cargo:", placeholder="Ex: Operador")
    
    st.markdown("---")
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_coleta_v14"):
        st.markdown("#### QUESTIONÁRIO TÉCNICO (COPSOQ)")
        st.caption("🔒 ESTA AVALIAÇÃO É ANÔNIMA E SIGILOSA. OS DADOS SERÃO TRATADOS COLETIVAMENTE.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 1. DEMANDAS")
            p1 = st.radio("O RITMO DE TRABALHO É INTENSO?", list(escala.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p2 = st.radio("AS TAREFAS SÃO EMOCIONALMENTE DESGASTANTES?", list(escala.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### 2. CONTROLE")
            p3 = st.radio("VOCÊ TEM INFLUÊNCIA SOBRE AS DECISÕES NO TRABALHO?", list(escala.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p4 = st.radio("O TRABALHO PERMITE APRENDER NOVAS HABILIDADES?", list(escala.keys()), index=None)
            
        with col2:
            st.markdown("### 3. SUPORTE SOCIAL")
            p5 = st.radio("RECEBE APOIO DA CHEFIA QUANDO PRECISA?", list(escala.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p6 = st.radio("HÁ COLABORAÇÃO ENTRE OS COLEGAS?", list(escala.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("### 4. SAÚDE E INSEGURANÇA")
            p7 = st.radio("SENTE-SE TENSO OU ESTRESSADO ULTIMAMENTE?", list(escala.keys()), index=None)
            st.markdown("<br>", unsafe_allow_html=True)
            p8 = st.radio("TEM RECEIO DE SER DEMITIDO EM BREVE?", list(escala.keys()), index=None)

        st.markdown("---")
        st.markdown("### 5. RELAÇÕES INTERPESSOAIS E CONDUTA")
        st.warning("As perguntas abaixo referem-se a situações vividas nos últimos 12 meses no ambiente de trabalho.")
        
        col3, col4 = st.columns(2)
        with col3:
            p9 = st.radio("VOCÊ FOI EXPOSTO A SITUAÇÕES DE HUMILHAÇÃO OU ASSÉDIO MORAL?", list(escala.keys()), index=None)
        with col4:
            p10 = st.radio("VOCÊ FOI EXPOSTO A SITUAÇÕES DE ASSÉDIO SEXUAL (CONDUTAS INADEQUADAS OU INDESEJADAS)?", list(escala.keys()), index=None)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit = st.form_submit_button("FINALIZAR E GRAVAR DIAGNÓSTICO")

    if submit:
        respostas = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
        if None in respostas or not empresa or not setor:
            st.error("⚠️ Atenção: Preencha todos os campos e responda todas as perguntas (incluindo Assédio Moral/Sexual).")
        else:
            v_dem = (escala[p1] + escala[p2]) / 2
            v_con = (escala[p3] + escala[p4]) / 2
            v_sup = (escala[p5] + escala[p6]) / 2
            v_sau, v_ins = escala[p7], escala[p8]
            v_amor, v_asex = escala[p9], escala[p10]

            classif = "Baixo Risco"
            if v_amor > 25 or v_asex > 0: 
                classif = "ALERTA GRAVE (Conduta Inadequada)"
            elif v_dem > 60 and v_con < 40: 
                classif = "ALTO RISCO (Alta Tensão)"

            try:
                nova_linha = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                    "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                    "Saude": v_sau, "Inseguranca": v_ins, 
                    "Assedio_Moral": v_amor, "Assedio_Sexual": v_asex,
                    "Classificacao_Risco": classif, 
                    "Parecer_Tecnico": f"Avaliação técnica em {setor}", 
                    "Link_Grafico": ""
                }])
                df_b = conn.read(worksheet="Página1", ttl=0)
                conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                st.success(f"DADOS DE {funcao.upper()} GRAVADOS COM SUCESSO!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro na gravação: {e}")

    st.markdown("---")
    st.caption("© 2026 HMM Serviços - Segurança do Trabalho e Meio Ambiente. Todos os direitos reservados.")

# --- ABA 2: PAINEL DE ANÁLISE ---
with tab2:
    st.subheader("🔐 Painel de Análise")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_v14")

    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    lista_emp = sorted(df['Empresa'].unique())
                    emp_sel = st.selectbox("1. SELECIONE A EMPRESA:", lista_emp, index=None, placeholder="Escolha a empresa")
                with c_f2:
                    if emp_sel:
                        df_emp = df[df['Empresa'] == emp_sel]
                        lista_set = sorted(df_emp['Setor'].unique())
                        set_sel = st.selectbox("2. SELECIONE O SETOR:", lista_set, index=None, placeholder="Escolha o setor")
                    else: set_sel = None

                if set_sel:
                    df_set = df_emp[df_emp['Setor'] == set_sel]
                    # Incluindo as novas colunas na média para o Radar
                    cols_analise = ['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca', 'Assedio_Moral', 'Assedio_Sexual']
                    m = df_set[cols_analise].mean()
                    
                    st.markdown(f"### 📊 DIAGNÓSTICO CONSOLIDADO: {set_sel.upper()}")
                    
                    if m['Assedio_Moral'] > 0 or m['Assedio_Sexual'] > 0:
                        st.error("🚩 ALERTA PERICIAL: Ocorrências de Assédio Moral ou Sexual detectadas neste setor.")

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

                    status_final = "ESTÁVEL"
                    if m['Demanda'] > 60 and m['Controle'] < 40: status_final = "CRÍTICO (Alta Tensão)"
                    if m['Assedio_Moral'] > 25 or m['Assedio_Sexual'] > 5: status_final = "CRÍTICO (Violação de Conduta)"
                    
                    relatorio = f"EMPRESA: {emp_sel.upper()} | SETOR: {set_sel.upper()}\nDATA: {datetime.now().strftime('%d/%m/%Y')}\nDIAGNÓSTICO: {status_final}\n"
                    relatorio += f"MÉDIA ASSÉDIO MORAL: {m['Assedio_Moral']:.1f}\nMÉDIA ASSÉDIO SEXUAL: {m['Assedio_Sexual']:.1f}"
                    st.text_area("TEXTO PARA O LAUDO:", relatorio, height=300)
            else:
                st.warning("BANCO DE DADOS VAZIO.")
        except Exception as e:
            st.error(f"Erro: {e}")
    
    st.markdown("---")
    st.caption("© 2026 HMM Serviços - Engenharia e Perícias. Todos os direitos reservados.")
