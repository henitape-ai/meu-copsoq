import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Página
st.set_page_config(page_title="Expert COPSOQ III - Pericia", layout="wide")

# Inicializa a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Inicializa o estado da sessão para o gráfico não sumir
if 'df_grafico' not in st.session_state:
    st.session_state.df_grafico = None

st.title("📊 Sistema de Avaliação Psicossocial - COPSOQ III")
st.markdown("---")

# Barra Lateral
with st.sidebar:
    st.header("📋 Identificação")
    empresa = st.text_input("Empresa:", "Minha Empresa")
    setor = st.selectbox("Setor:", ["Produção", "Logística", "Administrativo", "Operacional", "Vendas"])
    st.divider()

escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

# 3. Formulário
with st.form("form_copsoq"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. Exigências")
        p1 = st.radio("Trabalha muito rápido?", list(escala.keys()), index=2)
        p2 = st.radio("Trabalho desigual?", list(escala.keys()), index=2)
        st.markdown("#### 2. Autonomia")
        p3 = st.radio("Influência nas decisões?", list(escala.keys()), index=2)
        p4 = st.radio("Aprende coisas novas?", list(escala.keys()), index=2)
    with col2:
        st.markdown("#### 3. Liderança")
        p5 = st.radio("Superior planeja bem?", list(escala.keys()), index=2)
        p6 = st.radio("Apoio dos colegas?", list(escala.keys()), index=2)
        st.markdown("#### 4. Saúde")
        p7 = st.radio("Sente-se tenso/estressado?", list(escala.keys()), index=2)
        p8 = st.radio("Afeta vida pessoal?", list(escala.keys()), index=2)
    
    submit = st.form_submit_button("Finalizar Avaliação")

# 4. Processamento
if submit:
    dados = {
        'Exigências': (escala[p1] + escala[p2]) / 2,
        'Autonomia': (escala[p3] + escala[p4]) / 2,
        'Liderança': (escala[p5] + escala[p6]) / 2,
        'Saúde': (escala[p7] + escala[p8]) / 2
    }
    # Guarda o resultado na sessão
    st.session_state.df_grafico = pd.DataFrame(list(dados.items()), columns=['Dimensão', 'Pontuação'])
    st.session_state.dados_finais = dados

    try:
        nova_linha = pd.DataFrame([{
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Empresa": empresa, "Setor": setor,
            "Exigencias": dados['Exigências'], "Autonomia": dados['Autonomia'],
            "Liderança": dados['Liderança'], "Saude": dados['Saúde']
        }])
        conn.create(data=nova_linha)
        st.success("✅ Enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro na gravação: {e}")

# 5. ÁREA DO PERITO (Sempre visível após o primeiro envio)
if st.session_state.df_grafico is not None:
    st.markdown("---")
    with st.expander("🔐 Área do Perito (Acesso Restrito)"):
        senha = st.text_input("Digite a senha:", type="password", key="key_perito")
        
        if senha == "1234":
            st.subheader(f"📊 Análise Técnica - {empresa}")
            
            # Gera o gráfico de radar
            fig = px.line_polar(
                st.session_state.df_grafico, 
                r='Pontuação', 
                theta='Dimensão', 
                line_close=True, 
                range_r=[0,100]
            )
            fig.update_traces(fill='toself', line_color='blue')
            st.plotly_chart(fig, use_container_width=True)
            
            d = st.session_state.dados_finais
            resumo = "🚩 ALTO RISCO" if d['Saúde'] > 70 or d['Exigências'] > 70 else "✅ NORMAL"
            st.info(f"**Parecer:** {resumo} | Saúde: {d['Saúde']} | Exigências: {d['Exigências']}")
        elif senha != "":
            st.error("Senha incorreta.")
