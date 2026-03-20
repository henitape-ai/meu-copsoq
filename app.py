import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão HMM
st.set_page_config(page_title="HMM Serviços", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📊 Avaliação Psicossocial COPSOQ - HMM Serviços")
st.markdown("---")

# 2. Navegação por Abas (Mobile e Desktop)
tab1, tab2 = st.tabs(["📝 Coleta de Dados", "🔐 Painel de Análise"])

# --- ABA 1: COLETA DE DADOS EM CAMPO ---
with tab1:
    st.subheader("📋 Identificação da Avaliação")
    
    # Identificação visível no corpo principal
    c_id1, c_id2, c_id3 = st.columns([2, 1, 1])
    with c_id1: empresa = st.text_input("Empresa Avaliada:", "Nome da Empresa")
    with c_id2: setor = st.text_input("Setor:")
    with c_id3: funcao = st.text_input("Função/ Cargo:")
    
    st.markdown("---")
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_coleta_hmm_v10_1"):
        st.markdown("#### 📝 Questionário Técnico (COPSOQ III)")
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
                "Parecer_Tecnico": f"Avaliação técnica setorial em {setor}", 
                "Link_Grafico": ""
            }])
            df_b = conn.read(worksheet="Página1", ttl=0)
            conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
            st.success(f"✅ Avaliação de {funcao} registrada com sucesso!")
            st.balloons()
        except Exception as e:
            if "200" in str(e): st.success("✅ Diagnóstico enviado!")
            else: st.error(f"Erro na Gravação: {e}")

# --- ABA 2: PAINEL DE ANÁLISE E LAUDO ---
with tab2:
    st.subheader("🔐 Painel de Análise e Laudo Técnico")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_v10_1")

    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    lista_emp = sorted(df['Empresa'].unique())
                    emp_sel = st.selectbox("1. Selecione a Empresa:", lista_emp)
                    df_emp = df[df['Empresa'] == emp_sel]
                with c_f2:
                    lista_set = sorted(df_emp['Setor'].unique())
                    set_sel = st.selectbox("2. Selecione o Setor:", lista_set)
                    df_set = df_emp[df_emp['Setor'] == set_sel]

                m = df_set[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca']].mean()
                
                st.markdown(f"### 📊 Diagnóstico Consolidado: {set_sel}")
                col_radar, col_metrics = st.columns([2, 1])
                
                with col_radar:
                    radar_df = pd.DataFrame({'Eixo': m.index, 'Valor': m.values})
                    fig = px.line_polar(radar_df, r='Valor', theta='Eixo', line_close=True, range_r=[0,100])
                    fig.update_traces(fill='toself', line_color='red')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_metrics:
                    st.write("**Médias do Setor:**")
                    st.dataframe(m)
                    st.metric("Amostra (N)", len(df_set))

                status = "ESTÁVEL"
                explicacao = "Os índices estão em zona de equilíbrio organizacional."
                
                if m['Demanda'] > 60 and m['Controle'] < 40:
                    status = "CRÍTICO (Alta Tensão)"
                    explicacao = "Setor com Alta Demanda e Baixo Controle. Risco elevado de adoecimento (Karasek)."
                elif m['Demanda'] > 60:
                    status = "ALERTA (Sobrecarga)"
                    explicacao = "O ritmo e carga de trabalho exigem atenção."

                relatorio = f"""
RESUMO AVALIAÇÃO
--------------------------------------------------
EMPRESA: {emp_sel} | SETOR: {set_sel}
DATA: {datetime.now().strftime("%d/%m/%Y")}
DIAGNÓSTICO: {status}
--------------------------------------------------
FUNDAMENTAÇÃO TÉCNICA:

- Demandas ({m['Demanda']:.1f} pts): {"Carga de trabalho elevada." if m['Demanda'] > 60 else "Carga equilibrada."}
- Controle ({m['Controle']:.1f} pts): {"Baixa autonomia nas tarefas." if m['Controle'] < 40 else "Boa autonomia e domínio técnico."}
- Suporte ({m['Suporte']:.1f} pts): {"Apoio organizacional frágil." if m['Suporte'] < 40 else "Presença de suporte social protetivo."}

ANÁLISE: {explicacao}
--------------------------------------------------
"""
                st.markdown("---")
                st.subheader("📑 Texto para o Laudo")
                st.text_area("Selecione e copie para o Word:", relatorio, height=400)
                
            else:
                st.warning("Banco de dados vazio.")
        except Exception as e:
            st.error(f"Erro no processamento: {e}")
    elif senha != "":
        st.error("Senha incorreta.")
