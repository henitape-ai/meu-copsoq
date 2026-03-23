import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS E CONEXÃO
st.set_page_config(page_title="HMM - Gestão Psicossocial V23.5", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ESTILIZAÇÃO E CABEÇALHO ---
st.title("🚀 Programa de Avaliação de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.markdown(f"""
**Responsável Técnico:** Eng. Henrique | **Data:** {datetime.now().strftime('%d/%m/%Y')}  
🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)
---
⚠️ **CONFIDENCIALIDADE:** Esta avaliação é 100% anônima. Os dados são tratados de forma coletiva.
""")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta (41 Itens)", "📊 Painel de Gestão e Gráficos"])

# --- DICIONÁRIOS DE ESCALAS (LÓGICA COPSOQ III) ---
# Escala Direta: Sempre = 100 (Risco Alto)
esc_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
# Escala Inversa: Nunca = 100 (Risco Alto)
esc_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}
# Escala de Intensidade (Significado/Satisfação)
esc_int = {"Extremamente": 100, "Muito": 75, "Moderadamente": 50, "Um pouco": 25, "Nunca / Quase Nunca": 0}
# Escala de Saúde (Excelente = 0 / Deficitária = 100)
esc_sau = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

with tab1:
    with st.form("form_41_v23_5", clear_on_submit=True):
        st.subheader("📋 Identificação da Unidade")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:")
        with c2: setr = st.text_input("Setor:")
        with c3: func = st.text_input("Função:")
        with c4: idade = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        st.markdown("---")
        col_esq, col_dir = st.columns(2)

        with col_esq:
            st.info("### 1. EXIGÊNCIAS E CARGA")
            q1 = st.radio("1. Carga de trabalho mal distribuída?", list(esc_dir.keys()), index=None)
            q2 = st.radio("2. Falta de tempo para as tarefas?", list(esc_dir.keys()), index=None)
            q3 = st.radio("3. Precisa trabalhar muito rápido?", list(esc_dir.keys()), index=None)
            q4 = st.radio("4. Exige atenção constante?", list(esc_dir.keys()), index=None)
            q5 = st.radio("5. Exige tomar decisões difíceis?", list(esc_dir.keys()), index=None)
            q6 = st.radio("6. Exige emocionalmente de você?", list(esc_dir.keys()), index=None)

            st.info("### 2. INFLUÊNCIA E DESENVOLVIMENTO")
            q7 = st.radio("7. Tem influência no seu trabalho?", list(esc_inv.keys()), index=None)
            q8 = st.radio("8. O trabalho exige iniciativa?", list(esc_inv.keys()), index=None)
            q9 = st.radio("9. Permite aprender coisas novas?", list(esc_inv.keys()), index=None)

            st.info("### 3. INFORMAÇÃO E PAPEL")
            q10 = st.radio("10. Informado sobre decisões e mudanças?", list(esc_inv.keys()), index=None)
            q11 = st.radio("11. Recebe informações necessárias?", list(esc_inv.keys()), index=None)
            q12 = st.radio("12. Sabe exatamente suas responsabilidades?", list(esc_inv.keys()), index=None)

            st.info("### 4. RELAÇÕES SOCIAIS E LIDERANÇA")
            q13 = st.radio("13. Reconhecido e apreciado pela gerência?", list(esc_inv.keys()), index=None)
            q14 = st.radio("14. Tratado de forma justa?", list(esc_inv.keys()), index=None)
            q15 = st.radio("15. Tem ajuda e apoio do superior?", list(esc_inv.keys()), index=None)
            q16 = st.radio("16. Bom ambiente com os colegas?", list(esc_inv.keys()), index=None)
            q17 = st.radio("17. Chefia oferece oportunidades?", list(esc_inv.keys()), index=None)
            q18 = st.radio("18. Chefia planeja bem o trabalho?", list(esc_inv.keys()), index=None)
            q19 = st.radio("19. Gerência confia nos funcionários?", list(esc_inv.keys()), index=None)
            q20 = st.radio("20. Confia na informação da gerência?", list(esc_inv.keys()), index=None)
            q21 = st.radio("21. Conflitos resolvidos de forma justa?", list(esc_inv.keys()), index=None)
            q22 = st.radio("22. Trabalho igualmente distribuído?", list(esc_inv.keys()), index=None)

        with col_dir:
            st.success("### 5. SIGNIFICADO E SATISFAÇÃO")
            q23 = st.radio("23. Capaz de resolver problemas?", list(esc_inv.keys()), index=None)
            q24 = st.radio("24. Trabalho tem significado?", list(esc_int.keys()), index=None)
            q25 = st.radio("25. Trabalho é importante?", list(esc_int.keys()), index=None)
            q26 = st.radio("26. Problemas da empresa são seus?", list(esc_int.keys()), index=None)
            q27 = st.radio("27. Satisfação global com o trabalho?", list(esc_int.keys()), index=None)

            st.success("### 6. SEGURANÇA E SAÚDE")
            q28 = st.radio("28. Preocupado com desemprego?", list(esc_int.keys()), index=None)
            q29 = st.radio("29. Em geral, avalia sua saúde como:", list(esc_sau.keys()), index=None)

            st.success("### 7. INTERFACE TRABALHO-VIDA")
            q30 = st.radio("30. Afeta vida privada (Energia)?", list(esc_int.keys()), index=None)
            q31 = st.radio("31. Afeta vida privada (Tempo)?", list(esc_int.keys()), index=None)

            st.error("### 8. SAÚDE MENTAL E EXAUSTÃO")
            q32 = st.radio("32. Acorda à noite / Dificuldade de sono?", list(esc_dir.keys()), index=None)
            q33 = st.radio("33. Sente-se fisicamente exausto?", list(esc_dir.keys()), index=None)
            q34 = st.radio("34. Sente-se emocionalmente exausto?", list(esc_dir.keys()), index=None)
            q35 = st.radio("35. Sente-se irritado?", list(esc_dir.keys()), index=None)
            q36 = st.radio("36. Sente-se ansioso?", list(esc_dir.keys()), index=None)
            q37 = st.radio("37. Sente-se triste?", list(esc_dir.keys()), index=None)

            st.error("### 9. COMPORTAMENTOS OFENSIVOS")
            q38 = st.radio("38. Alvo de insultos ou provocações?", list(esc_dir.keys()), index=None)
            q39 = st.radio("39. Exposto a assédio sexual indesejado?", list(esc_dir.keys()), index=None)
            q40 = st.radio("40. Ameaças de violência?", list(esc_dir.keys()), index=None)
            q41 = st.radio("41. Violência física?", list(esc_dir.keys()), index=None)

        if st.form_submit_button("✅ GRAVAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Atenção: Preencha todas as questões para salvar.")
            else:
                try:
                    v_dem = (esc_dir[q1]+esc_dir[q2]+esc_dir[q3]+esc_dir[q4]+esc_dir[q5]+esc_dir[q6])/6
                    v_con = (esc_inv[q7]+esc_inv[q8]+esc_inv[q9])/3
                    v_lid = (esc_inv[q13]+esc_inv[q14]+esc_inv[q15]+esc_inv[q16]+esc_inv[q17]+esc_inv[q18]+esc_inv[q19]+esc_inv[q20]+esc_inv[q21]+esc_inv[q22])/10
                    v_men = (esc_dir[q32]+esc_dir[q33]+esc_dir[q34]+esc_dir[q35]+esc_dir[q36]+esc_dir[q37])/6
                    v_ofe = (esc_dir[q38]+esc_dir[q39]+esc_dir[q40]+esc_dir[q41])/4
                    v_sat = (esc_int[q27])

                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": emp.strip(), "Setor": setr.strip(), "Funcao": func.strip(), "Idade": idade,
                        "Demanda": v_dem, "Controle": v_con, "Lideranca": v_lid,
                        "Satisfacao": v_sat, "Saude_Geral": esc_sau[q29], 
                        "Saude_Mental": v_men, "Ofensivo": v_ofe
                    }])
                    df_base = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_base, nova_linha], ignore_index=True))
                    st.success("✅ DADOS GRAVADOS COM SUCESSO!")
                    st.balloons()
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE GESTÃO (PRÉ-RELATÓRIO) ---
with tab2:
    st.subheader("🔐 Área de Gestão Restrita")
    senha = st.text_input("Digite a senha de acesso:", type="password", key="pwd_v23_5")
    
    if senha == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            df['Setor'] = df['Setor'].astype(str).str.strip()

            st.markdown("### 🔍 Filtros de Análise")
            c1, c2 = st.columns(2)
            with c1:
                lista_emp = sorted(df['Empresa'].unique())
                emp_sel = st.selectbox("Selecione o Cliente:", lista_emp, index=None)
            
            if emp_sel:
                with c2:
                    lista_set = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                    set_sel = st.multiselect("Filtrar por Setor (Vazio = Geral):", lista_set)

                df_f = df[df['Empresa'] == emp_sel]
                tit_rel = f"GERAL - {emp_sel}"
                if set_sel:
                    df_f = df_f[df_f['Setor'].isin(set_sel)]
                    tit_rel = f"SETOR(ES): {', '.join(set_sel)}"

                cols = ['Demanda', 'Controle', 'Lideranca', 'Satisfacao', 'Saude_Mental', 'Ofensivo']
                med = df_f[cols].mean()

                st.markdown(f"### 📊 Mapa de Riscos: {tit_rel}")
                fig = px.line_polar(r=med.values, theta=med.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', line_color='red', fillcolor='rgba(255, 0, 0, 0.3)')
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")
                st.markdown("### 📝 Minuta de Pré-Relatório")
                
                txt_rel = f"""**RELATÓRIO TÉCNICO PSICOSSOCIAL**
**CLIENTE:** {emp_sel.upper()} | **UNIDADE:** {tit_rel}
**DATA:** {datetime.now().strftime('%d/%m/%Y')}
**METODOLOGIA:** Protocolo COPSOQ III (41 Indicadores)

**MÉDIAS OBTIDAS (0-100):**
- Demanda: {med['Demanda']:.1f} | Controle: {med['Controle']:.1f}
- Liderança: {med['Lideranca']:.1f} | Satisfação: {med['Satisfacao']:.1f}
- Saúde Mental: {med['Saude_Mental']:.1f} | Ofensivo: {med['Ofensivo']:.1f}

**ANÁLISE PRELIMINAR:**
"""
                if med['Demanda'] > 60 and med['Controle'] < 40:
                    txt_rel += "- ALERTA: Perfil de 'Alta Tensão' identificado.\n"
                if med['Ofensivo'] > 15:
                    txt_rel += "- ALERTA: Presença de comportamentos ofensivos.\n"
                
                txt_rel += f"\n**Responsável Técnico:** Eng. Henrique - HMM Serviços"
                st.text_area("Copie para o Word:", value=txt_rel, height=300)
        else: st.warning("Planilha sem dados.")
