import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES HMM SERVIÇOS
st.set_page_config(page_title="HMM Serviços - Gestão Psicossocial", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO PROFISSIONAL ---
st.title("🚀 Programa de Avaliação de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia de Segurança e Gestão Ocupacional")
st.markdown("""
**Responsável Técnico:** Eng. Henrique  
🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br) | 📍 Itapetininga/SP
""")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Coleta de Dados (Ficha)", "📊 Painel de Análise e Relatórios"])

# --- ABA 1: COLETA ---
with tab1:
    st.subheader("📋 Identificação da Unidade Avaliada")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: emp = st.text_input("Empresa Cliente:", placeholder="Ex: SENAC ou Mercado do Zé")
    with c2: setr = st.text_input("Setor:", placeholder="Ex: Administração")
    with c3: func = st.text_input("Função:", placeholder="Ex: Analista")
    
    esc = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_v22_7"):
        st.markdown("#### DIAGNÓSTICO DE FATORES PSICOSSOCIAIS")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 1. EXIGÊNCIAS (DEMANDAS)")
            p1_1 = st.radio("1.1 Você tem que trabalhar muito rápido?", list(esc.keys()), index=None)
            p1_2 = st.radio("1.2 O seu trabalho é emocionalmente desgastante?", list(esc.keys()), index=None)
            p1_3 = st.radio("1.3 O volume de trabalho é excessivo para o tempo disponível?", list(esc.keys()), index=None)
            p1_4 = st.radio("1.4 Você precisa lidar com prazos muito apertados?", list(esc.keys()), index=None)
            p1_5 = st.radio("1.5 O seu trabalho exige um esforço físico ou mental intenso?", list(esc.keys()), index=None)
            
            st.markdown("### 2. INFLUÊNCIA E DESENVOLVIMENTO (CONTROLE)")
            p2_1 = st.radio("2.1 Você tem influência sobre as decisões no seu trabalho?", list(esc.keys()), index=None)
            p2_2 = st.radio("2.2 O trabalho permite que você aprenda novas habilidades?", list(esc.keys()), index=None)
            
        with col2:
            st.markdown("### 3. RELAÇÕES E SUPORTE SOCIAL")
            p3_1 = st.radio("3.1 O seu superior imediato apoia você quando precisa?", list(esc.keys()), index=None)
            p3_2 = st.radio("3.2 Há um bom espírito de cooperação entre os colegas?", list(esc.keys()), index=None)
            
            st.markdown("### 4. SAÚDE E BEM-ESTAR")
            p4_1 = st.radio("4.1 Você tem se sentido tenso ou estressado ultimamente?", list(esc.keys()), index=None)
            p4_2 = st.radio("4.2 Você tem receio quanto à estabilidade no seu emprego?", list(esc.keys()), index=None)
            
            st.markdown("### 5. AMBIENTE ÉTICO (COMPLIANCE)")
            p5_1 = st.radio("5.1 No último ano, foi exposto a situações de humilhação ou insultos?", list(esc.keys()), index=None)
            p5_2 = st.radio("5.2 Foi alvo de comentários ou avanços sexuais indesejados?", list(esc.keys()), index=None)
        
        if st.form_submit_button("✅ SALVAR AVALIAÇÃO"):
            resp = [p1_1, p1_2, p1_3, p1_4, p1_5, p2_1, p2_2, p3_1, p3_2, p4_1, p4_2, p5_1, p5_2]
            if None in resp or not emp or not setr:
                st.error("⚠️ Atenção: Todos os campos da ficha devem ser preenchidos.")
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
                    st.success("✅ DADOS GRAVADOS NA BASE HMM SERVIÇOS!")
                    st.balloons()
                except Exception as e: st.error(f"Erro de Conexão: {e}")

# --- ABA 2: ANÁLISE ---
with tab2:
    st.subheader("🔐 Painel de Gestão e Relatórios")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_v22_7")
    if senha == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            df['Empresa'] = df['Empresa'].str.strip()
            df['Setor'] = df['Setor'].str.strip()
            emp_sel = st.selectbox("Selecione o Cliente:", sorted(df['Empresa'].unique()), index=None)
            if emp_sel:
                setores = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                set_sel = st.multiselect("Filtrar por Setor (Multiseleção):", setores)
                df_f = df[df['Empresa'] == emp_sel]
                if set_sel:
                    df_f = df_f[df_f['Setor'].isin(set_sel)]
                
                cols = ['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca', 'Assedio_Moral', 'Assedio_Sexual']
                m = df_f[cols].mean()
                
                # Visualização de Radar
                fig = px.line_polar(r=m.values, theta=m.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', line_color='red')
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(m.to_frame(name="Média Obtida").T.style.format("{:.1f}"))

                st.markdown("---")
                concl = st.text_area("✍️ Conclusão Estratégica para o Word:", value="Análise baseada no equilíbrio Demanda-Controle.", height=150)
                
                if st.button("🚀 GERAR RELATÓRIO FORMATADO"):
                    nome_s = ", ".join(set_sel) if set_sel else "UNIDADE COMPLETA"
                    txt = f"RELATÓRIO DE GESTÃO PSICOSSOCIAL - HMM SERVIÇOS\n"
                    txt += f"CLIENTE: {emp_sel.upper()}\n"
                    txt += f"SETOR ANALISADO: {nome_s}\n"
                    txt += f"Amostra: {len(df_f)} avaliados | Data: {datetime.now().strftime('%d/%m/%Y')}\n"
                    txt += "="*50 + "\n"
                    txt += f"Demanda: {m['Demanda']:.1f} | Controle: {m['Controle']:.1f}\n"
                    txt += f"Suporte Social: {m['Suporte']:.1f} | Estresse/Saúde: {m['Saude']:.1f}\n"
                    txt += f"Insegurança Laboral: {m['Inseguranca']:.1f}\n"
                    txt += f"Assédio Moral: {m['Assedio_Moral']:.1f} | Assédio Sexual: {m['Assedio_Sexual']:.1f}\n"
                    txt += "="*50 + "\n\nPARECER TÉCNICO:\n" + concl + "\n\n"
                    txt += "METODOLOGIA: Protocolo Internacional COPSOQ III / Modelo de Karasek.\n"
                    txt += "Eng. Henrique - HMM Serviços"
                    st.text_area("📋 COPIE O CONTEÚDO PARA O WORD:", txt, height=400)
        else: st.warning("Aguardando dados na base.")

# --- RODAPÉ TÉCNICO ---
st.markdown("---")
st.caption("© 2026 HMM Serviços - Engenharia e Segurança do Trabalho. Sistema de Monitoramento Psicossocial Blindado via COPSOQ III.")
