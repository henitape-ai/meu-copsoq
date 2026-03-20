import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão
st.set_page_config(page_title="HMM Serviços - Diagnóstico 4.0", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_radar_preview' not in st.session_state:
    st.session_state.df_radar_preview = None

st.title("📊 Protocolo COPSOQ III - HMM Serviços")
st.markdown("---")

# 2. Interface em Abas
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
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📈 Demandas**")
            p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
            p2 = st.radio("Tarefas emocionalmente desgastantes?", list(escala.keys()), index=2)
            st.markdown("**🛠️ Controle**")
            p3 = st.radio("Tem influência sobre as decisões?", list(escala.keys()), index=2)
            p4 = st.radio("Trabalho permite aprender novas habilidades?", list(escala.keys()), index=2)
        with c2:
            st.markdown("**🤝 Suporte Social**")
            p5 = st.radio("Recebe apoio da chefia?", list(escala.keys()), index=2)
            p6 = st.radio("Colaboração entre colegas?", list(escala.keys()), index=2)
            st.markdown("**⚠️ Saúde e Insegurança**")
            p7 = st.radio("Sente-se tenso/estressado?", list(escala.keys()), index=2)
            p9 = st.radio("Medo de perder o emprego?", list(escala.keys()), index=2)
        submit = st.form_submit_button("Finalizar e Gravar Diagnóstico")

    if submit:
        v_dem = (escala[p1] + escala[p2]) / 2
        v_con = (escala[p3] + escala[p4]) / 2
        v_sup = (escala[p5] + escala[p6]) / 2
        v_sau = escala[p7]
        v_ins = escala[p9]
        
        # Lógica Karasek / NR-17
        classificacao = "Baixo Risco"
        parecer = "✅ Ambiente equilibrado."
        if v_dem > 66 and v_con < 40:
            classificacao = "ALTO RISCO"
            parecer = "🚩 CRÍTICO: Alta Demanda e Baixo Controle (High Strain)."
        elif v_dem > 66 or v_sau > 66:
            classificacao = "Risco Moderado"
            parecer = "⚠️ ATENÇÃO: Monitoramento recomendado."

        try:
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                "Saude": v_sau, "Inseguranca": v_ins, "Significado": 50,
                "Classificacao_Risco": classificacao, "Parecer_Tecnico": parecer, "Link_Grafico": ""
            }])
            df_base = conn.read(worksheet="Página1", ttl=0)
            df_final = pd.concat([df_base, nova_linha], ignore_index=True)
            conn.update(worksheet="Página1", data=df_final)
            st.success("✅ Diagnóstico gravado com sucesso!")
            st.balloons()
        except Exception as e:
            if "200" in str(e): st.success("✅ Diagnóstico enviado!")
            else: st.error(f"Erro: {e}")

# --- ABA 2: GERADOR DE LAUDOS (O QUE VOCÊ VIU NO PRINT) ---
with tab2:
    st.subheader("🔑 Acesso Restrito ao Perito")
    # A senha que você usou no print
    acesso = st.text_input("Digite a senha para desbloquear:", type="password", key="login_perito")

    if acesso == "HMM2024":
        try:
            df_h = conn.read(worksheet="Página1", ttl=0)
            if not df_h.empty:
                # 1. Filtro Empresa
                list_emp = sorted(df_h['Empresa'].unique())
                emp_sel = st.selectbox("1. Selecione a Empresa:", list_emp)
                
                # 2. Filtro Setor
                df_set = df_h[df_h['Empresa'] == emp_sel]
                list_set = sorted(df_set['Setor'].unique())
                set_sel = st.selectbox("2. Selecione o Setor:", list_set)
                
                # 3. Filtro Periciado
                df_per = df_set[df_set['Setor'] == set_sel]
                labels = df_per['Funcao'] + " (" + df_per['Data'] + ")"
                func_sel = st.selectbox("3. Selecione a Avaliação:", labels)

                if st.button("Gerar Texto e Gráfico do Laudo"):
                    d = df_per[labels == func_sel].iloc[0]
                    
                    # Gráfico Polar Individual
                    st.markdown(f"### 📊 Perfil Psicossocial: {d['Funcao']}")
                    radar_data = pd.DataFrame([
                        {'Eixo': 'Demanda', 'Valor': d['Demanda']}, {'Eixo': 'Controle', 'Valor': d['Controle']},
                        {'Eixo': 'Suporte', 'Valor': d['Suporte']}, {'Eixo': 'Saúde', 'Valor': d['Saude']},
                        {'Eixo': 'Insegurança', 'Valor': d['Inseguranca']}
                    ])
                    fig = px.line_polar(radar_data, r='Valor', theta='Eixo', line_close=True, range_r=[0,100])
                    fig.update_traces(fill='toself', line_color='red')
                    st.plotly_chart(fig)

                    # Texto para Cópia
                    relatorio = f"""
RELATÓRIO TÉCNICO - HMM SERVIÇOS
--------------------------------------------------
EMPRESA: {d['Empresa']} | SETOR: {d['Setor']}
CARGO: {d['Funcao']} | DATA: {d['Data']}
--------------------------------------------------
RESULTADOS (COPSOQ III):
- Demanda: {d['Demanda']} pts
- Controle: {d['Controle']} pts
- Suporte: {d['Suporte']} pts
- Estresse: {d['Saude']} pts
- Classificação: {d['Classificacao_Risco']}

PARECER: {d['Parecer_Tecnico']}
--------------------------------------------------
                    """
                    st.text_area("Copie o texto para o seu laudo oficial:", relatorio, height=350)
            else:
                st.warning("Planilha vazia.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
    elif acesso != "":
        st.error("Senha incorreta.")
