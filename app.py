import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS E CONEXÃO
st.set_page_config(page_title="HMM - Gestão V24.9", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO PROFISSIONAL ---
st.title("Avaliação de Riscos Psicossociais")
st.subheader("HMM Serviços - Engenharia de Segurança do Trabalho")
st.markdown(f"**Responsável Técnico:** Henrique Motta de Miranda | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

st.warning("⚠️ **AVALIAÇÃO ANÔNIMA:** Coleta realizada de forma estritamente anônima. Sigilo garantido pela HMM Serviços.")

tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Resultados"])

# --- DICIONÁRIOS DE ESCALAS ---
esc_padrao = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca / Quase nunca"]
esc_assedio = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca"]

map_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0, "Nunca": 0}
map_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}

with tab1:
    with st.form("form_v24_9", clear_on_submit=True):
        st.markdown("### Identificação Geral")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:")
        with c2: setr = st.text_input("Setor:")
        with c3: func = st.text_input("Função (Opcional):")
        with c4: idade_val = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        col_a, col_b = st.columns(2)
        with col_a:
            st.info("### 1. CARGA E EXIGÊNCIAS")
            q1 = st.radio("**1. Trabalho acumulado por má divisão?**", esc_padrao, index=None)
            q2 = st.radio("**2. Falta tempo para as tarefas?**", esc_padrao, index=None)
            q3 = st.radio("**3. Ritmo de trabalho acelerado?**", esc_padrao, index=None)
            q4 = st.radio("**4. Atenção total constante?**", esc_padrao, index=None)
            q5 = st.radio("**5. Decisões muito difíceis?**", esc_padrao, index=None)
            q6 = st.radio("**6. Trabalho emocionalmente cansativo?**", esc_padrao, index=None)
            st.info("### 2. SUA AUTONOMIA")
            q7 = st.radio("**7. Decide como fazer suas tarefas?**", esc_padrao, index=None)
            q8 = st.radio("**8. Exige muita iniciativa própria?**", esc_padrao, index=None)
            q9 = st.radio("**9. Consegue aprender coisas novas?**", esc_padrao, index=None)
            st.info("### 3. COMUNICAÇÃO")
            q10 = st.radio("**10. Avisado sobre mudanças e planos?**", esc_padrao, index=None)
            q11 = st.radio("**11. Recebe informações necessárias?**", esc_padrao, index=None)
            q12 = st.radio("**12. Sabe suas responsabilidades?**", esc_padrao, index=None)
            st.info("### 4. LIDERANÇA")
            q13 = st.radio("**13. Chefia valoriza seu trabalho?**", esc_padrao, index=None)
            q14 = st.radio("**14. Tratado de forma justa?**", esc_padrao, index=None)
            q15 = st.radio("**15. Recebe apoio do superior?**", esc_padrao, index=None)
            q16 = st.radio("**16. Bom ambiente com colegas?**", esc_padrao, index=None)
            q17 = st.radio("**17. Incentivo ao desenvolvimento?**", esc_padrao, index=None)
            q18 = st.radio("**18. Chefe planeja bem o trabalho?**", esc_padrao, index=None)
            q19 = st.radio("**19. Gerência confia na equipe?**", esc_padrao, index=None)
            q20 = st.radio("**20. Confia na gerência?**", esc_padrao, index=None)
            q21 = st.radio("**21. Conflitos resolvidos justamente?**", esc_padrao, index=None)
            q22 = st.radio("**22. Trabalho dividido igualmente?**", esc_padrao, index=None)
        with col_b:
            st.success("### 5. SATISFAÇÃO")
            q23 = st.radio("**23. Capaz de resolver problemas?**", esc_padrao, index=None)
            q24 = st.radio("**24. Trabalho com significado real?**", esc_padrao, index=None)
            q25 = st.radio("**25. Sente que seu trabalho é importante?**", esc_padrao, index=None)
            q26 = st.radio("**26. Problemas da empresa são seus?**", esc_padrao, index=None)
            q27 = st.radio("**27. Satisfação global com o trabalho?**", esc_padrao, index=None)
            st.success("### 6. SEGURANÇA E SAÚDE")
            q28 = st.radio("**28. Tem medo de ficar desempregado?**", esc_padrao, index=None)
            q29 = st.radio("**29. Como avalia sua saúde geral?**", esc_padrao, index=None)
            st.success("### 7. VIDA PRIVADA")
            q30 = st.radio("**30. Trabalho tira energia da vida privada?**", esc_padrao, index=None)
            q31 = st.radio("**31. Trabalho toma tempo da vida privada?**", esc_padrao, index=None)
            st.error("### 8. SAÚDE E BEM ESTAR")
            q32 = st.radio("**32. Dificuldade para dormir?**", esc_padrao, index=None)
            q33 = st.radio("**33. Sentiu esgotamento físico?**", esc_padrao, index=None)
            q34 = st.radio("**34. Sentiu esgotar emocionalmente?**", esc_padrao, index=None)
            q35 = st.radio("**35. Sentiu irritação frequente?**", esc_padrao, index=None)
            q36 = st.radio("**36. Sentiu ansiedade?**", esc_padrao, index=None)
            q37 = st.radio("**37. Sentiu tristeza?**", esc_padrao, index=None)
            st.error("### 9. COMPORTAMENTO OFENSIVO")
            q38 = st.radio("**38. Alvo de insultos ou provocações?**", esc_assedio, index=None)
            q39 = st.radio("**39. Exposto a assédio sexual?**", esc_assedio, index=None)
            q40 = st.radio("**40. Sofreu ameaças de violência?**", esc_assedio, index=None)
            q41 = st.radio("**41. Sofreu agressão física?**", esc_assedio, index=None)

        if st.form_submit_button("✅ GRAVAR DIAGNÓSTICO"):
            resps = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
            if None in resps or not emp or not setr:
                st.error("⚠️ Responda todas as perguntas.")
            else:
                try:
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
                    st.balloons()
                except Exception as e: st.error(f"Erro: {e}")

# --- ABA 2: PAINEL DE GESTÃO ---
with tab2:
    st.subheader("🔐 Painel do Consultor HMM")
    acesso = st.text_input("Senha de Acesso:", type="password", key="pwd_v24_9")
    if acesso == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            df['Setor'] = df['Setor'].astype(str).str.strip()
            emp_sel = st.selectbox("Selecione o Cliente:", sorted(df['Empresa'].unique()), index=None)
            if emp_sel:
                lista_set = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                set_sel = st.multiselect("Filtrar Setores:", lista_set)
                df_f = df[df['Empresa'] == emp_sel]
                if set_sel: df_f = df_f[df_f['Setor'].isin(set_sel)]
                m = df_f[['Demanda', 'Controle', 'Lideranca', 'Satisfacao', 'Saude_Mental', 'Ofensivo']].mean()
                
                fig = px.line_polar(r=m.values, theta=m.index, line_close=True, range_r=[0,100])
                fig.update_traces(fill='toself', line_color='red', fillcolor='rgba(255, 0, 0, 0.3)')
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📋 Médias e Sugestões Técnicas")
                for dim, valor in m.items():
                    cor = "green" if valor < 33 else "orange" if valor < 66 else "red"
                    
                    # AJUSTE DA REGRA DO ITEM 09 (OFENSIVO): TOLERÂNCIA ZERO
                    if dim == "Ofensivo" and valor > 0:
                        st.error(f"🚨 **{dim}: {valor:.1f} - OBSERVAÇÃO RÁPIDA (CRÍTICO)**")
                        st.caption("👉 **Ação Imediata:** Realizar auditoria ética, reforçar canal de denúncias e treinamento anti-assédio.")
                    else:
                        st.markdown(f"**{dim}:** :{cor}[{valor:.1f}]")
                        if valor > 33:
                            if dim == "Demanda": st.caption("👉 **Atenção:** Revisar distribuição de carga e prazos.")
                            if dim == "Controle": st.caption("👉 **Atenção:** Fomentar autonomia técnica e decisões participativas.")
                            if dim == "Lideranca": st.caption("👉 **Atenção:** Treinamento de Soft Skills e feedback.")
                            if dim == "Satisfacao": st.caption("👉 **Atenção:** Planos de reconhecimento e valorização.")
                            if dim == "Saude_Mental": st.caption("👉 **Atenção:** Monitoramento de fadiga e saúde mental.")
                    st.markdown("---")
        else: st.warning("Aguardando registros.")

# --- RODAPÉ ---
st.markdown("---")
st.caption("© 2026 HMM Serviços - Engenharia de Segurança do Trabalho. Todos os direitos reservados.")
