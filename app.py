import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações Iniciais - HMM Serviços
st.set_page_config(page_title="HMM Serviços - Perícia 3.0", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa memória para evitar que o gráfico suma
if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos")
st.markdown("---")

# 2. Sidebar de Identificação
with st.sidebar:
    st.header("📋 Identificação")
    empresa = st.text_input("Empresa:", "Empresa Teste")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função:")
    st.divider()
    st.info("HMM Serviços - Itapetininga/SP")

escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário de Coleta
with st.form("form_final_perito"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Demandas")
        p1 = st.radio("Ritmo intenso?", list(escala.keys()), index=2)
        p2 = st.radio("Desgaste emocional?", list(escala.keys()), index=2)
        st.markdown("#### 🛠️ Controle")
        p3 = st.radio("Influência nas decisões?", list(escala.keys()), index=2)
        p4 = st.radio("Aprende coisas novas?", list(escala.keys()), index=2)
    with c2:
        st.markdown("#### 🤝 Suporte")
        p5 = st.radio("Apoio da chefia?", list(escala.keys()), index=2)
        p6 = st.radio("Colaboração de colegas?", list(escala.keys()), index=2)
        st.markdown("#### ⚠️ Saúde e Insegurança")
        p7 = st.radio("Sente-se estressado?", list(escala.keys()), index=2)
        p9 = st.radio("Medo de demissão?", list(escala.keys()), index=2)
    submit = st.form_submit_button("Registrar e Empilhar Dados")

# 4. Lógica de Gravação (Append Limpo)
if submit:
    # Cálculo das Dimensões
    v_dem = (escala[p1] + escala[p2]) / 2
    v_con = (escala[p3] + escala[p4]) / 2
    v_sup = (escala[p5] + escala[p6]) / 2
    v_sau = escala[p7]
    v_ins = escala[p9]
    v_sig = 50 
    
    st.session_state.df_radar = pd.DataFrame([
        {'Dimensão': 'Demanda', 'Score': v_dem},
        {'Dimensão': 'Controle', 'Score': v_con},
        {'Dimensão': 'Suporte', 'Score': v_sup},
        {'Dimensão': 'Saúde', 'Score': v_sau},
        {'Dimensão': 'Insegurança', 'Score': v_ins}
    ])

    try:
        # Ordem idêntica às 10 colunas da nova planilha
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor, "Funcao": funcao,
            "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
            "Saude": v_sau, "Inseguranca": v_ins, "Significado": v_sig
        }])
        
        # Lê a Página1 (que agora estará limpa)
        df_base = conn.read(worksheet="Página1")
        # Anexa o novo dado
        df_final = pd.concat([df_base, nova_linha], ignore_index=True)
        # Atualiza a planilha
        conn.update(worksheet="Página1", data=df_final)
        
        st.success("✅ Nova planilha iniciada e registro gravado com sucesso!")
        st.balloons()
    except Exception as e:
        st.error(f"Erro: {e}. Verifique o link nos Secrets e o nome da aba 'Página1'.")

# 5. Área do Perito
if st.session_state.df_radar is not None:
    st.markdown("---")
    with st.expander("🔐 Área de Análise (Uso do Perito)"):
        senha = st.text_input("Senha:", type="password")
        if senha == "1234":
            st.subheader(f"📊 Análise: {funcao} - {empresa}")
            fig = px.line_polar(st.session_state.df_radar, r='Score', theta='Dimensão', 
                               line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)
