import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS HMM
st.set_page_config(page_title="HMM - Gestão Ocupacional V27.7", layout="wide")

# --- BLOCO DE ESTILO (BLINDAGEM TOTAL DESKTOP & MOBILE) ---
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
st.markdown(f"**Responsável Técnico:** Henrique Motta de Miranda | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
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
    st.warning("**AVALIAÇÃO ANÔNIMA:** Coleta estritamente anônima e protegida conforme normas de ética laboral.")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Resultados"])

# DICIONÁRIOS DE ESCALAS
esc_padrao = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca"]
esc_saude = ["Excelente", "Muito Boa", "Boa", "Razoável", "Deficitária"]

# MAPAS DE PESOS (Lógica HMM: Direto para Risco / Inverso para Proteção)
map_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca": 0}
map_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca": 100}
map_saude_val = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

with tab1:
    # FORMULÁRIO EM COLUNA ÚNICA PARA MELHOR FOCO E UX
    with st.form("form_v27_7", clear_on_submit=True):
        st.markdown("### 1️⃣ Identificação Geral")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:").strip()
        with c2: setr = st.text_input("Setor:").strip()
        with c3: func = st.text_input("Função (Opcional):").strip()
        with c4: idade_val = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        st.markdown("---")
        
        st.info("### 1. CARGA E EXIGÊNCIAS (Demandas do Trabalho)")
        q1 = st.radio("**1. O seu trabalho fica acumulado por má divisão?**", esc_padrao, index=None)
        q2 = st.radio("**2. Com que frequência falta tempo para terminar todas as tarefas?**", esc_padrao, index=None)
        q3 = st.radio("**3. Você precisa trabalhar num ritmo muito acelerado?**", esc_padrao, index=None)
        q4 = st.radio("**4. O serviço exige a sua atenção constante e total?**", esc_padrao, index=None)
        q5 = st.radio("**5. No seu dia a dia, precisa de tomar decisões muito difíceis?**", esc_padrao, index=None)
        q6 = st.radio("**6. Considera o seu trabalho cansativo do ponto de vista emocional?**", esc_padrao, index=None)
        
        st.info("### 2. SUA AUTONOMIA (Controle sobre o Trabalho)")
        q7 = st.radio("**7. Consegue decidir como ou de que forma faz as suas tarefas?**", esc_padrao, index=None)
        q8 = st.radio("**8. O seu trabalho exige que você tenha iniciativa própria?**", esc_padrao, index=None)
        q9 = st.radio("**9. No seu serviço, você consegue aprender coisas novas?**", esc_padrao, index=None)
        
        st.info("### 3. COMUNICAÇÃO ORGANIZACIONAL")
        q10 = st.radio("**10. É avisado com antecedência sobre mudanças e planos futuros?**", esc_padrao, index=None)
        q11 = st.radio("**11. Recebe todas as informações de que necessita para trabalhar bem?**", esc_padrao, index=None)
        q12 = st.radio("**12. Sabe exatamente quais são as suas responsabilidades?**", esc_padrao, index=None)
        
        st.info("### 4. LIDERANÇA E RELAÇÕES SOCIAIS")
        q13 = st.radio("**13. A chefia/gerência valoriza e aprecia o que você faz?**", esc_padrao, index=None)
        q14 = st.radio("**14. Você é tratado de forma justa no seu local de trabalho?**", esc_padrao, index=None)
        q15 = st.radio("**15. O seu superior imediato apoia você quando precisa?**", esc_padrao, index=None)
        q16 = st.radio("**16. Existe um bom relacionamento entre você e os seus colegas?**", esc_padrao, index=None)
        q17 = st.radio("**17. A chefia incentiva o seu desenvolvimento profissional?**", esc_padrao, index=None)
        q18 = st.radio("**18. Considera que o seu chefe planeja bem o trabalho?**", esc_padrao, index=None)
        q19 = st.radio("**19. A gerência confia nos funcionários para fazerem bem o serviço?**", esc_padrao, index=None)
        q20 = st.radio("**20. Você confia nas informações que recebe da gerência?**", esc_padrao, index=None)
        q21 = st.radio("**21. Os problemas e conflitos são resolvidos de forma justa?**", esc_padrao, index=None)
        q22 = st.radio("**22. Considera que o trabalho é dividido de forma igualitária?**", esc_padrao, index=None)
        
        st.success("### 5. SATISFAÇÃO E SIGNIFICADO")
        q23 = st.radio("**23. Sente-se capaz de resolver os problemas se tentar o suficiente?**", esc_padrao, index=None)
        q24 = st.radio("**24. O seu trabalho tem um significado importante para si?**", esc_padrao, index=None)
        q25 = st.radio("**25. Sente que aquilo que você faz na empresa é importante?**", esc_padrao, index=None)
        q26 = st.radio("**26. Sente que os problemas da empresa são seus também?**", esc_padrao, index=None)
        q27 = st.radio("**27. No geral, o quanto está satisfeito com o seu trabalho?**", esc_padrao, index=None)
        
        st.success("### 6. SEGURANÇA E SAÚDE")
        q28 = st.radio("**28. Sente-se preocupado ou com medo de perder o emprego?**", esc_padrao, index=None)
        q29 = st.radio("**29. De uma forma geral, como avalia a sua saúde hoje?**", esc_saude, index=None)
        
        st.success("### 7. INTERFACE TRABALHO-VIDA PRIVADA")
        q30 = st.radio("**30. O trabalho tira-lhe energia que afeta a sua vida privada?**", esc_padrao, index=None)
        q31 = st.radio("**31. O trabalho toma-lhe muito do tempo da sua vida privada?**", esc_padrao, index=None)
        
        st.error("### 8. BEM-ESTAR E SAÚDE MENTAL (Últimas 4 semanas)")
        q32 = st.radio("**32. Teve dificuldade em adormecer ou dormir seguido?**", esc_padrao, index=None)
        q33 = st.radio("**33. Sentiu-se exausto fisicamente?**", esc_padrao, index=None)
        q34 = st.radio("**34. Sentiu-se exausto emocionalmente?**", esc_padrao, index=None)
        q35 = st.radio("**35. Sentiu-se irritado com facilidade?**", esc_padrao, index=None)
        q36 = st.radio("**36. Sentiu-se ansioso ou tenso?**", esc_padrao, index=None)
        q37 = st.radio("**37. Sentiu-se triste ou em baixo?**", esc_padrao, index=None)
        
        st.error("### 9. COMPORTAMENTO OFENSIVO") 
        q38 = st.radio("**38. Foi alvo de insultos ou provocações verbais?**", esc_padrao, index=None)
        q39 = st.radio("**39. Foi exposto a investidas sexuais indesejadas?**", esc_padrao, index=None)
        q40 = st.radio("**40. Sofreu ameaças de violência no trabalho?**", esc_padrao, index=None)
        q41 = st.radio("**41. Sofreu algum tipo de agressão física?**", esc_padrao, index=None)

        st.markdown("---")
        if st.form_submit_button("✅ FINALIZAR E ENVIAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Por favor, responda a todas as 41 questões e preencha Empresa/Setor.")
            else:
                try:
                    # CÁLCULOS MÉTRICOS HMM (Normalizados 0-100)
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
                    st.success("✅ DIAGNÓSTICO ENVIADO COM SUCESSO!")
                    st.balloons()
                except Exception as e: st.error(f"Erro de conexão: {e}")

# --- ABA 2: PAINEL DE GESTÃO ---
with tab2:
    st.subheader("🔐 Painel de Consultoria HMM")
    acesso = st.text_input("Senha de Acesso:", type="password")
    if acesso == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            emp_sel = st.selectbox("Selecione o Cliente:", sorted(df['Empresa'].unique()), index=None)
            if emp_sel:
                df_f = df[df['Empresa'] == emp_sel]
                set_sel = st.multiselect("Filtrar Setores:", sorted(df_f['Setor'].unique()))
                if set_sel: df_f = df_f[df_f['Setor'].isin(set_sel)]
                
                # Gráfico Radar de Síntese
                m = df_f[['Demanda', 'Controle', 'Lideranca', 'Satisfacao', 'Saude_Mental', 'Ofensivo']].mean()
                fig = px.line_polar(r=m.values, theta=m.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', fillcolor='rgba(255, 0, 0, 0.3)', line_color='red')
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📋 Parecer Técnico de Prevenção")
                if 'Saude_Geral' in df_f.columns:
                    val_sg = df_f['Saude_Geral'].mean()
                    if not pd.isna(val_sg): st.info(f"📌 Autopercepção de Saúde Geral: {val_sg:.1f}")

                acoes = {
                    "Demanda": {"baixo": "Monitorar carga atual.", "medio": "Revisar fluxos e prazos.", "alto": "Reduzir carga urgente."},
                    "Controle": {"baixo": "Manter autonomia técnica.", "medio": "Aumentar participação decisória.", "alto": "Intervir na autonomia operacional."},
                    "Lideranca": {"baixo": "Liderança em conformidade.", "medio": "Treinar gestores em Soft Skills.", "alto": "Reciclar suporte social e gestão."},
                    "Satisfacao": {"baixo": "Bom engajamento.", "medio": "Reforçar valorização e feedback.", "alto": "Risco crítico de turnover."},
                    "Saude_Mental": {"baixo": "Indicadores estáveis.", "medio": "Implementar pausas ativas.", "alto": "Apoio psicossocial imediato."}
                }
                for dim, valor in m.items():
                    if dim == "Ofensivo":
                        if valor > 0: st.error(f"🚨 {dim}: {valor:.1f} - CRÍTICO (ÉTICA)"); st.caption("👉 Ação: Auditoria e reforço do Código de Conduta.")
                        else: st.success(f"✅ {dim}: {valor:.1f} - CONFORMIDADE ÉTICA")
                    else:
                        cor = "green" if valor < 33.4 else "orange" if valor < 66.7 else "red"
                        faixa = "baixo" if valor < 33.4 else "medio" if valor < 66.7 else "alto"
                        st.markdown(f"**{dim}:** :{cor}[{valor:.1f}]")
                        if dim in acoes: st.caption(f"👉 Ação Recomendada: {acoes[dim][faixa]}")
                    st.markdown("---")
        else: st.info("Aguardando registros na base de dados.")

st.markdown("---")
st.caption("© 2026 HMM Serviços - Engenharia de Segurança do Trabalho.")
