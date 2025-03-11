# app.py
import streamlit as st
from model import load_model
from utils import generate_response
from cache import init_cache_db

st.title("🏦 BDI (Banco de Dados Intelligence)")

# Inicializa o banco de cache
init_cache_db()

# Carrega o modelo (usando cache do Streamlit)
model = load_model()
if model:
    st.success("✅ Modelo carregado com sucesso!")

# Interface para consulta
with st.form("query_form"):
    user_input = st.text_area("Digite sua pergunta:", "Qual foi o último valor do IPCA em Recife?")
    submitted = st.form_submit_button("Consultar")
    if submitted:
        response = generate_response(user_input, model)
        st.markdown(response)
