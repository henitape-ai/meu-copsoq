import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão
st.set_page_config(page_title="HMM Serviços - Perícia Mobile", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

if 'df_radar' not in st.session_state:
    st.session_state.df_radar = None

st.title("📊 Protocolo COPSOQ III - HMM Serviços")
st.markdown("---")

# 2. Interface Principal em Abas
tab1, tab2 = st.tabs(["📝 Nova Avaliação", "🔐 Gerador de Relatórios"])

# --- ABA 1: COLETA DE DADOS (VISÍVEL NO CELULAR) ---
with tab1:
    st.subheader("📋 Identificação da Perícia")
    
    # Campos agora no corpo principal para facilitar no celular
    col_id1, col_id2, col_id3 = st.columns([2, 1, 1])
    with col_id1:
        empresa = st.text_input("Empresa Avaliada:", "Nome da Empresa")
    with col_id2:
        setor = st.text_input("Setor:")
    with col_id3:
        funcao = st.text_input("Função/Cargo:")
    
    st.markdown("---")
    
    escala = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_coleta_mobile"):
        st.markdown("#### 📝 Questionário Técnico")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**📈 Demandas**")
            p1 = st.radio("O ritmo de trabalho é intenso?", list(escala.keys()), index=2)
            p2 = st.radio("Tarefas emocionalmente desgastantes?", list(escala.keys()), index=2)
            st.markdown("**🛠️ Controle**")
            p3 = st.radio("Tem influência sobre as decisões?", list(escala.keys()), index=2)
            p4 = st.radio("Trabalho permite aprender coisas novas?", list(escala.keys()), index=2)
        with c2:
            st.markdown("**🤝 Suporte Social**")
            p5 = st.radio("Recebe apoio da chefia?", list(escala.keys()), index=2)
            p6 = st.radio("Colaboração entre colegas?", list(escala.keys()), index=2)
            st.markdown("**⚠️ Saúde e Insegurança**")
            p7 = st.radio("Sente-se tenso/estressado?", list(escala.keys()), index=2)
            p9 = st.radio("Medo de perder o emprego?", list(escala.keys()), index=2)
        
        submit = st.form_submit_button("Finalizar e Gravar na Planilha")

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
            st.success("✅ Avaliação registrada com sucesso!")
            st.balloons()
        except Exception as e:
            if "200" in str(e): st.success("✅ Enviado com sucesso!")
            else: st.error(f"Erro: {e}")

# --- ABA 2: GERADOR COM SENHA (MANTIDO) ---
with tab2:
    st.subheader("🔑 Acesso Restrito ao Perito")
    senha = st.text_input("Digite a senha para acessar o relatório:", type="password")

    if senha == "HMM2024":
        try:
            df_h = conn.read(worksheet="Página1", ttl=0)
            if not df_h.empty:
                st.info("Filtre os dados para gerar o laudo.")
                
                list_emp = sorted(df_h['Empresa'].unique())
                emp_sel = st.selectbox("1. Selecione a Empresa:", list_emp)
                
                df_setores = df_h[df_h['Empresa'] == emp_sel]
                list_set = sorted(df_setores['Setor'].unique())
                set_sel = st.selectbox("2. Selecione o Setor:", list_set)
                
                df_final_sel = df_setores[df_setores['Setor'] == set_sel]
                id_label = df_final_sel['Funcao'] + " (Data: " + df_final_sel['Data'] + ")"
                func_sel = st.selectbox("3. Selecione a Avaliação:", id_label)

                if st.button("Gerar Relatório Estruturado"):
                    d = df_final_sel[id_label == func_sel].iloc[0]
                    status = "EQUILÍBRIO"
                    if d['Demanda'] > 60 and d['Controle'] < 40: status = "ALTA TENSÃO (RISCO)"
                    
                    texto = f"RELATÓRIO HMM SERVIÇOS\nEMPRESA: {d['Empresa']}\nSETOR: {d['Setor']}\nFUNÇÃO: {d['Funcao']}\nDATA: {d['Data']}\n\nRESULTADOS:\nDemanda: {d['Demanda']}\nControle: {d['Controle']}\nSuporte: {d['Suporte']}\nSaúde: {d['Saude']}\nInsegurança: {d['Inseguranca']}\n\nPARECER: {status}"
                    st.text_area("Copie o texto:", texto, height=300)
            else:
                st.warning("Planilha vazia.")
        except Exception as e:
            st.error(f"Erro: {e}")
