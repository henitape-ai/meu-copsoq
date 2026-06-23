import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import numpy as np

# 1. CONFIGURAÇÕES TÉCNICAS HMM
st.set_page_config(page_title="HMM - Gestão Ocupacional V37.0", layout="wide")

# --- BLOCO DE ESTILO (BLINDAGEM E AJUSTE DE VISUALIZAÇÃO) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stAppDeployButton {display: none !important;}
            #stDecoration {display: none !important;}
            [data-testid="stStatusWidget"] {display: none !important;}
            .block-container { padding-top: 1rem !important; }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("Levantamento das Condições e Organização do Trabalho")
st.subheader("HMM Serviços - Engenharia de Segurança do Trabalho")
st.markdown(f"**Responsável Técnico:** Henrique Motta de Miranda | 🌐 [www.hmmservicos.com.br](http://www.hmmservicos.com.br)")
st.markdown("---")

# --- TEXTO DE BOAS-VINDAS E ORIENTAÇÕES FIXAS ---
with st.container():
    st.markdown("### Bem-vindo(a) à pesquisa sobre comportamentos no ambiente de trabalho!")
    st.warning("**AVALIAÇÃO ANÔNIMA:** Suas respostas são confidenciais e protegidas por algoritmos de integridade.")
    
    st.markdown("""
    <div style="border: 1px solid #e6e9ef; padding: 20px; border-radius: 10px; background-color: #f8f9fb; margin-bottom: 20px;">
        <h4 style="margin-top:0; color: #1f3d5a;"> Orientações sobre a Escala de Resposta:</h4>
        <p>Por favor, leia atentamente as opções antes de responder cada questão:</p>
        <ul style="list-style-type: none; padding-left: 0;">
            <li><b>• NUNCA:</b> não ocorre em nenhuma situação.</li>
            <li><b>• RARAMENTE:</b> ocorre em pouquíssimas situações.</li>
            <li><b>• ÀS VEZES:</b> ocorre em algumas situações.</li>
            <li><b>• FREQUENTEMENTE:</b> ocorre na maioria das situações.</li>
            <li><b>• SEMPRE:</b> ocorre em todas as situações.</li>
        </ul>
        <hr style="margin: 10px 0; border: 0.5px solid #d1d5db;">
        <small style="color: #6b7280;"><i><b>Este diagnóstico segue o protocolo internacional COPSOQ II. </i></small>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 Formulário de Coleta", "📊 Painel de Resultados"])

# DICIONÁRIOS DE ESCALAS
esc_padrao = ["Sempre", "Frequentemente", "As vezes", "Raramente", "Nunca"]
esc_saude = ["Excelente", "Muito Boa", "Boa", "Razoável", "Deficitária"]

# MAPAS DE PESOS (Lógica HMM)
map_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca": 0}
map_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca": 100}
map_saude_val = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

with tab1:
    with st.form("form_v37_0", clear_on_submit=False):
        st.markdown("### Identificação Geral")
        c1, c2, c3, c4 = st.columns(4)
        with c1: emp = st.text_input("Empresa Cliente:").strip()
        with c2: setr = st.text_input("Setor:").strip()
        with c3: func = st.text_input("Função:").strip()
        with c4: idade_val = st.number_input("Idade:", min_value=14, max_value=100, value=30)

        st.markdown("---")
        
        st.info("### 1. CARGA E EXIGÊNCIAS")
        q1 = st.radio("**1. O seu trabalho fica acumulado por má divisão?**", esc_padrao, index=None)
        q2 = st.radio("**2. Falta tempo para terminar suas tarefas?**", esc_padrao, index=None)
        q3 = st.radio("**3. Precisa trabalhar num ritmo muito acelerado?**", esc_padrao, index=None)
        q4 = st.radio("**4. O serviço exige a sua atenção constante e total?**", esc_padrao, index=None)
        q5 = st.radio("**5. No seu dia a dia, precisa de tomar decisões muito difíceis?**", esc_padrao, index=None)
        q6 = st.radio("**6. Considera o seu trabalho cansativo do ponto de vista emocional?**", esc_padrao, index=None)
        
        st.info("### 2. SUA AUTONOMIA")
        q7 = st.radio("**7. Consegue decidir como ou de que forma faz as suas tarefas?**", esc_padrao, index=None)
        q8 = st.radio("**8. O seu trabalho exige que você tenha iniciativa própria?**", esc_padrao, index=None)
        q9 = st.radio("**9. No seu serviço, você consegue aprender coisas novas?**", esc_padrao, index=None)
        
        st.info("### 3. COMUNICAÇÃO")
        q10 = st.radio("**10. É avisado com antecedência sobre mudanças e planos futuros?**", esc_padrao, index=None)
        q11 = st.radio("**11. Recebe todas as informações de que necessita?**", esc_padrao, index=None)
        q12 = st.radio("**12. Sabe exatamente quais são as suas responsabilidades?**", esc_padrao, index=None)
        
        st.info("### 4. LIDERANÇA")
        q13 = st.radio("**13. A chefia/gerência valoriza e aprecia o que você faz?**", esc_padrao, index=None)
        q14 = st.radio("**14. Você é tratado de forma justa no seu local de trabalho?**", esc_padrao, index=None)
        q15 = st.radio("**15. O seu superior imediato apoia você quando precisa?**", esc_padrao, index=None)
        q16 = st.radio("**16. Existe um bom relacionamento com os seus colegas?**", esc_padrao, index=None)
        q17 = st.radio("**17. A chefia incentiva o seu desenvolvimento profissional?**", esc_padrao, index=None)
        q18 = st.radio("**18. Considera que o seu chefe planeja bem o trabalho?**", esc_padrao, index=None)
        q19 = st.radio("**19. A gerência confia nos funcionários?**", esc_padrao, index=None)
        q20 = st.radio("**20. Você confia nas informações que recebe da gerência?**", esc_padrao, index=None)
        q21 = st.radio("**21. Os problemas e conflitos são resolvidos justamente?**", esc_padrao, index=None)
        q22 = st.radio("**22. Considera que o trabalho é dividido igualmente?**", esc_padrao, index=None)
        
        st.success("### 5. SATISFAÇÃO")
        q23 = st.radio("**23. Sente-se capaz de resolver os problemas do dia a dia?**", esc_padrao, index=None)
        q24 = st.radio("**24. O seu trabalho tem um significado importante para si?**", esc_padrao, index=None)
        q25 = st.radio("**25. Sente que aquilo que faz na empresa é importante?**", esc_padrao, index=None)
        q26 = st.radio("**26. Sente que os problemas da empresa são seus também?**", esc_padrao, index=None)
        q27 = st.radio("**27. No geral, o quanto está satisfeito com o trabalho?**", esc_padrao, index=None)
        
        st.success("### 6. SEGURANÇA E SAÚDE")
        q28 = st.radio("**28. Tem medo de perder o emprego?**", esc_padrao, index=None)
        q29 = st.radio("**29. Como avalia a sua saúde hoje?**", esc_saude, index=None)
        
        st.success("### 7. VIDA PRIVADA")
        q30 = st.radio("**30. O trabalho tira energia da sua vida privada?**", esc_padrao, index=None)
        q31 = st.radio("**31. O trabalho toma muito do tempo da sua vida privada?**", esc_padrao, index=None)
        
        st.error("### 8. BEM-ESTAR")
        q32 = st.radio("**32. Teve dificuldade em adormecer ou dormir?**", esc_padrao, index=None)
        q33 = st.radio("**33. Sentiu-se exausto fisicamente?**", esc_padrao, index=None)
        q34 = st.radio("**34. Sentiu-se exausto emocionalmente?**", esc_padrao, index=None)
        q35 = st.radio("**35. Sentiu-se irritado com facilidade?**", esc_padrao, index=None)
        q36 = st.radio("**36. Sentiu-se ansioso ou tenso?**", esc_padrao, index=None)
        q37 = st.radio("**37. Sentiu-se triste ou desanimado?**", esc_padrao, index=None)
        
        st.error("### 9. COMPORTAMENTO OFENSIVO") 
        q38 = st.radio("**38. Foi alvo de insultos ou provocações verbais?**", esc_padrao, index=None)
        q39 = st.radio("**39. Foi Exposto (a) a investidas sexuais indesejadas?**", esc_padrao, index=None)
        q40 = st.radio("**40. Sofreu ameaças de violência no trabalho?**", esc_padrao, index=None)
        q41 = st.radio("**41. Sofreu agressão física?**", esc_padrao, index=None)

        if st.form_submit_button("✅ ENVIAR DIAGNÓSTICO"):
            todas_respostas = {
                "Nome da Empresa": emp, "Setor": setr,
                "Questão 1": q1, "Questão 2": q2, "Questão 3": q3, "Questão 4": q4, "Questão 5": q5, "Questão 6": q6,
                "Questão 7": q7, "Questão 8": q8, "Questão 9": q9, "Questão 10": q10, "Questão 11": q11, "Questão 12": q12,
                "Questão 13": q13, "Questão 14": q14, "Questão 15": q15, "Questão 16": q16, "Questão 17": q17, "Questão 18": q18,
                "Questão 19": q19, "Questão 20": q20, "Questão 21": q21, "Questão 22": q22, "Questão 23": q23, "Questão 24": q24,
                "Questão 25": q25, "Questão 26": q26, "Questão 27": q27, "Questão 28": q28, "Questão 29": q29, "Questão 30": q30,
                "Questão 31": q31, "Questão 32": q32, "Questão 33": q33, "Questão 34": q34, "Questão 35": q35, "Questão 36": q36,
                "Questão 37": q37, "Questão 38": q38, "Questão 39": q39, "Questão 40": q40, "Questão 41": q41
            }
            
            faltantes = [campo for campo, valor in todas_respostas.items() if not valor]

            if faltantes:
                st.error(f"⚠️ **Erro no envio!** Por favor, responda os seguintes itens obrigatórios: \n\n {', '.join(faltantes)}")
            else:
                try:
                    gatilhos_ofensivos = ["Sempre", "Frequentemente", "As vezes", "Raramente"]
                    ofensivos_detalhados = []
                    if q38 in gatilhos_ofensivos: ofensivos_detalhados.append(f"Q38 ({q38})")
                    if q39 in gatilhos_ofensivos: ofensivos_detalhados.append(f"Q39 ({q39})")
                    if q40 in gatilhos_ofensivos: ofensivos_detalhados.append(f"Q40 ({q40})")
                    if q41 in gatilhos_ofensivos: ofensivos_detalhados.append(f"Q41 ({q41})")
                    
                    det_ofensivo = ", ".join(ofensivos_detalhados) if ofensivos_detalhados else "Nenhum desvio crítico"

                    resps_list = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24,q25,q26,q27,q28,q29,q30,q31,q32,q33,q34,q35,q36,q37,q38,q39,q40,q41]
                    pesos_val = [map_dir.get(q, 50) for q in resps_list if q in map_dir]
                    std_dev = np.std(pesos_val)
                    gap_info = abs(map_dir[q12] - map_dir[q11])
                    
                    status_int = "Confiável"
                    if std_dev < 10: status_int = "Inconsistente (Polarização)"
                    if gap_info > 75: status_int = "Inconsistente (Dissonância)"
                    
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
                        "Satisfacao": v_sat, "Saude_Geral": v_sg, "Saude_Mental": v_men, "Ofensivo": v_ofe,
                        "Integridade": status_int,
                        "Detalhe_Ofensivo": det_ofensivo
                    }])
                    df_b = conn.read(worksheet="Página1", ttl=0)
                    conn.update(worksheet="Página1", data=pd.concat([df_b, nova_linha], ignore_index=True))
                    st.success("DADOS GRAVADOS COM SUCESSO!")
                    st.balloons()
                except Exception as e: st.error(f"Erro na gravação: {e}")

# --- ABA 2: PAINEL DE GESTÃO (INTEGRANDO COPSOQ II + KARASEK) ---
with tab2:
    st.subheader("🔐 Painel de Consultoria Especializada HMM")
    if st.text_input("Senha de Acesso Profissional:", type="password") == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        if not df.empty:
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            
            st.sidebar.markdown("### Filtros de Auditoria")
            solo_confiavel = st.sidebar.checkbox("Excluir amostras inconsistentes", value=False)
            
            if solo_confiavel:
                if 'Integridade' in df.columns:
                    df = df[df['Integridade'] == "Confiável"]

            emp_sel = st.selectbox("Selecione o Cliente:", sorted(df['Empresa'].unique()), index=None)
            
            if emp_sel:
                df_f = df[df['Empresa'] == emp_sel]
                set_sel = st.multiselect("Filtrar por Setor:", sorted(df_f['Setor'].unique()))
                if set_sel: df_f = df_f[df_f['Setor'].isin(set_sel)]
                
                categorias = ['Demanda', 'Controle', 'Lideranca', 'Satisfacao', 'Saude_Mental', 'Ofensivo']
                m = df_f[categorias].mean()
                
                # Divisão visual em sub-abas no Painel
                p_tab1, p_tab2 = st.tabs(["📊 Protocolo COPSOQ II (NR-01)", "🧘 Matriz de Karasek (NR-17)"])
                
                with p_tab1:
                    st.markdown("### Gráfico Radar Psicossocial Organizacional")
                    fig = px.line_polar(r=m.values, theta=m.index, line_close=True, range_r=[0,100])
                    fig.update_traces(fill='toself', fillcolor='rgba(0, 0, 255, 0.2)', line_color='navy')
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                            angularaxis=dict(rotation=90, direction="clockwise", tickfont=dict(size=12))
                        ),
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("### 📋 Parecer de Nível de Risco Ocupacional (NR-01)")
                    if "Detalhe_Ofensivo" in df_f.columns:
                        alertas_reais = df_f[df_f['Detalhe_Ofensivo'] != "Nenhum desvio crítico"]['Detalhe_Ofensivo'].dropna()
                        if not alertas_reais.empty:
                            st.warning("⚠️ **Histórico de Condutas Inadequadas Sinalizadas na Base (Incluindo Nível Raramente):**")
                            for item in alertas_reais.unique():
                                st.write(f"• {item}")
                    
                    acoes_hmm = {
                        "Demanda": {"baixo": "Carga em conformidade.", "medio": "Revisar fluxos técnicos.", "alto": "Reduzir sobrecarga urgente."},
                        "Controle": {"baixo": "Autonomia preservada.", "medio": "Aumentar participação.", "alto": "Intervir na gestão técnica."},
                        "Lideranca": {"baixo": "Liderança protetiva.", "medio": "Treinar gestores.", "alto": "Reciclar suporte social."},
                        "Satisfacao": {"baixo": "Alto engajamento.", "medio": "Reforçar valorização.", "alto": "Risco de turnover/passivo."},
                        "Saude_Mental": {"baixo": "Indicadores estáveis.", "medio": "Pausas ativas sugeridas.", "alto": "Apoio psicossocial imediato."}
                    }
                    
                    for dim, valor in m.items():
                        if dim == "Ofensivo":
                            if valor > 0: st.error(f"🚨 **{dim}: {valor:.2f} - ALERTA ÉTICO**")
                            else: st.success(f"✅ **{dim}: {valor:.1f} - CONFORMIDADE ÉTICA**")
                        else:
                            cor = "green" if valor < 33.4 else "orange" if valor < 66.7 else "red"
                            faixa = "baixo" if valor < 33.4 else "medio" if valor < 66.7 else "alto"
                            st.markdown(f"**{dim}:** :{cor}[{valor:.1f}]")
                            if dim in acoes_hmm: st.caption(f"🎯 **Medida de Prevenção:** {acoes_hmm[dim][faixa]}")
                        st.markdown("---")
                
                with p_tab2:
                    # TÍTULO E AJUSTE DO BOTÃO POPOVER PARA CONSULTA CONCEITUAL
                    c_tit, c_pop = st.columns([3, 1])
                    with c_tit:
                        st.markdown("### Quadrantes do Modelo Demanda-Controle de Karasek")
                    with c_pop:
                        with st.popover("📖 Legenda e Significado dos Quadrantes"):
                            st.markdown("""
                            ### Significado dos Quadrantes de Karasek (NR-17):
                            
                            * 🔵 **Trabalho Ativo (Alta Demanda / Alto Controle):** 
                            O ritmo e volume de trabalho são elevados, porém os colaboradores possuem ampla autonomia técnico-operatória para organizar as tarefas e propor soluções. Promove **motivação, aprendizado e crescimento profissional**.
                            
                            * 🔴 **Alta Exigência / Alta Tensão (Alta Demanda / Baixo Controle):** 
                            **Zona de Risco Crítico.** Pressão de tempo severa associada a prazos rígidos, combinada com nenhuma ou baixíssima autonomia. Cenário com altíssima correlação com distúrbios psicossomáticos, esgotamento físico/mental (*Burnout*) e passivos jurídicos.
                            
                            * 🟡 **Trabalho Passivo (Baixa Demanda / Baixo Controle):** 
                            O ritmo operacional é calmo ou reduzido, mas os funcionários não possuem margem de decisão ou incentivo à iniciativa. Risco voltado ao desenvolvimento de **monotonia laboral, apatia operacional e desmotivação crônica**.
                            
                            * 🟢 **Baixa Exigência (Baixa Demanda / Alto Controle):** 
                            Ambiente confortável e seguro. Baixa pressão temporal combinada com excelente autonomia sobre os métodos operatórios. Indicadores estáveis com baixo potencial gerador de estresse ocupacional.
                            """)
                    
                    # Inversão do Controle para o gráfico de Karasek (onde Alto Controle/Autonomia é protetivo)
                    x_controle = 100 - m['Controle']
                    y_demanda = m['Demanda']
                    
                    # Definição do Quadrante com base no ponto de corte mediano (50 pontos)
                    if y_demanda >= 50 and x_controle < 50:
                        quadrante = "Trabalho de Alta Exigência (High Strain)"
                        detalhe_q = "🔴 **Risco Máximo de Adoecimento:** Alta pressão de tempo e baixa autonomia técnico-operatória."
                    elif y_demanda >= 50 and x_controle >= 50:
                        quadrante = "Trabalho Ativo (Active Job)"
                        detalhe_q = "🔵 **Alta Motivação e Aprendizado:** Desafios elevados, mas com alta autonomia para resolvê-los."
                    elif y_demanda < 50 and x_controle < 50:
                        quadrante = "Trabalho Passivo (Passive Job)"
                        detalhe_q = "🟡 **Risco de Monotonia e Desmotivação:** Baixa cobrança, porém sem espaço para crescimento ou iniciativa."
                    else:
                        quadrante = "Trabalho de Baixa Exigência (Low Strain)"
                        detalhe_q = "🟢 **Ambiente Confortável e Seguro:** Baixas demandas e excelente controle sobre o ritmo."

                    # Geração do Gráfico de Quadrantes Interativo via Plotly
                    fig_k = go.Figure()
                    fig_k.add_shape(type="rect", x0=0, y0=50, x1=50, y1=100, fillcolor="rgba(255,0,0,0.1)", line_width=0) # Alta Exigência
                    fig_k.add_shape(type="rect", x0=50, y0=50, x1=100, y1=100, fillcolor="rgba(0,0,255,0.1)", line_width=0) # Trabalho Ativo
                    fig_k.add_shape(type="rect", x0=0, y0=0, x1=50, y1=50, fillcolor="rgba(255,255,0,0.1)", line_width=0) # Trabalho Passivo
                    fig_k.add_shape(type="rect", x0=50, y0=0, x1=100, y1=50, fillcolor="rgba(0,255,0,0.1)", line_width=0) # Baixa Exigência
                    
                    fig_k.add_trace(go.Scatter(x=[x_controle], y=[y_demanda], mode='markers+text', 
                                               marker=dict(size=14, color='black', symbol='diamond'),
                                               text=[f" {emp_sel}"], textposition="top right"))
                    
                    fig_k.update_layout(
                        xaxis=dict(title="CONTROLE (Autonomia / Uso de Habilidades)", range=[0,100], fixedrange=True),
                        yaxis=dict(title="DEMANDA (Carga / Ritmo de Trabalho)", range=[0,100], fixedrange=True),
                        margin=dict(l=40, r=40, t=20, b=40),
                        showlegend=False
                    )
                    st.plotly_chart(fig_k, use_container_width=True)
                    
                    st.markdown(f"#### **Diagnóstico Ergonômico Organizacional (NR-17):**")
                    st.markdown(f"O setor selecionado está classificado como: **{quadrante}**")
                    st.info(detalhe_q)
                    
        else: st.info("Base de dados vazia.")

st.markdown("---")
st.caption("© 2026 HMM Serviços - Engenharia de Segurança do Trabalho.")
