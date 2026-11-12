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

def salvar_config(config_dict):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, ensure_ascii=False, indent=4)

config = carregar_config()

# Estilos Visuais Aprimorados (Centralização Blindada para Projetor e Estabilidade Visual)
st.markdown("""
    <style>
    .stApp {
        background-color: #0B2545;
        color: white;
    }
    audio {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }
    .placar-topo {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #F4D35E !important;
    }
    .placar-alerta {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #FF4B4B !important;
    }
    .main-card {
        background-color: #134074;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        margin-bottom: 25px;
    }
    .main-card h3 {
        font-size: 32px !important;
        line-height: 1.4 !important;
        color: #FFFFFF !important;
    }
    /* RESPOSTAS BEM GRANDES E LEGÍVEIS */
    .stRadio div[role="radiogroup"] label div p {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    .stRadio div[role="radiogroup"] label {
        padding: 12px 0px !important;
    }
    /* FORÇAR CENTRALIZAÇÃO ABSOLUTA DE TODOS OS BOTÕES E DO MENU */
    div.stButton, [data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    div.stButton > button, [data-testid="stButton"] > button {
        background-color: #134074;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        width: 100% !important;
        max-width: 500px !important;
        padding: 16px !important;
        border: 2px solid #1F618D;
        font-size: 22px !important;
        display: block !important;
        margin: 8px auto !important;
        text-align: center !important;
    }
    div.stButton > button:hover, [data-testid="stButton"] > button:hover {
        background-color: #1F618D;
        color: white;
        border-color: #F4D35E;
    }
    .st-key-sair_sis button {
        background-color: #E74C3C !important;
        border: none !important;
    }
    .st-key-sair_sis button:hover {
        background-color: #C0392B !important;
    }
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
    }
    .dado-box {
        font-size: 80px;
        text-align: center;
        font-weight: bold;
        color: #F4D35E;
        background-color: #134074;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

def carregar_dados():
    perguntas_padrao = [
        {"pergunta": "Em que ano foi proclamado o Dogma da Imaculada Conceição pelo Papa Pio IX?", "opcoes": ["A) 1854", "B) 1950", "C) 1891", "D) 1250"], "resposta": "A) 1854"},
        {"pergunta": "Qual é a cor litúrgica principal associada às festividades de Nossa Senhora?", "opcoes": ["A) Vermelho", "B) Azul / Branco", "C) Verde", "D) Roxo"], "resposta": "B) Azul / Branco"},
        {"pergunta": "Quem foi a jovem santa a quem Nossa Senhora apareceu em Lourdes, França?", "opcoes": ["A) Santa Teresinha", "B) Santa Clara", "C) Santa Bernadette", "D) Santa Rita"], "resposta": "C) Santa Bernadette"}
    ]
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados.get("perguntas", perguntas_padrao), dados.get("participantes", []), dados.get("historico", [])
        except Exception:
            pass
    return perguntas_padrao, [], []

def salvar_dados(perguntas, participantes, historico):
    dados = {"perguntas": perguntas, "participantes": participantes, "historico": historico}
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Função blindada em Base64 HTML: nunca some no st.rerun(), não pisca e fica 100% centralizada
def mostrar_santa(largura_custom=None):
    img_path = config.get("imagem_ns", "nossa_senhora.png")
    largura = largura_custom if largura_custom is not None else config.get("tamanho_imagem", 360)
    
    html_bloco = "<div style='text-align: center; width: 100%;'>"
    html_bloco += "<h3 style='margin-bottom: 15px; color: #FFFFFF;'>🌸 Imaculada Conceição</h3>"
    
    if os.path.exists(img_path):
        try:
            with open(img_path, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            html_bloco += (
                f"<img src='data:image/png;base64,{b64_img}' "
                f"style='width: {largura}px; max-width: 100%; height: auto; "
                f"margin: 0 auto; display: block; border-radius: 12px; "
                f"box-shadow: 0 4px 15px rgba(0,0,0,0.4);' />"
            )
        except Exception:
            html_bloco += "<p style='color: #F4D35E;'>Erro ao ler imagem.</p>"
    else:
        html_bloco += f"<p style='color: #8DA9C4;'>Imagem '{img_path}' não encontrada.</p>"
        
    html_bloco += "</div>"
    st.markdown(html_bloco, unsafe_allow_html=True)

# Inicialização de Estados da Sessão
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"
if "participante" not in st.session_state:
    st.session_state.participante = ""
if "pergunta_idx" not in st.session_state:
    st.session_state.pergunta_idx = 0
if "pontuacao" not in st.session_state:
    st.session_state.pontuacao = 0
if "acertos" not in st.session_state:
    st.session_state.acertos = 0
if "perguntas_sessao" not in st.session_state:
    st.session_state.perguntas_sessao = []
if "respondido" not in st.session_state:
    st.session_state.respondido = False
if "ultima_resposta_correta" not in st.session_state:
    st.session_state.ultima_resposta_correta = None
if "dado_girado" not in st.session_state:
    st.session_state.dado_girado = False
if "resultado_dado" not in st.session_state:
    st.session_state.resultado_dado = None
if "editando_idx" not in st.session_state:
    st.session_state.editando_idx = None
if "tempo_restante" not in st.session_state:
    st.session_state.tempo_restante = 30

perguntas, participantes, historico = carregar_dados()

# Ficheiros de áudio locais
SOM_TIC_TAK = "tictak.mp3"
SOM_DADO = "paramomentododado.mp3"
SOM_ACERTO = "ElevenLabs_Efeito_sonoro_de_aplausos_altos_indicando_uma_resposta.mp3"
SOM_ERRO = "ElevenLabs_Efeito_sonoro_de_trombone_triste_quando_um_personagem.mp3"

def tocar_audio_invisivel(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)

# ==============================================================================
# 1. MENU PRINCIPAL (100% CENTRALIZADO PARA PROJETOR)
# ==============================================================================
if st.session_state.pagina == "menu":
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 46px;'>⛪ Festejos da Imaculada Conceição ⛪</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #8DA9C4; margin-bottom: 35px;'>Quiz da Imaculada (Pressione F11 para tela cheia)</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        if st.button("▶️ Jogar / Iniciar Quiz", use_container_width=True):
            st.session_state.pagina = "selecionar_participante"
            st.rerun()
            
        if st.button("👥 Cadastrar Participantes", use_container_width=True):
            st.session_state.pagina = "cadastrar_participantes"
            st.rerun()
            
        if st.button("📝 Cadastrar / Gerir / Editar Perguntas", use_container_width=True):
            st.session_state.pagina = "gerir_perguntas"
            st.rerun()
            
        if st.button("📊 Histórico de Acertos e Prêmios", use_container_width=True):
            st.session_state.pagina = "historico"
            st.rerun()
            
        if st.button("⚙️ Configurações (Imagem & Tempos)", use_container_width=True):
            st.session_state.pagina = "configuracoes"
            st.rerun()
            
        if st.button("🚪 Sair / Fechar Sistema", key="sair_sis", use_container_width=True):
            st.warning("Para fechar o sistema no navegador, basta fechar esta aba ou janela.")

# ==============================================================================
# 2. SELECIONAR PARTICIPANTE
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    st.markdown("<h2 style='text-align: center; margin-bottom: 25px;'>👤 Identificação do Participante</h2>", unsafe_allow_html=True)
    
    col_esq, col_dir = st.columns([2, 1])
    
    with col_dir:
        mostrar_santa()
        
    with col_esq:
        nome_digitado = st.text_input("Selecione ou Insira o Participante:")
        st.write("Ou escolha da lista cadastrada:")
        
        escolha_lista = st.selectbox("Lista de Participantes:", ["-- Selecione da lista --"] + participantes, label_visibility="collapsed") if participantes else "-- Selecione da lista --"
        
        st.write("")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("▶️ Iniciar com este Participante", use_container_width=True):
                nome_final = ""
                if escolha_lista != "-- Selecione da lista --":
                    nome_final = escolha_lista
                elif nome_digitado.strip():
                    nome_final = nome_digitado.strip()
                    if nome_final not in participantes:
                        participantes.append(nome_final)
                        salvar_dados(perguntas, participantes, historico)
                
                if nome_final:
                    st.session_state.participante = nome_final
                    st.session_state.pergunta_idx = 0
                    st.session_state.pontuacao = 0
                    st.session_state.acertos = 0
                    st.session_state.respondido = False
                    st.session_state.dado_girado = False
                    st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                    
                    sessao = []
                    for p in perguntas:
                        ops = list(p["opcoes"])
                        random.shuffle(ops)
                        sessao.append({"pergunta": p["pergunta"], "opcoes": ops, "resposta": p["resposta"]})
                    random.shuffle(sessao)
                    st.session_state.perguntas_sessao = sessao
                    
                    st.session_state.pagina = "jogo"
                    st.rerun()
                else:
                    st.warning("Por favor, insira ou selecione um nome válido.")
                    
            if st.button("⬅️ Voltar ao Menu", use_container_width=True):
                st.session_state.pagina = "menu"
                st.rerun()

# ==============================================================================
# 3. TELA DO JOGO (COL_DIR RENDERIZADA ANTES DE COL_ESQ E DO ST.RERUN)
# ==============================================================================
elif st.session_state.pagina == "jogo":
    p_idx = st.session_state.pergunta_idx
    total_p = len(st.session_state.perguntas_sessao)
    
    if p_idx >= total_p:
        st.session_state.pagina = "fim"
        st.rerun()

    # Tocar o tic-tak em segundo plano de forma 100% invisível
    if not st.session_state.respondido and os.path.exists(SOM_TIC_TAK):
        with open(SOM_TIC_TAK, "rb") as f:
            b64_t = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<audio autoplay loop src="data:audio/mp3;base64,{b64_t}"></audio>', unsafe_allow_html=True)

    # 1º Criamos as duas colunas
    col_esq, col_dir = st.columns([2, 1])
    
    # 2º RENDERIZAMOS A IMAGEM DA SANTA IMEDIATAMENTE (ANTES DO LOOP DO RELÓGIO!)
    with col_dir:
        mostrar_santa()

    # 3º Agora processamos a pergunta e o cronómetro na coluna da esquerda
    with col_esq:
        p = st.session_state.perguntas_sessao[p_idx]
        
        c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
        c1.markdown(f"<span class='placar-topo
