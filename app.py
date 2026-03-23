import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# 1. CONFIGURAÇÕES TÉCNICAS
st.set_page_config(page_title="HMM - Gestão V23.5", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CABEÇALHO ---
st.title("🚀 Sistema de Gestão Psicossocial")
st.subheader("HMM Serviços - Engenharia e Segurança do Trabalho")
st.markdown("---")

tab1, tab2 = st.tabs(["📝 Coleta de Dados", "📊 Painel de Gestão e Gráficos"])

# --- DICIONÁRIOS DE ESCALAS (OMITIDOS AQUI PARA BREVIDADE, MAS MANTENHA OS DA V23.4) ---
esc_dir = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
esc_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}
esc_int = {"Extremamente": 100, "Muito": 75, "Moderadamente": 50, "Um pouco": 25, "Nunca / Quase Nunca": 0}
esc_sau = {"Excelente": 0, "Muito Boa": 25, "Boa": 50, "Razoável": 75, "Deficitária": 100}

# --- ABA 1: FORMULÁRIO (CÓDIGO IGUAL À V23.4) ---
with tab1:
    st.info("Formulário de 41 itens ativo para coleta.")
    # (O código do formulário da V23.4 deve permanecer aqui)

# --- ABA 2: PAINEL DE GESTÃO (PRE-RELATÓRIO) ---
with tab2:
    st.subheader("🔐 Área do Consultor HMM")
    acesso = st.text_input("Senha:", type="password", key="pwd_v23_5")
    
    if acesso == "HMM2024":
        df = conn.read(worksheet="Página1", ttl=0)
        
        if not df.empty:
            # Limpeza de dados
            df['Empresa'] = df['Empresa'].astype(str).str.strip()
            df['Setor'] = df['Setor'].astype(str).str.strip()

            # FILTROS
            st.markdown("### 🔍 Filtros de Relatório")
            c1, c2 = st.columns(2)
            with c1:
                lista_emp = sorted(df['Empresa'].unique())
                emp_sel = st.selectbox("Selecione o Cliente:", lista_emp, index=None)
            
            if emp_sel:
                with c2:
                    lista_set = sorted(df[df['Empresa'] == emp_sel]['Setor'].unique())
                    set_sel = st.multiselect("Filtrar Setores (Deixe vazio para Geral):", lista_set)

                # Filtragem dos dados
                df_f = df[df['Empresa'] == emp_sel]
                titulo_relatorio = f"GERAL - {emp_sel}"
                
                if set_sel:
                    df_f = df_f[df_f['Setor'].isin(set_sel)]
                    titulo_relatorio = f"SETOR(ES): {', '.join(set_sel)}"

                # CÁLCULO DE MÉDIAS
                cols_radar = ['Demanda', 'Controle', 'Lideranca', 'Satisfacao', 'Saude_Mental', 'Ofensivo']
                medias = df_f[cols_radar].mean()

                # GRÁFICO DE RADAR
                st.markdown(f"### 📊 Mapa de Riscos: {titulo_relatorio}")
                fig = px.line_polar(
                    r=medias.values, 
                    theta=medias.index, 
                    line_close=True, 
                    range_r=[0,100],
                    title=f"Perfil Psicossocial - {emp_sel}"
                )
                fig.update_traces(fill='toself', line_color='red', fillcolor='rgba(255, 0, 0, 0.3)')
                st.plotly_chart(fig, use_container_width=True)

                # PRÉ-RELATÓRIO TÉCNICO
                st.markdown("---")
                st.markdown("### 📝 Minuta de Pré-Relatório")
                
                txt_rel = f"""**RELATÓRIO TÉCNICO DE DIAGNÓSTICO PSICOSSOCIAL**
**CLIENTE:** {emp_sel.upper()}
**UNIDADE ANALISADA:** {titulo_relatorio}
**DATA DE EMISSÃO:** {datetime.now().strftime('%d/%m/%Y')}
**METODOLOGIA:** Protocolo COPSOQ III (41 Indicadores)

**1. RESULTADOS OBTIDOS (MÉDIAS 0-100):**
* Exigências/Demanda: {medias['Demanda']:.1f}
* Autonomia/Controle: {medias['Controle']:.1f}
* Qualidade da Liderança: {medias['Lideranca']:.1f}
* Satisfação com Trabalho: {medias['Satisfacao']:.1f}
* Índice de Saúde Mental: {medias['Saude_Mental']:.1f}
* Comportamentos Ofensivos: {medias['Ofensivo']:.1f}

**2. ANÁLISE PRELIMINAR:**
"""
                # Lógica de diagnóstico automático
                if medias['Demanda'] > 60 and medias['Controle'] < 40:
                    txt_rel += "- Alerta crítico de Alta Tensão (Modelo de Karasek).\n"
                if medias['Ofensivo'] > 20:
                    txt_rel += "- Presença de comportamentos ofensivos acima do limite de tolerância.\n"
                if medias['Lideranca'] < 50:
                    txt_rel += "- Necessidade de intervenção em treinamento de liderança e suporte social.\n"
                
                txt_rel += f"\n**Responsável Técnico:** Eng. Henrique - HMM Serviços"
                
                st.text_area("Copie para o Word/PDF:", value=txt_rel, height=350)
                
        else:
            st.warning("Aguardando inserção de dados no Google Sheets.")
