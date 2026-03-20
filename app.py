import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia - HMM Serviços
st.set_page_config(page_title="HMM Serviços - Perícia Avançada", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa estados de memória para persistência dos dados na tela
if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None
if 'dados_finais' not in st.session_state:
    st.session_state.dados_finais = None

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos Ocupacionais")
st.markdown("---")

# 2. Sidebar de Identificação do Periciado
with st.sidebar:
    st.header("📋 Identificação")
    empresa = st.text_input("Empresa Avaliada:", "Empresa Exemplo")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função/Cargo:")
    st.divider()
    st.info("HMM Serviços - Itapetininga/SP\nEngenharia e Perícias Judiciais")

# Escala Likert padrão COPSOQ (0-100)
escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário de Coleta Técnica
st.subheader(f"Avaliação de Campo: {funcao}")
with st.form("form_pericial_estavel"):
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 📈 Demandas (Psicológicas e Ritmo)")
        p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
        p2 = st.radio("As tarefas são emocionalmente desgastantes?", list(escala.keys()), index=2)
        
        st.markdown("#### 🛠️ Controle (Autonomia e Influência)")
        p3 = st.radio("Você tem influência sobre as decisões do seu trabalho?", list(escala.keys()), index=2)
        p4 = st.radio("O seu trabalho permite aprender coisas novas?", list(escala.keys()), index=2)

    with c2:
        st.markdown("#### 🤝 Suporte Social e Liderança")
        p5 = st.radio("Recebe apoio técnico/emocional da chefia?", list(escala.keys()), index=2)
        p6 = st.radio("Há um clima de colaboração entre os colegas?", list(escala.keys()), index=2)
        
        st.markdown("#### ⚠️ Saúde e Insegurança")
        p7 = st.radio("Sente-se tenso ou estressado ultimamente?", list(escala.keys()), index=2)
        p9 = st.radio("Tem receio de ser demitido em breve?", list(escala.keys()), index=2)

    submit = st.form_submit_button("Registrar e Enviar Avaliação")

# 4. Processamento de Dados e Gravação (Append)
if submit:
    # Cálculo das médias das dimensões
    v_dem = (escala[p1] + escala[p2]) / 2
    v_con = (escala[p3] + escala[p4]) / 2
    v_sup = (escala[p5] + escala[p6]) / 2
    v_sau = escala[p7]
    v_ins = escala[p9]
    v_sig = 50 # Valor fixo para manter estrutura da planilha
    
    # Armazena para o gráfico de radar
    st.session_state.df_radar = pd.DataFrame([
        {'Dimensão': 'Demanda', 'Score': v_dem},
        {'Dimensão': 'Controle', 'Score': v_con},
        {'Dimensão': 'Suporte', 'Score': v_sup},
        {'Dimensão': 'Saúde', 'Score': v_sau},
        {'Dimensão': 'Insegurança', 'Score': v_ins}
    ])
    st.session_state.dados_finais = {"dem": v_dem, "con": v_con, "sau": v_sau}

    try:
        # Prepara a linha exatamente conforme o cabeçalho de 10 colunas
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa,
            "Setor": setor,
            "Funcao": funcao,
            "Demanda": v_dem,
            "Controle": v_con,
            "Suporte": v_sup,
            "Saude": v_sau,
            "Inseguranca": v_ins,
            "Significado": v_sig
        }])
        
        # Lê a base existente na Página1
        df_base = conn.read(worksheet="Página1")
        
        # Concatena o novo registro (Append)
        df_final = pd.concat([df_base, nova_linha], ignore_index=True)
        
        # Atualiza a planilha (Sobrescreve a aba com a lista atualizada)
        conn.update(worksheet="Página1", data=df_final)
        
        st.success(f"✅ Sucesso! Avaliação de {funcao} registrada na Página1.")
        st.balloons()
        
    except Exception as e:
        st.error(f"Erro na gravação: {e}")
        st.info("Dica: Certifique-se de que a aba da planilha se chama exatamente 'Página1'.")

# 5. Área do Perito (Análise Técnica)
if st.session_state.df_radar is not None:
    st.markdown("---")
    with st.expander("🔐 Área de Análise (Uso Exclusivo do Perito)"):
        senha = st.text_input("Senha de Acesso:", type="password", key="sec_key_2026")
        
        if senha == "1234":
            st.subheader(f"📊 Laudo Técnico Individual: {funcao}")
            
            # Gráfico de Radar
            fig = px.line_polar(
                st.session_state.df_radar, 
                r='Score', 
                theta='Dimensão', 
                line_close=True, 
                range_r=[0,100]
            )
            fig.update_traces(fill='toself', line_color='red')
            st.plotly_chart(fig, use_container_width=True)
            
            # Parecer baseado no Modelo de Karasek
            df = st.session_state.dados_finais
            if df['dem'] > 75 and df['con'] < 40:
                st.error("🚩 **RISCO CRÍTICO:** Alta Demanda e Baixo Controle detectados. Risco elevado de adoecimento ocupacional.")
            elif df['sau'] > 75:
                st.warning("⚠️ **ALERTA:** Níveis de estresse e fadiga acima do limite de segurança.")
            else:
                st.info("✅ **ESTÁVEL:** Indicadores técnicos dentro da normalidade para esta amostra.")
        elif senha != "":
            st.error("Senha incorreta.")
