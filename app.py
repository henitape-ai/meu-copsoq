import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS
st.set_page_config(page_title="HMM - Diagnóstico V23.4", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("🚀 Programa de Avaliação de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.markdown(f"**Responsável:** Eng. Henrique | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# Definição das Abas
tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Gestão"])

# --- ESCALAS ---
esc_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
esc_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}
esc_int = {"Extremamente": 100, "Muito": 75, "Moderadamente": 50, "Um pouco": 25, "Nunca / Quase Nunca": 0}
esc_sau = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

# --- ABA 1: FORMULÁRIO ---
with tab1:
    st.info("⚠️ **ANONIMATO:** Esta avaliação é estritamente anônima.")
    with st.form("form_completo_v23_4", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1: emp = st.text_input("Empresa:")
        with c2: setr = st.text_input("Setor:")
        with c3: func = st.text_input("Função (Opcional):")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.info("### 1. EXIGÊNCIAS")
            q1 = st.radio("1. Carga mal distribuída?", list(esc_dir.keys()), index=None)
            q2 = st.radio("2. Falta de tempo?", list(esc_dir.keys()), index=None)
            q3 = st.radio("3. Trabalha muito rápido?", list(esc_dir.keys()), index=None)
            q4 = st.radio("4. Atenção constante?", list(esc_dir.keys()), index=None)
            q5 = st.radio("5. Decisões difíceis?", list(esc_dir.keys()), index=None)
            q6 = st.radio("6. Exigência emocional?", list(esc_dir.keys()), index=None)
            st.info("### 2. CONTROLE")
            q7 = st.radio("7. Influência no trabalho?", list(esc_inv.keys()), index=None)
            q8 = st.radio("8. Exige iniciativa?", list(esc_inv.keys()), index=None)
            q9 = st.radio("9. Aprender coisas novas?", list(esc_inv.keys()), index=None)
            st.info("### 3. INFORMAÇÃO")
            q10 = st.radio("10. Informado sobre mudanças?", list(esc_inv.keys()), index=None)
            q11 = st.radio("11. Recebe informações?", list(esc_inv.keys()), index=None)
            q12 = st.radio("12. Sabe responsabilidades?", list(esc_inv.keys()), index=None)
            st.info("### 4. LIDERANÇA (10 ITENS)")
            q13 = st.radio("13. Reconhecido pela gerência?", list(esc_inv.keys()), index=None)
            q14 = st.radio("14. Tratado justamente?", list(esc_inv.keys()), index=None)
            q15 = st.radio("15. Apoio do superior?", list(esc_inv.keys()), index=None)
            q16 = st.radio("16. Bom ambiente?", list(esc_inv.keys()), index=None)
            q17 = st.radio("17. Oportunidade desenvolvimento?", list(esc_inv.keys()), index=None)
            q18 = st.radio("18. Planejamento da chefia?", list(esc_inv.keys()), index=None)
            q19 = st.radio("19. Gerência confia na equipe?", list(esc_inv.keys()), index=None)
            q20 = st.radio("20. Confia na gerência?", list(esc_inv.keys()), index=None)
            q21 = st.radio("21. Conflitos resolvidos?", list(esc_inv.keys()), index=None)
            q22 = st.radio("22. Trabalho distribuído?", list(esc_inv.keys()), index=None)
        with col_b:
            st.success("### 5. SATISFAÇÃO")
            q23 = st.radio("23. Resolve problemas?", list(esc_inv.keys()), index=None)
            q24 = st.radio("24. Trabalho com significado?", list(esc_int.keys()), index=None)
            q25 = st.radio("25. Trabalho importante?", list(esc_int.keys()), index=None)
            q26 = st.radio("26. Problemas são seus?", list(esc_int.keys()), index=None)
            q27 = st.radio("27. Satisfação global?", list(esc_int.keys()), index=None)
            st.success("### 6. SEGURANÇA")
            q28 = st.radio("28. Medo desemprego?", list(esc_int.keys()), index=None)
            q29 = st.radio("29. Saúde geral?", list(esc_sau.keys()), index=None)
            st.success("### 7. VIDA PRIVADA")
            q30 = st.radio("30. Afeta Energia?", list(esc_int.keys()), index=None)
            q31 = st.radio("31. Afeta Tempo?", list(esc_int.keys()), index=None)
            st.error("### 8. SAÚDE MENTAL")
            q32 = st.radio("32. Sono ruim?", list(esc_dir.keys()), index=None)
            q33 = st.radio("33. Exaustão física?", list(esc_dir.keys()), index=None)
            q34 = st.radio("34. Exaustão emocional?", list(esc_dir.keys()), index=None)
            q35 = st.radio("35. Irritação?", list(esc_dir.keys()), index=None)
            q36 = st.radio("36. Ansiedade?", list(esc_dir.keys()), index=None)
            q37 = st.radio("37. Tristeza?", list(esc_dir.keys()), index=None)
            st.error("### 9. ÉTICA/OFENSIVO")
            q38 = st.radio("38. Insultos?", list(esc_dir.keys()), index=None)
            q39 = st.radio("39. Assédio sexual?", list(esc_dir.keys()), index=None)
            q40 = st.radio("40. Ameaça violência?", list(esc_dir.keys()), index=None)
            q41 = st.radio("41. Violência física?", list(esc_dir.keys()), index=None)

        if st.form_submit_button("✅ ENVIAR RESPOSTAS"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Responda todas as perguntas.")
            else:
                try:
                    v_dem = (esc_dir[q1]+esc_dir[q2]+esc_dir[q3]+esc_dir[q4]+esc_dir[q5]+esc_dir[q6])/6
                    v_con = (esc_inv[q7]+esc_inv[q8]+esc_inv[q9])/3
                    v_lid = (esc_inv[q13]+esc_inv[q14]+esc_inv[q15]+esc_inv[q16]+esc_inv[q17]+esc_inv[q18]+esc_inv[q19]+esc_inv[q20]+esc_inv[q21]+esc_inv[q22])/10
                    v_men = (esc_dir[q32]+esc_dir[q33]+esc_dir[q34]+esc_dir[q35]+esc_dir[q36]+esc_dir[q37])/6
                    v_ofe = (esc_dir[q38]+esc_dir[q39]+esc_dir[q40]+esc_dir[q41])/4
                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": emp.strip(), "Setor": setr.strip(), "Funcao": func.strip(),
                        "Demanda": v_dem, "Controle": v_con, "Lideranca": v_lid,
                        "Satisfacao": esc_int[q27], "Saude_Geral": esc_sau[q29], 
                        "Saude_Mental": v_men, "Ofensivo": v_ofe
                    }])
                    df_b = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                    st.success("✅ GRAVADO!")
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE GESTÃO (ISOLADO) ---
with tab2:
    st.subheader("🔐 Acesso Restrito HMM")
    # Uso de 'key' única e sem dependência de formulário
    acesso = st.text_input("Digite a senha para liberar os dados:", type="password", key="pwd_manager")
    
    if acesso == "HMM2024":
        st.success("Acesso Liberado!")
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            st.dataframe(df.tail(10)) # Mostra os últimos 10 envios
            # Botão de Relatório
            if st.button("🚀 GERAR MÉDIAS GERAIS"):
                m = df[['Demanda', 'Controle', 'Lideranca', 'Saude_Mental', 'Ofensivo']].mean()
                st.write(m)
        else: st.warning("Planilha vazia.")
