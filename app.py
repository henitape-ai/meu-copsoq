import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS HMM
st.set_page_config(page_title="HMM - Gestão Ocupacional V27.5", layout="wide")

# --- BLOCO DE ESTILO (BLINDAGEM TOTAL) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stAppDeployButton {display: none !important;}
            #stDecoration {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}
            div[data-testid="stStatusWidget"] {display: none !important;}
            .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
            [data-testid="stHeader"] {display: none !important;}
            [data-testid="stToolbar"] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("Avaliação de Comportamentos no Ambiente de Trabalho")
st.subheader("HMM Serviços - Engenharia de Segurança do Trabalho")
st.markdown(f"**Responsável Técnico:** Henrique Motta de Miranda 
🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# --- TEXTO DE BOAS-VINDAS ---
with st.container():
    st.markdown("### Bem-vindo(a) à pesquisa sobre comportamentos no ambiente de trabalho!")
    st.markdown("Por favor, leia atentamente as opções de resposta antes de iniciar:")
    col_inst1, col_inst2 = st.columns(2)
    with col_inst1:
        st.write("- **NUNCA:** não ocorre em nenhuma situação.")
        st.write("- **RARAMENTE:** ocorre em pouquíssimas situações.")
        st.write("- **ÀS VEZES:** ocorre em algumas situações, mas não é frequente.")
        st.write("- **FREQUENTEMENTE:** ocorre na maioria das situações.")
        st.write("- **SEMPRE:** ocorre em todas as situações.")
    st.warning("**AVALIAÇÃO ANÔNIMA:** Coleta estritamente anônima e protegida.")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Resultados"])

# DICIONÁRIOS DE ESCALAS
esc_padrao = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca"]
esc_saude = ["Excelente", "Muito Boa", "Boa", "Razoável", "Deficitária"]

# MAPAS DE PESOS
map_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca": 0}
map_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca": 100}
map_saude_val = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

with tab1:
    with st.form("form_v27_5", clear_on_submit=True):
        st.markdown("### Identificação Geral")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:").strip()
        with c2: setr = st.text_input("Setor:").strip()
        with c3: func = st.text_input("Função (Opcional):").strip()
        with c4: idade_val = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        col_a, col_b = st.columns(2)
        with col_a:
            st.info("### 1. CARGA E EXIGÊNCIAS")
            q1 = st.radio("**1. O seu trabalho fica acumulado por má divisão?**", esc_padrao, index=None)
            q2 = st.radio("**2. Falta tempo para terminar suas tarefas?**", esc_padrao, index=None)
            q3 = st.radio("**3. Precisa trabalhar em ritmo acelerado?**", esc_padrao, index=None)
            q4 = st.radio("**4. O serviço exige atenção total o tempo todo?**", esc_padrao, index=None)
            q5 = st.radio("**5. Precisa tomar decisões muito difíceis?**", esc_padrao, index=None)
            q6 = st.radio("**6. O trabalho é cansativo emocionalmente?**", esc_padrao, index=None)
            st.info("### 2. SUA AUTONOMIA")
            q7 = st.radio("**7. Consegue decidir como fazer as tarefas?**", esc_padrao, index=None)
            q8 = st.radio("**8. O trabalho exige iniciativa própria?**", esc_padrao, index=None)
            q9 = st.radio("**9. Consegue aprender coisas novas?**", esc_padrao, index=None)
            st.info("### 3. COMUNICAÇÃO")
            q10 = st.radio("**10. Avisado sobre mudanças e planos futuros?**", esc_padrao, index=None)
            q11 = st.radio("**11. Recebe informações necessárias?**", esc_padrao, index=None)
            q12 = st.radio("**12. Sabe exatamente suas responsabilidades?**", esc_padrao, index=None)
            st.info("### 4. LIDERANÇA")
            q13 = st.radio("**13. A chefia valoriza o que você faz?**", esc_padrao, index=None)
            q14 = st.radio("**14. É tratado de forma justa?**", esc_padrao, index=None)
            q15 = st.radio("**15. O chefe apoia você quando precisa?**", esc_padrao, index=None)
            q16 = st.radio("**16. Existe bom relacionamento com os colegas?**", esc_padrao, index=None)
            q17 = st.radio("**17. A chefia incentiva seu desenvolvimento?**", esc_padrao, index=None)
            q18 = st.radio("**18. O chefe sabe planejar bem o trabalho?**", esc_padrao, index=None)
            q19 = st.radio("**19. A gerência confia nos funcionários?**", esc_padrao, index=None)
            q20 = st.radio("**20. Você confia nas informações da gerência?**", esc_padrao, index=None)
            q21 = st.radio("**21. Os conflitos são resolvidos justamente?**", esc_padrao, index=None)
            q22 = st.radio("**22. O trabalho é dividido igualmente?**", esc_padrao, index=None)
            
        with col_b:
            st.success("### 5. SATISFAÇÃO")
            q23 = st.radio("**23. Consegue resolver os problemas do dia a dia?**", esc_padrao, index=None)
            q24 = st.radio("**24. O trabalho tem significado importante para você?**", esc_padrao, index=None)
            q25 = st.radio("**25. Sente que o que faz é importante?**", esc_padrao, index=None)
            q26 = st.radio("**26. Sente que os problemas da empresa são seus?**", esc_padrao, index=None)
            q27 = st.radio("**27. No geral, o quanto está satisfeito?**", esc_padrao, index=None)
            st.success("### 6. SEGURANÇA E SAÚDE")
            q28 = st.radio("**28. Tem medo de perder o emprego?**", esc_padrao, index=None)
            q29 = st.radio("**29. Como você avalia a sua saúde em geral?**", esc_saude, index=None)
            st.success("### 7. VIDA PESSOAL")
            q30 = st.radio("**30. O trabalho tira energia da vida privada?**", esc_padrao, index=None)
            q31 = st.radio("**31. O trabalho toma muito do seu tempo livre?**", esc_padrao, index=None)
            st.error("### 8. BEM-ESTAR")
            q32 = st.radio("**32. Teve dificuldade para dormir?**", esc_padrao, index=None)
            q33 = st.radio("**33. Sentiu-se esgotado fisicamente?**", esc_padrao, index=None)
            q34 = st.radio("**34. Sentiu-se esgotado emocionalmente?**", esc_padrao, index=None)
            q35 = st.radio("**35. Sentiu-se irritado com facilidade?**", esc_padrao, index=None)
            q36 = st.radio("**36. Sentiu-se ansioso?**", esc_padrao, index=None)
            q37 = st.radio("**37. Sentiu-se triste?**", esc_padrao, index=None)
            st.error("### 9. COMPORTAMENTO OFENSIVO") 
            q38 = st.radio("**38. Alvo de insultos ou provocações?**", esc_padrao, index=None)
            q39 = st.radio("**39. Alvo de investidas sexuais indesejadas?**", esc_padrao, index=None)
            q40 = st.radio("**40. Sofreu ameaças de violência?**", esc_padrao, index=None)
            q41 = st.radio("**41. Sofreu agressão física?**", esc_padrao, index=None)

        if st.form_submit_button("✅ ENVIAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Responda todas as 41 questões.")
            else:
                try:
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
                        "Satisfacao": v_sat, "Saude_Geral": v_sg, "Saude_Mental": v_men, "Ofensivo": v_ofe
                    }])
                    df_b = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                    st.success("✅ DADOS GRAVADOS!")
                    st.balloons()
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL ---
with tab2:
    st.subheader("🔐 Painel de Gestão HMM")
    acesso = st.text_input("Senha:", type="password")
    if acesso == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            # CORREÇÃO DO ERRO: Uso do .str antes do .strip()
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            emp_sel = st.selectbox("Cliente:", sorted(df['Empresa'].unique()), index=None)
            if emp_sel:
                df_f = df[df['Empresa'] == emp_sel]
                set_sel = st.multiselect("Setores:", sorted(df_f['Setor'].unique()))
                if set_sel: df_f = df_f[df_f['Setor'].isin(set_sel)]
                
                m = df_f[['Demanda', 'Controle', 'Lideranca', 'Satisfacao', 'Saude_Mental', 'Ofensivo']].mean()
                fig = px.line_polar(r=m.values, theta=m.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', fillcolor='rgba(255, 0, 0, 0.3)', line_color='red')
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📋 Parecer Técnico")
                if 'Saude_Geral' in df_f.columns:
                    val_sg = df_f['Saude_Geral'].mean()
                    if not pd.isna(val_sg): st.info(f"📌 Autopercepção de Saúde Geral: {val_sg:.1f}")

                acoes = {
                    "Demanda": {"baixo": "Monitorar carga.", "medio": "Revisar fluxos.", "alto": "Reduzir carga."},
                    "Controle": {"baixo": "Boa autonomia.", "medio": "Aumentar participação.", "alto": "Intervir na autonomia."},
                    "Lideranca": {"baixo": "Liderança ok.", "medio": "Treinar gestores.", "alto": "Reciclar gestão."},
                    "Satisfacao": {"baixo": "Engajamento bom.", "medio": "Valorizar equipe.", "alto": "Risco de turnover."},
                    "Saude_Mental": {"baixo": "Saúde ok.", "medio": "Pausas ativas.", "alto": "Apoio psicológico."}
                }
                for dim, valor in m.items():
                    if dim == "Ofensivo":
                        if valor > 0: st.error(f"🚨 {dim}: {valor:.1f} - CRÍTICO"); st.caption("👉 Auditoria Ética.")
                        else: st.success(f"✅ {dim}: {valor:.1f} - CONFORMIDADE")
                    else:
                        cor = "green" if valor < 33 else "orange" if valor < 66 else "red"
                        faixa = "baixo" if valor < 33 else "medio" if valor < 66 else "alto"
                        st.markdown(f"**{dim}:** :{cor}[{valor:.1f}]")
                        if dim in acoes: st.caption(f"👉 Ação: {acoes[dim][faixa]}")
                    st.markdown("---")
        else: st.info("Sem dados.")

st.markdown("---")
st.caption("© 2026 HMM Serviços - Engenharia de Segurança do Trabalho.")
