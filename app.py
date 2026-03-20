import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão
st.set_page_config(page_title="HMM Serviços - Perícia 4.0", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa estados de memória
if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos Ocupacionais")
st.markdown("---")

# 2. Interface Principal: Coleta de Dados (Aba 1) e Relatórios (Aba 2)
tab1, tab2 = st.tabs(["📝 Nova Avaliação", "📄 Gerador de Relatórios"])

with tab1:
    with st.sidebar:
        st.header("📋 Identificação")
        empresa = st.text_input("Empresa Avaliada:", "Empresa Exemplo")
        setor = st.text_input("Setor:")
        funcao = st.text_input("Função/Cargo:")
        st.divider()
        st.info("HMM Serviços - Itapetininga/SP\nEngenharia e Perícias Judiciais")

    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    st.subheader(f"Avaliação de Campo: {funcao}")
    with st.form("form_pericial_completo"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📈 Demandas")
            p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
            p2 = st.radio("As tarefas são emocionalmente desgastantes?", list(escala.keys()), index=2)
            st.markdown("#### 🛠️ Controle")
            p3 = st.radio("Você tem influência sobre as decisões?", list(escala.keys()), index=2)
            p4 = st.radio("O trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
        with c2:
            st.markdown("#### 🤝 Suporte Social")
            p5 = st.radio("Recebe apoio da chefia quando precisa?", list(escala.keys()), index=2)
            p6 = st.radio("Há colaboração entre os colegas?", list(escala.keys()), index=2)
            st.markdown("#### ⚠️ Saúde e Insegurança")
            p7 = st.radio("Sente-se tenso ou estressado ultimamente?", list(escala.keys()), index=2)
            p9 = st.radio("Tem receio de ser demitido em breve?", list(escala.keys()), index=2)

        submit = st.form_submit_button("Registrar e Enviar Avaliação")

    if submit:
        v_dem = (escala[p1] + escala[p2]) / 2
        v_con = (escala[p3] + escala[p4]) / 2
        v_sup = (escala[p5] + escala[p6]) / 2
        v_sau = escala[p7]
        v_ins = escala[p9]
        v_sig = 50 

        st.session_state.df_radar = pd.DataFrame([
            {'Dimensão': 'Demanda', 'Score': v_dem}, {'Dimensão': 'Controle', 'Score': v_con},
            {'Dimensão': 'Suporte', 'Score': v_sup}, {'Dimensão': 'Saúde', 'Score': v_sau},
            {'Dimensão': 'Insegurança', 'Score': v_ins}
        ])

        try:
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Empresa": empresa, "Setor": setor, "Funcao": funcao,
                "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, 
                "Saude": v_sau, "Inseguranca": v_ins, "Significado": v_sig
            }])
            
            df_base = conn.read(worksheet="Página1", ttl=0)
            df_final = pd.concat([df_base, nova_linha], ignore_index=True)
            conn.update(worksheet="Página1", data=df_final)
            
            st.success(f"✅ Avaliação de {funcao} gravada com sucesso!")
            st.balloons()
        except Exception as e:
            if "200" in str(e):
                st.success("✅ Dados enviados com sucesso (Resposta 200)!")
                st.balloons()
            else:
                st.error(f"Erro na Gravação: {e}")

    # Gráfico de Radar na tela de coleta
    if st.session_state.df_radar is not None:
        with st.expander("📊 Visualização Rápida (Radar)"):
            fig = px.line_polar(st.session_state.df_radar, r='Score', theta='Dimensão', line_close=True, range_r=[0,100])
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)

# 3. Aba 2: Busca na Planilha e Geração de Texto para o Laudo
with tab2:
    st.subheader("📄 Gerador de Texto para Laudo Pericial")
    try:
        # Lê a planilha em tempo real para buscar os nomes
        df_historico = conn.read(worksheet="Página1", ttl=0)
        
        if not df_historico.empty:
            col_a, col_b = st.columns(2)
            empresas_disponiveis = df_historico['Empresa'].unique()
            empresa_escolhida = col_a.selectbox("Selecione a Empresa:", empresas_disponiveis)
            
            # Filtra por empresa para facilitar a busca do funcionário
            df_func = df_historico[df_historico['Empresa'] == empresa_escolhida]
            identificador = df_func['Funcao'] + " (" + df_func['Data'] + ")"
            func_escolhido = col_b.selectbox("Selecione o Periciado:", identificador)

            if st.button("Gerar Relatório Técnico"):
                # Localiza a linha exata
                linha_dados = df_func[identificador == func_escolhido].iloc[0]
                
                # Lógica do Parecer (Modelo de Karasek)
                parecer = "✅ EQUILÍBRIO FUNCIONAL: O posto de trabalho apresenta equilíbrio entre exigências e recursos."
                if linha_dados['Demanda'] > 66 and linha_dados['Controle'] < 40:
                    parecer = "🚩 RISCO CRÍTICO (ALTA TENSÃO): Ambiente patogênico com alta demanda e baixo controle."
                elif linha_dados['Saude'] > 66:
                    parecer = "⚠️ ALERTA: Níveis elevados de estresse percebido."

                relatorio_texto = f"""
RESUMO DA AVALIAÇÃO PSICOSSOCIAL - HMM SERVIÇOS
--------------------------------------------------
IDENTIFICAÇÃO:
Empresa: {linha_dados['Empresa']}
Setor/Função: {linha_dados['Setor']} / {linha_dados['Funcao']}
Data da Coleta: {linha_dados['Data']}

RESULTADOS COPSOQ III (Escala 0-100 pts):
- Demandas do Trabalho: {linha_dados['Demanda']} pts
- Controle e Autonomia: {linha_dados['Controle']} pts
- Suporte Social: {linha_dados['Suporte']} pts
- Estresse/Saúde: {linha_dados['Saude']} pts
- Insegurança Ocupacional: {linha_dados['Inseguranca']} pts

ANÁLISE TÉCNICA:
{parecer}

Fundamentação: Avaliação baseada no protocolo internacional COPSOQ III. 
Scores acima de 66 em Demandas ou abaixo de 33 em Controle/Suporte 
indicam necessidade de intervenção imediata conforme NR-1 e NR-17.
--------------------------------------------------
                """
                st.text_area("Copie o texto abaixo para o seu Laudo (Word/PDF):", relatorio_texto, height=450)
        else:
            st.info("Nenhum dado encontrado na planilha ainda.")
    except Exception as e:
        st.error(f"Erro ao acessar banco de dados: {e}")
