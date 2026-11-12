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

# Estilos Visuais Aprimorados (Layout Limpo, Centralizado e Ocultação de Players)
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
    /* FORÇAR CENTRALIZAÇÃO E TAMANHO IDEAL DE TODOS OS BOTÕES */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .stButton>button {
        background-color: #134074;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        max-width: 450px;
        padding: 16px;
        border: 2px solid #1F618D;
        font-size: 20px !important;
        display: block;
        margin: 8px auto;
    }
    .stButton>button:hover {
        background-color: #1F618D;
        color: white;
    }
    .st-key-sair>button {
        background-color: #E74C3C !important;
        border: none !important;
    }
    .st-key-sair>button:hover {
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

def carregar_config():
    config_padrao = {
        "imagem_ns": "nossa_senhora.png",
        "tempo_pergunta": 30,
        "tempo_alerta": 4
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

def salvar_config(config):
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

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
config = carregar_config()

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
# 1. MENU PRINCIPAL
# ==============================================================================
if st.session_state.pagina == "menu":
    st.markdown("<h1 style='text-align: center;'>⛪ Festejos da Imaculada Conceição ⛪</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #8DA9C4;'>Quiz da Imaculada (Pressione F11 para tela cheia)</h4>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Jogar / Iniciar Quiz"):
            st.session_state.pagina = "selecionar_participante"
            st.rerun()
            
        if st.button("👥 Cadastrar Participantes"):
            st.session_state.pagina = "cadastrar_participantes"
            st.rerun()
            
        if st.button("📝 Cadastrar / Gerir / Editar Perguntas"):
            st.session_state.pagina = "gerir_perguntas"
            st.rerun()
            
        if st.button("📊 Histórico de Acertos e Prêmios"):
            st.session_state.pagina = "historico"
            st.rerun()
            
        if st.button("⚙️ Configurações (Imagem & Tempos)"):
            st.session_state.pagina = "configuracoes"
            st.rerun()
            
        st.markdown('<div class="st-key-sair">', unsafe_allow_html=True)
        if st.button("🚪 Sair / Fechar Sistema", key="sair_sis"):
            st.warning("Para fechar o sistema no navegador, basta fechar esta aba ou janela.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. SELECIONAR PARTICIPANTE
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    st.markdown("<h2>👤 Identificação do Participante</h2>", unsafe_allow_html=True)
    
    col_esq, col_dir = st.columns([2, 1])
    with col_esq:
        nome_digitado = st.text_input("Selecione ou Insira o Participante:")
        st.write("Ou escolha da lista cadastrada:")
        
        escolha_lista = st.selectbox("Lista de Participantes:", ["-- Selecione da lista --"] + participantes, label_visibility="collapsed") if participantes else "-- Selecione da lista --"
        
        st.write("")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("▶️ Iniciar com este Participante"):
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
                        sessao.append({"pergunta": p["pergunta"], "opcoes": ops, "resposta": p["resposta"]})
                    random.shuffle(sessao)
                    st.session_state.perguntas_sessao = sessao
                    
                    st.session_state.pagina = "jogo"
                    st.rerun()
                else:
                    st.warning("Por favor, insira ou selecione um nome válido.")
                    
            if st.button("⬅️ Voltar ao Menu"):
                st.session_state.pagina = "menu"
                st.rerun()
            
    with col_dir:
        st.markdown("<div style='text-align: center;'><h3 style='margin-bottom: 10px;'>🌸 Imaculada Conceição</h3></div>", unsafe_allow_html=True)
        img_path = config.get("imagem_ns", "nossa_senhora.png")
        if os.path.exists(img_path):
            col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
            with col_img2:
                st.image(img_path, use_container_width=True)

# ==============================================================================
# 3. TELA DO JOGO (COM IMAGEM FIXA E TIC-TAK EM SEGUNDO PLANO)
# ==============================================================================
elif st.session_state.pagina == "jogo":
    p_idx = st.session_state.pergunta_idx
    total_p = len(st.session_state.perguntas_sessao)
    
    # Tocar o tic-tak em segundo plano de forma 100% invisível
    if not st.session_state.respondido and os.path.exists(SOM_TIC_TAK):
        with open(SOM_TIC_TAK, "rb") as f:
            b64_t = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<audio autoplay loop src="data:audio/mp3;base64,{b64_t}"></audio>', unsafe_allow_html=True)

    # Layout com colunas principais fixas (Esquerda: Jogo | Direita: Imagem da Santa)
    col_esq, col_dir = st.columns([2, 1])
    
    with col_esq:
        c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
        c1.markdown(f"<span class='placar-topo'>👤 {st.session_state.participante}</span>", unsafe_allow_html=True)
        placeholder_tempo = c2.empty()
        c3.markdown(f"<span class='placar-topo'>⭐ {st.session_state.pontuacao} pts</span>", unsafe_allow_html=True)
        c4.markdown(f"<span class='placar-topo'>🎯 {st.session_state.acertos}/3</span>", unsafe_allow_html=True)
        st.divider()

        if p_idx < total_p:
            p = st.session_state.perguntas_sessao[p_idx]
            
            st.markdown(f"<div class='main-card'><h3>Q{p_idx + 1}: {p['pergunta']}</h3></div>", unsafe_allow_html=True)
            
            if not st.session_state.respondido:
                escolha = st.radio("Escolha a alternativa correta:", p["opcoes"], key=f"resp_{p_idx}", label_visibility="collapsed")
                st.write("")
                
                if st.button("✅ Confirmar Resposta"):
                    st.session_state.respondido = True
                    st.session_state.ultima_resposta_correta = (escolha == p["resposta"])
                    
                    if st.session_state.ultima_resposta_correta:
                        st.session_state.pontuacao += 100
                        st.session_state.acertos += 1
                    st.rerun()
                
                # Relógio dinâmico segundo a segundo
                if st.session_state.tempo_restante > 0:
                    placeholder_tempo.markdown(f"<span class='placar-topo'>⏳ {st.session_state.tempo_restante}s</span>", unsafe_allow_html=True)
                    time.sleep(1)
                    st.session_state.tempo_restante -= 1
                    st.rerun()
                else:
                    st.session_state.respondido = True
                    st.session_state.ultima_resposta_correta = False
                    st.rerun()
            else:
                placeholder_tempo.markdown(f"<span class='placar-topo'>⏳ Fim</span>", unsafe_allow_html=True)
                
                # Exibe o feedback e toca o som correspondente sem bloquear a interface
                if st.session_state.ultima_resposta_correta:
                    st.success("🎉 Resposta CORRETA! Parabéns!")
                    tocar_audio_invisivel(SOM_ACERTO)
                else:
                    st.error(f"❌ Resposta INCORRETA! A correta era: **{p['resposta']}**")
                    tocar_audio_invisivel(SOM_ERRO)
                
                st.write("")
                if st.button("➡️ Próxima Pergunta"):
                    st.session_state.respondido = False
                    st.session_state.pergunta_idx += 1
                    st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                    
                    if st.session_state.acertos >= 3:
                        st.session_state.acertos = 0
                        st.session_state.dado_girado = False
                        st.session_state.pagina = "dado"
                    elif st.session_state.pergunta_idx >= total_p:
                        st.session_state.pagina = "fim"
                    st.rerun()
            
            st.write("")
            if st.button("🚪 Parar e Voltar ao Menu", key="sair_jogo"):
                st.session_state.respondido = False
                st.session_state.pagina = "menu"
                st.rerun()
        else:
            st.session_state.pagina = "fim"
            st.rerun()
            
    with col_dir:
        st.markdown("<div style='text-align: center;'><h3 style='margin-bottom: 10px;'>🌸 Imaculada Conceição</h3></div>", unsafe_allow_html=True)
        img_path = config.get("imagem_ns", "nossa_senhora.png")
        if os.path.exists(img_path):
            col_img1, col_img2, col_img3 = st.columns([1, 4, 1])
            with col_img2:
                st.image(img_path, use_container_width=True)

# ==============================================================================
# 4. SALA DO DADO PREMIADO
# ==============================================================================
elif st.session_state.pagina == "dado":
    st.markdown("<h1 style='text-align: center;'>🎲 SALA DO DADO PREMIADO! 🎲</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #8DA9C4;'>Parabéns, {st.session_state.participante}! Acertaste 3 perguntas seguidas!</h3>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        placeholder_dado = st.empty()
        
        if not st.session_state.dado_girado:
            placeholder_dado.markdown("<div class='dado-box'>🎲</div>", unsafe_allow_html=True)
            if st.button("🎲 GIRAR O DADO AGORA"):
                tocar_audio_invisivel(SOM_DADO)
                
                # Triplo do tempo de rotação do dado (36 passos)
                for _ in range(36):
                    num_aleatorio = random.randint(1, 6)
                    placeholder_dado.markdown(f"<div class='dado-box' style='color: #8DA9C4;'>【 {num_aleatorio} 】</div>", unsafe_allow_html=True)
                    time.sleep(0.1)
                
                resultado_final = random.randint(1, 6)
                st.session_state.resultado_dado = resultado_final
                st.session_state.dado_girado = True
                
                reg = f"Participante: {st.session_state.participante} | Ganhou o Dado (Resultado: {resultado_final})"
                historico.append(reg)
                salvar_dados(perguntas, participantes, historico)
                st.rerun()
        else:
            res = st.session_state.resultado_dado
            placeholder_dado.markdown(f"<div class='dado-box' style='color: #2ECC71;'>【 {res} 】 🎉</div>", unsafe_allow_html=True)
            
            tocar_audio_invisivel(SOM_ACERTO)
                
            st.success(f"O participante {st.session_state.participante} tirou o número {res} e ganhou o prémio!")
            
            if st.button("🏠 Voltar ao Menu Inicial"):
                st.session_state.dado_girado = False
                st.session_state.pagina = "menu"
                st.rerun()

# ==============================================================================
# 5. TELA FINAL / AGRADECIMENTO
# ==============================================================================
elif st.session_state.pagina == "fim":
    reg_final = f"Participante: {st.session_state.participante} | Pontuação Final: {st.session_state.pontuacao} Pontos"
    if reg_final not in historico:
        historico.append(reg_final)
        salvar_dados(perguntas, participantes, historico)
        
    st.markdown("<h1 style='text-align: center;'>🎉 PARABÉNS! 🎉</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Participante: {st.session_state.participante}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: #F4D35E;'>Pontuação Final: {st.session_state.pontuacao} Pontos</h2>", unsafe_allow_html=True)
    st.write("")
    
    img_path = config.get("imagem_ns", "nossa_senhora.png")
    if os.path.exists(img_path):
        col_img1, col_img2, col_img3 = st.columns([2, 1, 2])
        with col_img2:
            st.image(img_path, use_container_width=True)
            
    st.markdown("<p style='text-align: center; font-style: italic; font-size: 20px;'>Que Nossa Senhora Imaculada Conceição abençoe grandemente a tua família!</p>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Voltar ao Menu Inicial"):
            st.session_state.pagina = "menu"
            st.rerun()

# ==============================================================================
# 6. CADASTRAR PARTICIPANTES
# ==============================================================================
elif st.session_state.pagina == "cadastrar_participantes":
    st.markdown("<h2>👥 Gestão de Participantes</h2>", unsafe_allow_html=True)
    novo_p = st.text_input("Nome do novo participante:")
    if st.button("Adicionar à Lista"):
        if novo_p.strip() and novo_p.strip() not in participantes:
            participantes.append(novo_p.strip())
            salvar_dados(perguntas, participantes, historico)
            st.success(f"Participante '{novo_p.strip()}' cadastrado com sucesso!")
        else:
            st.warning("Insira um nome válido ou já existente.")
            
    st.write("### Participantes Atuais:")
    for p in participantes:
        st.write(f"- {p}")
        
    st.write("")
    if st.button("⬅️ Voltar ao Menu"):
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 7. HISTÓRICO
# ==============================================================================
elif st.session_state.pagina == "historico":
    st.markdown("<h2>📊 Histórico de Acertos e Prêmios</h2>", unsafe_allow_html=True)
    if historico:
        for item in historico:
            st.write(f"- {item}")
        if st.button("🗑️ Limpar Histórico"):
            historico.clear()
            salvar_dados(perguntas, participantes, historico)
            st.rerun()
    else:
        st.info("Ainda não existem registos no histórico.")
        
    st.write("")
    if st.button("⬅️ Voltar ao Menu"):
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 8. CADASTRAR / GERIR / EDITAR PERGUNTAS
# ==============================================================================
elif st.session_state.pagina == "gerir_perguntas":
    st.markdown("<h2>📝 Gestão e Edição de Perguntas</h2>", unsafe_allow_html=True)
    
    col_A, col_B = st.columns([2, 1])
    with col_B:
        if st.button("➕ Nova Pergunta"):
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
    st.write("### 📋 Lista de Perguntas Cadastradas:")
    
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
    if st.button("⬅️ Voltar ao Menu"):
        st.session_state.editando_idx = None
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 9. PAINEL DE CONFIGURAÇÕES (IMAGEM & TEMPOS)
# ==============================================================================
elif st.session_state.pagina == "configuracoes":
    st.markdown("<h2>⚙️ Painel de Configurações (Imagem & Tempos)</h2>", unsafe_allow_html=True)
    st.write("Gere a imagem institucional e os tempos do quiz.")
    st.write("")
    
    col_cfg1, col_cfg2 = st.columns([2, 1])
    
    with col_cfg1:
        tempo_perg_val = st.number_input("Tempo por pergunta (seg):", value=config.get("tempo_pergunta", 30))
        tempo_alerta_val = st.number_input("Tempo Alerta Vermelho (seg):", value=config.get("tempo_alerta", 4))
        
    with col_cfg2:
        st.markdown("### 🖼️ Pré-visualização da Imagem")
        img_path = config.get("imagem_ns", "nossa_senhora.png")
        if os.path.exists(img_path):
            col_pr1, col_pr2, col_pr3 = st.columns([1, 4, 1])
            with col_pr2:
                st.image(img_path, use_container_width=True)
            
        up_img = st.file_uploader("Carregar nova imagem institucional", type=["png", "jpg", "jpeg"], key="up_img_ns")
        if up_img is not None:
            with open("nossa_senhora.png", "wb") as f:
                f.write(up_img.getbuffer())
            config["imagem_ns"] = "nossa_senhora.png"
            salvar_config(config)
            st.success("Imagem atualizada com sucesso!")
            st.rerun()

    st.write("")
    col_bot1, col_bot2 = st.columns([1, 1])
    with col_bot1:
        if st.button("💾 Salvar Configurações"):
            config["tempo_pergunta"] = int(tempo_perg_val)
            config["tempo_alerta"] = int(tempo_alerta_val)
            salvar_config(config)
            st.success("Configurações salvas com sucesso!")
            
    with col_bot2:
        if st.button("⬅️ Voltar ao Menu"):
            st.session_state.pagina = "menu"
            st.rerun()
