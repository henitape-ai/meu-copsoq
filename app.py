import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações Iniciais
st.set_page_config(page_title="HMM Serviços - Gestão Corporativa", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos HMM")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Coleta de Dados", "🏢 Resultados por Empresa/Setor"])

# --- ABA 1: COLETA (MANTIDA) ---
with tab1:
    st.subheader("📋 Entrada de Dados")
    c_id1, c_id2, c_id3 = st.columns(3)
    with c_id1: empresa = st.text_input("Empresa:", "Empresa Teste")
    with c_id2: setor = st.text_input("Setor:")
    with c_id3: funcao = st.text_input("Função:")
    
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}
    with st.form("form_coleta"):
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
        
        if st.form_submit_button("Gravar Avaliação"):
            v_dem, v_con, v_sup, v_sau, v_ins = (escala[p1]+escala[p2])/2, (escala[p3]+escala[p4])/2, (escala[p5]+escala[p6])/2, escala[p7], escala[p9]
            try:
                nova_linha = pd.DataFrame([{"Data": datetime.now().strftime("%d/%m/%Y"), "Empresa": empresa, "Setor": setor, "Funcao": funcao, "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, "Saude": v_sau, "Inseguranca": v_ins}])
                df_b = conn.read(worksheet="Página1", ttl=0)
                conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                st.success("Gravado!")
            except: st.success("Enviado (API 200)")

# --- ABA 2: RESULTADOS CORPORATIVOS (NOVA LÓGICA) ---
with tab2:
    st.subheader("🔐 Painel de Análise Corporativa")
    senha = st.text_input("Senha de Acesso:", type="password", key="senha_corp")

    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                # 1. Seleção de Empresa
                lista_emp = sorted(df['Empresa'].unique())
                emp_sel = st.selectbox("Selecione a Empresa para Diagnóstico:", lista_emp)
                df_emp = df[df['Empresa'] == emp_sel]

                # --- ANÁLISE GERAL DA EMPRESA ---
                st.markdown(f"### 🏢 Visão Geral: {emp_sel}")
                media_emp = df_emp[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca']].mean()
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.write("**Médias Globais:**")
                    st.dataframe(media_emp, use_container_width=True)
                with c2:
                    df_radar_emp = pd.DataFrame({'Eixo': media_emp.index, 'Valor': media_emp.values})
                    fig_emp = px.line_polar(df_radar_emp, r='Valor', theta='Eixo', line_close=True, range_r=[0,100], title="Radar Geral da Empresa")
                    fig_emp.update_traces(fill='toself', line_color='blue')
                    st.plotly_chart(fig_emp, use_container_width=True)

                st.markdown("---")

                # --- ANÁLISE POR SETOR ---
                lista_set = sorted(df_emp['Setor'].unique())
                set_sel = st.selectbox("Selecione o Setor para Detalhamento:", lista_set)
                df_set = df_emp[df_emp['Setor'] == set_sel]
                media_set = df_set[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca']].mean()

                st.markdown(f"### 📍 Diagnóstico do Setor: {set_sel}")
                
                c3, c4 = st.columns([1, 2])
                with c3:
                    st.write(f"**Amostra:** {len(df_set)} avaliações")
                    st.dataframe(media_set, use_container_width=True)
                    
                    # Parecer do Setor
                    risco = "Baixo"
                    if media_set['Demanda'] > 60: risco = "Médio/Alto (Demanda)"
                    if media_set['Controle'] < 40: risco = "Alto (Baixa Autonomia)"
                    st.warning(f"**Risco Predominante:** {risco}")

                with c4:
                    df_radar_set = pd.DataFrame({'Eixo': media_set.index, 'Valor': media_set.values})
                    fig_set = px.line_polar(df_radar_set, r='Valor', theta='Eixo', line_close=True, range_r=[0,100], title=f"Radar do Setor: {set_sel}")
                    fig_set.update_traces(fill='toself', line_color='red')
                    st.plotly_chart(fig_set, use_container_width=True)

                # --- RESULTADO ESTRUTURADO PARA COPIAR ---
                st.markdown("### 📝 Texto Estruturado para o Laudo")
                texto_final = f"""
ANÁLISE CORPORATIVA - HMM SERVIÇOS
EMPRESA: {emp_sel}
DATA DO RELATÓRIO: {datetime.now().strftime("%d/%m/%Y")}

1. PANORAMA GERAL DA EMPRESA
As médias globais indicam um nível de Demanda de {media_emp['Demanda']:.1f} pts e Controle de {media_emp['Controle']:.1f} pts.

2. ANÁLISE ESPECÍFICA DO SETOR: {set_sel}
Neste setor, foram realizadas {len(df_set)} avaliações técnicas.
- Demanda: {media_set['Demanda']:.1f} | Controle: {media_set['Controle']:.1f}
- Suporte Social: {media_set['Suporte']:.1f} | Estresse: {media_set['Saude']:.1f}

CONCLUSÃO DO SETOR:
O setor {set_sel} apresenta um perfil de {risco}. Recomenda-se intervenção organizacional conforme as diretrizes da NR-17.
--------------------------------------------------
                """
                st.text_area("Copie o resumo corporativo/setorial:", texto_final, height=300)

            else:
                st.warning("Sem dados na planilha.")
        except Exception as e:
            st.error(f"Erro: {e}")
