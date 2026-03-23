import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES HMM SERVIÇOS
st.set_page_config(page_title="HMM Serviços - Diagnóstico Completo", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("🚀 Programa de Avaliação de Riscos Psicossociais")
st.subheader("HMM Serviços - Diagnóstico Avançado (41 Indicadores)")
st.markdown("""
**Responsável Técnico:** Eng. Henrique | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)
---
⚠️ **ANONIMATO GARANTIDO:** Suas respostas são confidenciais e processadas de forma coletiva.
""")

tab1, tab2 = st.tabs(["📝 Formuário de Coleta", "📊 Painel de Análise Profissional"])

# --- DICIONÁRIO DE ESCALAS ---
# Escala de Frequência Padrão
esc_f = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
# Escala de Intensidade (Significado/Satisfação)
esc_i = {"Extremamente": 100, "Muito": 75, "Moderadamente": 50, "Um pouco": 25, "Nunca / Quase Nunca": 0}
# Escala de Saúde
esc_s = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

with tab1:
    with st.form("form_v23"):
        # IDENTIFICAÇÃO
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa:")
        with c2: setr = st.text_input("Setor:")
        with c3: func = st.text_input("Função:")
        with c4: idade = st.number_input("Idade:", min_value=14, max_value=100, step=1)

        st.markdown("---")
        col_a, col_b = st.columns(2)

        with col_a:
            st.info("### 1. EXIGÊNCIAS E TRABALHO")
            q1 = st.radio("1. Carga de trabalho mal distribuída?", list(esc_f.keys()), index=None)
            q2 = st.radio("2. Falta de tempo para completar tarefas?", list(esc_f.keys()), index=None)
            q3 = st.radio("3. Precisa trabalhar muito rápido?", list(esc_f.keys()), index=None)
            q4 = st.radio("4. Exige atenção constante?", list(esc_f.keys()), index=None)
            q5 = st.radio("5. Exige tomar decisões difíceis?", list(esc_f.keys()), index=None)
            q6 = st.radio("6. Exige emocionalmente de você?", list(esc_f.keys()), index=None)

            st.info("### 2. INFLUÊNCIA E DESENVOLVIMENTO")
            q7 = st.radio("7. Elevado grau de influência?", list(esc_f.keys()), index=None)
            q8 = st.radio("8. Exige iniciativa?", list(esc_f.keys()), index=None)
            q9 = st.radio("9. Permite aprender coisas novas?", list(esc_f.keys()), index=None)

            st.info("### 3. INFORMAÇÃO E PAPEL NO TRABALHO")
            q10 = st.radio("10. Informado sobre decisões importantes?", list(esc_f.keys()), index=None)
            q11 = st.radio("11. Recebe toda informação necessária?", list(esc_f.keys()), index=None)
            q12 = st.radio("12. Sabe exatamente suas responsabilidades?", list(esc_f.keys()), index=None)

            st.info("### 4. RELAÇÕES SOCIAIS E LIDERANÇA")
            q13 = st.radio("13. Reconhecido pela gerência?", list(esc_f.keys()), index=None)
            q14 = st.radio("14. Tratado de forma justa?", list(esc_f.keys()), index=None)
            q15 = st.radio("15. Tem apoio do superior imediato?", list(esc_f.keys()), index=None)
            q16 = st.radio("16. Bom ambiente com colegas?", list(esc_f.keys()), index=None)
            q17 = st.radio("17. Chefia oferece desenvolvimento?", list(esc_f.keys()), index=None)
            q18 = st.radio("18. Chefia é boa no planejamento?", list(esc_f.keys()), index=None)
            q19 = st.radio("19. Gerência confia nos funcionários?", list(esc_f.keys()), index=None)
            q20 = st.radio("20. Confia na informação da gerência?", list(esc_f.keys()), index=None)
            q21 = st.radio("21. Conflitos resolvidos de forma justa?", list(esc_f.keys()), index=None)
            q22 = st.radio("22. Trabalho distribuído igualmente?", list(esc_f.keys()), index=None)

        with col_b:
            st.success("### 5. SIGNIFICADO E SATISFAÇÃO")
            q23 = st.radio("23. Capaz de resolver problemas?", list(esc_f.keys()), index=None)
            q24 = st.radio("24. Trabalho tem significado?", list(esc_i.keys()), index=None)
            q25 = st.radio("25. Sente que o trabalho é importante?", list(esc_i.keys()), index=None)
            q26 = st.radio("26. Problemas da empresa são seus também?", list(esc_i.keys()), index=None)
            q27 = st.radio("27. Satisfação global com o trabalho?", list(esc_i.keys()), index=None)

            st.success("### 6. SEGURANÇA E SAÚDE GERAL")
            q28 = st.radio("28. Preocupado com desemprego?", list(esc_i.keys()), index=None)
            q29 = st.radio("29. Em geral, sua saúde é:", list(esc_s.keys()), index=None)

            st.success("### 7. INTERFACE TRABALHO-INDIVÍDUO")
            q30 = st.radio("30. Afeta vida privada negativamente (Energia)?", list(esc_i.keys()), index=None)
            q31 = st.radio("31. Afeta vida privada negativamente (Tempo)?", list(esc_i.keys()), index=None)

            st.error("### 8. SAÚDE MENTAL E EXAUSTÃO")
            q32 = st.radio("32. Dificuldade para dormir?", list(esc_f.keys()), index=None)
            q33 = st.radio("33. Fisicamente exausto?", list(esc_f.keys()), index=None)
            q34 = st.radio("34. Emocionalmente exausto?", list(esc_f.keys()), index=None)
            q35 = st.radio("35. Irritado?", list(esc_f.keys()), index=None)
            q36 = st.radio("36. Ansioso?", list(esc_f.keys()), index=None)
            q37 = st.radio("37. Triste?", list(esc_f.keys()), index=None)

            st.error("### 9. COMPORTAMENTOS OFENSIVOS")
            q38 = st.radio("38. Insultos ou provocações verbais?", list(esc_f.keys()), index=None)
            q39 = st.radio("39. Assédio sexual indesejado?", list(esc_f.keys()), index=None)
            q40 = st.radio("40. Ameaças de violência?", list(esc_f.keys()), index=None)
            q41 = st.radio("41. Violência física?", list(esc_f.keys()), index=None)

        if st.form_submit_button("✅ GRAVAR DIAGNÓSTICO COMPLETO"):
            # Lógica de cálculo simplificada por blocos para o Sheets
            try:
                # Médias por Dimensão (Engenharia HMM)
                v_demanda = (esc_f[q1]+esc_f[q2]+esc_f[q3]+esc_f[q4]+esc_f[q5]+esc_f[q6])/6
                v_controle = (esc_f[q7]+esc_f[q8]+esc_f[q9])/3
                v_lideranca = (esc_f[q13]+esc_f[q14]+esc_f[q15]+esc_f[q16]+esc_f[q17]+esc_f[q18]+esc_f[q19]+esc_f[q20]+esc_f[q21]+esc_f[q22])/10
                v_saude_mental = (esc_f[q32]+esc_f[q33]+esc_f[q34]+esc_f[q35]+esc_f[q36]+esc_f[q37])/6
                v_ofensivo = (esc_f[q38]+esc_f[q39]+esc_f[q40]+esc_f[q41])/4

                nova_linha = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Empresa": emp, "Setor": setr, "Funcao": func, "Idade": idade,
                    "Demanda": v_demanda, "Controle": v_controle, "Lideranca": v_lideranca,
                    "Satisfacao": esc_i[q27], "Saude_Geral": esc_s[q29], 
                    "Saude_Mental": v_saude_mental, "Ofensivo": v_ofensivo
                }])
                
                df_b = conn.read(worksheet="Página1", ttl=0)
                conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                st.success("✅ DADOS GRAVADOS COM SUCESSO!")
            except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: ANÁLISE --- (Simplificada para o exemplo)
with tab2:
    st.info("Utilize a senha HMM2024 para acessar os dashboards avançados baseados nestas 41 questões.")
