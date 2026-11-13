# ==============================================================================
# SUPER QUIZ MULTI-TEMAS - ARQUITETURA MODULAR COM FICHEIROS .JSON 🎲🏆🚀
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time
import base64
import re

ARQUIVO_DADOS_GERAL = "dados_quiz_geral.json"
ARQUIVO_CONFIG = "config_quiz_geral.json"

NIVEIS_DIFICULDADE = ["🟢 Fácil", "🟡 Médio", "🟠 Difícil", "🔴 Impossível"]

MULTIPLICADOR_PONTOS = {
    "🟢 Fácil": 1.0,
    "🟡 Médio": 1.5,
    "🟠 Difícil": 2.5,
    "🔴 Impossível": 5.0
}

# ==============================================================================
# MAPEAMENTO DOS 9 FICHEIROS .JSON, CORES, PÔSTERES E FRASES FINAIS
# ==============================================================================
INFO_MODOS = {
    "⛪ Igreja": {
        "arquivo_json": "banco_igreja.json",
        "cor_fundo": "#0B2545", "cor_card": "#134074", "cor_texto": "#FFFFFF",
        "cor_destaque": "#F4D35E", "cor_botao": "#134074", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#1F618D",
        "icone": "⛪", "titulo_card": "🌸 Imaculada Conceição", "sub_card": "Fé, História, Santos e Sagradas Escrituras",
        "img_padrao": "nossa_senhora.png",
        "msg_final": "Que Nossa Senhora Imaculada Conceição abençoe grandemente a ti e a toda a tua família! 🙏✨"
    },
    "🦸 Super-Heróis": {
        "arquivo_json": "banco_herois.json",
        "cor_fundo": "#0A1128", "cor_card": "#1C2541", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFD166", "cor_botao": "#B80C09", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#FFD166",
        "icone": "🦸‍♂️", "titulo_card": "⚡ Universo dos Heróis", "sub_card": "Marvel, DC, Quadrinhos e Superpoderes",
        "img_padrao": "tema_herois.png",
        "msg_final": "Missão cumprida, herói! Mostraste que tens superpoderes de conhecimento e salvaste o multiverso! 🦸‍♂️⚡"
    },
    "🍎 Frutas": {
        "arquivo_json": "banco_frutas.json",
        "cor_fundo": "#1B4332", "cor_card": "#2D6A4F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFD166", "cor_botao": "#40916C", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#95D5B2",
        "icone": "🍉", "titulo_card": "🍎 Pomar Tropical", "sub_card": "Frutas, Vitaminas, Sabores e Natureza",
        "img_padrao": "tema_frutas.png",
        "msg_final": "Que desempenho refrescante! Colheste os melhores resultados no nosso pomar de conhecimentos! 🍉🍍"
    },
    "🍔 Comidas": {
        "arquivo_json": "banco_comidas.json",
        "cor_fundo": "#370617", "cor_card": "#6A040F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFBA08", "cor_botao": "#9D0208", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#F48C06",
        "icone": "🍔", "titulo_card": "👨‍🍳 Mestre da Culinária", "sub_card": "Pratos Típicos, Sabores do Brasil e do Mundo",
        "img_padrao": "tema_comidas.png",
        "msg_final": "Parabéns, Mestre-Cuca! Temperaste esta partida com muito talento e deste um show de gastronomia! 👨‍🍳🍔"
    },
    "📺 Novelas": {
        "arquivo_json": "banco_novelas.json",
        "cor_fundo": "#3C096C", "cor_card": "#5A189A", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FF9E00", "cor_botao": "#7B2CBF", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#E0AAFF",
        "icone": "📺", "titulo_card": "🎭 Clássicos da TV", "sub_card": "Vilãs Icônicas, Bordões e Grandes Tramas",
        "img_padrao": "tema_novelas.png",
        "msg_final": "Cena digna de último capítulo em horário nobre! Brilhaste como protagonista nesta novela! 📺🌟"
    },
    "🎬 Filmes": {
        "arquivo_json": "banco_filmes.json",
        "cor_fundo": "#121212", "cor_card": "#1F1F1F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#D4AF37", "cor_botao": "#292929", "cor_texto_botao": "#D4AF37", "cor_borda_botao": "#D4AF37",
        "icone": "🎬", "titulo_card": "🍿 Sessão de Cinema", "sub_card": "Sucessos de Bilheteria, Oscar e Clássicos",
        "img_padrao": "tema_filmes.png",
        "msg_final": "E o Óscar vai para... TI! Uma atuação digna de tapete vermelho e recorde de bilheteira! 🎬🏆"
    },
    "🎨 Desenhos": {
        "arquivo_json": "banco_desenhos.json",
        "cor_fundo": "#003049", "cor_card": "#00507A", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FCBF49", "cor_botao": "#F77F00", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#FCBF49",
        "icone": "🎨", "titulo_card": "🎈 Mundo Animado", "sub_card": "Desenhos Clássicos, Nostalgia e Diversão",
        "img_padrao": "tema_desenhos.png",
        "msg_final": "Isso é tudo, pessoal! Mandaste super bem e garantiste a diversão com gostinho de infância! 🎨🎈"
    },
    "⚔️ Animes": {
        "arquivo_json": "banco_animes.json",
        "cor_fundo": "#10002B", "cor_card": "#240046", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00F5D4", "cor_botao": "#7209B7", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#F72585",
        "icone": "⚔️", "titulo_card": "🐉 Arena Otaku", "sub_card": "Dragon Ball, Naruto, One Piece, Solo Leveling e mais!",
        "img_padrao": "tema_animes.png",
        "msg_final": "O teu poder de luta passou de 8.000! Despertaste o instinto superior e dominaste a Arena Otaku! ⚔️🔥"
    },
    "💼 Trabalhos & Profissões": {
        "arquivo_json": "banco_trabalhos.json",
        "cor_fundo": "#1B263B", "cor_card": "#283845", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00B4D8", "cor_botao": "#415A77", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#90E0EF",
        "icone": "💼", "titulo_card": "🛠️ Mundo das Profissões", "sub_card": "Tecnologia, Saúde, Engenharia e Ofícios",
        "img_padrao": "tema_trabalhos.png",
        "msg_final": "Trabalho de excelência! Mostraste competência máxima e mereces uma promoção com louvor! 💼🚀"
    },
    "🎲 Misturadão (Todos os Temas)": {
        "arquivo_json": None,
        "cor_fundo": "#1F1147", "cor_card": "#341F6F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00F5D4", "cor_botao": "#4E2A84", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#00F5D4",
        "icone": "🎲", "titulo_card": "🌟 Desafio Misturadão", "sub_card": "Todos os 9 Bancos de Dados Juntos num Só Jogo!",
        "img_padrao": "tema_misturadao.png",
        "msg_final": "Incrível! Encaraste o desafio supremo de todos os temas e provaste que sabes de tudo um pouco! 🎲👑"
    }
}

LISTA_MODOS_JOGO = list(INFO_MODOS.keys())
TEMAS_INDIVIDUAIS = [m for m in LISTA_MODOS_JOGO if INFO_MODOS[m]["arquivo_json"] is not None]

# ==============================================================================
# LEITURA E GRAVAÇÃO MODULAR DOS FICHEIROS .JSON DE CADA TEMA
# ==============================================================================
def normalizar_chave_nivel(chave_json):
    """Garante compatibilidade quer o JSON use 'Normal'/'Médio' ou 'Hard'/'Difícil'."""
    c = chave_json.lower()
    if "fácil" in c or "facil" in c:
        return "🟢 Fácil"
    if "médio" in c or "medio" in c or "normal" in c:
        return "🟡 Médio"
    if "difícil" in c or "dificil" in c or "hard" in c:
        return "🟠 Difícil"
    if "impossível" in c or "impossivel" in c:
        return "🔴 Impossível"
    return None

def carregar_banco_tema(modo):
    """Lê o ficheiro .json específico de um modo e organiza nos 4 níveis padrão."""
    estrutura = {niv: [] for niv in NIVEIS_DIFICULDADE}
    arq = INFO_MODOS.get(modo, {}).get("arquivo_json")
    if not arq or not os.path.exists(arq):
        return estrutura
        
    try:
        with open(arq, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, dict):
                for k, lista_p in dados.items():
                    niv_padrao = normalizar_chave_nivel(k)
                    if niv_padrao and isinstance(lista_p, list):
                        estrutura[niv_padrao].extend(lista_p)
            elif isinstance(dados, list):
                estrutura["🟢 Fácil"] = dados
    except Exception as e:
        st.error(f"Erro ao ler o ficheiro '{arq}': {e}")
        
    return estrutura

def salvar_banco_tema(modo, dict_niveis):
    """Salva as perguntas de um modo diretamente no seu ficheiro .json próprio."""
    arq = INFO_MODOS.get(modo, {}).get("arquivo_json")
    if arq:
        with open(arq, "w", encoding="utf-8") as f:
            json.dump(dict_niveis, f, ensure_ascii=False, indent=2)

def carregar_todos_bancos():
    return {modo: carregar_banco_tema(modo) for modo in TEMAS_INDIVIDUAIS}

def carregar_participantes_historico():
    participantes_atuais = []
    historico_atual = []
    if os.path.exists(ARQUIVO_DADOS_GERAL):
        try:
            with open(ARQUIVO_DADOS_GERAL, "r", encoding="utf-8") as f:
                dados = json.load(f)
                participantes_atuais = dados.get("participantes", [])
                historico_atual = dados.get("historico", [])
        except Exception:
            pass
    return participantes_atuais, historico_atual

def salvar_participantes_historico(participantes, historico):
    dados = {
        "participantes": participantes,
        "historico": historico
    }
    with open(ARQUIVO_DADOS_GERAL, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ==============================================================================
# CONFIGURAÇÕES GERAIS DO SISTEMA
# ==============================================================================
def obter_config_padrao():
    return {
        "tamanho_imagem": 360,
        "borda_imagem": 14,
        "usar_fundo_img": False,
        "imagem_fundo": "fundo_quiz_geral.png",
        "opacidade_fundo": 0.7,
        "tema_menu_inicial": "⛪ Igreja",
        "titulos_temas": {m: INFO_MODOS[m]["titulo_card"] for m in INFO_MODOS},
        "msgs_finais_temas": {m: INFO_MODOS[m]["msg_final"] for m in INFO_MODOS},
        
        "tempo_pergunta": 30,
        "tempo_alerta": 5,
        "acertos_para_dado": 3,
        "pontos_por_acerto": 100,
        "ativar_sons": True,
        "ativar_baloes": True,
        
        "tam_fonte_titulo": 46,
        "tam_fonte_pergunta": 30,
        "tam_fonte_opcoes": 24,
        "tam_fonte_placar": 20,
        "tam_fonte_botao": 22,
        "largura_botao": 520,
        "altura_botao": 16,
        "raio_borda_botao": 10,
        
        "titulo_aba": "Super Quiz Multi-Temas",
        "icone_aba": "🎲",
        "txt_titulo_menu": "🎲 SUPER QUIZ MULTI-TEMAS 🎲",
        "txt_subtitulo_menu": "Escolhe o teu tema, seleciona a dificuldade e desafia os teus conhecimentos! (F11 para ecrã inteiro)",
        "txt_btn_jogar": "▶️ Jogar / Escolher Modo de Jogo",
        "txt_btn_participantes": "👥 Cadastrar Participantes",
        "txt_btn_perguntas": "📝 Gerir Perguntas por Tema & Nível",
        "txt_btn_historico": "📊 Histórico e Ranking Top 5",
        "txt_btn_config": "⚙️ Configurações (Imagens, Textos & Regras)",
        "txt_btn_sair": "🚪 Sair / Fechar Sistema",
        "txt_sala_dado": "🎲 SALA DO DADO PREMIADO! 🎲",
        "txt_sub_dado": "Parabéns! Chegou a hora de lançar o dado!",
        "txt_titulo_fim": "🎉 FIM DA PARTIDA! PARABÉNS! 🎉"
    }

def carregar_config():
    padrao = obter_config_padrao()
    if os.path.exists(ARQUIVO_CONFIG):
        try:
            with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                for k, v in padrao.items():
                    if k not in cfg:
                        cfg[k] = v
                for dict_key in ["titulos_temas", "msgs_finais_temas"]:
                    if dict_key not in cfg or not isinstance(cfg[dict_key], dict):
                        cfg[dict_key] = padrao[dict_key]
                    else:
                        for m in INFO_MODOS:
                            if m not in cfg[dict_key]:
                                cfg[dict_key][m] = padrao[dict_key][m]
                return cfg
        except Exception:
            pass
    return padrao

def salvar_config(config_dict):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, ensure_ascii=False, indent=4)

config = carregar_config()

# Inicialização de Estados da Sessão
estados_iniciais = {
    "pagina": "menu", "participante": "", "modo_jogo_ativo": None,
    "dificuldade_ativa": "🟢 Fácil", "pergunta_idx": 0, "pontuacao": 0, "acertos": 0,
    "total_acertos_partida": 0, "total_erros_partida": 0,
    "inicio_partida": None, "tempo_final_congelado": None, "perguntas_sessao": [],
    "respondido": False, "ultima_resposta_correta": None, "dado_girado": False,
    "resultado_dado": None, "editando_idx": None, "tempo_restante": 30,
    "baloes_mostrados": False, "dado_disponivel": False, "historico_salvo_partida": False,
    "up_cnt": 0, "msg_upload_ok": "", "tema_gerir_selecionado": "⛪ Igreja",
    "nivel_gerir_selecionado": "🟢 Fácil", "tema_img_cfg": "⛪ Igreja", "limpar_tela_jogo": False,
    "modo_mobile": False
}
for chave, valor_padrao in estados_iniciais.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor_padrao

st.set_page_config(
    page_title=config.get("titulo_aba", "Super Quiz"),
    page_icon=config.get("icone_aba", "🎲"),
    layout="centered" if st.session_state.modo_mobile else "wide"
)

# ==============================================================================
# GERADOR DE CSS DINÂMICO (ADAPTA PARA MODO MOBILE OU DESKTOP)
# ==============================================================================
def obter_modo_visual_atual():
    modo_ativo = st.session_state.get("modo_jogo_ativo")
    if modo_ativo in INFO_MODOS:
        return modo_ativo
    tema_menu = config.get("tema_menu_inicial", "⛪ Igreja")
    return tema_menu if tema_menu in INFO_MODOS else "⛪ Igreja"

def obter_paleta_ativa():
    return INFO_MODOS[obter_modo_visual_atual()]

def aplicar_estilos_dinamicos():
    paleta = obter_paleta_ativa()
    bg_css = f"background-color: {paleta['cor_fundo']};"
    is_mob = st.session_state.get("modo_mobile", False)
    
    larg_max = 380 if is_mob else config.get("largura_botao", 520)
    f_titulo = 28 if is_mob else config.get("tam_fonte_titulo", 46)
    f_perg   = 21 if is_mob else config.get("tam_fonte_pergunta", 30)
    f_opcoes = 18 if is_mob else config.get("tam_fonte_opcoes", 24)
    f_placar = 15 if is_mob else config.get("tam_fonte_placar", 20)
    f_botao  = 17 if is_mob else config.get("tam_fonte_botao", 22)
    pad_btn  = 11 if is_mob else config.get("altura_botao", 16)
    pad_card = 16 if is_mob else 28

    if config.get("usar_fundo_img") and os.path.exists(config.get("imagem_fundo", "")):
        try:
            with open(config["imagem_fundo"], "rb") as f:
                b64_bg = base64.b64encode(f.read()).decode("utf-8")
            op = config.get("opacidade_fundo", 0.7)
            bg_css = (
                f"background: linear-gradient(rgba(0,0,0,{op}), rgba(0,0,0,{op})), "
                f"url('data:image/png;base64,{b64_bg}') no-repeat center center fixed !important; "
                f"background-size: cover !important;"
            )
        except Exception:
            pass

    st.markdown(f"""
        <style>
        .stApp {{
            {bg_css}
            color: {paleta['cor_texto']};
            transition: background-color 0.4s ease;
        }}
        .block-container {{
            padding-top: {'1.5rem' if is_mob else '2.5rem'} !important;
            padding-left: {'0.8rem' if is_mob else '3rem'} !important;
            padding-right: {'0.8rem' if is_mob else '3rem'} !important;
        }}
        audio {{
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }}
        .placar-topo {{
            font-size: {f_placar}px !important;
            font-weight: bold !important;
            color: {paleta['cor_destaque']} !important;
            text-align: center !important;
            display: block !important;
            width: 100% !important;
        }}
        .placar-alerta {{
            font-size: {f_placar + 2}px !important;
            font-weight: bold !important;
            color: #FF4B4B !important;
            text-align: center !important;
            display: block !important;
            width: 100% !important;
        }}
        .placar-mobile-box {{
            background-color: rgba(0,0,0,0.35);
            border: 1px solid {paleta['cor_destaque']};
            border-radius: 12px;
            padding: 8px 10px;
            margin-bottom: 12px;
            text-align: center;
            font-size: 15px;
            font-weight: bold;
            color: {paleta['cor_destaque']};
        }}
        .badge-wrapper {{
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin: 8px auto !important;
            text-align: center !important;
        }}
        .badge-modo {{
            background-color: {paleta['cor_botao']};
            color: {paleta['cor_destaque']};
            padding: {'6px 14px' if is_mob else '8px 22px'};
            border-radius: 25px;
            border: 2px solid {paleta['cor_destaque']};
            font-weight: bold;
            font-size: {'14px' if is_mob else '19px'};
            display: inline-block;
            text-align: center !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .main-card {{
            background-color: {paleta['cor_card']};
            padding: {pad_card}px;
            border-radius: 14px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.45);
            margin-bottom: 16px;
            border: 2px solid {paleta['cor_borda_botao']};
            text-align: center !important;
        }}
        .main-card h3 {{
            font-size: {f_perg}px !important;
            line-height: 1.35 !important;
            color: {paleta['cor_texto']} !important;
            margin: 0 !important;
            text-align: center !important;
        }}
        div[data-testid="stTextInput"], div[data-testid="stSelectbox"] {{
            max-width: {larg_max}px !important;
            width: 100% !important;
            margin: 0 auto 10px auto !important;
        }}
        div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label {{
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            text-align: center !important;
            font-size: {'15px' if is_mob else '18px'} !important;
            font-weight: bold !important;
            margin-bottom: 4px !important;
        }}
        div[data-testid="stTextInput"] label p, div[data-testid="stSelectbox"] label p {{
            font-size: {'15px' if is_mob else '18px'} !important;
            font-weight: bold !important;
            text-align: center !important;
            width: 100% !important;
        }}
        div[data-testid="stTextInput"] input {{
            text-align: center !important;
            font-size: {'17px' if is_mob else '20px'} !important;
            font-weight: 600 !important;
        }}
        .stRadio div[role="radiogroup"] label div p {{
            font-size: {f_opcoes}px !important;
            font-weight: 700 !important;
            color: {paleta['cor_texto']} !important;
        }}
        .stRadio div[role="radiogroup"] label {{
            padding: {'6px 0px' if is_mob else '10px 0px'} !important;
        }}
        div.stButton, [data-testid="stButton"], .stElementContainer:has(button) {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            margin: 0 auto !important;
        }}
        div.stButton > button, [data-testid="stButton"] > button {{
            background-color: {paleta['cor_botao']} !important;
            color: {paleta['cor_texto_botao']} !important;
            font-weight: bold !important;
            border-radius: {config['raio_borda_botao']}px !important;
            width: 100% !important;
            max-width: {larg_max}px !important;
            padding: {pad_btn}px !important;
            border: 2px solid {paleta['cor_borda_botao']} !important;
            font-size: {f_botao}px !important;
            display: block !important;
            margin: 6px auto !important;
            text-align: center !important;
            transition: all 0.2s ease !important;
        }}
        div.stButton > button:hover, [data-testid="stButton"] > button:hover {{
            filter: brightness(1.2) !important;
            border-color: {paleta['cor_destaque']} !important;
        }}
        .st-key-btn_toggle_mob button {{
            font-size: 15px !important;
            padding: 8px 18px !important;
            max-width: 240px !important;
            margin: 0 auto 12px auto !important;
            border-radius: 25px !important;
            background-color: rgba(255,255,255,0.14) !important;
            border: 2px solid {paleta['cor_destaque']} !important;
            color: {paleta['cor_destaque']} !important;
        }}
        .st-key-btn_ir_dado, .st-key-btn_ir_dado > div,
        .st-key-btn_iniciar_quiz_sel, .st-key-btn_iniciar_quiz_sel > div {{
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            margin: 0 auto !important;
        }}
        .st-key-btn_ir_dado button, .st-key-btn_iniciar_quiz_sel button {{
            background-color: #F4D35E !important;
            color: #0B2545 !important;
            border: 3px solid #FFFFFF !important;
            font-size: {f_botao + 1}px !important;
            max-width: {larg_max}px !important;
            width: 100% !important;
            margin: 8px auto !important;
            box-shadow: 0 0 20px rgba(244, 211, 94, 0.7) !important;
        }}
        .st-key-sair_sis button {{
            background-color: #E74C3C !important;
            border: none !important;
            color: #FFFFFF !important;
        }}
        h1 {{
            font-size: {f_titulo}px !important;
        }}
        h1, h2, h3, h4, p, label {{
            color: {paleta['cor_texto']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# IMAGEM DINÂMICA DA COLUNA DIREITA
# ==============================================================================
def mostrar_painel_tema(modo_especifico=None, largura_custom=None, borda_custom=None):
    modo = modo_especifico if modo_especifico in INFO_MODOS else obter_modo_visual_atual()
    info = INFO_MODOS[modo]
    is_mob = st.session_state.get("modo_mobile", False)
    
    largura_padrao = 220 if is_mob else config.get("tamanho_imagem", 360)
    largura = largura_custom if largura_custom is not None else largura_padrao
    borda = borda_custom if borda_custom is not None else config.get("borda_imagem", 14)
    titulo_topo = config.get("titulos_temas", {}).get(modo, info["titulo_card"])
    arq_img = info["img_padrao"]

    html_bloco = "<div style='text-align: center; width: 100%; display: flex; flex-direction: column; align-items: center;'>"
    if titulo_topo.strip():
        html_bloco += f"<h4 style='margin-bottom: 10px; color: {info['cor_texto']}; text-align: center;'>{titulo_topo}</h4>"

    if os.path.exists(arq_img):
        try:
            with open(arq_img, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            html_bloco += (
                f"<img src='data:image/png;base64,{b64_img}' "
                f"style='width: {largura}px; max-width: 90%; height: auto; "
                f"margin: 0 auto; display: block; border-radius: {borda}px; "
                f"border: 3px solid {info['cor_destaque']}; "
                f"box-shadow: 0 8px 25px rgba(0,0,0,0.5);' />"
            )
        except Exception:
            pass
    else:
        min_h = 200 if is_mob else 330
        tam_ico = 70 if is_mob else 115
        tam_tit = 20 if is_mob else 26
        html_bloco += (
            f"<div style='width: {largura}px; max-width: 92%; min-height: {min_h}px; margin: 0 auto; "
            f"background: radial-gradient(circle at top, {info['cor_botao']} 0%, {info['cor_card']} 60%, {info['cor_fundo']} 100%); "
            f"border-radius: {borda}px; border: 3px solid {info['cor_destaque']}; "
            f"box-shadow: 0 10px 28px rgba(0,0,0,0.55); display: flex; flex-direction: column; "
            f"align-items: center; justify-content: center; padding: 18px 14px; box-sizing: border-box;'>"
            f"<div style='font-size: {tam_ico}px; line-height: 1.1; margin-bottom: 10px; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.4));'>{info['icone']}</div>"
            f"<div style='font-size: {tam_tit}px; font-weight: 800; color: {info['cor_destaque']}; margin-bottom: 6px; text-align: center;'>{modo}</div>"
            f"<div style='font-size: 14px; color: {info['cor_texto']}; opacity: 0.9; text-align: center; line-height: 1.3;'>{info['sub_card']}</div>"
            f"</div>"
        )

    html_bloco += "</div>"
    st.markdown(html_bloco, unsafe_allow_html=True)

# ==============================================================================
# UTILITÁRIOS E DADO 3D
# ==============================================================================
def limpar_prefixo_opcao(texto):
    return re.sub(r'^[A-Da-d][\)\.\-]\s*', '', texto.strip())

def formatar_tempo_partida(segundos_totais):
    segundos_int = max(0, int(segundos_totais))
    minutos = segundos_int // 60
    segundos = segundos_int % 60
    return f"{minutos:02d}m {segundos:02d}s"

def obter_tempo_decorrido():
    if st.session_state.get("tempo_final_congelado") is not None:
        return st.session_state.tempo_final_congelado
    inicio = st.session_state.get("inicio_partida")
    if inicio is None:
        return 0
    return int(time.time() - inicio)

def extrair_ranking_top5(lista_historico):
    registos = []
    for item in lista_historico:
        m_nome = re.search(r"Participante:\s*([^|]+)", item)
        m_pts = re.search(r"Pontos(?: Final)?:\s*(\d+)", item)
        m_modo = re.search(r"Modo:\s*([^|]+)", item)
        if m_nome and m_pts:
            registos.append({
                "nome": m_nome.group(1).strip(),
                "pontos": int(m_pts.group(1)),
                "modo": m_modo.group(1).strip() if m_modo else "Geral"
            })
    registos.sort(key=lambda x: x["pontos"], reverse=True)
    return registos[:5]

def renderizar_dado_3d(numero_final=None, animar=False):
    paleta = obter_paleta_ativa()
    rotacoes_finais = {
        1: "rotateX(0deg) rotateY(0deg) rotateZ(0deg)",
        2: "rotateX(0deg) rotateY(-180deg) rotateZ(0deg)",
        3: "rotateX(0deg) rotateY(-90deg) rotateZ(0deg)",
        4: "rotateX(0deg) rotateY(90deg) rotateZ(0deg)",
        5: "rotateX(-90deg) rotateY(0deg) rotateZ(0deg)",
        6: "rotateX(90deg) rotateY(0deg) rotateZ(0deg)"
    }
    
    if numero_final is None:
        transform_final = "rotateX(-22deg) rotateY(-38deg) rotateZ(5deg)"
    else:
        transform_final = rotacoes_finais.get(numero_final, "rotateX(0deg) rotateY(0deg)")

    css_animacao = ""
    classe_cubo = "cube"
    classe_sombra = "shadow"
    
    if animar and numero_final is not None:
        classe_cubo = "cube rolando"
        classe_sombra = "shadow sombra-rolando"
        css_animacao = f"""
        @keyframes lancamentoDado {{
            0%   {{ transform: translateY(40px) scale(0.6) rotateX(0deg) rotateY(0deg) rotateZ(0deg); }}
            20%  {{ transform: translateY(-95px) scale(1.18) rotateX(540deg) rotateY(360deg) rotateZ(180deg); }}
            45%  {{ transform: translateY(15px) scale(0.95) rotateX(1080deg) rotateY(720deg) rotateZ(360deg); }}
            65%  {{ transform: translateY(-45px) scale(1.06) rotateX(1440deg) rotateY(1080deg) rotateZ(520deg); }}
            82%  {{ transform: translateY(8px) scale(0.98) rotateX(1750deg) rotateY(1380deg) rotateZ(690deg); }}
            92%  {{ transform: translateY(-12px) scale(1.02) {transform_final}; }}
            100% {{ transform: translateY(0px) scale(1) {transform_final}; }}
        }}
        @keyframes sombraPulando {{
            0%   {{ transform: scale(0.5); opacity: 0.2; }}
            20%  {{ transform: scale(1.5); opacity: 0.12; filter: blur(16px); }}
            45%  {{ transform: scale(0.85); opacity: 0.55; filter: blur(6px); }}
            65%  {{ transform: scale(1.25); opacity: 0.22; filter: blur(12px); }}
            82%  {{ transform: scale(0.92); opacity: 0.55; filter: blur(6px); }}
            92%  {{ transform: scale(1.05); opacity: 0.38; filter: blur(8px); }}
            100% {{ transform: scale(0.95); opacity: 0.5; filter: blur(7px); }}
        }}
        .rolando {{
            animation: lancamentoDado 3.6s cubic-bezier(0.22, 0.61, 0.36, 1) forwards !important;
        }}
        .sombra-rolando {{
            animation: sombraPulando 3.6s cubic-bezier(0.22, 0.61, 0.36, 1) forwards !important;
        }}
        """

    badge_html = ""
    if numero_final is not None and not animar:
        badge_html = f"<div class='resultado-texto'>🎉 SAIU O NÚMERO {numero_final}! 🎉</div>"
    elif animar:
        badge_html = "<div class='resultado-texto' style='color: #8DA9C4;'>🎲 Lançando o dado...</div>"
    else:
        badge_html = "<div class='resultado-texto' style='color: #8DA9C4;'>Toque abaixo para jogar o dado!</div>"

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            margin: 0; padding: 0; background: transparent;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            font-family: sans-serif; overflow: hidden;
        }}
        .palco-dado {{
            background: radial-gradient(circle, {paleta['cor_card']} 0%, {paleta['cor_fundo']} 90%);
            border: 3px solid {'#2ECC71' if (numero_final and not animar) else paleta['cor_destaque']};
            border-radius: 20px; width: 94%; max-width: 500px; height: 310px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); position: relative; margin: 0 auto;
        }}
        .scene {{ width: 130px; height: 130px; perspective: 750px; margin-top: 20px; }}
        .cube {{
            width: 130px; height: 130px; position: relative;
            transform-style: preserve-3d; transform: {transform_final}; transition: transform 0.5s ease;
        }}
        .face {{
            position: absolute; width: 130px; height: 130px;
            background: linear-gradient(145deg, #FFFFFF, #E4E7EC);
            border: 2px solid #CBD2D9; border-radius: 22px; box-sizing: border-box;
            padding: 16px; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, 1fr);
            box-shadow: inset 0 0 14px rgba(0,0,0,0.18), 0 2px 6px rgba(0,0,0,0.25);
        }}
        .pip {{
            width: 24px; height: 24px; border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #333333, #090909);
            align-self: center; justify-self: center;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.7), 0 1px 1px rgba(255,255,255,0.8);
        }}
        .pip.red {{
            width: 30px; height: 30px;
            background: radial-gradient(circle at 35% 35%, #FF4B4B, #B80000);
        }}
        .front  {{ transform: rotateY(0deg) translateZ(65px); }}
        .back   {{ transform: rotateY(180deg) translateZ(65px); }}
        .right  {{ transform: rotateY(90deg) translateZ(65px); }}
        .left   {{ transform: rotateY(-90deg) translateZ(65px); }}
        .top    {{ transform: rotateX(90deg) translateZ(65px); }}
        .bottom {{ transform: rotateX(-90deg) translateZ(65px); }}
        .shadow {{
            width: 115px; height: 26px; background: rgba(0, 0, 0, 0.5);
            border-radius: 50%; filter: blur(7px); margin-top: 32px;
        }}
        .resultado-texto {{
            margin-top: 16px; font-size: 22px; font-weight: 800;
            color: {paleta['cor_destaque']}; text-shadow: 0 2px 8px rgba(0,0,0,0.5);
            text-align: center; padding: 0 10px;
        }}
        {css_animacao}
    </style>
    </head>
    <body>
        <div class="palco-dado">
            <div class="scene">
                <div class="{classe_cubo}">
                    <div class="face front"><span class="pip red" style="grid-area: 2 / 2;"></span></div>
                    <div class="face back"><span class="pip" style="grid-area: 1 / 1;"></span><span class="pip" style="grid-area: 3 / 3;"></span></div>
                    <div class="face right"><span class="pip" style="grid-area: 1 / 1;"></span><span class="pip" style="grid-area: 2 / 2;"></span><span class="pip" style="grid-area: 3 / 3;"></span></div>
                    <div class="face left"><span class="pip" style="grid-area: 1 / 1;"></span><span class="pip" style="grid-area: 1 / 3;"></span><span class="pip" style="grid-area: 3 / 1;"></span><span class="pip" style="grid-area: 3 / 3;"></span></div>
                    <div class="face top"><span class="pip" style="grid-area: 1 / 1;"></span><span class="pip" style="grid-area: 1 / 3;"></span><span class="pip" style="grid-area: 2 / 2;"></span><span class="pip" style="grid-area: 3 / 1;"></span><span class="pip" style="grid-area: 3 / 3;"></span></div>
                    <div class="face bottom"><span class="pip" style="grid-area: 1 / 1;"></span><span class="pip" style="grid-area: 1 / 3;"></span><span class="pip" style="grid-area: 2 / 1;"></span><span class="pip" style="grid-area: 2 / 3;"></span><span class="pip" style="grid-area: 3 / 1;"></span><span class="pip" style="grid-area: 3 / 3;"></span></div>
                </div>
            </div>
            <div class="{classe_sombra}"></div>
            {badge_html}
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=330)

aplicar_estilos_dinamicos()

bancos_perguntas = carregar_todos_bancos()
participantes, historico = carregar_participantes_historico()

SOM_TIC_TAK = "tictak.mp3"
SOM_DADO = "paramomentododado.mp3"
SOM_ACERTO = "ElevenLabs_Efeito_sonoro_de_aplausos_altos_indicando_uma_resposta.mp3"
SOM_ERRO = "ElevenLabs_Efeito_sonoro_de_trombone_triste_quando_um_personagem.mp3"

def tocar_audio_invisivel(caminho_arquivo, loop=False):
    if config.get("ativar_sons", True) and os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            attr_loop = "loop" if loop else ""
            st.markdown(f'<audio autoplay {attr_loop} src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)

def soltar_baloes():
    if config.get("ativar_baloes", True):
        st.balloons()

# ==============================================================================
# SLOTS DE CONTEÚDO INDEPENDENTES (ELIMINA FANTASMAS NA Q1)
# ==============================================================================
slot_selecao = st.empty()
slot_jogo = st.empty()
slot_outros = st.empty()

def ir_para_pagina(nova_pagina):
    slot_selecao.empty()
    slot_jogo.empty()
    slot_outros.empty()
    st.session_state.pagina = nova_pagina
    st.rerun()

# ==============================================================================
# 1. MENU PRINCIPAL (COM BOTÃO ÚNICO DE ALTERNAR MOBILE / DESKTOP)
# ==============================================================================
if st.session_state.pagina == "menu":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        st.session_state.modo_jogo_ativo = None
        
        txt_toggle_mob = "🖥️ Mudar para Desktop" if st.session_state.modo_mobile else "📱 Mudar para Mobile"
        if st.button(txt_toggle_mob, key="btn_toggle_mob"):
            st.session_state.modo_mobile = not st.session_state.modo_mobile
            st.rerun()

        st.markdown(
            f"<h1 style='text-align: center;'>{config['txt_titulo_menu']}</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h4 style='text-align: center; opacity: 0.85; margin-bottom: 25px;'>{config['txt_subtitulo_menu']}</h4>",
            unsafe_allow_html=True
        )
        
        if st.session_state.modo_mobile:
            if st.button(config["txt_btn_jogar"], use_container_width=True):
                st.session_state.modo_jogo_ativo = LISTA_MODOS_JOGO[0]
                ir_para_pagina("selecionar_participante")
            if st.button(config["txt_btn_participantes"], use_container_width=True):
                ir_para_pagina("cadastrar_participantes")
            if st.button(config["txt_btn_perguntas"], use_container_width=True):
                ir_para_pagina("gerir_perguntas")
            if st.button(config["txt_btn_historico"], use_container_width=True):
                ir_para_pagina("historico")
            if st.button(config["txt_btn_config"], use_container_width=True):
                ir_para_pagina("configuracoes")
            if st.button(config["txt_btn_sair"], key="sair_sis", use_container_width=True):
                st.warning("Para fechar o sistema no navegador, basta fechar esta aba ou janela.")
        else:
            col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
            with col2:
                if st.button(config["txt_btn_jogar"], use_container_width=True):
                    st.session_state.modo_jogo_ativo = LISTA_MODOS_JOGO[0]
                    ir_para_pagina("selecionar_participante")
                if st.button(config["txt_btn_participantes"], use_container_width=True):
                    ir_para_pagina("cadastrar_participantes")
                if st.button(config["txt_btn_perguntas"], use_container_width=True):
                    ir_para_pagina("gerir_perguntas")
                if st.button(config["txt_btn_historico"], use_container_width=True):
                    ir_para_pagina("historico")
                if st.button(config["txt_btn_config"], use_container_width=True):
                    ir_para_pagina("configuracoes")
                if st.button(config["txt_btn_sair"], key="sair_sis", use_container_width=True):
                    st.warning("Para fechar o sistema no navegador, basta fechar esta aba ou janela.")

# ==============================================================================
# 2. SELECIONAR PARTICIPANTE + MODO + DIFICULDADE (EM TODOS OS TEMAS!)
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    slot_jogo.empty()
    slot_outros.empty()
    with slot_selecao.container():
        st.markdown("<h2 style='text-align: center; margin-bottom: 18px;'>👤 Participante & Modo de Jogo</h2>", unsafe_allow_html=True)
        
        if st.session_state.modo_mobile:
            col_esq = st.container()
            col_dir = st.container()
        else:
            col_esq, col_dir = st.columns([1.8, 1.2])
        
        with col_esq:
            nome_digitado = st.text_input("1️⃣ Digite o nome do Participante:", key="input_nome_part_sel")
            escolha_lista = st.selectbox(
                "Ou escolha da lista cadastrada:",
                ["-- Selecione da lista --"] + participantes,
                key="sel_lista_part_sel"
            ) if participantes else "-- Selecione da lista --"
            
            idx_modo_atual = LISTA_MODOS_JOGO.index(st.session_state.modo_jogo_ativo) if st.session_state.modo_jogo_ativo in LISTA_MODOS_JOGO else 0
            modo_escolhido = st.selectbox(
                "2️⃣ Escolha o Modo de Jogo:",
                LISTA_MODOS_JOGO,
                index=idx_modo_atual,
                key="sel_modo_jogo_sel"
            )
            
            if modo_escolhido != st.session_state.modo_jogo_ativo:
                st.session_state.modo_jogo_ativo = modo_escolhido
                st.rerun()

            # Todos os modos (inclusive o Misturadão!) agora têm seleção dos 4 Níveis de Dificuldade!
            idx_dif = NIVEIS_DIFICULDADE.index(st.session_state.dificuldade_ativa) if st.session_state.dificuldade_ativa in NIVEIS_DIFICULDADE else 0
            dif_escolhida = st.selectbox(
                "3️⃣ Escolha o Nível de Dificuldade:",
                NIVEIS_DIFICULDADE,
                index=idx_dif,
                key="sel_dif_jogo_sel"
            )
            st.session_state.dificuldade_ativa = dif_escolhida

            pts_base_cfg = config.get("pontos_por_acerto", 100)
            pts_partida = int(pts_base_cfg * MULTIPLICADOR_PONTOS.get(dif_escolhida, 1.0))

            if modo_escolhido == "🎲 Misturadão (Todos os Temas)":
                qtd_disp = sum(len(bancos_perguntas.get(m, {}).get(dif_escolhida, [])) for m in TEMAS_INDIVIDUAIS)
            else:
                qtd_disp = len(bancos_perguntas.get(modo_escolhido, {}).get(dif_escolhida, []))

            resumo_badge = f"🎯 {modo_escolhido} ({dif_escolhida}) — {qtd_disp} perguntas | ⭐ {pts_partida} pts/acerto"
            txt_botao_ini = f"▶️ Iniciar: {modo_escolhido} ({dif_escolhida})"
                
            st.markdown(
                f"<div class='badge-wrapper'><div class='badge-modo'>{resumo_badge}</div></div>",
                unsafe_allow_html=True
            )
            
            if st.button(txt_botao_ini, key="btn_iniciar_quiz_sel", use_container_width=True):
                nome_final = ""
                if escolha_lista != "-- Selecione da lista --":
                    nome_final = escolha_lista
                elif nome_digitado.strip():
                    nome_final = nome_digitado.strip()
                    if nome_final not in participantes:
                        participantes.append(nome_final)
                        salvar_participantes_historico(participantes, historico)
                
                if nome_final:
                    if modo_escolhido == "🎲 Misturadão (Todos os Temas)":
                        lista_base = []
                        for m in TEMAS_INDIVIDUAIS:
                            lista_base.extend(bancos_perguntas.get(m, {}).get(dif_escolhida, []))
                    else:
                        lista_base = list(bancos_perguntas.get(modo_escolhido, {}).get(dif_escolhida, []))
                        
                    if not lista_base:
                        arq_faltando = INFO_MODOS.get(modo_escolhido, {}).get("arquivo_json", "banco.json")
                        st.error(f"⚠️ Nenhuma pergunta encontrada para {modo_escolhido} no nível {dif_escolhida}! Verifique o ficheiro '{arq_faltando}'.")
                    else:
                        st.session_state.participante = nome_final
                        st.session_state.modo_jogo_ativo = modo_escolhido
                        st.session_state.dificuldade_ativa = dif_escolhida
                        st.session_state.pergunta_idx = 0
                        st.session_state.pontuacao = 0
                        st.session_state.acertos = 0
                        st.session_state.total_acertos_partida = 0
                        st.session_state.total_erros_partida = 0
                        st.session_state.inicio_partida = time.time()
                        st.session_state.tempo_final_congelado = None
                        st.session_state.historico_salvo_partida = False
                        st.session_state.respondido = False
                        st.session_state.dado_girado = False
                        st.session_state.baloes_mostrados = False
                        st.session_state.dado_disponivel = False
                        st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                        
                        # Embaralha a ordem das 4 alternativas dentro da própria pergunta (sem misturar com outras perguntas!)
                        letras_fixas = ["A)", "B)", "C)", "D)"]
                        sessao = []
                        for p in lista_base:
                            resp_limpa = limpar_prefixo_opcao(p["resposta"])
                            opcoes_limpas = [limpar_prefixo_opcao(op) for op in p["opcoes"]]
                            random.shuffle(opcoes_limpas)
                            
                            opcoes_formatadas = []
                            nova_resposta_correta = ""
                            for idx_letra, texto_op in enumerate(opcoes_limpas):
                                prefixo = letras_fixas[idx_letra] if idx_letra < len(letras_fixas) else f"{idx_letra+1})"
                                op_final = f"{prefixo} {texto_op}"
                                opcoes_formatadas.append(op_final)
                                if texto_op == resp_limpa:
                                    nova_resposta_correta = op_final
                                    
                            if not nova_resposta_correta and opcoes_formatadas:
                                nova_resposta_correta = opcoes_formatadas[0]
                                
                            sessao.append({
                                "pergunta": p["pergunta"],
                                "opcoes": opcoes_formatadas,
                                "resposta": nova_resposta_correta
                            })
                            
                        random.shuffle(sessao)
                        st.session_state.perguntas_sessao = sessao
                        st.session_state.limpar_tela_jogo = True
                        ir_para_pagina("jogo")
                else:
                    st.warning("⚠️ Por favor, digite ou selecione o nome do participante!")
                    
            if st.button("⬅️ Voltar ao Menu", key="btn_voltar_sel_part", use_container_width=True):
                st.session_state.modo_jogo_ativo = None
                ir_para_pagina("menu")

        with col_dir:
            mostrar_painel_tema(modo_especifico=modo_escolhido)

# ==============================================================================
# 3. TELA DO JOGO
# ==============================================================================
elif st.session_state.pagina == "jogo":
    slot_selecao.empty()
    slot_outros.empty()
    
    if st.session_state.get("limpar_tela_jogo", False):
        st.session_state.limpar_tela_jogo = False
        st.rerun()

    with slot_jogo.container():
        p_idx = st.session_state.pergunta_idx
        total_p = len(st.session_state.perguntas_sessao)
        meta_dado = config.get("acertos_para_dado", 3)
        dif_atual = st.session_state.get("dificuldade_ativa", "🟢 Fácil")
        mult = MULTIPLICADOR_PONTOS.get(dif_atual, 1.0)
        pts_acerto = int(config.get("pontos_por_acerto", 100) * mult)
        paleta = obter_paleta_ativa()
        
        if p_idx >= total_p:
            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
            ir_para_pagina("fim")

        if not st.session_state.respondido:
            tocar_audio_invisivel(SOM_TIC_TAK, loop=True)

        if st.session_state.modo_mobile:
            col_jogo_esq = st.container()
            col_jogo_dir = None
        else:
            col_jogo_esq, col_jogo_dir = st.columns([2.1, 0.9])
            with col_jogo_dir:
                mostrar_painel_tema()

        with col_jogo_esq:
            p = st.session_state.perguntas_sessao[p_idx]
            tempo_total_fmt = formatar_tempo_partida(obter_tempo_decorrido())
            txt_dif_badge = f" ({dif_atual})" if dif_atual else ""
            icone_trofeu = "🏆" if st.session_state.dado_disponivel else ""
            
            st.markdown(
                f"<div class='badge-wrapper'><div class='badge-modo'>{st.session_state.modo_jogo_ativo}{txt_dif_badge} &nbsp;|&nbsp; Q{p_idx + 1}/{total_p}</div></div>",
                unsafe_allow_html=True
            )
            
            if st.session_state.modo_mobile:
                placeholder_tempo = st.empty()
                st.markdown(
                    f"<div class='placar-mobile-box'>"
                    f"👤 {st.session_state.participante} &nbsp;|&nbsp; ⭐ {st.session_state.pontuacao} &nbsp;|&nbsp; "
                    f"✅{st.session_state.total_acertos_partida} ❌{st.session_state.total_erros_partida} &nbsp;|&nbsp; "
                    f"🎯{st.session_state.acertos}/{meta_dado}{icone_trofeu} &nbsp;|&nbsp; ⏱️{tempo_total_fmt}"
                    f"</div>",
                    unsafe_allow_html=True
                )
            else:
                c1, c2, c3, c4, c5 = st.columns([1.3, 0.9, 1.1, 0.9, 1.4])
                c1.markdown(f"<span class='placar-topo'>👤 {st.session_state.participante}</span>", unsafe_allow_html=True)
                placeholder_tempo = c2.empty()
                c3.markdown(f"<span class='placar-topo'>⏱️ {tempo_total_fmt}</span>", unsafe_allow_html=True)
                c4.markdown(f"<span class='placar-topo'>⭐ {st.session_state.pontuacao}</span>", unsafe_allow_html=True)
                c5.markdown(
                    f"<span class='placar-topo'>✅{st.session_state.total_acertos_partida} ❌{st.session_state.total_erros_partida} | 🎯{st.session_state.acertos}/{meta_dado}{icone_trofeu}</span>",
                    unsafe_allow_html=True
                )
                st.divider()

            st.markdown(f"<div class='main-card'><h3>Q{p_idx + 1}: {p['pergunta']}</h3></div>", unsafe_allow_html=True)
            
            if not st.session_state.respondido:
                escolha = st.radio(
                    "Escolha a alternativa correta:",
                    p["opcoes"],
                    index=None,
                    key=f"resp_{p_idx}",
                    label_visibility="collapsed"
                )
                
                aviso_selecao = st.empty()
                
                if st.button("✅ Confirmar Resposta", key=f"btn_conf_resp_{p_idx}", use_container_width=True):
                    if escolha is None:
                        aviso_selecao.warning("⚠️ Selecione uma alternativa antes de confirmar!")
                    else:
                        st.session_state.respondido = True
                        st.session_state.ultima_resposta_correta = (escolha == p["resposta"])
                        
                        if st.session_state.ultima_resposta_correta:
                            st.session_state.pontuacao += pts_acerto
                            st.session_state.acertos += 1
                            st.session_state.total_acertos_partida += 1
                            if st.session_state.acertos >= meta_dado:
                                st.session_state.dado_disponivel = True
                        else:
                            st.session_state.total_erros_partida += 1
                        st.rerun()
                
                if st.button("🚪 Parar e Finalizar Partida", key=f"sair_jogo_{p_idx}", use_container_width=True):
                    st.session_state.respondido = False
                    st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                    ir_para_pagina("fim")

                if st.session_state.tempo_restante > 0:
                    classe_cor = "placar-alerta" if st.session_state.tempo_restante <= config.get("tempo_alerta", 5) else "placar-topo"
                    placeholder_tempo.markdown(f"<span class='{classe_cor}'>⏳ Tempo: {st.session_state.tempo_restante}s</span>", unsafe_allow_html=True)
                    time.sleep(1)
                    st.session_state.tempo_restante -= 1
                    st.rerun()
                else:
                    st.session_state.respondido = True
                    st.session_state.ultima_resposta_correta = (escolha is not None and escolha == p["resposta"])
                    if st.session_state.ultima_resposta_correta:
                        st.session_state.pontuacao += pts_acerto
                        st.session_state.acertos += 1
                        st.session_state.total_acertos_partida += 1
                        if st.session_state.acertos >= meta_dado:
                            st.session_state.dado_disponivel = True
                    else:
                        st.session_state.total_erros_partida += 1
                    st.rerun()
            else:
                placeholder_tempo.markdown("<span class='placar-topo'>⏳ Fim do Tempo</span>", unsafe_allow_html=True)
                
                if st.session_state.ultima_resposta_correta:
                    st.success(f"🎉 Resposta CORRETA! (+{pts_acerto} pontos)")
                    tocar_audio_invisivel(SOM_ACERTO)
                else:
                    st.error(f"❌ Resposta INCORRETA! A correta era: **{p['resposta']}**")
                    tocar_audio_invisivel(SOM_ERRO)
                
                if st.session_state.dado_disponivel:
                    if not st.session_state.baloes_mostrados:
                        soltar_baloes()
                        st.session_state.baloes_mostrados = True
                    
                    if st.session_state.ultima_resposta_correta:
                        st.markdown(
                            f"<h3 style='text-align: center; color: {paleta['cor_destaque']};'>🏆 DADO PREMIADO LIBERADO ({st.session_state.acertos} ACERTOS)!<br>"
                            f"<span style='font-size: 18px; opacity: 0.85;'>Quer continuar respondendo ou encerrar para girar o dado agora?</span></h3>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<h3 style='text-align: center; color: {paleta['cor_destaque']};'>🏆 Fim da sequência! Mas já garantiu o seu Dado Premiado! 🏆</h3>",
                            unsafe_allow_html=True
                        )
                    
                    if st.session_state.pergunta_idx + 1 < total_p:
                        if st.button("➡️ Próxima Pergunta (Continuar Desafio)", key=f"btn_prox_des_{p_idx}", use_container_width=True):
                            st.session_state.respondido = False
                            st.session_state.pergunta_idx += 1
                            st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                            st.rerun()
                    else:
                        st.info("🎉 Você respondeu a todas as perguntas deste modo!")
                    
                    if st.button("🎲 IR PARA O DADO PREMIADO AGORA!", key="btn_ir_dado", use_container_width=True):
                        st.session_state.acertos = 0
                        st.session_state.dado_disponivel = False
                        st.session_state.baloes_mostrados = False
                        st.session_state.respondido = False
                        st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                        st.session_state.dado_girado = False
                        ir_para_pagina("dado")
                else:
                    if st.button("➡️ Próxima Pergunta", key=f"btn_prox_norm_{p_idx}", use_container_width=True):
                        st.session_state.respondido = False
                        st.session_state.pergunta_idx += 1
                        st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                        
                        if st.session_state.pergunta_idx >= total_p:
                            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                            ir_para_pagina("fim")
                        else:
                            st.rerun()
                
                if st.button("🚪 Parar e Finalizar Partida", key=f"sair_jogo_resp_{p_idx}", use_container_width=True):
                    st.session_state.respondido = False
                    st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                    ir_para_pagina("fim")

# ==============================================================================
# 4. SALA DO DADO PREMIADO
# ==============================================================================
elif st.session_state.pagina == "dado":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        dif_str = f" - {st.session_state.dificuldade_ativa}" if st.session_state.get("dificuldade_ativa") else ""
        st.markdown(f"<h1 style='text-align: center;'>{config['txt_sala_dado']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; opacity: 0.85;'>{st.session_state.participante} ({st.session_state.modo_jogo_ativo}{dif_str}) — {config['txt_sub_dado']}</h4>", unsafe_allow_html=True)
        
        placeholder_dado = st.empty()
        
        if not st.session_state.dado_girado:
            with placeholder_dado.container():
                renderizar_dado_3d(numero_final=None, animar=False)
                
            if st.button("🎲 JOGAR O DADO AGORA", key="btn_ir_dado", use_container_width=True):
                resultado_final = random.randint(1, 6)
                tocar_audio_invisivel(SOM_DADO)
                
                with placeholder_dado.container():
                    renderizar_dado_3d(numero_final=resultado_final, animar=True)
                
                time.sleep(3.7)
                
                st.session_state.resultado_dado = resultado_final
                st.session_state.dado_girado = True
                
                tempo_gasto_fmt = formatar_tempo_partida(obter_tempo_decorrido())
                total_resp = st.session_state.total_acertos_partida + st.session_state.total_erros_partida
                precisao = int((st.session_state.total_acertos_partida / total_resp) * 100) if total_resp > 0 else 0
                reg = (
                    f"Participante: {st.session_state.participante} | "
                    f"Modo: {st.session_state.modo_jogo_ativo}{dif_str} | "
                    f"Pontos: {st.session_state.pontuacao} | "
                    f"Acertos: {st.session_state.total_acertos_partida} | "
                    f"Erros: {st.session_state.total_erros_partida} | "
                    f"Precisão: {precisao}% | "
                    f"Tempo: {tempo_gasto_fmt} | "
                    f"Dado: Saiu {resultado_final}"
                )
                historico.append(reg)
                salvar_participantes_historico(participantes, historico)
                st.session_state.historico_salvo_partida = True
                st.rerun()
        else:
            res = st.session_state.resultado_dado
            with placeholder_dado.container():
                renderizar_dado_3d(numero_final=res, animar=False)
            
            tocar_audio_invisivel(SOM_ACERTO)
            soltar_baloes()
                
            st.success(f"O participante {st.session_state.participante} tirou o número {res} no dado e ganhou o prêmio!")
            
            if st.button("🏁 Encerrar Partida e Ver Resumo Final", key="btn_ir_dado", use_container_width=True):
                st.session_state.dado_girado = False
                if st.session_state.tempo_final_congelado is None:
                    st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                ir_para_pagina("fim")

# ==============================================================================
# 5. TELA FINAL / AGRADECIMENTO
# ==============================================================================
elif st.session_state.pagina == "fim":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        modo_fim = obter_modo_visual_atual()
        dif_str = f" - {st.session_state.dificuldade_ativa}" if st.session_state.get("dificuldade_ativa") else ""
        paleta = obter_paleta_ativa()
        if st.session_state.tempo_final_congelado is None:
            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
            
        tempo_final_fmt = formatar_tempo_partida(st.session_state.tempo_final_congelado)
        total_resp = st.session_state.total_acertos_partida + st.session_state.total_erros_partida
        precisao = int((st.session_state.total_acertos_partida / total_resp) * 100) if total_resp > 0 else 0
        
        if not st.session_state.historico_salvo_partida:
            reg_final = (
                f"Participante: {st.session_state.participante} | "
                f"Modo: {modo_fim}{dif_str} | "
                f"Pontos: {st.session_state.pontuacao} | "
                f"Acertos: {st.session_state.total_acertos_partida} | "
                f"Erros: {st.session_state.total_erros_partida} | "
                f"Precisão: {precisao}% | "
                f"Tempo Total: {tempo_final_fmt}"
            )
            historico.append(reg_final)
            salvar_participantes_historico(participantes, historico)
            st.session_state.historico_salvo_partida = True
            
        st.markdown(f"<h1 style='text-align: center;'>{config['txt_titulo_fim']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>Participante: {st.session_state.participante} ({modo_fim}{dif_str})</h3>", unsafe_allow_html=True)
        st.markdown(
            f"<h4 style='text-align: center; color: {paleta['cor_destaque']};'>"
            f"⭐ {st.session_state.pontuacao} Pontos &nbsp;|&nbsp; "
            f"✅ {st.session_state.total_acertos_partida} Acertos &nbsp;|&nbsp; "
            f"❌ {st.session_state.total_erros_partida} Erros &nbsp;|&nbsp; "
            f"🎯 {precisao}% Precisão &nbsp;|&nbsp; "
            f"⏱️ Tempo: {tempo_final_fmt}"
            f"</h4>",
            unsafe_allow_html=True
        )
        
        mostrar_painel_tema(modo_especifico=modo_fim)
        
        frase_do_tema = config.get("msgs_finais_temas", {}).get(modo_fim, INFO_MODOS[modo_fim]["msg_final"])
        st.markdown(
            f"<p style='text-align: center; font-style: italic; font-size: 20px; font-weight: 600; "
            f"color: {paleta['cor_destaque']} !important; margin-top: 15px;'>{frase_do_tema}</p>",
            unsafe_allow_html=True
        )
        
        if st.session_state.dado_disponivel:
            if st.button("🎲 IR PARA O DADO PREMIADO AGORA!", key="btn_ir_dado", use_container_width=True):
                st.session_state.dado_disponivel = False
                st.session_state.dado_girado = False
                ir_para_pagina("dado")
                
        if st.button("🏠 Voltar ao Menu Inicial", use_container_width=True):
            st.session_state.modo_jogo_ativo = None
            ir_para_pagina("menu")

# ==============================================================================
# 6. CADASTRAR PARTICIPANTES
# ==============================================================================
elif st.session_state.pagina == "cadastrar_participantes":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        st.markdown("<h2 style='text-align: center;'>👥 Gestão de Participantes</h2>", unsafe_allow_html=True)
        if st.button("⬅️ Voltar ao Menu", key="voltar_part_topo"):
            ir_para_pagina("menu")
                
        novo_p = st.text_input("Nome do novo participante:")
        if st.button("➕ Adicionar à Lista"):
            if novo_p.strip() and novo_p.strip() not in participantes:
                participantes.append(novo_p.strip())
                salvar_participantes_historico(participantes, historico)
                st.success(f"Participante '{novo_p.strip()}' cadastrado com sucesso!")
                st.rerun()
            else:
                st.warning("Insira um nome válido ou já existente.")
                
        st.markdown("<h3 style='text-align: center; margin-top: 20px;'>Participantes Atuais:</h3>", unsafe_allow_html=True)
        if participantes:
            for p in list(participantes):
                st.markdown(f"<h4 style='text-align: center;'>👤 {p}</h4>", unsafe_allow_html=True)
                if st.button(f"🗑️ Remover {p}", key=f"del_part_{p}"):
                    participantes.remove(p)
                    salvar_participantes_historico(participantes, historico)
                    st.rerun()
        else:
            st.info("Nenhum participante cadastrado.")

# ==============================================================================
# 7. HISTÓRICO + RANKING TOP 5
# ==============================================================================
elif st.session_state.pagina == "historico":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        st.markdown("<h2 style='text-align: center;'>🏆 Ranking Top 5 & Histórico de Partidas</h2>", unsafe_allow_html=True)
        if st.button("⬅️ Voltar ao Menu", key="voltar_hist_topo"):
            ir_para_pagina("menu")
        
        top5 = extrair_ranking_top5(historico)
        if top5:
            st.markdown("<h3 style='text-align: center; color: #F4D35E;'>🥇 Pódio dos Melhores Jogadores</h3>", unsafe_allow_html=True)
            medalhas = ["🥇 1º", "🥈 2º", "🥉 3º", "🏅 4º", "🏅 5º"]
            if st.session_state.modo_mobile:
                for idx_r, reg_r in enumerate(top5):
                    st.markdown(
                        f"<div class='main-card' style='padding: 12px; margin-bottom: 10px;'>"
                        f"<h4 style='text-align: center; color: #F4D35E !important;'>{medalhas[idx_r]} — {reg_r['nome']} (⭐ {reg_r['pontos']} pts)</h4>"
                        f"<p style='text-align: center; font-size: 13px; margin: 0;'>{reg_r['modo']}</p>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                cols_rk = st.columns(len(top5))
                for idx_r, reg_r in enumerate(top5):
                    with cols_rk[idx_r]:
                        st.markdown(
                            f"<div class='main-card' style='padding: 15px;'>"
                            f"<h4 style='text-align: center; color: #F4D35E !important;'>{medalhas[idx_r]}</h4>"
                            f"<h3 style='text-align: center;'>{reg_r['nome']}</h3>"
                            f"<p style='text-align: center; font-weight: bold; font-size: 20px;'>⭐ {reg_r['pontos']} pts</p>"
                            f"<p style='text-align: center; font-size: 14px; opacity: 0.85;'>{reg_r['modo']}</p>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
        
        st.divider()
        if historico:
            st.write("### 📜 Todos os Registos (Selecione para apagar):")
            itens_para_apagar = []
            for idx, item in enumerate(historico):
                if st.checkbox(item, key=f"chk_hist_{idx}"):
                    itens_para_apagar.append(item)
            
            if itens_para_apagar and st.button("🗑️ Apagar Selecionados"):
                for it in itens_para_apagar:
                    historico.remove(it)
                salvar_participantes_historico(participantes, historico)
                st.rerun()
            if st.button("🗑️ Limpar Todo o Histórico"):
                historico.clear()
                salvar_participantes_historico(participantes, historico)
                st.rerun()
        else:
            st.info("Ainda não existem registos no histórico.")

# ==============================================================================
# 8. GERIR / EDITAR PERGUNTAS DIRETO NOS FICHEIROS .JSON DE CADA TEMA
# ==============================================================================
elif st.session_state.pagina == "gerir_perguntas":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        st.markdown("<h2 style='text-align: center;'>📝 Gestão de Perguntas (Ficheiros .JSON Independentes)</h2>", unsafe_allow_html=True)
        
        if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_topo", use_container_width=True):
            st.session_state.editando_idx = None
            st.session_state.modo_jogo_ativo = None
            ir_para_pagina("menu")
        if st.button("➕ Nova Pergunta neste Nível", key="btn_nova_perg_topo", use_container_width=True):
            st.session_state.editando_idx = -1
            st.rerun()

        idx_t = TEMAS_INDIVIDUAIS.index(st.session_state.tema_gerir_selecionado) if st.session_state.tema_gerir_selecionado in TEMAS_INDIVIDUAIS else 0
        tema_sel_gerir = st.selectbox("📂 1. Selecione o Banco de Dados (.json):", TEMAS_INDIVIDUAIS, index=idx_t)
        
        if tema_sel_gerir != st.session_state.tema_gerir_selecionado:
            st.session_state.tema_gerir_selecionado = tema_sel_gerir
            st.session_state.modo_jogo_ativo = tema_sel_gerir
            st.session_state.editando_idx = None
            st.rerun()

        idx_n = NIVEIS_DIFICULDADE.index(st.session_state.nivel_gerir_selecionado) if st.session_state.nivel_gerir_selecionado in NIVEIS_DIFICULDADE else 0
        niv_sel_gerir = st.selectbox("🎯 2. Selecione o Nível de Dificuldade:", NIVEIS_DIFICULDADE, index=idx_n)
        if niv_sel_gerir != st.session_state.nivel_gerir_selecionado:
            st.session_state.nivel_gerir_selecionado = niv_sel_gerir
            st.session_state.editando_idx = None
            st.rerun()

        arq_nome = INFO_MODOS[tema_sel_gerir]["arquivo_json"]
        perguntas_do_tema = bancos_perguntas.get(tema_sel_gerir, {}).get(niv_sel_gerir, [])
        rotulo_banco = f"{tema_sel_gerir} — {niv_sel_gerir} ({arq_nome})"

        if st.session_state.editando_idx is not None:
            idx_edit = st.session_state.editando_idx
            is_novo = (idx_edit == -1)
            
            titulo_form = f"Adicionar Nova Pergunta em {rotulo_banco}" if is_novo else f"Editar Pergunta #{idx_edit + 1} ({rotulo_banco})"
            st.markdown(f"<h3 style='text-align: center;'>{titulo_form}</h3>", unsafe_allow_html=True)
            
            p_val = perguntas_do_tema[idx_edit]["pergunta"] if not is_novo else ""
            ops_val = perguntas_do_tema[idx_edit]["opcoes"] if not is_novo else ["A) ", "B) ", "C) ", "D) "]
            resp_val = perguntas_do_tema[idx_edit]["resposta"] if not is_novo else "A) "
            
            with st.form("form_edit_pergunta"):
                nova_p = st.text_input("Enunciado da Pergunta:", value=p_val)
                op1 = st.text_input("Opção 1:", value=ops_val[0] if len(ops_val)>0 else "")
                op2 = st.text_input("Opção 2:", value=ops_val[1] if len(ops_val)>1 else "")
                op3 = st.text_input("Opção 3:", value=ops_val[2] if len(ops_val)>2 else "")
                op4 = st.text_input("Opção 4:", value=ops_val[3] if len(ops_val)>3 else "")
                correta = st.text_input("Texto exato da Resposta Correta:", value=resp_val)
                
                btn_sub = st.form_submit_button("💾 Salvar no Ficheiro .JSON")
                if btn_sub:
                    if nova_p and op1 and op2 and op3 and op4 and correta:
                        ops = [op1, op2, op3, op4]
                        if correta in ops:
                            item_novo = {"pergunta": nova_p, "opcoes": ops, "resposta": correta}
                            if is_novo:
                                perguntas_do_tema.insert(0, item_novo)
                            else:
                                perguntas_do_tema[idx_edit] = item_novo
                            bancos_perguntas[tema_sel_gerir][niv_sel_gerir] = perguntas_do_tema
                            salvar_banco_tema(tema_sel_gerir, bancos_perguntas[tema_sel_gerir])
                            st.session_state.editando_idx = None
                            st.success(f"Pergunta salva com sucesso em '{arq_nome}'!")
                            st.rerun()
                        else:
                            st.error("A resposta correta tem de coincidir exatamente com uma das 4 opções.")
                    else:
                        st.warning("Preencha todos os campos.")
                        
            if st.button("❌ Cancelar Edição"):
                st.session_state.editando_idx = None
                st.rerun()
                
        st.write("---")
        st.markdown(f"<h3 style='text-align: center;'>📋 {rotulo_banco} — {len(perguntas_do_tema)} perguntas</h3>", unsafe_allow_html=True)
        
        busca_txt = st.text_input("🔍 Filtrar / Pesquisar pergunta neste banco:", "")
        
        for idx, item in enumerate(perguntas_do_tema):
            if busca_txt.strip().lower() in item["pergunta"].lower() or busca_txt.strip().lower() in item["resposta"].lower():
                col_txt, col_edit, col_del = st.columns([5, 1, 1])
                with col_txt:
                    st.write(f"**{idx+1}. {item['pergunta']}** *(Resp: {item['resposta']})*")
                with col_edit:
                    if st.button("✏️", key=f"edit_p_{tema_sel_gerir}_{niv_sel_gerir}_{idx}"):
                        st.session_state.editando_idx = idx
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_p_{tema_sel_gerir}_{niv_sel_gerir}_{idx}"):
                        perguntas_do_tema.pop(idx)
                        bancos_perguntas[tema_sel_gerir][niv_sel_gerir] = perguntas_do_tema
                        salvar_banco_tema(tema_sel_gerir, bancos_perguntas[tema_sel_gerir])
                        st.rerun()

# ==============================================================================
# 9. CONFIGURAÇÕES SIMPLIFICADAS E DIRETAS
# ==============================================================================
elif st.session_state.pagina == "configuracoes":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        st.markdown("<h2 style='text-align: center;'>⚙️ Painel de Configurações</h2>", unsafe_allow_html=True)
        if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_cfg_topo"):
            st.session_state.msg_upload_ok = ""
            st.session_state.modo_jogo_ativo = None
            ir_para_pagina("menu")

        if st.session_state.msg_upload_ok:
            st.success(st.session_state.msg_upload_ok)
            st.session_state.msg_upload_ok = ""

        aba_img, aba_regras_tam, aba_textos, aba_sons = st.tabs([
            "🖼️ 1. Imagens & Frases",
            "🎯 2. Regras & Tamanhos",
            "✍️ 3. Textos do Menu",
            "🔊 4. Sons & Restauro"
        ])
        
        with aba_img:
            col_im1, col_im2 = st.columns([1.5, 1]) if not st.session_state.modo_mobile else (st.container(), st.container())
            with col_im1:
                st.markdown("<h3 style='text-align: center;'>🖼️ Personalizar Imagem e Frase Final de cada Tema</h3>", unsafe_allow_html=True)
                idx_tm = LISTA_MODOS_JOGO.index(st.session_state.tema_img_cfg) if st.session_state.tema_img_cfg in LISTA_MODOS_JOGO else 0
                tema_cfg_sel = st.selectbox("Selecione o Tema para personalizar:", LISTA_MODOS_JOGO, index=idx_tm)
                
                if tema_cfg_sel != st.session_state.tema_img_cfg:
                    st.session_state.tema_img_cfg = tema_cfg_sel
                    st.session_state.modo_jogo_ativo = tema_cfg_sel
                    st.rerun()

                titulo_tema_atual = st.text_input(
                    f"Legenda acima da imagem ({tema_cfg_sel}):",
                    value=config.get("titulos_temas", {}).get(tema_cfg_sel, INFO_MODOS[tema_cfg_sel]["titulo_card"])
                )
                config["titulos_temas"][tema_cfg_sel] = titulo_tema_atual

                msg_final_tema_atual = st.text_input(
                    f"Frase de Parabéns no Final da Partida ({tema_cfg_sel}):",
                    value=config.get("msgs_finais_temas", {}).get(tema_cfg_sel, INFO_MODOS[tema_cfg_sel]["msg_final"])
                )
                config["msgs_finais_temas"][tema_cfg_sel] = msg_final_tema_atual

                arq_destino_tema = INFO_MODOS[tema_cfg_sel]["img_padrao"]
                up_img_tema = st.file_uploader(
                    f"Subir foto personalizada para {tema_cfg_sel} (PNG/JPG):",
                    type=["png", "jpg", "jpeg"],
                    key=f"up_img_t_{st.session_state.up_cnt}"
                )
                if up_img_tema is not None:
                    with open(arq_destino_tema, "wb") as f:
                        f.write(up_img_tema.getbuffer())
                    salvar_config(config)
                    st.session_state.up_cnt += 1
                    st.session_state.msg_upload_ok = f"✅ Nova imagem para o tema {tema_cfg_sel} salva com sucesso!"
                    st.rerun()

                if tema_cfg_sel != "⛪ Igreja" and os.path.exists(arq_destino_tema):
                    if st.button(f"🗑️ Remover foto e usar Pôster Automático de {tema_cfg_sel}"):
                        os.remove(arq_destino_tema)
                        st.session_state.msg_upload_ok = f"✅ Pôster ilustrado automático de {tema_cfg_sel} reativado!"
                        st.rerun()

                st.divider()
                st.markdown("<h3 style='text-align: center;'>🎨 Cor do Menu Inicial e Moldura</h3>", unsafe_allow_html=True)
                idx_m_ini = LISTA_MODOS_JOGO.index(config.get("tema_menu_inicial", "⛪ Igreja")) if config.get("tema_menu_inicial") in LISTA_MODOS_JOGO else 0
                tema_menu_val = st.selectbox("Qual paleta de cores usar no Menu Principal (Home)?", LISTA_MODOS_JOGO, index=idx_m_ini)
                tamanho_img_val = st.slider("Largura da Imagem / Pôster Lateral (px):", 200, 600, int(config.get("tamanho_imagem", 360)), 10)
                borda_img_val = st.slider("Arredondamento da Moldura (px):", 0, 100, int(config.get("borda_imagem", 14)), 2)

                st.divider()
                st.markdown("<h3 style='text-align: center;'>🌄 Wallpaper de Plano de Fundo (Opcional)</h3>", unsafe_allow_html=True)
                usar_bg_img = st.checkbox("Usar imagem de Wallpaper no fundo da tela", value=config.get("usar_fundo_img", False))
                opacidade_bg_val = st.slider("Escurecer Wallpaper de fundo:", 0.0, 0.95, float(config.get("opacidade_fundo", 0.7)), 0.05)
                up_bg = st.file_uploader("Carregar Wallpaper (PNG/JPG):", type=["png", "jpg", "jpeg"], key=f"up_bg_{st.session_state.up_cnt}")
                if up_bg is not None:
                    with open("fundo_quiz_geral.png", "wb") as f:
                        f.write(up_bg.getbuffer())
                    config["imagem_fundo"] = "fundo_quiz_geral.png"
                    config["usar_fundo_img"] = True
                    salvar_config(config)
                    st.session_state.up_cnt += 1
                    st.session_state.msg_upload_ok = "✅ Wallpaper carregado com sucesso!"
                    st.rerun()

            with col_im2:
                st.markdown("<h4 style='text-align: center;'>🖼️ Pré-visualização</h4>", unsafe_allow_html=True)
                mostrar_painel_tema(modo_especifico=tema_cfg_sel, largura_custom=tamanho_img_val, borda_custom=borda_img_val)
                st.markdown(
                    f"<p style='text-align: center; font-style: italic; margin-top: 15px;'>\"{msg_final_tema_atual}\"</p>",
                    unsafe_allow_html=True
                )

        with aba_regras_tam:
            st.markdown("<h3 style='text-align: center;'>🎯 Regras da Partida</h3>", unsafe_allow_html=True)
            cr1, cr2 = st.columns(2)
            with cr1:
                tempo_perg_val = st.number_input("Tempo por Pergunta (seg):", 5, 300, int(config.get("tempo_pergunta", 30)))
                tempo_alerta_val = st.number_input("Alerta Vermelho nos últimos (seg):", 1, 30, int(config.get("tempo_alerta", 5)))
            with cr2:
                acertos_dado_val = st.number_input("Acertos para liberar o Dado:", 1, 20, int(config.get("acertos_para_dado", 3)))
                pts_acerto_val = st.number_input("Pontos Base por Acerto:", 10, 1000, int(config.get("pontos_por_acerto", 100)), 10)

            st.divider()
            st.markdown("<h3 style='text-align: center;'>📏 Ajuste de Tamanho (Modo Desktop)</h3>", unsafe_allow_html=True)
            ct1, ct2 = st.columns(2)
            with ct1:
                larg_btn_val = st.slider("Largura Máxima dos Botões e Caixas (px):", 300, 900, int(config.get("largura_botao", 520)), 10)
                alt_btn_val = st.slider("Altura dos Botões (px):", 8, 36, int(config.get("altura_botao", 16)), 2)
                tam_f_btn_val = st.slider("Tamanho da Letra dos Botões (px):", 14, 36, int(config.get("tam_fonte_botao", 22)), 1)
            with ct2:
                tam_f_tit_val = st.slider("Tamanho do Título Principal (px):", 28, 72, int(config.get("tam_fonte_titulo", 46)), 2)
                tam_f_perg_val = st.slider("Tamanho da Letra da Pergunta (px):", 20, 50, int(config.get("tam_fonte_pergunta", 30)), 1)
                tam_f_opc_val = st.slider("Tamanho da Letra das Alternativas A, B, C, D (px):", 16, 42, int(config.get("tam_fonte_opcoes", 24)), 1)

        with aba_textos:
            st.markdown("<h3 style='text-align: center;'>✍️ Textos e Títulos do Sistema</h3>", unsafe_allow_html=True)
            tx1, tx2 = st.columns(2)
            with tx1:
                txt_tit_menu_val = st.text_input("Título Principal do Menu:", value=config.get("txt_titulo_menu", ""))
                txt_sub_menu_val = st.text_input("Subtítulo do Menu:", value=config.get("txt_subtitulo_menu", ""))
                txt_sala_dado_val = st.text_input("Título da Sala do Dado:", value=config.get("txt_sala_dado", ""))
                txt_sub_dado_val = st.text_input("Subtítulo da Sala do Dado:", value=config.get("txt_sub_dado", ""))
                txt_tit_fim_val = st.text_input("Título da Tela Final:", value=config.get("txt_titulo_fim", ""))
            with tx2:
                txt_b_jogar_val = st.text_input("Texto do Botão Jogar:", value=config.get("txt_btn_jogar", ""))
                txt_b_part_val = st.text_input("Texto do Botão Participantes:", value=config.get("txt_btn_participantes", ""))
                txt_b_perg_val = st.text_input("Texto do Botão Perguntas:", value=config.get("txt_btn_perguntas", ""))
                txt_b_hist_val = st.text_input("Texto do Botão Histórico:", value=config.get("txt_btn_historico", ""))
                txt_b_cfg_val = st.text_input("Texto do Botão Configurações:", value=config.get("txt_btn_config", ""))
                txt_b_sair_val = st.text_input("Texto do Botão Sair:", value=config.get("txt_btn_sair", ""))

        with aba_sons:
            st.markdown("<h3 style='text-align: center;'>🔊 Efeitos Sonoros e Animações</h3>", unsafe_allow_html=True)
            cs1, cs2 = st.columns(2)
            with cs1:
                ativar_sons_val = st.checkbox("🔊 Ativar Efeitos Sonoros do Jogo", value=config.get("ativar_sons", True))
                ativar_baloes_val = st.checkbox("🎈 Ativar Chuva de Balões nas Conquistas", value=config.get("ativar_baloes", True))
            with cs2:
                st.write("**Substituir ficheiros de áudio (MP3):**")
                up_som_tic = st.file_uploader("Som do Relógio (Tic-Tac):", type=["mp3"], key=f"up_s1_{st.session_state.up_cnt}")
                if up_som_tic is not None:
                    with open(SOM_TIC_TAK, "wb") as f: f.write(up_som_tic.getbuffer())
                    st.session_state.up_cnt += 1
                    st.session_state.msg_upload_ok = "✅ Som Tic-Tac atualizado!"
                    st.rerun()
                up_som_dado = st.file_uploader("Som a Girar o Dado:", type=["mp3"], key=f"up_s2_{st.session_state.up_cnt}")
                if up_som_dado is not None:
                    with open(SOM_DADO, "wb") as f: f.write(up_som_dado.getbuffer())
                    st.session_state.up_cnt += 1
                    st.session_state.msg_upload_ok = "✅ Som do Dado atualizado!"
                    st.rerun()
                up_som_ok = st.file_uploader("Som de Resposta Certa (Aplausos):", type=["mp3"], key=f"up_s3_{st.session_state.up_cnt}")
                if up_som_ok is not None:
                    with open(SOM_ACERTO, "wb") as f: f.write(up_som_ok.getbuffer())
                    st.session_state.up_cnt += 1
                    st.session_state.msg_upload_ok = "✅ Som de Acerto atualizado!"
                    st.rerun()
                up_som_err = st.file_uploader("Som de Resposta Errada:", type=["mp3"], key=f"up_s4_{st.session_state.up_cnt}")
                if up_som_err is not None:
                    with open(SOM_ERRO, "wb") as f: f.write(up_som_err.getbuffer())
                    st.session_state.up_cnt += 1
                    st.session_state.msg_upload_ok = "✅ Som de Erro atualizado!"
                    st.rerun()

            st.divider()
            st.markdown("<h3 style='text-align: center;'>♻️ Restaurar Configurações Visuais</h3>", unsafe_allow_html=True)
            if st.button("🔄 Restaurar Configurações Padrão", key="btn_restaurar_orig"):
                salvar_config(obter_config_padrao())
                st.session_state.up_cnt += 1
                st.session_state.msg_upload_ok = "🔄 Configurações visuais restauradas com sucesso!"
                st.rerun()

        st.write("---")
        if st.button("💾 SALVAR CONFIGURAÇÕES", key="btn_ir_dado", use_container_width=True):
            config.update({
                "tema_menu_inicial": tema_menu_val,
                "usar_fundo_img": usar_bg_img,
                "opacidade_fundo": float(opacidade_bg_val),
                "largura_botao": int(larg_btn_val),
                "altura_botao": int(alt_btn_val),
                "tam_fonte_botao": int(tam_f_btn_val),
                "tam_fonte_titulo": int(tam_f_tit_val),
                "tam_fonte_pergunta": int(tam_f_perg_val),
                "tam_fonte_opcoes": int(tam_f_opc_val),
                "txt_titulo_menu": txt_tit_menu_val,
                "txt_subtitulo_menu": txt_sub_menu_val,
                "txt_sala_dado": txt_sala_dado_val,
                "txt_sub_dado": txt_sub_dado_val,
                "txt_titulo_fim": txt_tit_fim_val,
                "txt_btn_jogar": txt_b_jogar_val,
                "txt_btn_participantes": txt_b_part_val,
                "txt_btn_perguntas": txt_b_perg_val,
                "txt_btn_historico": txt_b_hist_val,
                "txt_btn_config": txt_b_cfg_val,
                "txt_btn_sair": txt_b_sair_val,
                "tamanho_imagem": int(tamanho_img_val),
                "borda_imagem": int(borda_img_val),
                "tempo_pergunta": int(tempo_perg_val),
                "tempo_alerta": int(tempo_alerta_val),
                "acertos_para_dado": int(acertos_dado_val),
                "pontos_por_acerto": int(pts_acerto_val),
                "ativar_sons": bool(ativar_sons_val),
                "ativar_baloes": bool(ativar_baloes_val)
            })
            salvar_config(config)
            st.session_state.msg_upload_ok = "✅ Configurações salvas com sucesso!"
            st.rerun()
            
        if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_cfg_rodape", use_container_width=True):
            st.session_state.msg_upload_ok = ""
            st.session_state.modo_jogo_ativo = None
            ir_para_pagina("menu")
