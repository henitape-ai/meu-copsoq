import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações e Conexão
st.set_page_config(page_title="HMM Serviços - Diagnóstico Corporativo", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📊 Protocolo COPSOQ III - HMM Serviços")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Coleta de Dados", "🏢 Resultados Corporativos"])

# --- ABA 1: COLETA (COM GRAVAÇÃO DE 13 COLUNAS) ---
with tab1:
    st.subheader("📋 Entrada de Dados")
    c_id1, c_id2, c_id3 = st.columns([2,1,1])
    with c_id1: empresa = st.text_input("Empresa:", "Nome da Empresa")
    with c_id2: setor = st.text_input("Setor:")
    with c_id3: funcao = st.text_input("Função:")
    
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}
    with st.form("form_coleta_completa"):
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.radio("Ritmo intenso?", list(escala.keys()), index=2)
            p2 = st.radio("Desgaste emocional?", list(escala.keys()), index=2)
            p3 = st.radio("Influência nas decisões?", list(escala.keys()), index=2)
            p4 = st.radio("Aprende coisas novas?", list(escala.keys()), index=2)
        with col2:
            p5 = st.radio("Apoio da chefia?", list(escala.keys()), index=2)
            p6 = st.radio("Colaboração de colegas?", list(escala.keys()), index=2)
            p7 = st.radio("Sente-se estressado?", list(escala.keys()), index=2)
            p9 = st.radio("Medo de demissão?", list(escala.keys()), index=2)
        
        if st.form_submit_button("Gravar Avaliação e Diagnóstico"):
            # Cálculos dos Scores
            v_dem = (escala[p1] + escala[p2]) / 2
            v_con = (escala[p3] + escala[p4]) / 2
            v_sup = (escala[p5] + escala[p6]) / 2
            v_sau, v_ins = escala[p7], escala[p9]

            # Lógica de Diagnóstico para a Planilha
            classificacao = "Baixo Risco"
            parecer = "✅ Ambiente equilibrado."
            if v_dem > 60 and v_con < 40:
                classificacao = "ALTO RISCO"
                parecer = "🚩 ALERTA: Alta Demanda e Baixo Controle (Risco de Adoecimento)."
            elif v_dem > 60 or v_sau > 60:
                classificacao = "Risco Moderado"
                parecer = "⚠️ ATENÇÃO: Monitoramento recomendado devido a scores elevados."

            try:
                # MONTAGEM DA LINHA COM AS 13 COLUNAS (A ATÉ M)
                nova_linha = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                    "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                    "Saude": v_sau, "Inseguranca": v_ins, "Significado": 50,
                    "Classificacao_Risco": classificacao,
                    "Parecer_Tecnico": parecer,
                    "Link_Grafico": "" 
                }])
                
                df_b = conn.read(worksheet="Página1", ttl=0)
                # Garante que as colunas novas existam no DataFrame lido para não dar erro de merge
                df_final = pd.concat([df_b, nova_linha], ignore_index=True)
                conn.update(worksheet="Página1", data=df_final)
                
                st.success(f"✅ Diagnóstico de {funcao} gravado nas 13 colunas!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro na gravação: {e}")

# --- ABA 2: RESULTADOS (VISÃO CORPORATIVA) ---
with tab2:
    st.subheader("🔐 Painel de Análise")
    senha = st.text_input("Senha:", type="password", key="senha_perito")
    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                # Filtro Empresa
                lista_emp = sorted(df['Empresa'].unique())
                emp_sel = st.selectbox("Selecione a Empresa:", lista_emp)
                df_emp = df[df['Empresa'] == emp_sel]

                # Filtro Setor
                lista_set = sorted(df_emp['Setor'].unique())
                set_sel = st.selectbox("Selecione o Setor:", lista_set)
                df_set = df_emp[df_emp['Setor'] == set_sel]
                
                # Médias
                media_set = df_set[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca']].mean()
                
                st.markdown(f"### 📊 Diagnóstico Consolidado: {set_sel}")
                col_radar, col_dados = st.columns([2, 1])
                
                with col_radar:
                    radar_df = pd.DataFrame({'Eixo': media_set.index, 'Valor': media_set.values})
                    fig = px.line_polar(radar_df, r='Valor', theta='Eixo', line_close=True, range_r=[0,100])
                    fig.update_traces(fill='toself', line_color='red')
                    st.plotly_chart(fig)
                
                with col_dados:
                    st.write("**Médias do Setor:**")
                    st.dataframe(media_set)
                    st.write(f"**Amostra:** {len(df_set)} pessoas")
            else:
                st.warning("Planilha vazia.")
        except Exception as e:
            st.error(f"Erro: {e}")
