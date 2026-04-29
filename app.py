import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import numpy as np # Adicionado para cálculos de integridade

# 1. CONFIGURAÇÕES TÉCNICAS HMM
st.set_page_config(page_title="HMM - Gestão Ocupacional V28.1", layout="wide")

# --- BLOCO DE ESTILO ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stAppDeployButton {display: none !important;}
            #stDecoration {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}
            .block-container { padding-top: 1rem !important; }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("Levantamento das Condições e Organização do Trabalho")
st.subheader("HMM Serviços - Engenharia de Segurança do Trabalho")
st.markdown(f"**Responsável Técnico:** Henrique Motta de Miranda | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# --- TEXTO DE BOAS-VINDAS ---
with st.container():
    st.markdown("### Bem-vindo(a) à pesquisa sobre comportamentos no ambiente de trabalho!")
    st.warning("**AVALIAÇÃO ANÔNIMA:** Suas respostas serão confidenciais e protegidas pela LGPD.")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Resultados"])

# ESCALAS E MAPAS
esc_padrao = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca"]
esc_saude = ["Excelente", "Muito Boa", "Boa", "Razoável", "Deficitária"]

map_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca": 0}
map_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca": 100}
map_saude_val = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

with tab1:
    with st.form("form_v28_1", clear_on_submit=True):
        st.markdown("### Identificação Geral")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:").strip()
        with c2: setr = st.text_input("Setor:").strip()
        with c3: func = st.text_input("Função:").strip()
        with c4: idade_val = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        # Seções do Formulário (Resumido para o exemplo, mantenha as 41 questões do seu original)
        st.info("### 1. CARGA E EXIGÊNCIAS")
        q1 = st.radio("**1. O seu trabalho fica acumulado por má divisão?**", esc_padrao, index=None)
        q2 = st.radio("**2. Falta tempo para terminar suas tarefas?**", esc_padrao, index=None)
        q3 = st.radio("**3. Precisa trabalhar num ritmo muito acelerado?**", esc_padrao, index=None)
        q4 = st.radio("**4. O serviço exige a sua atenção constante e total?**", esc_padrao, index=None)
        q5 = st.radio("**5. No seu dia a dia, precisa de tomar decisões muito difíceis?**", esc_padrao, index=None)
        q6 = st.radio("**6. Considera o seu trabalho cansativo do ponto de vista emocional?**", esc_padrao, index=None)
        
        st.info("### 2. SUA AUTONOMIA")
        q7 = st.radio("**7. Consegue decidir como ou de que forma faz as suas tarefas?**", esc_padrao, index=None)
        q8 = st.radio("**8. O seu trabalho exige que você tenha iniciativa própria?**", esc_padrao, index=None)
        q9 = st.radio("**9. No seu serviço, você consegue aprender coisas novas?**", esc_padrao, index=None)
        
        st.info("### 3. COMUNICAÇÃO")
        q10 = st.radio("**10. É avisado com antecedência sobre mudanças e planos futuros?**", esc_padrao, index=None)
        q11 = st.radio("**11. Recebe todas as informações de que necessita?**", esc_padrao, index=None)
        q12 = st.radio("**12. Sabe exatamente quais são as suas responsabilidades?**", esc_padrao, index=None)
        
        # ... (Manter aqui todas as questões de 13 a 37 do seu original) ...
        # (Para este exemplo, simulei as variáveis faltantes como None)
        q13=q14=q15=q16=q17=q18=q19=q20=q21=q22=q23=q24=q25=q26=q27=q28=q29=q30=q31=q32=q33=q34=q35=q36=q37=None

        st.error("### 9. COMPORTAMENTO OFENSIVO") 
        q38 = st.radio("**38. Foi alvo de insultos ou provocações verbais?**", esc_padrao, index=None)
        q39 = st.radio("**39. Foi Exposto (a) a investidas sexuais indesejadas?**", esc_padrao, index=None)
        q40 = st.radio("**40. Sofreu ameaças de violência no trabalho?**", esc_padrao, index=None)
        q41 = st.radio("**41. Sofreu agressão física?**", esc_padrao, index=None)

        if st.form_submit_button("✅ ENVIAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Responda todas as 41 questões.")
            else:
                try:
                    # --- ALGORITMO DE INTEGRIDADE HMM ---
                    pesos_brutos = [map_dir.get(q, 50) for q in resps if q in map_dir]
                    desvio = np.std(pesos_brutos)
                    
                    # Teste de Dissonância (Ex: Q12 vs Q10)
                    # Se q12 é "Sempre" (100) e q10 é "Nunca" (0), há uma discrepância alta.
                    diff_controle = abs(map_dir[q12] - map_dir[q10])
                    
                    status_integridade = "Confiável"
                    if desvio < 10: status_integridade = "Inconsistente (Polarização)"
                    if diff_controle > 75: status_integridade = "Inconsistente (Contradição)"
                    
                    # CÁLCULOS DOS ITENS AGREGADOS
                    v_dem = sum([map_dir[q] for q in [q1,q2,q3,q4,q5,q6]]) / 6
                    v_con = sum([map_inv[q] for q in [q7,q8,q9,q10,q11,q12]]) / 6
                    v_lid = sum([map_inv[q] for q in [q13,q14,q15,q16,q17,q18,q19,q20,q21,q22]]) / 10
                    v_sat = sum([map_inv[q] for q in [q23,q24,q25,q26,q27]]) / 5
                    v_sg = map_saude_val[q29]
                    v_men = (map_dir[q28] + v_sg + sum([map_dir[q] for q in [q30,q31,q32,q33,q34,q35,q36,q37]])) / 10
                    v_ofe = sum([map_dir[q] for q in [q38,q39,q40,q41]]) / 4
                    
                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": emp, "Setor": setr, "Funcao": func, "Idade": idade_val,
                        "Demanda": v_dem, "Controle": v_con, "Lideranca": v_lid,
                        "Satisfacao": v_sat, "Saude_Geral": v_sg, "Saude_Mental": v_men, "Ofensivo": v_ofe,
                        "Integridade": status_integridade # Nova Coluna
                    }])
                    
                    df_b = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                    st.success("✅ DIAGNÓSTICO PROCESSADO!")
                    st.balloons()
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE GESTÃO ---
with tab2:
    st.subheader("🔐 Painel de Consultoria HMM")
    if st.text_input("Senha de Acesso:", type="password") == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            # Filtro de Integridade para o Consultor
            if st.checkbox("Excluir respostas inconsistentes da média"):
                df = df[df['Integridade'] == "Confiável"]
            
            # ... (Restante do seu código de Radar e Gráficos permanece igual) ...
            # Lembre de manter o padrão visual que você já criou.
