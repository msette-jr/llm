# model.py
import os
import streamlit as st
from gpt4all import GPT4All
from config import MODEL_PATH

@st.cache_resource
def load_model():
    """Carrega o modelo GPT4All apenas uma vez."""
    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ Modelo não encontrado: {MODEL_PATH}")
        return None
    try:
        return GPT4All(MODEL_PATH)
    except Exception as e:
        st.error(f"❌ Erro ao carregar o modelo GPT4All: {str(e)}")
        return None
