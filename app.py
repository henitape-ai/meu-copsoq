import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# CONFIGURAÇÕES HMM
st.set_page_config(page_title="HMM Serviços - Diagnóstico V23.2", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# DICIONÁRIOS TÉCNICOS DE PONTUAÇÃO
# Escala Padrão: Nunca=0 (Bom) / Sempre=100 (Ruim)
esc_f = {"Sempre": 100, "Frequentemente": 75, "As vezes": 50, "Raramente": 25, "Nunca / Quase nunca": 0}
# Escala Inversa: Nunca=100 (Ruim) / Sempre=0 (Bom)
esc_inv = {"Sempre": 0, "Frequentemente": 25, "As vezes": 50, "Raramente": 75, "Nunca / Quase nunca": 100}

st.title("🚀 Diagnóstico Psicossocial HMM")
st.info("O sistema identifica automaticamente se 'Nunca' representa baixo risco ou alerta crítico.")

# ... (Estrutura de formulário enviada anteriormente) ...

# EXEMPLO DE CÁLCULO DE LIDERANÇA (ITENS INVERSOS)
# Se o funcionário nunca tem apoio (Q15), o risco é 100.
# v_lideranca = (esc_inv[q13] + esc_inv[q14] + esc_inv[q15] ...) / 10
