import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Página e Estilo
st.set_page_config(page_title="Expert COPSOQ III - HMM Serviços", layout="wide")

# Inicializa a conexão com o Google Sheets via Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa a memória do gráfico para não sumir ao digitar a senha
if 'df_grafico' not in st.session_state:
    st.session_state.df_grafico = None

st.title("📊 Avaliação Psicossocial Avançada - COPSOQ III")
st.markdown("---")

# 2. Identificação Técnica (Barra Lateral)
with st.sidebar:
    st.header("📋 Dados da Perícia")
    empresa = st.text_input("Empresa Avaliada:", "Empresa Exemplo")
    setor = st.text_input("Setor:")
    funcao = st.text_input("Função/Cargo do Periciado:")
    st.divider()
    st.info("HMM Serviços - Engenharia de Segurança e Perícias Judiciais")

# Escala Likert de 0 a 100
escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

st.subheader(f"Questionário de Campo - Função: {funcao}")

# 3. Formulário de Coleta (Questões Ampliadas)
with st.form("form_copsoq_completo"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 1. Exigências e Ritmo")
        p1 = st.radio("Você precisa trabalhar muito rápido?", list(escala.keys()), index=2)
        p2 = st.radio("O trabalho é distribuído de forma desigual?", list(escala.keys()), index=2)
        
        st.markdown("#### 2. Autonomia e Influência")
        p3 = st.radio("Você tem influência sobre as decisões do seu trabalho?", list(escala.keys()), index=2)
        p4 = st.radio("O seu trabalho permite aprender coisas novas?", list(escala.keys()), index=2)

        st.markdown("#### 3. Insegurança e Significado")
        p9 = st.radio("Você tem receio de ser demitido em breve?", list(escala.keys()), index=2)
        p10 = st.radio("Você sente que o seu trabalho é importante?", list(escala.keys()), index=2)

    with col2:
        st.markdown("#### 4. Liderança e Apoio Social")
        p5 = st.radio("O seu superior imediato planeja bem o trabalho?", list(escala.keys()), index=2)
        p6 = st.radio("Você recebe ajuda e apoio de seus colegas?", list(escala.keys()), index=2)
        
        st.markdown("#### 5. Saúde e Estresse")
        p7 = st.radio("Sente-se tenso ou estressado ultimamente?", list(escala.keys()), index=2)
        p8 = st.radio("O trabalho afeta sua vida familiar/pessoal?", list(escala.keys()), index=2)

    submit = st.form_submit_button("Finalizar e Gravar Dados")

# 4. Processamento, Cálculo e Gravação no Banco de Dados
if submit:
    # Cálculo das Dimensões Técnicas
    dados = {
        'Exigências': (escala[p1] + escala[p2]) / 2,
        'Autonomia': (escala[p3] + escala[p4]) / 2,
        'Liderança': (escala[p5] + escala[p6]) / 2,
        'Saúde': (escala[p7] + escala[p8]) / 2,
        'Insegurança': escala[p9],
        'Significado': escala[p10]
    }
    
    # Salva na sessão para visualização posterior do perito
    st.session_state.df_grafico = pd.DataFrame(list(dados.items()), columns=['Dimensão', 'Pontuação'])
    st.session_state.dados_pericia = dados

    try:
        # Prepara a linha de dados
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa,
            "Setor": setor,
            "Funcao": funcao,
            "Exigencias": dados['Exigências'],
            "Autonomia": dados['Autonomia'],
            "Liderança": dados['Liderança'],
            "Saude": dados['Saúde'],
            "Inseguranca": dados['Insegurança'],
            "Significado": dados['Significado']
        }])
        
        # O comando 'create' adiciona uma nova linha na planilha existente
        conn.create(data=nova_linha)
        
        st.success(f"✅ Avaliação de {funcao} registrada com sucesso na base de dados!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Erro ao gravar no Google Drive: {e}")

st.markdown("---")

# 5. ÁREA RESTRITA DO PERITO (Desbloqueio com Senha)
if st.session_state.df_grafico is not None:
    with st.expander("🔐 Visualizar Análise Técnica (Uso Exclusivo do Perito)"):
        senha = st.text_input("Senha de Acesso:", type="password", key="auth_perito")
        
        if senha == "1234":
            st.subheader(f"📊 Laudo Técnico: {funcao} - {empresa}")
            
            # Gráfico de Radar Profissional
            fig = px.line_polar(
                st.session_state.df_grafico, 
                r='Pontuação', 
                theta='Dimensão', 
                line_close=True, 
                range_r=[0,100]
            )
            fig.update_traces(fill='toself', line_color='blue', markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Parecer Técnico Automático baseado no Modelo de Karasek
            d = st.session_state.dados_pericia
            st.markdown("### 📝 Conclusão Preliminar")
            
            if d['Exigências'] > 75 and d['Autonomia'] < 40:
                st.error("🚩 **RISCO CRÍTICO:** Alta demanda combinada com baixa autonomia. Risco elevado de doenças ocupacionais psicossociais.")
            elif d['Saúde'] > 70:
                st.warning("⚠️ **ALERTA:** Níveis de estresse e impacto na saúde acima da média de segurança.")
            else:
                st.info("✅ **ESTÁVEL:** Indicadores técnicos dentro dos parâmetros de normalidade para a amostra.")
                
        elif senha != "":
            st.error("Senha incorreta. Acesso negado.")
