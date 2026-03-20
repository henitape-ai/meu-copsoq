import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. Configurações de Engenharia e Conexão HMM
st.set_page_config(page_title="HMM Serviços - Portal de Avaliação", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO INSTITUCIONAL ---
st.title("Avaliação de Riscos Psicossociais (COPSOQ III)")
st.subheader("HMM Serviços - Engenharia e Perícias")
st.caption("🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# 2. Navegação por Abas
tab1, tab2 = st.tabs(["📝 Coleta de Dados (Público)", "🔐 Painel de Análise (Privado)"])

# --- ABA 1: COLETA (O QUE O FUNCIONÁRIO VÊ) ---
with tab1:
    st.subheader("📋 Identificação da Avaliação")
    c_id1, c_id2, c_id3 = st.columns([2, 1, 1])
    with c_id1: empresa = st.text_input("Empresa Avaliada:", placeholder="Nome do Cliente")
    with c_id2: setor = st.text_input("Setor:", placeholder="Ex: Oficina")
    with c_id3: funcao = st.text_input("Função/Cargo:", placeholder="Ex: Mecânico")
    
    escala_freq = {"Sempre": 100, "Frequentemente": 75, "Às vezes": 50, "Raramente": 25, "Nunca": 0}

    with st.form("form_v16"):
        st.markdown("#### QUESTIONÁRIO TÉCNICO")
        st.caption("🔒 ANONIMATO GARANTIDO: Os dados são processados coletivamente.")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 1. EXIGÊNCIAS")
            p1 = st.radio("VOCÊ TEM QUE TRABALHAR MUITO RÁPIDO?", list(escala_freq.keys()), index=None)
            p2 = st.radio("O SEU TRABALHO É EMOCIONALMENTE DESGASTANTE?", list(escala_freq.keys()), index=None)
            st.markdown("### 2. CONTROLE")
            p3 = st.radio("TEM INFLUÊNCIA SOBRE AS DECISÕES NO TRABALHO?", list(escala_freq.keys()), index=None)
            p4 = st.radio("TEM OPORTUNIDADE DE APRENDER COISAS NOVAS?", list(escala_freq.keys()), index=None)
        with col2:
            st.markdown("### 3. SUPORTE")
            p5 = st.radio("O SUPERIOR APOIA VOCÊ QUANDO PRECISA?", list(escala_freq.keys()), index=None)
            p6 = st.radio("HÁ COOPERAÇÃO ENTRE OS COLEGAS?", list(escala_freq.keys()), index=None)
            st.markdown("### 4. SAÚDE/INSEGURANÇA")
            p7 = st.radio("SENTIU-SE TENSO OU ESTRESSADO?", list(escala_freq.keys()), index=None)
            p8 = st.radio("PREOCUPADO EM FICAR DESEMPREGADO?", list(escala_freq.keys()), index=None)
        
        st.markdown("### 5. CONDUTA ÉTICA")
        p9 = st.radio("EXPOSTO A HUMILHAÇÃO OU ASSÉDIO MORAL?", list(escala_freq.keys()), index=None)
        p10 = st.radio("EXPOSTO A ASSÉDIO SEXUAL (INVESTIDAS INDESEJADAS)?", list(escala_freq.keys()), index=None)
        
        if st.form_submit_button("ENVIAR DIAGNÓSTICO"):
            respostas = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
            if None in respostas or not empresa or not setor:
                st.error("⚠️ Responda todas as questões.")
            else:
                try:
                    v_dem, v_con, v_sup = (escala_freq[p1]+escala_freq[p2])/2, (escala_freq[p3]+escala_freq[p4])/2, (escala_freq[p5]+escala_freq[p6])/2
                    nova_linha = pd.DataFrame([{"Data": datetime.now().strftime("%d/%m/%Y %H:%M"), "Empresa": empresa, "Setor": setor, "Funcao": funcao, "Demanda": v_dem, "Controle": v_con, "Suporte": v_sup, "Saude": escala_freq[p7], "Inseguranca": escala_freq[p8], "Assedio_Moral": escala_freq[p9], "Assedio_Sexual": escala_freq[p10], "Classificacao_Risco": "Processado", "Parecer_Tecnico": "COPSOQ III", "Link_Grafico": "" }])
                    df_b = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                    st.success("✅ DADOS GRAVADOS!")
                    st.balloons()
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL PRIVADO (SÓ VOCÊ VÊ O MANUAL) ---
with tab2:
    st.subheader("🔐 Gestão de Riscos e Manual do Perito")
    senha = st.text_input("Senha de Acesso:", type="password", key="login_v16")

    if senha == "HMM2024":
        try:
            df = conn.read(worksheet="Página1", ttl=0)
            if not df.empty:
                c_f1, c_f2 = st.columns(2)
                with c_f1:
                    emp_sel = st.selectbox("Selecione a Empresa:", sorted(df['Empresa'].unique()), index=None)
                with c_f2:
                    if emp_sel:
                        set_sel = st.selectbox("Selecione o Setor:", sorted(df[df['Empresa'] == emp_sel]['Setor'].unique()), index=None)
                    else: set_sel = None

                if set_sel:
                    df_set = df[(df['Empresa'] == emp_sel) & (df['Setor'] == set_sel)]
                    m = df_set[['Demanda', 'Controle', 'Suporte', 'Saude', 'Inseguranca', 'Assedio_Moral', 'Assedio_Sexual']].mean()
                    
                    st.markdown(f"### 📊 Diagnóstico Setorial: {set_sel.upper()}")
                    col_radar, col_metrics = st.columns([2, 1])
                    with col_radar:
                        fig = px.line_polar(pd.DataFrame({'Eixo': m.index, 'Valor': m.values}), r='Valor', theta='Eixo', line_close=True, range_r=[0,100])
                        fig.update_traces(fill='toself', line_color='red')
                        st.plotly_chart(fig, use_container_width=True)
                    with col_metrics:
                        st.write("**MÉDIAS CALCULADAS:**")
                        st.dataframe(m)
                        st.metric("TOTAL DE AVALIAÇÕES", len(df_set))

                    # --- MANUAL DO PERITO (SÓ APARECE AQUI) ---
                    st.markdown("---")
                    with st.expander("📖 MANUAL DE INTERPRETAÇÃO TÉCNICA (EXCLUSIVO HMM SERVIÇOS)"):
                        st.info("**Como interpretar os eixos do radar:**")
                        st.markdown("""
                        * **DEMANDA (> 60):** Indica sobrecarga. Juridicamente correlacionado a pedidos de horas extras e fadiga.
                        * **CONTROLE (< 40):** O trabalhador não tem autonomia. Aumenta o nexo causal em casos de depressão ocupacional.
                        * **SUPORTE (< 40):** Indica liderança falha ou isolamento social. Crítico para clima organizacional.
                        * **SAÚDE (> 50):** Somatização do estresse. Indica risco iminente de afastamento (NTEP).
                        * **ASSÉDIO (> 0):** Qualquer valor acima de zero exige investigação imediata (Lei 14.457/22).
                        
                        **MODELO DE KARASEK:**
                        1. **Alta Tensão:** Demanda Alta + Controle Baixo (Risco máximo).
                        2. **Trabalho Ativo:** Demanda Alta + Controle Alto (Desafiador, mas saudável).
                        3. **Trabalho Passivo:** Demanda Baixa + Controle Baixo (Desmotivador).
                        """)
                    
                    st.text_area("TEXTO PARA O LAUDO:", f"EMPRESA: {emp_sel}\nSETOR: {set_sel}\nMETODOLOGIA: COPSOQ III", height=150)
            else: st.warning("Sem dados.")
        except Exception as e: st.error(f"Erro: {e}")
