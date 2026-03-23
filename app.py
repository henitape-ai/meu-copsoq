import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES HMM SERVIÇOS
st.set_page_config(page_title="HMM Serviços - Diagnóstico 41 Itens", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("🚀 Programa de Avaliação de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia e Gestão Ocupacional")
st.markdown("""
**Responsável Técnico:** Eng. Henrique | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)
---
⚠️ **ANONIMATO:** Esta avaliação é estritamente anônima e confidencial.
""")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta (41 Itens)", "📊 Painel de Análise"])

# --- DICIONÁRIOS DE ESCALAS ---
esc_f = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
esc_i = {"Extremamente": 100, "Muito": 75, "Moderadamente": 50, "Um pouco": 25, "Nunca / Quase Nunca": 0}
esc_s = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

with tab1:
    with st.form("form_v23_1"):
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa:")
        with c2: setr = st.text_input("Setor:")
        with c3: func = st.text_input("Função:")
        with c4: idade = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        col_a, col_b = st.columns(2)
        with col_a:
            st.info("### 1. EXIGÊNCIAS E TRABALHO")
            q1 = st.radio("1. Carga de trabalho mal distribuída?", list(esc_f.keys()), index=None)
            q2 = st.radio("2. Falta de tempo para tarefas?", list(esc_f.keys()), index=None)
            q3 = st.radio("3. Precisa trabalhar muito rápido?", list(esc_f.keys()), index=None)
            q4 = st.radio("4. Exige atenção constante?", list(esc_f.keys()), index=None)
            q5 = st.radio("5. Exige decisões difíceis?", list(esc_f.keys()), index=None)
            q6 = st.radio("6. Exige emocionalmente de você?", list(esc_f.keys()), index=None)
            st.info("### 2. INFLUÊNCIA E DESENVOLVIMENTO")
            q7 = st.radio("7. Grau de influência no trabalho?", list(esc_f.keys()), index=None)
            q8 = st.radio("8. Exige iniciativa?", list(esc_f.keys()), index=None)
            q9 = st.radio("9. Permite aprender coisas novas?", list(esc_f.keys()), index=None)
            st.info("### 3. INFORMAÇÃO E PAPEL")
            q10 = st.radio("10. Informado sobre mudanças?", list(esc_f.keys()), index=None)
            q11 = st.radio("11. Recebe informações necessárias?", list(esc_f.keys()), index=None)
            q12 = st.radio("12. Sabe suas responsabilidades?", list(esc_f.keys()), index=None)
            st.info("### 4. RELAÇÕES E LIDERANÇA")
            q13 = st.radio("13. Reconhecido pela gerência?", list(esc_f.keys()), index=None)
            q14 = st.radio("14. Tratado de forma justa?", list(esc_f.keys()), index=None)
            q15 = st.radio("15. Apoio do superior imediato?", list(esc_f.keys()), index=None)
            q16 = st.radio("16. Bom ambiente com colegas?", list(esc_f.keys()), index=None)
            q17 = st.radio("17. Chefia oferece desenvolvimento?", list(esc_f.keys()), index=None)
            q18 = st.radio("18. Chefia planeja bem o trabalho?", list(esc_f.keys()), index=None)
            q19 = st.radio("19. Gerência confia na equipe?", list(esc_f.keys()), index=None)
            q20 = st.radio("20. Confia na gerência?", list(esc_f.keys()), index=None)
            q21 = st.radio("21. Conflitos resolvidos justamente?", list(esc_f.keys()), index=None)
            q22 = st.radio("22. Trabalho distribuído igualmente?", list(esc_f.keys()), index=None)
        with col_b:
            st.success("### 5. SIGNIFICADO E SATISFAÇÃO")
            q23 = st.radio("23. Capaz de resolver problemas?", list(esc_f.keys()), index=None)
            q24 = st.radio("24. Trabalho tem significado?", list(esc_i.keys()), index=None)
            q25 = st.radio("25. Sente que o trabalho é importante?", list(esc_i.keys()), index=None)
            q26 = st.radio("26. Problemas da empresa são seus?", list(esc_i.keys()), index=None)
            q27 = st.radio("27. Satisfação global?", list(esc_i.keys()), index=None)
            st.success("### 6. SEGURANÇA E SAÚDE")
            q28 = st.radio("28. Preocupado com desemprego?", list(esc_i.keys()), index=None)
            q29 = st.radio("29. Como avalia sua saúde geral?", list(esc_s.keys()), index=None)
            st.success("### 7. INTERFACE VIDA-TRABALHO")
            q30 = st.radio("30. Afeta vida privada (Energia)?", list(esc_i.keys()), index=None)
            q31 = st.radio("31. Afeta vida privada (Tempo)?", list(esc_i.keys()), index=None)
            st.error("### 8. SAÚDE MENTAL")
            q32 = st.radio("32. Acorda à noite / Sono ruim?", list(esc_f.keys()), index=None)
            q33 = st.radio("33. Fisicamente exausto?", list(esc_f.keys()), index=None)
            q34 = st.radio("34. Emocionalmente exausto?", list(esc_f.keys()), index=None)
            q35 = st.radio("35. Irritado?", list(esc_f.keys()), index=None)
            q36 = st.radio("36. Ansioso?", list(esc_f.keys()), index=None)
            q37 = st.radio("37. Triste?", list(esc_f.keys()), index=None)
            st.error("### 9. COMPORTAMENTOS OFENSIVOS")
            q38 = st.radio("38. Insultos ou provocações?", list(esc_f.keys()), index=None)
            q39 = st.radio("39. Assédio sexual indesejado?", list(esc_f.keys()), index=None)
            q40 = st.radio("40. Ameaças de violência?", list(esc_f.keys()), index=None)
            q41 = st.radio("41. Violência física?", list(esc_f.keys()), index=None)

        if st.form_submit_button("✅ ENVIAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Erro: Existem perguntas sem resposta. Verifique todos os campos.")
            else:
                try:
                    # Cálculos das Médias
                    v_dem = (esc_f[q1]+esc_f[q2]+esc_f[q3]+esc_f[q4]+esc_f[q5]+esc_f[q6])/6
                    v_con = (esc_f[q7]+esc_f[q8]+esc_f[q9])/3
                    v_lid = (esc_f[q13]+esc_f[q14]+esc_f[q15]+esc_f[q16]+esc_f[q17]+esc_f[q18]+esc_f[q19]+esc_f[q20]+esc_f[q21]+esc_f[q22])/10
                    v_men = (esc_f[q32]+esc_f[q33]+esc_f[q34]+esc_f[q35]+esc_f[q36]+esc_f[q37])/6
                    v_ofe = (esc_f[q38]+esc_f[q39]+esc_f[q40]+esc_f[q41])/4

                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": emp.strip(), "Setor": setr.strip(), "Funcao": func.strip(), "Idade": idade,
                        "Demanda": v_dem, "Controle": v_con, "Lideranca": v_lid,
                        "Satisfacao": esc_i[q27], "Saude_Geral": esc_s[q29], 
                        "Saude_Mental": v_men, "Ofensivo": v_ofe
                    }])
                    df_base = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_base, nova_linha], ignore_index=True))
                    st.success("✅ DIAGNÓSTICO GRAVADO COM SUCESSO!")
                    st.balloons()
                except Exception as e: st.error(f"Erro ao gravar: {e}")

# --- ABA 2: ANÁLISE ---
with tab2:
    st.info("Acesse com a senha HMM2024 para visualizar as médias das 41 questões.")
