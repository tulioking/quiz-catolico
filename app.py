# ==============================================================================
# QUIZ CATÓLICO DOS FESTEJOS - VERSÃO WEB OFICIAL COMPLETA (STREAMLIT) ⛪🎵🎲
# ==============================================================================

import streamlit as st
import random
import json
import os
import time
import base64

ARQUIVO_DADOS = "dados_quiz_igreja.json"
ARQUIVO_CONFIG = "config_quiz.json"

st.set_page_config(page_title="Festejos da Imaculada Conceição", page_icon="⛪", layout="wide")

def carregar_config():
    config_padrao = {
        "imagem_ns": "nossa_senhora.png",
        "tempo_pergunta": 30,
        "tempo_alerta": 4,
        "tamanho_imagem": 360
    }
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                for k, v in config_padrao.items():
                    if k not in cfg:
                        cfg[k] = v
                return cfg
        except Exception:
            pass
    return config_padrao

config = carregar_config()

# Estilos Visuais Aprimorados (Layout Centralizado, Ocultação de Players e Tamanho Dinâmico da Imagem)
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #0B2545;
        color: white;
    }}
    audio {{
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }}
    .placar-topo {{
        font-size: 24px !important;
        font-weight: bold !important;
        color: #F4D35E !important;
    }}
    .main-card {{
        background-color: #134074;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        margin-bottom: 25px;
    }}
    .main-card h3 {{
        font-size: 32px !important;
        line-height: 1.4 !important;
        color: #FFFFFF !important;
    }}
    /* RESPOSTAS BEM GRANDES E LEGÍVEIS */
    .stRadio div[role="radiogroup"] label div p {{
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }}
    .stRadio div[role="radiogroup"] label {{
        padding: 12px 0px !important;
    }}
    /* IMAGEM CENTRALIZADA E COM TAMANHO CONFIGURÁVEL */
    [data-testid="stImage"] img {{
        max-width: {config.get("tamanho_imagem", 360)}px !important;
        margin: 0 auto !important;
        display: block !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }}
    /* FORÇAR CENTRALIZAÇÃO E TAMANHO IDEAL DE TODOS OS BOTÕES */
    .stButton {{
        display: flex;
        justify-content: center;
        width: 100%;
    }}
    .stButton>button {{
        background-color: #134074;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        max-width: 450px;
