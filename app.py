import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS
st.set_page_config(page_title="HMM - Gestão V24.2", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("🚀 Diagnóstico de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.markdown(f"**Responsável Técnico:** Eng. Henrique | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

st.warning("🔒 **AVALIAÇÃO ANÔNIMA:** Esta coleta de dados é realizada de forma estritamente anônima.")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Resultados"])

# --- ESCALAS ---
esc_f = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
esc_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}
esc_int = {"Extremamente": 100, "Muito": 75, "Moderadamente": 50, "Um pouco": 25, "Nunca / Quase nunca": 0}
esc_sau = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}
esc_n9 = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca": 0}

with tab1:
    # Usamos st.container para organizar a validação
    with st.container():
        st.markdown("### 📋 Identificação Geral")
        c1, c2, c3, c4 = st.columns(4)
        emp = c1.text_input("Empresa Cliente:", key="emp_input")
        setr = c2.text_input("Setor:", key="setr_input")
        func = c3.text_input("Função (Opcional):", key="func_input")
        idade_val = c4.number_input("Idade:", min_value=14, max_value=100, value=30, key="idade_input")

        col_a, col_b = st.columns(2)
        
        with col_a:
            st.info("### 1. CARGA E EXIGÊNCIAS")
            q1 = st.radio("**1. Trabalho acumulado por má divisão?**", list(esc_f.keys()), index=None, key="q1")
            q2 = st.radio("**2. Falta tempo para as tarefas?**", list(esc_f.keys()), index=None, key="q2")
            q3 = st.radio("**3. Ritmo de trabalho acelerado?**", list(esc_f.keys()), index=None, key="q3")
            q4 = st.radio("**4. Exige atenção total constante?**", list(esc_f.keys()), index=None, key="q4")
            q5 = st.radio("**5. Precisa tomar decisões difíceis?**", list(esc_f.keys()), index=None, key="q5")
            q6 = st.radio("**6. Trabalho emocionalmente cansativo?**", list(esc_f.keys()), index=None, key="q6")
            
            st.info("### 2. AUTONOMIA")
            q7 = st.radio("**7. Decide como fazer suas tarefas?**", list(esc_inv.keys()), index=None, key="q7")
            q8 = st.radio("**8. Exige muita iniciativa própria?**", list(esc_inv.keys()), index=None, key="q8")
            q9 = st.radio("**9. Consegue aprender coisas novas?**", list(esc_inv.keys()), index=None, key="q9")
            
            st.info("### 3. COMUNICAÇÃO")
            q10 = st.radio("**10. Avisado sobre mudanças e planos?**", list(esc_inv.keys()), index=None, key="q10")
            q11 = st.radio("**11. Recebe informações necessárias?**", list(esc_inv.keys()), index=None, key="q11")
            q12 = st.radio("**12. Sabe suas responsabilidades?**", list(esc_inv.keys()), index=None, key="q12")
            
            st.info("### 4. LIDERANÇA")
            q13 = st.radio("**13. Chefia valoriza seu trabalho?**", list(esc_inv.keys()), index=None, key="q13")
            q14 = st.radio("**14. Tratado de forma justiça?**", list(esc_inv.keys()), index=None, key="q14")
            q15 = st.radio("**15. Apoio do superior imediato?**", list(esc_inv.keys()), index=None, key="q15")
            q16 = st.radio("**16. Bom ambiente com colegas?**", list(esc_inv.keys()), index=None, key="q16")
            q17 = st.radio("**17. Incentivo ao desenvolvimento?**", list(esc_inv.keys()), index=None, key="q17")
            q18 = st.radio("**18. Chefe planeja bem o trabalho?**", list(esc_inv.keys()), index=None, key="q18")
            q19 = st.radio("**19. Gerência confia na equipe?**", list(esc_inv.keys()), index=None, key="q19")
            q20 = st.radio("**20. Confia na gerência?**", list(esc_inv.keys()), index=None, key="q20")
            q21 = st.radio("**21. Conflitos resolvidos justamente?**", list(esc_inv.keys()), index=None, key="q21")
            q22 = st.radio("**22. Trabalho dividido igualmente?**", list(esc_inv.keys()), index=None, key="q22")

        with col_b:
            st.success("### 5. SIGNIFICADO E SATISFAÇÃO")
            q23 = st.radio("**23. Capaz de resolver problemas?**", list(esc_inv.keys()), index=None, key="q23")
            q24 = st.radio("**24. Trabalho com significado real?**", list(esc_int.keys()), index=None, key="q24")
            q25 = st.radio("**25. Sente que o trabalho é importante?**", list(esc_int.keys()), index=None, key="q25")
            q26 = st.radio("**26. Problemas da empresa são seus?**", list(esc_int.keys()), index=None, key="q26")
            q27 = st.radio("**27. Satisfação global com o trabalho?**", list(esc_int.keys()), index=None, key="q27")
            
            st.success("### 6. SEGURANÇA E SAÚDE")
            q28 = st.radio("**28. Medo de perder o emprego?**", list(esc_int.keys()), index=None, key="q28")
            q29 = st.radio("**29. Como avalia sua saúde geral?**", list(esc_sau.keys()), index=None, key="q29")
            
            st.success("### 7. VIDA PRIVADA")
            q30 = st.radio("**30. Trabalho tira energia da vida privada?**", list(esc_int.keys()), index=None, key="q30")
            q31 = st.radio("**31. Trabalho toma tempo da vida privada?**", list(esc_int.keys()), index=None, key="q31")
            
            st.error("### 8. COMO VOCÊ SE SENTE")
            q32 = st.radio("**32. Teve dificuldade para dormir?**", list(esc_f.keys()), index=None, key="q32")
            q33 = st.radio("**33. Sentiu esgotamento físico?**", list(esc_f.keys()), index=None, key="q33")
            q34 = st.radio("**34. Sentiu esgotamento emocional?**", list(esc_f.keys()), index=None, key="q34")
            q35 = st.radio("**35. Sentiu irritação frequente?**", list(esc_f.keys()), index=None, key="q35")
            q36 = st.radio("**36. Sentiu ansiedade?**", list(esc_f.keys()), index=None, key="q36")
            q37 = st.radio("**37. Sentiu tristeza?**", list(esc_f.keys()), index=None, key="q37")
            
            st.error("### 9. SITUAÇÕES DIFÍCEIS")
            q38 = st.radio("**38. Alvo de insultos ou provocações?**", list(esc_n9.keys()), index=None, key="q38")
            q39 = st.radio("**39. Exposto a assédio sexual?**", list(esc_n9.keys()), index=None, key="q39")
            q40 = st.radio("**40. Sofreu ameaças de violência?**", list(esc_n9.keys()), index=None, key="q40")
            q41 = st.radio("**41. Sofreu agressão física?**", list(esc_n9.keys()), index=None, key="q41")

        # BOTÃO FORA DO FORM PARA MANTER ESTADO
        if st.button("✅ FINALIZAR E GRAVAR DIAGNÓSTICO"):
            lista_q = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            
            indices_vazios = [i+1 for i, val in enumerate(lista_q) if val is None]
            
            if indices_vazios or not emp or not setr:
                st.error(f"⚠️ **ERRO:** Você esqueceu de responder as questões: {indices_vazios}. Por favor, verifique os campos marcados.")
                st.warning("As respostas marcadas foram mantidas. Complete apenas o que falta.")
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
                    st.success("✅ DIAGNÓSTICO GRAVADO COM SUCESSO! Você pode fechar esta página.")
                    st.balloons()
                except Exception as e: st.error(f"Erro ao gravar: {e}")

# --- ABA 2: PAINEL (CÓDIGO DA V24.1 MANTIDO) ---
with tab2:
    st.info("Acesso via senha HMM2024 para visualizar as sugestões técnicas.")
