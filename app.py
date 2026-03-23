import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS E CONEXÃO
st.set_page_config(page_title="HMM - Gestão V23.7", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("🚀 Diagnóstico de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.markdown(f"**Responsável:** Eng. Henrique | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Resultados"])

# --- DICIONÁRIOS DE ESCALAS ---
esc_f = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
esc_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}
esc_int = {"Extremamente": 100, "Muito": 75, "Moderadamente": 50, "Um pouco": 25, "Nunca / Quase nunca": 0}
esc_sau = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}
esc_n9 = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca": 0}

# --- ABA 1: FORMULÁRIO ---
with tab1:
    st.info("⚠️ **IMPORTANTE:** Esta avaliação é **ANÔNIMA**. Responda com sinceridade.")
    with st.form("form_v23_7", clear_on_submit=True):
        st.markdown("### 📋 Identificação")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:")
        with c2: setr = st.text_input("Setor:")
        with c3: func = st.text_input("Função (Opcional):")
        with c4: idade_val = st.number_input("Idade:", min_value=14, max_value=100, value=30) # Campo Idade Reinserido

        col_a, col_b = st.columns(2)
        with col_a:
            st.info("### 1. SOBRE SUA CARGA DE TRABALHO")
            q1 = st.radio("**1. O seu trabalho fica acumulado porque as tarefas são mal divididas?**", list(esc_f.keys()), index=None)
            q2 = st.radio("**2. Com que frequência falta tempo para você terminar tudo o que precisa fazer?**", list(esc_f.keys()), index=None)
            q3 = st.radio("**3. Você precisa trabalhar em um ritmo muito acelerado?**", list(esc_f.keys()), index=None)
            q4 = st.radio("**4. O seu serviço exige atenção total o tempo todo?**", list(esc_f.keys()), index=None)
            q5 = st.radio("**5. Você precisa tomar decisões muito difíceis no dia a dia?**", list(esc_f.keys()), index=None)
            q6 = st.radio("**6. O seu trabalho é cansativo do ponto de vista emocional?**", list(esc_f.keys()), index=None)
            st.info("### 2. SUA AUTONOMIA")
            q7 = st.radio("**7. Você consegue decidir como fazer as suas tarefas?**", list(esc_inv.keys()), index=None)
            q8 = st.radio("**8. O seu trabalho exige que você tenha iniciativa própria?**", list(esc_inv.keys()), index=None)
            q9 = st.radio("**9. No seu serviço, você consegue aprender coisas novas?**", list(esc_inv.keys()), index=None)
            st.info("### 3. COMUNICAÇÃO")
            q10 = st.radio("**10. Você é avisado com antecedência sobre mudanças e planos da empresa?**", list(esc_inv.keys()), index=None)
            q11 = st.radio("**11. Você recebe as informações que precisa para trabalhar bem?**", list(esc_inv.keys()), index=None)
            q12 = st.radio("**12. Você sabe exatamente quais são as suas responsabilidades?**", list(esc_inv.keys()), index=None)
            st.info("### 4. LIDERANÇA E AMBIENTE")
            q13 = st.radio("**13. A chefia reconhece e valoriza o que você faz?**", list(esc_inv.keys()), index=None)
            q14 = st.radio("**14. Você sente que é tratado de forma justa na empresa?**", list(esc_inv.keys()), index=None)
            q15 = st.radio("**15. O seu chefe ajuda e apoia você quando você precisa?**", list(esc_inv.keys()), index=None)
            q16 = st.radio("**16. Existe um bom relacionamento entre você e seus colegas?**", list(esc_inv.keys()), index=None)
            q17 = st.radio("**17. A chefia incentiva o seu desenvolvimento profissional?**", list(esc_inv.keys()), index=None)
            q18 = st.radio("**18. O seu chefe sabe planejar bem o trabalho da equipe?**", list(esc_inv.keys()), index=None)
            q19 = st.radio("**19. A gerência confia que os funcionários fazem um bom trabalho?**", list(esc_inv.keys()), index=None)
            q20 = st.radio("**20. Você confia nas informações que recebe da gerência?**", list(esc_inv.keys()), index=None)
            q21 = st.radio("**21. Os problemas no setor são resolvidos de forma justa?**", list(esc_inv.keys()), index=None)
            q22 = st.radio("**22. O trabalho é dividido de forma igual entre as pessoas?**", list(esc_inv.keys()), index=None)
        with col_b:
            st.success("### 5. SATISFAÇÃO")
            q23 = st.radio("**23. Você se sente capaz de resolver os problemas que aparecem?**", list(esc_inv.keys()), index=None)
            q24 = st.radio("**24. O seu trabalho tem um significado importante para você?**", list(esc_int.keys()), index=None)
            q25 = st.radio("**25. Você sente que o que você faz é importante?**", list(esc_int.keys()), index=None)
            q26 = st.radio("**26. Você sente que os problemas da empresa também são seus?**", list(esc_int.keys()), index=None)
            q27 = st.radio("**27. No geral, o quanto você está satisfeito com seu trabalho?**", list(esc_int.keys()), index=None)
            st.success("### 6. SEGURANÇA E SAÚDE")
            q28 = st.radio("**28. Você sente medo de perder o emprego?**", list(esc_int.keys()), index=None)
            q29 = st.radio("**29. De forma geral, como você avalia a sua saúde?**", list(esc_sau.keys()), index=None)
            st.success("### 7. TRABALHO E VIDA PESSOAL")
            q30 = st.radio("**30. O trabalho tira a energia da sua vida particular?**", list(esc_int.keys()), index=None)
            q31 = st.radio("**31. O trabalho toma muito do seu tempo privado?**", list(esc_int.keys()), index=None)
            st.error("### 8. COMO VOCÊ SE SENTE")
            q32 = st.radio("**32. Teve dificuldade para dormir ou acordou muito à noite?**", list(esc_f.keys()), index=None)
            q33 = st.radio("**33. Sentiu-se esgotado fisicamente?**", list(esc_f.keys()), index=None)
            q34 = st.radio("**34. Sentiu-se esgotado emocionalmente?**", list(esc_f.keys()), index=None)
            q35 = st.radio("**35. Sentiu-se irritado com facilidade?**", list(esc_f.keys()), index=None)
            q36 = st.radio("**36. Sentiu-se ansioso?**", list(esc_f.keys()), index=None)
            q37 = st.radio("**37. Sentiu-se triste?**", list(esc_f.keys()), index=None)
            st.error("### 9. SITUAÇÕES DIFÍCEIS")
            q38 = st.radio("**38. Foi alvo de insultos ou provocações?**", list(esc_n9.keys()), index=None)
            q39 = st.radio("**39. Passou por situação de assédio sexual indesejado?**", list(esc_n9.keys()), index=None)
            q40 = st.radio("**40. Sofreu ameaças de violência?**", list(esc_n9.keys()), index=None)
            q41 = st.radio("**41. Sofreu algum tipo de agressão física?**", list(esc_n9.keys()), index=None)

        if st.form_submit_button("✅ ENVIAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Preencha todas as perguntas.")
            else:
                try:
                    v_dem = (esc_f[q1]+esc_f[q2]+esc_f[q3]+esc_f[q4]+esc_f[q5]+esc_f[q6])/6
                    v_con = (esc_inv[q7]+esc_inv[q8]+esc_inv[q9])/3
                    v_lid = (esc_inv[q13]+esc_inv[q14]+esc_inv[q15]+esc_inv[q16]+esc_inv[q17]+esc_inv[q18]+esc_inv[q19]+esc_inv[q20]+esc_inv[q21]+esc_inv[q22])/10
                    v_men = (esc_f[q32]+esc_f[q33]+esc_f[q34]+esc_f[q35]+esc_f[q36]+esc_f[q37])/6
                    v_ofe = (esc_n9[q38]+esc_n9[q39]+esc_n9[q40]+esc_n9[q41])/4
                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": emp.strip(), "Setor": setr.strip(), "Funcao": func.strip(), "Idade": idade_val,
                        "Demanda": v_dem, "Controle": v_con, "Lideranca": v_lid,
                        "Satisfacao": esc_int[q27], "Saude_Geral": esc_sau[q29], 
                        "Saude_Mental": v_men, "Ofensivo": v_ofe
                    }])
                    df_base = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_base, nova_linha], ignore_index=True))
                    st.success("✅ DADOS GRAVADOS!")
                    st.balloons()
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE GESTÃO ---
with tab2:
    st.subheader("🔐 Painel do Consultor HMM
