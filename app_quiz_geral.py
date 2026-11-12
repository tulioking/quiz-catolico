# ==============================================================================
# QUIZ UNIVERSAL & FESTEJOS - VERSÃO ESTÚDIO PERSONALIZÁVEL (APP_QUIZ_GERAL) ⛪🎵🎲
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time
import base64
import re

# Ficheiros exclusivos para o Quiz Geral (não interfere no quiz da igreja!)
ARQUIVO_DADOS = "dados_quiz_geral.json"
ARQUIVO_CONFIG = "config_quiz_geral.json"

# ==============================================================================
# CONFIGURAÇÕES PADRÃO E TEMAS PRÉ-DEFINIDOS
# ==============================================================================
TEMAS_PRONTOS = {
    "Personalizado (Livre)": None,
    "Azul Mariano (Padrão)": {
        "cor_fundo": "#0B2545", "cor_card": "#134074", "cor_texto": "#FFFFFF",
        "cor_destaque": "#F4D35E", "cor_botao": "#134074", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#1F618D"
    },
    "Noite Dourada (Gala / Evento)": {
        "cor_fundo": "#121212", "cor_card": "#1E1E1E", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFD700", "cor_botao": "#292929", "cor_texto_botao": "#FFD700", "cor_borda_botao": "#FFD700"
    },
    "Verde Esperança (Jovens / Natureza)": {
        "cor_fundo": "#0F291E", "cor_card": "#1B4332", "cor_texto": "#FFFFFF",
        "cor_destaque": "#74C69D", "cor_botao": "#2D6A4F", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#52B788"
    },
    "Roxo Solene (Litúrgico / Elegante)": {
        "cor_fundo": "#240046", "cor_card": "#3C096C", "cor_texto": "#FFFFFF",
        "cor_destaque": "#E0AAFF", "cor_botao": "#5A189A", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#9D4EDD"
    },
    "Vermelho Festa (Quermesse / Dinâmico)": {
        "cor_fundo": "#370617", "cor_card": "#6A040F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFBA08", "cor_botao": "#9D0208", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#F48C06"
    }
}

def obter_config_padrao():
    return {
        # Imagens e Sons
        "imagem_ns": "nossa_senhora.png",
        "tamanho_imagem": 360,
        "borda_imagem": 12,
        "usar_fundo_img": False,
        "imagem_fundo": "fundo_quiz_geral.png",
        "opacidade_fundo": 0.7,
        
        # Regras do Jogo
        "tempo_pergunta": 30,
        "tempo_alerta": 5,
        "acertos_para_dado": 3,
        "pontos_por_acerto": 100,
        "ativar_sons": True,
        "ativar_baloes": True,
        
        # Cores
        "tema_escolhido": "Azul Mariano (Padrão)",
        "cor_fundo": "#0B2545",
        "cor_card": "#134074",
        "cor_texto": "#FFFFFF",
        "cor_destaque": "#F4D35E",
        "cor_botao": "#134074",
        "cor_texto_botao": "#FFFFFF",
        "cor_borda_botao": "#1F618D",
        "cor_botao_dado": "#F4D35E",
        "cor_botao_sair": "#E74C3C",
        
        # Tamanhos (Fontes e Botões)
        "tam_fonte_titulo": 46,
        "tam_fonte_pergunta": 32,
        "tam_fonte_opcoes": 26,
        "tam_fonte_placar": 22,
        "tam_fonte_botao": 22,
        "largura_botao": 500,
        "altura_botao": 16,
        "raio_borda_botao": 10,
        
        # Textos Físicos Personalizáveis
        "titulo_aba": "Quiz Geral Personalizável",
        "icone_aba": "🎲",
        "txt_titulo_menu": "⛪ Festejos da Imaculada Conceição ⛪",
        "txt_subtitulo_menu": "Quiz Interativo (Pressione F11 para ecrã inteiro)",
        "txt_titulo_imagem": "🌸 Imaculada Conceição",
        "txt_btn_jogar": "▶️ Jogar / Iniciar Quiz",
        "txt_btn_participantes": "👥 Cadastrar Participantes",
        "txt_btn_perguntas": "📝 Cadastrar / Gerir / Editar Perguntas",
        "txt_btn_historico": "📊 Histórico de Acertos e Prémios",
        "txt_btn_config": "⚙️ Estúdio de Personalização (Configurações)",
        "txt_btn_sair": "🚪 Sair / Fechar Sistema",
        "txt_sala_dado": "🎲 SALA DO DADO PREMIADO! 🎲",
        "txt_sub_dado": "Parabéns! Chegou a hora de lançar o dado!",
        "txt_titulo_fim": "🎉 FIM DA PARTIDA! PARABÉNS! 🎉",
        "txt_msg_final": "Que Nossa Senhora Imaculada Conceição abençoe grandemente a tua família!"
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
                return cfg
        except Exception:
            pass
    return padrao

def salvar_config(config_dict):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config_dict, f, ensure_ascii=False, indent=4)

config = carregar_config()

st.set_page_config(
    page_title=config.get("titulo_aba", "Quiz Geral"),
    page_icon=config.get("icone_aba", "🎲"),
    layout="wide"
)

# ==============================================================================
# GERADOR DE CSS DINÂMICO (APLICA CORES, PLANO DE FUNDO, BOTÕES E TAMANHOS)
# ==============================================================================
def aplicar_estilos_dinamicos():
    bg_css = f"background-color: {config['cor_fundo']};"
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
            color: {config['cor_texto']};
        }}
        audio {{
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }}
        .placar-topo {{
            font-size: {config['tam_fonte_placar']}px !important;
            font-weight: bold !important;
            color: {config['cor_destaque']} !important;
        }}
        .placar-alerta {{
            font-size: {config['tam_fonte_placar'] + 2}px !important;
            font-weight: bold !important;
            color: #FF4B4B !important;
        }}
        .main-card {{
            background-color: {config['cor_card']};
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.45);
            margin-bottom: 25px;
            border: 1px solid {config['cor_borda_botao']};
        }}
        .main-card h3 {{
            font-size: {config['tam_fonte_pergunta']}px !important;
            line-height: 1.4 !important;
            color: {config['cor_texto']} !important;
            margin: 0 !important;
        }}
        /* ALTERNATIVAS DE RESPOSTA */
        .stRadio div[role="radiogroup"] label div p {{
            font-size: {config['tam_fonte_opcoes']}px !important;
            font-weight: 700 !important;
            color: {config['cor_texto']} !important;
        }}
        .stRadio div[role="radiogroup"] label {{
            padding: 12px 0px !important;
        }}
        /* CENTRALIZAÇÃO E ESTILO DOS BOTÕES */
        div.stButton, [data-testid="stButton"], .stElementContainer:has(button) {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            margin: 0 auto !important;
        }}
        div.stButton > button, [data-testid="stButton"] > button {{
            background-color: {config['cor_botao']} !important;
            color: {config['cor_texto_botao']} !important;
            font-weight: bold !important;
            border-radius: {config['raio_borda_botao']}px !important;
            width: 100% !important;
            max-width: {config['largura_botao']}px !important;
            padding: {config['altura_botao']}px !important;
            border: 2px solid {config['cor_borda_botao']} !important;
            font-size: {config['tam_fonte_botao']}px !important;
            display: block !important;
            margin: 8px auto !important;
            text-align: center !important;
            transition: all 0.2s ease !important;
        }}
        div.stButton > button:hover, [data-testid="stButton"] > button:hover {{
            filter: brightness(1.2) !important;
            border-color: {config['cor_destaque']} !important;
        }}
        /* BOTÃO ESPECIAL DO DADO PREMIADO */
        .st-key-btn_ir_dado, .st-key-btn_ir_dado > div {{
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            margin: 0 auto !important;
        }}
        .st-key-btn_ir_dado button {{
            background-color: {config['cor_botao_dado']} !important;
            color: #0B2545 !important;
            border: 3px solid #FFFFFF !important;
            font-size: {config['tam_fonte_botao'] + 2}px !important;
            max-width: {config['largura_botao']}px !important;
            width: 100% !important;
            margin: 10px auto !important;
            box-shadow: 0 0 20px rgba(244, 211, 94, 0.7) !important;
        }}
        .st-key-sair_sis button {{
            background-color: {config['cor_botao_sair']} !important;
            border: none !important;
            color: #FFFFFF !important;
        }}
        h1, h2, h3, h4, p, label {{
            color: {config['cor_texto']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

aplicar_estilos_dinamicos()

# ==============================================================================
# FUNÇÕES DE DADOS E UTILITÁRIOS
# ==============================================================================
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

def mostrar_santa(largura_custom=None, borda_custom=None, titulo_custom=None):
    img_path = config.get("imagem_ns", "nossa_senhora.png")
    if not os.path.exists(img_path) and os.path.exists("nossa_senhora.png"):
        img_path = "nossa_senhora.png"
        
    largura = largura_custom if largura_custom is not None else config.get("tamanho_imagem", 360)
    borda = borda_custom if borda_custom is not None else config.get("borda_imagem", 12)
    titulo = titulo_custom if titulo_custom is not None else config.get("txt_titulo_imagem", "🌸 Imaculada Conceição")
    
    html_bloco = "<div style='text-align: center; width: 100%;'>"
    if titulo.strip():
        html_bloco += f"<h3 style='margin-bottom: 15px; color: {config['cor_texto']};'>{titulo}</h3>"
    
    if os.path.exists(img_path):
        try:
            with open(img_path, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            html_bloco += (
                f"<img src='data:image/png;base64,{b64_img}' "
                f"style='width: {largura}px; max-width: 100%; height: auto; "
                f"margin: 0 auto; display: block; border-radius: {borda}px; "
                f"box-shadow: 0 4px 15px rgba(0,0,0,0.45);' />"
            )
        except Exception:
            html_bloco += "<p style='color: #F4D35E;'>Erro ao ler imagem.</p>"
    else:
        html_bloco += f"<p style='color: #8DA9C4;'>Imagem '{img_path}' não encontrada.</p>"
        
    html_bloco += "</div>"
    st.markdown(html_bloco, unsafe_allow_html=True)

def renderizar_dado_3d(numero_final=None, animar=False):
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
        badge_html = "<div class='resultado-texto' style='color: #8DA9C4;'>🎲 A lançar o dado...</div>"
    else:
        badge_html = "<div class='resultado-texto' style='color: #8DA9C4;'>Clique no botão abaixo para jogar o dado!</div>"

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
            background: radial-gradient(circle, {config['cor_card']} 0%, {config['cor_fundo']} 90%);
            border: 3px solid {'#2ECC71' if (numero_final and not animar) else config['cor_destaque']};
            border-radius: 20px; width: 92%; max-width: 520px; height: 320px;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); position: relative; margin: 0 auto;
        }}
        .scene {{ width: 130px; height: 130px; perspective: 750px; margin-top: 25px; }}
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
            border-radius: 50%; filter: blur(7px); margin-top: 38px;
        }}
        .resultado-texto {{
            margin-top: 18px; font-size: 26px; font-weight: 800;
            color: {config['cor_destaque']}; text-shadow: 0 2px 8px rgba(0,0,0,0.5);
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
    components.html(html_code, height=345)

# Inicialização de Estados da Sessão
estados_iniciais = {
    "pagina": "menu", "participante": "", "pergunta_idx": 0, "pontuacao": 0,
    "acertos": 0, "total_acertos_partida": 0, "total_erros_partida": 0,
    "inicio_partida": None, "tempo_final_congelado": None, "perguntas_sessao": [],
    "respondido": False, "ultima_resposta_correta": None, "dado_girado": False,
    "resultado_dado": None, "editando_idx": None, "tempo_restante": 30,
    "baloes_mostrados": False, "dado_disponivel": False, "historico_salvo_partida": False,
    "up_cnt": 0, "msg_upload_ok": ""
}
for chave, valor_padrao in estados_iniciais.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor_padrao

perguntas, participantes, historico = carregar_dados()

# Ficheiros de áudio locais (partilhados na mesma pasta)
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
# 1. MENU PRINCIPAL (TOTALMENTE DINÂMICO E CENTRALIZADO)
# ==============================================================================
if st.session_state.pagina == "menu":
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<h1 style='text-align: center; font-size: {config['tam_fonte_titulo']}px;'>{config['txt_titulo_menu']}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<h4 style='text-align: center; opacity: 0.85; margin-bottom: 35px;'>{config['txt_subtitulo_menu']}</h4>",
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        if st.button(config["txt_btn_jogar"], use_container_width=True):
            st.session_state.pagina = "selecionar_participante"
            st.rerun()
            
        if st.button(config["txt_btn_participantes"], use_container_width=True):
            st.session_state.pagina = "cadastrar_participantes"
            st.rerun()
            
        if st.button(config["txt_btn_perguntas"], use_container_width=True):
            st.session_state.pagina = "gerir_perguntas"
            st.rerun()
            
        if st.button(config["txt_btn_historico"], use_container_width=True):
            st.session_state.pagina = "historico"
            st.rerun()
            
        if st.button(config["txt_btn_config"], use_container_width=True):
            st.session_state.pagina = "configuracoes"
            st.rerun()
            
        if st.button(config["txt_btn_sair"], key="sair_sis", use_container_width=True):
            st.warning("Para fechar o sistema no navegador, basta fechar este separador ou janela.")

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
                    
                    letras_fixas = ["A)", "B)", "C)", "D)"]
                    sessao = []
                    for p in perguntas:
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
                    
                    st.session_state.pagina = "jogo"
                    st.rerun()
                else:
                    st.warning("Por favor, insira ou selecione um nome válido.")
                    
            if st.button("⬅️ Voltar ao Menu", use_container_width=True):
                st.session_state.pagina = "menu"
                st.rerun()

# ==============================================================================
# 3. TELA DO JOGO
# ==============================================================================
elif st.session_state.pagina == "jogo":
    p_idx = st.session_state.pergunta_idx
    total_p = len(st.session_state.perguntas_sessao)
    meta_dado = config.get("acertos_para_dado", 3)
    pts_acerto = config.get("pontos_por_acerto", 100)
    
    if p_idx >= total_p:
        st.session_state.tempo_final_congelado = obter_tempo_decorrido()
        st.session_state.pagina = "fim"
        st.rerun()

    if not st.session_state.respondido:
        tocar_audio_invisivel(SOM_TIC_TAK, loop=True)

    col_esq, col_dir = st.columns([2, 1])
    
    with col_dir:
        mostrar_santa()

    with col_esq:
        p = st.session_state.perguntas_sessao[p_idx]
        tempo_total_fmt = formatar_tempo_partida(obter_tempo_decorrido())
        
        c1, c2, c3, c4, c5 = st.columns([1.4, 1, 1.1, 1, 1.3])
        c1.markdown(f"<span class='placar-topo'>👤 {st.session_state.participante}</span>", unsafe_allow_html=True)
        placeholder_tempo = c2.empty()
        c3.markdown(f"<span class='placar-topo'>⏱️ {tempo_total_fmt}</span>", unsafe_allow_html=True)
        c4.markdown(f"<span class='placar-topo'>⭐ {st.session_state.pontuacao}</span>", unsafe_allow_html=True)
        
        icone_trofeu = "🏆" if st.session_state.dado_disponivel else ""
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
            st.write("")
            
            aviso_selecao = st.empty()
            
            if st.button("✅ Confirmar Resposta", use_container_width=True):
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
            
            st.write("")
            if st.button("🚪 Parar e Finalizar Partida", key="sair_jogo", use_container_width=True):
                st.session_state.respondido = False
                st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                st.session_state.pagina = "fim"
                st.rerun()

            if st.session_state.tempo_restante > 0:
                classe_cor = "placar-alerta" if st.session_state.tempo_restante <= config.get("tempo_alerta", 5) else "placar-topo"
                placeholder_tempo.markdown(f"<span class='{classe_cor}'>⏳ {st.session_state.tempo_restante}s</span>", unsafe_allow_html=True)
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
            placeholder_tempo.markdown("<span class='placar-topo'>⏳ Fim</span>", unsafe_allow_html=True)
            
            if st.session_state.ultima_resposta_correta:
                st.success("🎉 Resposta CORRETA! Parabéns!")
                tocar_audio_invisivel(SOM_ACERTO)
            else:
                st.error(f"❌ Resposta INCORRETA! A correta era: **{p['resposta']}**")
                tocar_audio_invisivel(SOM_ERRO)
            
            st.write("")
            
            if st.session_state.dado_disponivel:
                if not st.session_state.baloes_mostrados:
                    soltar_baloes()
                    st.session_state.baloes_mostrados = True
                
                if st.session_state.ultima_resposta_correta:
                    st.markdown(
                        f"<h3 style='text-align: center; color: {config['cor_destaque']};'>🏆 DADO PREMIADO LIBERADO ({st.session_state.acertos} ACERTOS)!<br>"
                        f"<span style='font-size: 20px; opacity: 0.85;'>Quer continuar a responder ao desafio ou girar o dado agora?</span></h3>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"<h3 style='text-align: center; color: {config['cor_destaque']};'>🏆 Fim da sequência! Mas já garantiu o seu Dado Premiado! 🏆</h3>",
                        unsafe_allow_html=True
                    )
                
                if st.session_state.pergunta_idx + 1 < total_p:
                    if st.button("➡️ Próxima Pergunta (Continuar Desafio)", use_container_width=True):
                        st.session_state.respondido = False
                        st.session_state.pergunta_idx += 1
                        st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                        st.rerun()
                else:
                    st.info("🎉 Respondeu a todas as perguntas cadastradas no sistema!")
                
                if st.button("🎲 IR PARA O DADO PREMIADO AGORA!", key="btn_ir_dado", use_container_width=True):
                    st.session_state.acertos = 0
                    st.session_state.dado_disponivel = False
                    st.session_state.baloes_mostrados = False
                    st.session_state.respondido = False
                    st.session_state.pergunta_idx += 1
                    st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                    st.session_state.dado_girado = False
                    st.session_state.pagina = "dado"
                    st.rerun()
            else:
                if st.button("➡️ Próxima Pergunta", use_container_width=True):
                    st.session_state.respondido = False
                    st.session_state.pergunta_idx += 1
                    st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                    
                    if st.session_state.pergunta_idx >= total_p:
                        st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                        st.session_state.pagina = "fim"
                    st.rerun()
            
            st.write("")
            if st.button("🚪 Parar e Finalizar Partida", key="sair_jogo_resp", use_container_width=True):
                st.session_state.respondido = False
                st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                st.session_state.pagina = "fim"
                st.rerun()

# ==============================================================================
# 4. SALA DO DADO PREMIADO
# ==============================================================================
elif st.session_state.pagina == "dado":
    st.markdown(f"<h1 style='text-align: center;'>{config['txt_sala_dado']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; opacity: 0.85;'>{st.session_state.participante} — {config['txt_sub_dado']}</h3>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
                reg = (
                    f"Participante: {st.session_state.participante} | "
                    f"Pontos: {st.session_state.pontuacao} | "
                    f"Acertos: {st.session_state.total_acertos_partida} | "
                    f"Erros: {st.session_state.total_erros_partida} | "
                    f"Tempo: {tempo_gasto_fmt} | "
                    f"Dado: Saiu {resultado_final}"
                )
                historico.append(reg)
                salvar_dados(perguntas, participantes, historico)
                st.session_state.historico_salvo_partida = True
                st.rerun()
        else:
            res = st.session_state.resultado_dado
            with placeholder_dado.container():
                renderizar_dado_3d(numero_final=res, animar=False)
            
            tocar_audio_invisivel(SOM_ACERTO)
            soltar_baloes()
                
            st.success(f"O participante {st.session_state.participante} tirou o número {res} no dado e ganhou o prémio!")
            st.write("")
            
            if st.session_state.pergunta_idx < len(st.session_state.perguntas_sessao):
                if st.button("▶️ Continuar Quiz (Próxima Pergunta)", use_container_width=True):
                    st.session_state.dado_girado = False
                    st.session_state.historico_salvo_partida = False
                    st.session_state.pagina = "jogo"
                    st.rerun()
                    
            if st.button("🏁 Encerrar Partida e Ver Resumo Final", use_container_width=True):
                st.session_state.dado_girado = False
                st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                st.session_state.pagina = "fim"
                st.rerun()

# ==============================================================================
# 5. TELA FINAL / AGRADECIMENTO
# ==============================================================================
elif st.session_state.pagina == "fim":
    if st.session_state.tempo_final_congelado is None:
        st.session_state.tempo_final_congelado = obter_tempo_decorrido()
        
    tempo_final_fmt = formatar_tempo_partida(st.session_state.tempo_final_congelado)
    
    if not st.session_state.historico_salvo_partida:
        reg_final = (
            f"Participante: {st.session_state.participante} | "
            f"Pontos: {st.session_state.pontuacao} | "
            f"Acertos: {st.session_state.total_acertos_partida} | "
            f"Erros: {st.session_state.total_erros_partida} | "
            f"Tempo Total: {tempo_final_fmt}"
        )
        historico.append(reg_final)
        salvar_dados(perguntas, participantes, historico)
        st.session_state.historico_salvo_partida = True
        
    st.markdown(f"<h1 style='text-align: center;'>{config['txt_titulo_fim']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Participante: {st.session_state.participante}</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='text-align: center; color: {config['cor_destaque']};'>"
        f"⭐ {st.session_state.pontuacao} Pontos &nbsp;|&nbsp; "
        f"✅ {st.session_state.total_acertos_partida} Acertos &nbsp;|&nbsp; "
        f"❌ {st.session_state.total_erros_partida} Erros &nbsp;|&nbsp; "
        f"⏱️ Tempo: {tempo_final_fmt}"
        f"</h3>",
        unsafe_allow_html=True
    )
    st.write("")
    
    mostrar_santa()
            
    st.markdown(f"<p style='text-align: center; font-style: italic; font-size: 22px; margin-top: 15px;'>{config['txt_msg_final']}</p>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.dado_disponivel:
            if st.button("🎲 IR PARA O DADO PREMIADO AGORA!", key="btn_ir_dado", use_container_width=True):
                st.session_state.dado_disponivel = False
                st.session_state.dado_girado = False
                st.session_state.pagina = "dado"
                st.rerun()
                
        if st.button("🏠 Voltar ao Menu Inicial", use_container_width=True):
            st.session_state.pagina = "menu"
            st.rerun()

# ==============================================================================
# 6. CADASTRAR PARTICIPANTES (COM BOTÃO VOLTAR NO TOPO E NO FIM)
# ==============================================================================
elif st.session_state.pagina == "cadastrar_participantes":
    col_top1, col_top2 = st.columns([2, 1])
    with col_top1:
        st.markdown("<h2>👥 Gestão de Participantes</h2>", unsafe_allow_html=True)
    with col_top2:
        if st.button("⬅️ Voltar ao Menu", key="voltar_part_topo", use_container_width=True):
            st.session_state.pagina = "menu"
            st.rerun()
            
    novo_p = st.text_input("Nome do novo participante:")
    if st.button("Adicionar à Lista"):
        if novo_p.strip() and novo_p.strip() not in participantes:
            participantes.append(novo_p.strip())
            salvar_dados(perguntas, participantes, historico)
            st.success(f"Participante '{novo_p.strip()}' cadastrado com sucesso!")
            st.rerun()
        else:
            st.warning("Insira um nome válido ou já existente.")
            
    st.write("### Participantes Atuais:")
    if participantes:
        for p in list(participantes):
            col_p1, col_p2 = st.columns([4, 1])
            with col_p1:
                st.write(f"- {p}")
            with col_p2:
                if st.button("🗑️ Remover", key=f"del_part_{p}"):
                    participantes.remove(p)
                    salvar_dados(perguntas, participantes, historico)
                    st.success(f"Participante '{p}' removido!")
                    st.rerun()
    else:
        st.info("Nenhum participante cadastrado.")
        
    st.write("")
    if st.button("⬅️ Voltar ao Menu", key="voltar_part_fim"):
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 7. HISTÓRICO (COM BOTÃO VOLTAR NO TOPO E NO FIM)
# ==============================================================================
elif st.session_state.pagina == "historico":
    col_top_h1, col_top_h2 = st.columns([2, 1])
    with col_top_h1:
        st.markdown("<h2>📊 Histórico de Acertos, Tempos e Prémios</h2>", unsafe_allow_html=True)
    with col_top_h2:
        if st.button("⬅️ Voltar ao Menu", key="voltar_hist_topo", use_container_width=True):
            st.session_state.pagina = "menu"
            st.rerun()
            
    if historico:
        st.write("Selecione os itens que pretende apagar:")
        itens_para_apagar = []
        for idx, item in enumerate(historico):
            if st.checkbox(item, key=f"chk_hist_{idx}"):
                itens_para_apagar.append(item)
        
        st.write("")
        col_h1, col_h2 = st.columns([1, 1])
        with col_h1:
            if itens_para_apagar and st.button("🗑️ Apagar Selecionados"):
                for it in itens_para_apagar:
                    historico.remove(it)
                salvar_dados(perguntas, participantes, historico)
                st.success("Itens selecionados apagados com sucesso!")
                st.rerun()
        with col_h2:
            if st.button("🗑️ Limpar Todo o Histórico"):
                historico.clear()
                salvar_dados(perguntas, participantes, historico)
                st.rerun()
    else:
        st.info("Ainda não existem registos no histórico.")
        
    st.write("")
    if st.button("⬅️ Voltar ao Menu", key="voltar_hist_fim"):
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 8. CADASTRAR / GERIR / EDITAR PERGUNTAS (COM BOTÃO VOLTAR FIXO NO TOPO!)
# ==============================================================================
elif st.session_state.pagina == "gerir_perguntas":
    st.markdown("<h2>📝 Gestão e Edição de Perguntas</h2>", unsafe_allow_html=True)
    
    col_topo_esq, col_topo_dir = st.columns([1, 1])
    with col_topo_esq:
        if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_topo", use_container_width=True):
            st.session_state.editando_idx = None
            st.session_state.pagina = "menu"
            st.rerun()
    with col_topo_dir:
        if st.button("➕ Nova Pergunta", key="btn_nova_perg_topo", use_container_width=True):
            st.session_state.editando_idx = -1
            st.rerun()
            
    if st.session_state.editando_idx is not None:
        idx_edit = st.session_state.editando_idx
        is_novo = (idx_edit == -1)
        
        titulo_form = "Adicionar Nova Pergunta" if is_novo else f"Editar Pergunta #{idx_edit + 1}"
        st.write(f"### {titulo_form}")
        
        p_val = perguntas[idx_edit]["pergunta"] if not is_novo else ""
        ops_val = perguntas[idx_edit]["opcoes"] if not is_novo else ["", "", "", ""]
        resp_val = perguntas[idx_edit]["resposta"] if not is_novo else ""
        
        with st.form("form_edit_pergunta"):
            nova_p = st.text_input("Enunciado da Pergunta:", value=p_val)
            op1 = st.text_input("Opção 1:", value=ops_val[0] if len(ops_val)>0 else "")
            op2 = st.text_input("Opção 2:", value=ops_val[1] if len(ops_val)>1 else "")
            op3 = st.text_input("Opção 3:", value=ops_val[2] if len(ops_val)>2 else "")
            op4 = st.text_input("Opção 4:", value=ops_val[3] if len(ops_val)>3 else "")
            correta = st.text_input("Texto exato da Resposta Correta:", value=resp_val)
            
            btn_sub = st.form_submit_button("💾 Salvar Pergunta")
            if btn_sub:
                if nova_p and op1 and op2 and op3 and op4 and correta:
                    ops = [op1, op2, op3, op4]
                    if correta in ops:
                        item_novo = {"pergunta": nova_p, "opcoes": ops, "resposta": correta}
                        if is_novo:
                            perguntas.append(item_novo)
                        else:
                            perguntas[idx_edit] = item_novo
                        salvar_dados(perguntas, participantes, historico)
                        st.session_state.editando_idx = None
                        st.success("Pergunta salva com sucesso!")
                        st.rerun()
                    else:
                        st.error("A resposta correta tem de coincidir exatamente com uma das 4 opções.")
                else:
                    st.warning("Preencha todos os campos.")
                    
        if st.button("❌ Cancelar Edição"):
            st.session_state.editando_idx = None
            st.rerun()
            
    st.write("---")
    st.write(f"### 📋 Lista de Perguntas Cadastradas ({len(perguntas)} no total):")
    
    for idx, item in enumerate(perguntas):
        col_txt, col_edit, col_del = st.columns([5, 1, 1])
        with col_txt:
            st.write(f"**{idx+1}. {item['pergunta']}** (Resp: {item['resposta']})")
        with col_edit:
            if st.button("✏️", key=f"edit_p_{idx}"):
                st.session_state.editando_idx = idx
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"del_p_{idx}"):
                perguntas.pop(idx)
                salvar_dados(perguntas, participantes, historico)
                st.rerun()
                
    st.write("")
    if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_rodape", use_container_width=True):
        st.session_state.editando_idx = None
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 9. ESTÚDIO DE PERSONALIZAÇÃO TOTAL (AUTO-LIMPEZA DE UPLOADS PARA NUNCA TRAVAR)
# ==============================================================================
elif st.session_state.pagina == "configuracoes":
    col_cfg_top1, col_cfg_top2 = st.columns([2.2, 1])
    with col_cfg_top1:
        st.markdown("<h2>⚙️ Estúdio de Personalização Total</h2>", unsafe_allow_html=True)
    with col_cfg_top2:
        if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_cfg_topo", use_container_width=True):
            st.session_state.msg_upload_ok = ""
            st.session_state.pagina = "menu"
            st.rerun()

    if st.session_state.msg_upload_ok:
        st.success(st.session_state.msg_upload_ok)
        st.session_state.msg_upload_ok = ""

    st.markdown("<p style='opacity: 0.85;'>Personalize cores, planos de fundo, botões, tamanhos, textos, imagens e sons em submenus organizados.</p>", unsafe_allow_html=True)
    
    aba_cores, aba_botoes, aba_textos, aba_img_regras, aba_sons = st.tabs([
        "🎨 1. Cores & Fundo",
        "🔘 2. Botões & Tamanhos",
        "✍️ 3. Textos & Títulos",
        "🖼️ 4. Imagem & Regras",
        "🔊 5. Sons & Restauro"
    ])
    
    # --------------------------------------------------------------------------
    # SUBMENU 1: CORES & PLANO DE FUNDO
    # --------------------------------------------------------------------------
    with aba_cores:
        st.subheader("🎨 Paleta de Cores e Plano de Fundo")
        
        opcoes_temas = list(TEMAS_PRONTOS.keys())
        idx_tema = opcoes_temas.index(config.get("tema_escolhido", "Azul Mariano (Padrão)")) if config.get("tema_escolhido") in opcoes_temas else 0
        tema_sel = st.selectbox("Escolher Tema Pré-Definido (Submenu de Estilo Rápido):", opcoes_temas, index=idx_tema)
        
        if tema_sel != "Personalizado (Livre)" and tema_sel != config.get("tema_escolhido"):
            for k_cor, v_cor in TEMAS_PRONTOS[tema_sel].items():
                config[k_cor] = v_cor
            config["tema_escolhido"] = tema_sel
            salvar_config(config)
            st.rerun()

        c_cor1, c_cor2, c_cor3, c_cor4 = st.columns(4)
        with c_cor1:
            cor_fundo_val = st.color_picker("Cor do Fundo da Tela:", value=config.get("cor_fundo", "#0B2545"))
        with c_cor2:
            cor_card_val = st.color_picker("Cor da Caixa da Pergunta:", value=config.get("cor_card", "#134074"))
        with c_cor3:
            cor_texto_val = st.color_picker("Cor Geral dos Textos:", value=config.get("cor_texto", "#FFFFFF"))
        with c_cor4:
            cor_dest_val = st.color_picker("Cor de Destaque / Placar:", value=config.get("cor_destaque", "#F4D35E"))

        st.divider()
        st.subheader("🌄 Imagem de Plano de Fundo (Wallpaper Opcional)")
        usar_bg_img = st.checkbox("Usar uma imagem como Plano de Fundo da tela inteira", value=config.get("usar_fundo_img", False))
        opacidade_bg_val = st.slider("Escurecer imagem de fundo (para destacar os textos):", 0.0, 0.95, float(config.get("opacidade_fundo", 0.7)), 0.05)
        
        # A chave dinâmica com up_cnt limpa o componente automaticamente após salvar!
        up_bg = st.file_uploader("Carregar Imagem de Plano de Fundo (PNG/JPG):", type=["png", "jpg", "jpeg"], key=f"up_bg_{st.session_state.up_cnt}")
        if up_bg is not None:
            with open("fundo_quiz_geral.png", "wb") as f:
                f.write(up_bg.getbuffer())
            config["imagem_fundo"] = "fundo_quiz_geral.png"
            config["usar_fundo_img"] = True
            salvar_config(config)
            st.session_state.up_cnt += 1
            st.session_state.msg_upload_ok = "✅ Plano de fundo atualizado e aplicado automaticamente!"
            st.rerun()

    # --------------------------------------------------------------------------
    # SUBMENU 2: BOTÕES & CONTROLE DE TAMANHOS
    # --------------------------------------------------------------------------
    with aba_botoes:
        st.subheader("🔘 Cores dos Botões")
        cb1, cb2, cb3, cb4, cb5 = st.columns(5)
        with cb1:
            cor_btn_val = st.color_picker("Fundo do Botão:", value=config.get("cor_botao", "#134074"))
        with cb2:
            cor_txt_btn_val = st.color_picker("Texto do Botão:", value=config.get("cor_texto_botao", "#FFFFFF"))
        with cb3:
            cor_borda_btn_val = st.color_picker("Borda do Botão:", value=config.get("cor_borda_botao", "#1F618D"))
        with cb4:
            cor_btn_dado_val = st.color_picker("Botão do Dado:", value=config.get("cor_botao_dado", "#F4D35E"))
        with cb5:
            cor_btn_sair_val = st.color_picker("Botão Sair:", value=config.get("cor_botao_sair", "#E74C3C"))

        st.divider()
        st.subheader("📏 Controle de Tamanho dos Botões e Fontes")
        ct1, ct2 = st.columns(2)
        with ct1:
            larg_btn_val = st.slider("Largura Máxima dos Botões (px):", 250, 900, int(config.get("largura_botao", 500)), 10)
            alt_btn_val = st.slider("Altura / Espaçamento Interno do Botão (px):", 8, 36, int(config.get("altura_botao", 16)), 2)
            raio_btn_val = st.slider("Arredondamento dos Cantos do Botão (px):", 0, 40, int(config.get("raio_borda_botao", 10)), 2)
            tam_f_btn_val = st.slider("Tamanho da Letra dos Botões (px):", 14, 36, int(config.get("tam_fonte_botao", 22)), 1)
        with ct2:
            tam_f_tit_val = st.slider("Tamanho do Título Principal (px):", 28, 72, int(config.get("tam_fonte_titulo", 46)), 2)
            tam_f_perg_val = st.slider("Tamanho da Letra da Pergunta (px):", 20, 50, int(config.get("tam_fonte_pergunta", 32)), 1)
            tam_f_opc_val = st.slider("Tamanho da Letra das Alternativas A, B, C, D (px):", 16, 42, int(config.get("tam_fonte_opcoes", 26)), 1)
            tam_f_plac_val = st.slider("Tamanho da Letra do Placar no Topo (px):", 14, 36, int(config.get("tam_fonte_placar", 22)), 1)

    # --------------------------------------------------------------------------
    # SUBMENU 3: TEXTOS FÍSICOS & TÍTULOS
    # --------------------------------------------------------------------------
    with aba_textos:
        st.subheader("✍️ Modificar Todos os Textos Físicos do Sistema")
        tx1, tx2 = st.columns(2)
        with tx1:
            txt_tit_menu_val = st.text_input("Título Principal do Menu:", value=config.get("txt_titulo_menu", ""))
            txt_sub_menu_val = st.text_input("Subtítulo do Menu:", value=config.get("txt_subtitulo_menu", ""))
            txt_tit_img_val = st.text_input("Título acima da Imagem Lateral:", value=config.get("txt_titulo_imagem", ""))
            txt_sala_dado_val = st.text_input("Título da Sala do Dado:", value=config.get("txt_sala_dado", ""))
            txt_sub_dado_val = st.text_input("Subtítulo da Sala do Dado:", value=config.get("txt_sub_dado", ""))
            txt_tit_fim_val = st.text_input("Título da Tela Final:", value=config.get("txt_titulo_fim", ""))
            txt_msg_fim_val = st.text_input("Frase de Agradecimento no Final:", value=config.get("txt_msg_final", ""))
        with tx2:
            txt_b_jogar_val = st.text_input("Texto do Botão Jogar:", value=config.get("txt_btn_jogar", ""))
            txt_b_part_val = st.text_input("Texto do Botão Participantes:", value=config.get("txt_btn_participantes", ""))
            txt_b_perg_val = st.text_input("Texto do Botão Perguntas:", value=config.get("txt_btn_perguntas", ""))
            txt_b_hist_val = st.text_input("Texto do Botão Histórico:", value=config.get("txt_btn_historico", ""))
            txt_b_cfg_val = st.text_input("Texto do Botão Configurações:", value=config.get("txt_btn_config", ""))
            txt_b_sair_val = st.text_input("Texto do Botão Sair:", value=config.get("txt_btn_sair", ""))
            col_aba1, col_aba2 = st.columns([3, 1])
            with col_aba1:
                tit_aba_val = st.text_input("Nome na Aba do Navegador:", value=config.get("titulo_aba", ""))
            with col_aba2:
                ico_aba_val = st.text_input("Ícone da Aba:", value=config.get("icone_aba", "🎲"))

    # --------------------------------------------------------------------------
    # SUBMENU 4: IMAGEM LATERAL & REGRAS DO QUIZ
    # --------------------------------------------------------------------------
    with aba_img_regras:
        col_ir1, col_ir2 = st.columns([1.5, 1])
        with col_ir1:
            st.subheader("🖼️ Imagem Principal / Lateral")
            tamanho_img_val = st.slider("Largura da Imagem Lateral (px):", 150, 650, int(config.get("tamanho_imagem", 360)), 10)
            borda_img_val = st.slider("Arredondamento da Moldura da Imagem (px):", 0, 200, int(config.get("borda_imagem", 12)), 4)
            
            # Chave dinâmica: assim que escolhe a foto, salva, atualiza o preview e limpa a caixinha sozinho!
            up_img = st.file_uploader("Trocar Imagem Lateral (PNG/JPG):", type=["png", "jpg", "jpeg"], key=f"up_img_{st.session_state.up_cnt}")
            if up_img is not None:
                with open("imagem_geral.png", "wb") as f:
                    f.write(up_img.getbuffer())
                config["imagem_ns"] = "imagem_geral.png"
                salvar_config(config)
                st.session_state.up_cnt += 1
                st.session_state.msg_upload_ok = "✅ Nova imagem lateral carregada e ativada com sucesso!"
                st.rerun()

            st.divider()
            st.subheader("🎯 Regras da Partida")
            cr1, cr2 = st.columns(2)
            with cr1:
                tempo_perg_val = st.number_input("Tempo por Pergunta (seg):", 5, 300, int(config.get("tempo_pergunta", 30)))
                tempo_alerta_val = st.number_input("Alerta Vermelho nos últimos (seg):", 1, 30, int(config.get("tempo_alerta", 5)))
            with cr2:
                acertos_dado_val = st.number_input("Acertos para liberar o Dado:", 1, 20, int(config.get("acertos_para_dado", 3)))
                pts_acerto_val = st.number_input("Pontos ganhos por Acerto:", 10, 1000, int(config.get("pontos_por_acerto", 100)), 10)

        with col_ir2:
            st.markdown("<h4 style='text-align: center;'>🖼️ Pré-visualização ao Vivo</h4>", unsafe_allow_html=True)
            mostrar_santa(largura_custom=tamanho_img_val, borda_custom=borda_img_val, titulo_custom=txt_tit_img_val)

    # --------------------------------------------------------------------------
    # SUBMENU 5: EFEITOS SONOROS, EXTRAS & RESTAURO
    # --------------------------------------------------------------------------
    with aba_sons:
        st.subheader("🔊 Efeitos Sonoros e Animações")
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
        st.subheader("♻️ Restaurar Padrão de Fábrica")
        if st.button("🔄 Restaurar Todas as Configurações para o Original", key="btn_restaurar_orig"):
            salvar_config(obter_config_padrao())
            st.session_state.up_cnt += 1
            st.session_state.msg_upload_ok = "🔄 Configurações restauradas para o padrão original!"
            st.rerun()

    st.write("---")
    col_bot1, col_bot2 = st.columns([1, 1])
    with col_bot1:
        if st.button("💾 SALVAR TODAS AS MODIFICAÇÕES", key="btn_ir_dado", use_container_width=True):
            if (cor_fundo_val != config["cor_fundo"] or cor_card_val != config["cor_card"] or
                cor_btn_val != config["cor_botao"] or cor_dest_val != config["cor_destaque"]):
                config["tema_escolhido"] = "Personalizado (Livre)"
            else:
                config["tema_escolhido"] = tema_sel

            config.update({
                "cor_fundo": cor_fundo_val,
                "cor_card": cor_card_val,
                "cor_texto": cor_texto_val,
                "cor_destaque": cor_dest_val,
                "usar_fundo_img": usar_bg_img,
                "opacidade_fundo": float(opacidade_bg_val),
                "cor_botao": cor_btn_val,
                "cor_texto_botao": cor_txt_btn_val,
                "cor_borda_botao": cor_borda_btn_val,
                "cor_botao_dado": cor_btn_dado_val,
                "cor_botao_sair": cor_btn_sair_val,
                "largura_botao": int(larg_btn_val),
                "altura_botao": int(alt_btn_val),
                "raio_borda_botao": int(raio_btn_val),
                "tam_fonte_botao": int(tam_f_btn_val),
                "tam_fonte_titulo": int(tam_f_tit_val),
                "tam_fonte_pergunta": int(tam_f_perg_val),
                "tam_fonte_opcoes": int(tam_f_opc_val),
                "tam_fonte_placar": int(tam_f_plac_val),
                "txt_titulo_menu": txt_tit_menu_val,
                "txt_subtitulo_menu": txt_sub_menu_val,
                "txt_titulo_imagem": txt_tit_img_val,
                "txt_sala_dado": txt_sala_dado_val,
                "txt_sub_dado": txt_sub_dado_val,
                "txt_titulo_fim": txt_tit_fim_val,
                "txt_msg_final": txt_msg_fim_val,
                "txt_btn_jogar": txt_b_jogar_val,
                "txt_btn_participantes": txt_b_part_val,
                "txt_btn_perguntas": txt_b_perg_val,
                "txt_btn_historico": txt_b_hist_val,
                "txt_btn_config": txt_b_cfg_val,
                "txt_btn_sair": txt_b_sair_val,
                "titulo_aba": tit_aba_val,
                "icone_aba": ico_aba_val,
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
            st.session_state.msg_upload_ok = "✅ Todas as modificações foram aplicadas e salvas com sucesso!"
            st.rerun()
            
    with col_bot2:
        if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_cfg_rodape", use_container_width=True):
            st.session_state.msg_upload_ok = ""
            st.session_state.pagina = "menu"
            st.rerun()
