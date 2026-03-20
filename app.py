import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão
st.set_page_config(page_title="HMM Serviços - Perícia 5.0", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - Gestão de Riscos Ocupacionais")
st.markdown("---")

# 2. Interface Principal
tab1, tab2 = st.tabs(["📝 Nova Avaliação", "🔐 Gerador de Relatórios (Restrito)"])

# --- ABA 1: COLETA DE DADOS ---
with tab1:
    with st.sidebar:
        st.header("📋 Identificação de Campo")
        empresa = st.text_input("Empresa Avaliada:", "Nome da Empresa")
        setor = st.text_input("Setor:")
        funcao = st.text_input("Função/Cargo:")
        st.divider()
        st.info("HMM Serviços - Itapetininga/SP")

    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_coleta"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 📈 Demandas")
            p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
            p2 = st.radio("Tarefas emocionalmente desgastantes?", list(escala.keys()), index=2)
            st.markdown("#### 🛠️ Controle")
            p3 = st.radio("Tem influência sobre as decisões?", list(escala.keys()), index=2)
            p4 = st.radio("Trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
        with c2:
            st.markdown("#### 🤝 Suporte Social")
            p5 = st.radio("Recebe apoio da chefia?", list(escala.keys()), index=2)
            p6 = st.radio("Colaboração entre colegas?", list(escala.keys()), index=2)
            st.markdown("#### ⚠️ Saúde e Insegurança")
            p7 = st.radio("Sente-se tenso/estressado?", list(escala.keys()), index=2)
            p9 = st.radio("Medo de perder o emprego?", list(escala.keys()), index=2)
        
        submit = st.form_submit_button("Registrar na Planilha")

    if submit:
        v_dem = (escala[p1] + escala[p2]) / 2
        v_con = (escala[p3] + escala[p4]) / 2
        v_sup = (escala[p5] + escala[p6]) / 2
        v_sau = escala[p7]
        v_ins = escala[p9]
        v_sig = 50 

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
            st.success("✅ Gravado com sucesso!")
            st.balloons()
        except Exception as e:
            if "200" in str(e): st.success("✅ Enviado!")
            else: st.error(f"Erro: {e}")

# --- ABA 2: GERADOR COM SENHA E HIERARQUIA ---
with tab2:
    st.subheader("🔑 Acesso Restrito ao Perito")
    senha = st.text_input("Digite a senha para acessar o banco de dados:", type="password")

    if senha == "HMM2024": # Altere sua senha aqui
        try:
            df_h = conn.read(worksheet="Página1", ttl=0)
            
            if not df_h.empty:
                st.info("Filtre os dados abaixo para gerar o relatório específico.")
                
                # Nível 1: Empresa
                list_emp = sorted(df_h['Empresa'].unique())
                emp_sel = st.selectbox("1. Selecione a Empresa:", list_emp)
                
                # Nível 2: Setor (Filtrado pela Empresa)
                df_setores = df_h[df_h['Empresa'] == emp_sel]
                list_set = sorted(df_setores['Setor'].unique())
                set_sel = st.selectbox("2. Selecione o Setor:", list_set)
                
                # Nível 3: Funcionário/Data (Filtrado pelo Setor)
                df_final_sel = df_setores[df_setores['Setor'] == set_sel]
                id_label = df_final_sel['Funcao'] + " (Data: " + df_final_sel['Data'] + ")"
                func_sel = st.selectbox("3. Selecione a Avaliação:", id_label)

                if st.button("Gerar Relatório Estruturado"):
                    # Puxa os dados da linha escolhida
                    d = df_final_sel[id_label == func_sel].iloc[0]
                    
                    # Lógica de Classificação Karasek
                    status = "EQUILÍBRIO"
                    if d['Demanda'] > 60 and d['Controle'] < 40: status = "ALTA TENSÃO (RISCO)"
                    
                    texto = f"""
RELATÓRIO DE AVALIAÇÃO PSICOSSOCIAL - HMM SERVIÇOS
---------------------------------------------------------
EMPRESA: {d['Empresa']}
SETOR ANALISADO: {d['Setor']}
FUNÇÃO/CARGO: {d['Funcao']}
DATA: {d['Data']}
---------------------------------------------------------
RESULTADOS QUANTITATIVOS (COPSOQ III):
- Demanda Psicológica: {d['Demanda']} pts
- Controle/Autonomia: {d['Controle']} pts
- Suporte Social: {d['Suporte']} pts
- Estresse Percebido: {d['Saude']} pts
- Insegurança Ocupacional: {d['Inseguranca']} pts

PARECER TÉCNICO PRELIMINAR:
Status: {status}

O presente documento resume os fatores psicossociais do 
trabalhador no setor {d['Setor']}. Recomenda-se análise da 
NR-17 caso os níveis de demanda superem 60 pontos.
---------------------------------------------------------
                    """
                    st.text_area("Texto pronto para cópia:", texto, height=400)
                    
                    # Radar individual no relatório
                    st.markdown("### Gráfico Polar do Setor")
                    df_radar = pd.DataFrame([
                        {'D': 'Demanda', 'S': d['Demanda']}, {'D': 'Controle', 'S': d['Controle']},
                        {'D': 'Suporte', 'S': d['Suporte']}, {'D': 'Saúde', 'S': d['Saude']},
                        {'D': 'Insegurança', 'S': d['Inseguranca']}
                    ])
                    fig = px.line_polar(df_radar, r='S', theta='D', line_close=True, range_r=[0,100])
                    st.plotly_chart(fig)
            else:
                st.warning("Nenhum dado encontrado na planilha.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
    elif senha != "":
        st.error("Senha incorreta. Acesso negado.")
