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

tab1, tab2 = st.tabs(["📝 Coleta de Dados (Ficha)", "📊 Painel de Análise e Relatórios"])

# --- ABA 1: COLETA ---
with tab1:
    st.subheader("📋 Identificação da Unidade")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: empresa = st.text_input("Empresa:", placeholder="Nome do Cliente")
    with c2: setor = st.text_input("Setor:", placeholder="Ex: Produção")
    with c3: funcao = st.text_input("Função:", placeholder="Ex: Operador")
    
    escala_freq = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_v22_final"):
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
                        "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                        "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup,
                        "Saude": escala_freq[p4_1], "Inseguranca": escala_freq[p4_2],
                        "Assedio_Moral": escala_freq[p5_1], "Assedio_Sexual": escala_freq[p5_2],
                        "Status": "Finalizado", "Metodo": "COPSOQ III"
                    }])
                    df_base = conn.read(worksheet="Página1", ttl=0)
                    df_final = pd.concat([df_base, nova_linha], ignore_index=True)
                    conn.update(worksheet="Página1", data=df_final)
                    st.success("✅ DADOS ENVIADOS!")
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: ANÁLISE E RELATÓRIO ---
with tab2:
    st.subheader("🔐 Painel de Gestão HMM")
    senha = st.text_input("Senha:", type="password", key="login_final")
    if senha == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            emp_sel = st.selectbox("Empresa:", sorted(df['Empresa'].unique()), index=None)
            if emp_sel:
                setores = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                set_sel = st.multiselect("Filtrar por Setor:", setores)
                df_filtrado = df[df['Empresa'] == emp_sel]
                if set_sel:
                    df_filtrado = df_filtrado[df_filtrado['Setor'].isin(set_sel)]
                
                cols_radar = ['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca', 'Assedio_Moral', 'Assedio_Sexual']
                medias = df_filtrado[cols_radar].mean()
                
                # Gráfico e Tabela
                fig = px.line_polar(r=medias.values, theta=medias.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', line_color='red')
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(medias.to_frame(name="Valor Médio").T.style.format("{:.1f}"))

                st.markdown("---")
                conclusao = st.text_area("✍️ Conclusão Técnica:", value="Diagnóstico aponta perfil de [ALTA TENSÃO].", height=150)
                
                if st.button("🚀 GERAR RELATÓRIO"):
                    # Construção segura da String
                    minuta = f"RELATÓRIO TÉCNICO - {emp_sel.upper()}\n"
                    minuta += f"DATA: {datetime.now().strftime('%d/%m/%Y')}\n"
                    minuta += "="*40 + "\n"
                    minuta += f"Geral: {len(df_filtrado)} avaliados\n"
                    minuta += f"Demanda: {medias['Demanda']:.1f} | Controle: {medias['Controle']:.1f}\n"
                    minuta += f"Suporte: {medias['Suporte']:.1f} | Saúde: {medias['Saude']:.1f}\n"
                    minuta += f"Insegurança: {medias['Inseguranca']:.1f}\n"
                    minuta += f"Assédio Moral: {medias['Assedio_Moral']:.1f} | Sexual: {medias['Assedio_Sexual']:.1f}\n"
                    minuta += "="*40 + "\n\nCONCLUSÃO:\n" + conclusao + "\n\nEng. Henrique - HMM"
                    
                    st.text_area("COPIE PARA O WORD:", minuta, height=400)
        else: st.warning("Sem dados.")
