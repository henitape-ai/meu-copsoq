import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES HMM SERVIÇOS
st.set_page_config(page_title="HMM Serviços - Gestão Psicossocial", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("Programa de Avaliação de Riscos Psicossociais (COPSOQ III)")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.caption("🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Coleta de Dados (Ficha)", "📊 Painel de Análise e Relatórios"])

# --- ABA 1: COLETA ---
with tab1:
    st.subheader("📋 Identificação da Unidade")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: emp = st.text_input("Empresa:", placeholder="Nome do Cliente")
    with c2: setr = st.text_input("Setor:", placeholder="Ex: Produção")
    with c3: func = st.text_input("Função:", placeholder="Ex: Operador")
    
    esc = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_v22_6"):
        st.markdown("#### QUESTIONÁRIO DE DIAGNÓSTICO ORGANIZACIONAL")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 1. EXIGÊNCIAS (DEMANDAS)")
            p1_1 = st.radio("1.1 Trabalha muito rápido?", list(esc.keys()), index=None)
            p1_2 = st.radio("1.2 Trabalho emocionalmente desgastante?", list(esc.keys()), index=None)
            p1_3 = st.radio("1.3 Volume excessivo?", list(esc.keys()), index=None)
            p1_4 = st.radio("1.4 Prazos apertados?", list(esc.keys()), index=None)
            p1_5 = st.radio("1.5 Esforço intenso?", list(esc.keys()), index=None)
            st.markdown("### 2. INFLUÊNCIA (CONTROLE)")
            p2_1 = st.radio("2.1 Influência nas decisões?", list(esc.keys()), index=None)
            p2_2 = st.radio("2.2 Aprende coisas novas?", list(esc.keys()), index=None)
        with col2:
            st.markdown("### 3. SUPORTE SOCIAL")
            p3_1 = st.radio("3.1 Superior apoia?", list(esc.keys()), index=None)
            p3_2 = st.radio("3.2 Cooperação entre colegas?", list(esc.keys()), index=None)
            st.markdown("### 4. BEM-ESTAR")
            p4_1 = st.radio("4.1 Sente-se estressado?", list(esc.keys()), index=None)
            p4_2 = st.radio("4.2 Preocupado com estabilidade?", list(esc.keys()), index=None)
            st.markdown("### 5. AMBIENTE ÉTICO")
            p5_1 = st.radio("5.1 Humilhação ou assédio moral?", list(esc.keys()), index=None)
            p5_2 = st.radio("5.2 Assédio sexual?", list(esc.keys()), index=None)
        
        if st.form_submit_button("GRAVAR RESPOSTAS"):
            resp = [p1_1, p1_2, p1_3, p1_4, p1_5, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2]
            if None in resp or not emp or not setr:
                st.error("⚠️ Responda todas as questões.")
            else:
                try:
                    v_dem = (esc[p1_1]+esc[p1_2]+esc[p1_3]+esc[p1_4]+esc[p1_5])/5
                    v_con = (esc[p2_1]+esc[p2_2])/2
                    v_sup = (esc[p3_1]+esc[p3_2])/2
                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": emp.strip(), "Setor": setr.strip(), "Funcao": func.strip(),
                        "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup,
                        "Saude": esc[p4_1], "Inseguranca": esc[p4_2],
                        "Assedio_Moral": esc[p5_1], "Assedio_Sexual": esc[p5_2],
                        "Status": "Finalizado", "Metodo": "COPSOQ III"
                    }])
                    df_b = conn.read(worksheet="Página1", ttl=0)
                    df_f = pd.concat([df_b, nova_linha], ignore_index=True)
                    conn.update(worksheet="Página1", data=df_f)
                    st.success("✅ DADOS ENVIADOS!")
                    st.balloons()
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: ANÁLISE ---
with tab2:
    st.subheader("🔐 Painel de Gestão HMM")
    senha = st.text_input("Senha:", type="password", key="login_v22_6")
    if senha == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            df['Empresa'] = df['Empresa'].str.strip()
            df['Setor'] = df['Setor'].str.strip()
            emp_sel = st.selectbox("Escolha a Empresa:", sorted(df['Empresa'].unique()), index=None)
            if emp_sel:
                setores = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                set_sel = st.multiselect("Filtrar por Setor:", setores)
                df_f = df[df['Empresa'] == emp_sel]
                if set_sel:
                    df_f = df_f[df_f['Setor'].isin(set_sel)]
                
                cols = ['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca', 'Assedio_Moral', 'Assedio_Sexual']
                m = df_f[cols].mean()
                
                fig = px.line_polar(r=m.values, theta=m.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', line_color='red')
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(m.to_frame(name="Média").T.style.format("{:.1f}"))

                st.markdown("---")
                concl = st.text_area("✍️ Conclusão Técnica:", value="Diagnóstico: [ALTA TENSÃO].", height=150)
                
                if st.button("🚀 GERAR RELATÓRIO PARA O WORD"):
                    nome_s = ", ".join(set_sel) if set_sel else "GERAL"
                    txt = f"RELATÓRIO TÉCNICO - {emp_sel.upper()}\n"
                    txt += f"SETOR ANALISADO: {nome_s}\n"
                    txt += f"Amostra: {len(df_f)} avaliados.\n"
                    txt += f"Demanda: {m['Demanda']:.1f} | Controle: {m['Controle']:.1f}\n"
                    txt += f"Suporte: {m['Suporte']:.1f} | Saúde: {m['Saude']:.1f}\n"
                    txt += f"Insegurança: {m['Inseguranca']:.1f}\n"
                    txt += f"Assédio M/S: {m['Assedio_Moral']:.1f} / {m['Assedio_Sexual']:.1f}\n"
                    txt += f"CONCLUSÃO:\n{concl}\n\nEng. Henrique - HMM"
                    st.text_area("📋 COPIE:", txt, height=400)
        else: st.warning("Sem dados.")
