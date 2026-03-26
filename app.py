import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS E CONEXÃO
st.set_page_config(page_title="HMM - Gestão V24.5", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO PROFISSIONAL ---
st.title("🚀 Diagnóstico de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.markdown(f"**Responsável Técnico:** Eng. Henrique | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# --- AVISO DE ANONIMATO ---
st.warning("🔒 **AVALIAÇÃO ANÔNIMA:** Esta coleta de dados é realizada de forma estritamente anônima. "
           "As respostas são tratadas de forma coletiva, garantindo o sigilo do respondente.")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta (41 Itens)", "📊 Painel de Resultados & Plano de Ação"])

# --- DICIONÁRIOS DE ESCALAS PADRONIZADAS ---
# Escala Geral (Frequência, Intensidade e Saúde agora unificadas visualmente)
esc_padrao = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca / Quase nunca"]

# Escala Exclusiva para Comportamentos Ofensivos (Sem o 'quase nunca')
esc_assedio = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca"]

# Mapeamento Matemático (Invisível para o usuário)
map_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0, "Nunca": 0}
map_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}

with tab1:
    with st.form("form_v24_5", clear_on_submit=True):
        st.markdown("### 📋 Identificação Geral")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:")
        with c2: setr = st.text_input("Setor:")
        with c3: func = st.text_input("Função (Opcional):")
        with c4: idade_val = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        col_a, col_b = st.columns(2)
        with col_a:
            st.info("### 1. CARGA E EXIGÊNCIAS")
            q1 = st.radio("**1. O seu trabalho fica acumulado porque as tarefas são mal divididas?**", esc_padrao, index=None)
            q2 = st.radio("**2. Com que frequência falta tempo para você terminar tudo?**", esc_padrao, index=None)
            q3 = st.radio("**3. Você precisa trabalhar em um ritmo muito acelerado?**", esc_padrao, index=None)
            q4 = st.radio("**4. O seu serviço exige atenção total o tempo todo?**", esc_padrao, index=None)
            q5 = st.radio("**5. Você precisa tomar decisões muito difíceis no dia a dia?**", esc_padrao, index=None)
            q6 = st.radio("**6. O seu trabalho é cansativo do ponto de vista emocional?**", esc_padrao, index=None)
            st.info("### 2. SUA AUTONOMIA")
            q7 = st.radio("**7. Você consegue decidir como fazer as suas tarefas?**", esc_padrao, index=None)
            q8 = st.radio("**8. O seu trabalho exige que você tenha iniciativa própria?**", esc_padrao, index=None)
            q9 = st.radio("**9. No seu serviço, você consegue aprender coisas novas?**", esc_padrao, index=None)
            st.info("### 3. COMUNICAÇÃO")
            q10 = st.radio("**10. Avisado com antecedência sobre mudanças e planos da empresa?**", esc_padrao, index=None)
            q11 = st.radio("**11. Recebe as informações que precisa para trabalhar bem?**", esc_padrao, index=None)
            q12 = st.radio("**12. Você sabe exatamente quais são as suas responsabilidades?**", esc_padrao, index=None)
            st.info("### 4. LIDERANÇA")
            q13 = st.radio("**13. A chefia reconhece e valoriza o que você faz?**", esc_padrao, index=None)
            q14 = st.radio("**14. Você sente que é tratado de forma justa na empresa?**", esc_padrao, index=None)
            q15 = st.radio("**15. O seu chefe ajuda e apoia você quando precisa?**", esc_padrao, index=None)
            q16 = st.radio("**16. Existe um bom relacionamento entre você e seus colegas?**", esc_padrao, index=None)
            q17 = st.radio("**17. A chefia incentiva o seu desenvolvimento profissional?**", esc_padrao, index=None)
            q18 = st.radio("**18. O seu chefe sabe planejar bem o trabalho da equipe?**", esc_padrao, index=None)
            q19 = st.radio("**19. A gerência confia que os funcionários fazem um bom trabalho?**", esc_padrao, index=None)
            q20 = st.radio("**20. Você confia nas informações que recebe da gerência?**", esc_padrao, index=None)
            q21 = st.radio("**21. Os problemas no setor são resolvidos de forma justa?**", esc_padrao, index=None)
            q22 = st.radio("**22. O trabalho é dividido de forma igual entre as pessoas?**", esc_padrao, index=None)
        with col_b:
            st.success("### 5. SATISFAÇÃO")
            q23 = st.radio("**23. Você se sente capaz de resolver os problemas que aparecem?**", esc_padrao, index=None)
            q24 = st.radio("**24. O seu trabalho tem um significado importante para você?**", esc_padrao, index=None)
            q25 = st.radio("**25. Você sente que o que você faz é importante?**", esc_padrao, index=None)
            q26 = st.radio("**26. Você sente que os problemas da empresa também são seus?**", esc_padrao, index=None)
            q27 = st.radio("**27. No geral, o quanto você está satisfeito com seu trabalho?**", esc_padrao, index=None)
            st.success("### 6. SEGURANÇA E SAÚDE")
            q28 = st.radio("**28. Você sente medo de perder o emprego?**", esc_padrao, index=None)
            q29 = st.radio("**29. De forma geral, como você avalia a sua saúde?**", esc_padrao, index=None)
            st.success("### 7. TRABALHO E VIDA PESSOAL")
            q30 = st.radio("**30. O trabalho tira a energia da sua vida particular?**", esc_padrao, index=None)
            q31 = st.radio("**31. O trabalho toma muito do seu tempo privado?**", esc_padrao, index=None)
            st.error("### 8. COMO VOCÊ SE SENTE")
            q32 = st.radio("**32. Teve dificuldade para dormir ou acordou muito à noite?**", esc_padrao, index=None)
            q33 = st.radio("**33. Sentiu-se esgotado fisicamente?**", esc_padrao, index=None)
            q34 = st.radio("**34. Sentiu-se esgotado emocionalmente?**", esc_padrao, index=None)
            q35 = st.radio("**35. Sentiu-se irritado com facilidade?**", esc_padrao, index=None)
            q36 = st.radio("**36. Sentiu-se ansioso?**", esc_padrao, index=None)
            q37 = st.radio("**37. Sentiu-se triste?**", esc_padrao, index=None)
            st.error("### 9. ÉTICA E OFENSIVO")
            q38 = st.radio("**38. Foi alvo de insultos ou provocações verbais?**", esc_assedio, index=None)
            q39 = st.radio("**39. Passou por situação de assédio sexual indesejado?**", esc_assedio, index=None)
            q40 = st.radio("**40. Sofreu ameaças de violência?**", esc_assedio, index=None)
            q41 = st.radio("**41. Sofreu algum tipo de agressão física?**", esc_assedio, index=None)

        if st.form_submit_button("✅ GRAVAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Responda todas as perguntas.")
            else:
                try:
                    # Cálculo Médias com Mapeamento Unificado
                    v_dem = (map_dir[q1]+map_dir[q2]+map_dir[q3]+map_dir[q4]+map_dir[q5]+map_dir[q6])/6
                    v_con = (map_inv[q7]+map_inv[q8]+map_inv[q9])/3
                    v_lid = (map_inv[q13]+map_inv[q14]+map_inv[q15]+map_inv[q16]+map_inv[q17]+map_inv[q18]+map_inv[q19]+map_inv[q20]+map_inv[q21]+map_inv[q22])/10
                    v_men = (map_dir[q32]+map_dir[q33]+map_dir[q34]+map_dir[q35]+map_dir[q36]+map_dir[q37])/6
                    v_ofe = (map_dir[q38]+map_dir[q39]+map_dir[q40]+map_dir[q41])/4
                    nova_linha = pd.DataFrame([{
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "Empresa": emp.strip(), "Setor": setr.strip(), "Funcao": func.strip(), "Idade": idade_val,
                        "Demanda": v_dem, "Controle": v_con, "Lideranca": v_lid,
                        "Satisfacao": map_dir[q27], "Saude_Geral": map_dir[q29], 
                        "Saude_Mental": v_men, "Ofensivo": v_ofe
                    }])
                    df_b = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                    st.success("✅ DADOS GRAVADOS COM SUCESSO!")
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE GESTÃO (MANTIDO) ---
with tab2:
    st.subheader("🔐 Painel do Consultor HMM")
    acesso = st.text_input("Senha:", type="password", key="pwd_v24_5")
    if acesso == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            df['Setor'] = df['Setor'].astype(str).str.strip()
            emp_sel = st.selectbox("Selecione o Cliente:", sorted(df['Empresa'].unique()), index=None)
            if emp_sel:
                lista_set = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                set_sel = st.multiselect("Setores:", lista_set)
                df_f = df[df['Empresa'] == emp_sel]
                if set_sel: df_f = df_f[df_f['Setor'].isin(set_sel)]
                m = df_f[['Demanda', 'Controle', 'Lideranca', 'Satisfacao', 'Saude_Mental', 'Ofensivo']].mean()
                
                fig = px.line_polar(r=m.values, theta=m.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', line_color='red', fillcolor='rgba(255, 0, 0, 0.3)')
                st.plotly_chart(fig, use_container_width=True)

                for dim, valor in m.items():
                    cor = "green" if valor < 33 else "orange" if valor < 66 else "red"
                    st.markdown(f"**{dim}:** :{cor}[{valor:.1f}]")
                    if valor > 33:
                        if dim == "Demanda": st.caption("👉 **Atenção:** Revisar distribuição de carga e prazos.")
                        if dim == "Lideranca": st.caption("👉 **Atenção:** Treinamento de Soft Skills para gestores.")
                        if dim == "Ofensivo": st.caption("👉 **Crítico:** Implementar Compliance e Canal de Denúncias.")
                    st.markdown("---")
        else: st.warning("Aguardando registros.")

# --- RODAPÉ ---
st.markdown("---")
st.caption("© 2026 HMM Serviços - Engenharia e Segurança do Trabalho. Todos os direitos reservados.")
