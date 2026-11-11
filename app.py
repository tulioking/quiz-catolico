# ==============================================================================
# QUIZ CATÓLICO DOS FESTEJOS - VERSÃO WEB FINAL (STREAMLIT) ⛪🎵🎲
# ==============================================================================

import streamlit as st
import random
import json
import os
import time

ARQUIVO_DADOS = "dados_quiz_igreja.json"
ARQUIVO_CONFIG = "config_quiz.json"

st.set_page_config(page_title="Quiz Católico - Imaculada Conceição", page_icon="⛪", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #0B2545;
        color: white;
    }
    .main-card {
        background-color: #134074;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #134074;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        padding: 12px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #1F618D;
        color: white;
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

perguntas, participantes, historico = carregar_dados()

# ==============================================================================
# 1. MENU PRINCIPAL
# ==============================================================================
if st.session_state.pagina == "menu":
    st.markdown("<h1 style='text-align: center;'>⛪ Festejos da Imaculada Conceição ⛪</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #8DA9C4;'>Quiz Oficial Paroquial</h4>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Jogar / Iniciar Quiz"):
            st.session_state.pagina = "selecionar_participante"
            st.rerun()
            
        if st.button("👥 Cadastrar Participantes"):
            st.session_state.pagina = "cadastrar_participantes"
            st.rerun()
            
        if st.button("📝 Gerir / Editar Perguntas"):
            st.session_state.pagina = "gerir_perguntas"
            st.rerun()
            
        if st.button("📊 Histórico de Acertos e Prêmios"):
            st.session_state.pagina = "historico"
            st.rerun()

# ==============================================================================
# 2. SELECIONAR PARTICIPANTE
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    st.markdown("<h2>👤 Identificação do Participante</h2>", unsafe_allow_html=True)
    
    nome_digitado = st.text_input("Digite o nome do participante:")
    escolha_lista = st.selectbox("Ou escolha da lista cadastrada:", ["-- Selecione da lista --"] + participantes) if participantes else "-- Selecione da lista --"
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Iniciar Quiz"):
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
                
    with col2:
        if st.button("⬅️ Voltar ao Menu"):
            st.session_state.pagina = "menu"
            st.rerun()

# ==============================================================================
# 3. TELA DO JOGO
# ==============================================================================
elif st.session_state.pagina == "jogo":
    p_idx = st.session_state.pergunta_idx
    total_p = len(st.session_state.perguntas_sessao)
    
    col_esq, col_dir = st.columns([2, 1])
    
    with col_esq:
        col_a, col_b, col_c = st.columns(3)
        col_a.markdown(f"**Participante:** {st.session_state.participante}")
        col_b.markdown(f"**Pontos:** {st.session_state.pontuacao}")
        col_c.markdown(f"**Acertos:** {st.session_state.acertos}/3")
        st.divider()
        
        if p_idx < total_p:
            p = st.session_state.perguntas_sessao[p_idx]
            
            st.markdown(f"<div class='main-card'><h3>Q{p_idx + 1}: {p['pergunta']}</h3></div>", unsafe_allow_html=True)
            
            escolha = st.radio("Escolha a alternativa correta:", p["opcoes"], key=f"resp_{p_idx}")
            st.write("")
            
            if not st.session_state.respondido:
                if st.button("✅ Confirmar Resposta"):
                    st.session_state.respondido = True
                    st.session_state.ultima_resposta_correta = (escolha == p["resposta"])
                    
                    if st.session_state.ultima_resposta_correta:
                        st.session_state.pontuacao += 100
                        st.session_state.acertos += 1
                    st.rerun()
            else:
                if st.session_state.ultima_resposta_correta:
                    st.success("🎉 Resposta CORRETA! Parabéns!")
                else:
                    st.error(f"❌ Resposta INCORRETA! A correta era: **{p['resposta']}**")
                
                if st.button("➡️ Próxima Pergunta"):
                    st.session_state.respondido = False
                    st.session_state.pergunta_idx += 1
                    
                    if st.session_state.acertos >= 3:
                        st.session_state.acertos = 0
                        st.session_state.dado_girado = False
                        st.session_state.pagina = "dado"
                    elif st.session_state.pergunta_idx >= total_p:
                        st.session_state.pagina = "fim"
                    st.rerun()
            
            st.write("")
            if st.button("🚪 Parar e Sair para o Menu"):
                st.session_state.respondido = False
                st.session_state.pagina = "menu"
                st.rerun()
        else:
            st.session_state.pagina = "fim"
            st.rerun()
            
    with col_dir:
        st.markdown("<h3 style='text-align: center;'>🌸 Imaculada Conceição</h3>", unsafe_allow_html=True)
        if os.path.exists("nossa_senhora.png"):
            st.image("nossa_senhora.png", use_container_width=True)
        else:
            st.info("[ Imagem 'nossa_senhora.png' não encontrada na pasta ]")

# ==============================================================================
# 4. SALA DO DADO PREMIADO (AGORA RETORNA AO MENU APÓS O PRÉMIO)
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
                for _ in range(12):
                    num_aleatorio = random.randint(1, 6)
                    placeholder_dado.markdown(f"<div class='dado-box' style='color: #8DA9C4;'>【 {num_aleatorio} 】</div>", unsafe_allow_html=True)
                    time.sleep(0.08)
                
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
    
    if os.path.exists("nossa_senhora.png"):
        col_img1, col_img2, col_img3 = st.columns([2, 1, 2])
        with col_img2:
            st.image("nossa_senhora.png", use_container_width=True)
            
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
# 8. GERIR PERGUNTAS
# ==============================================================================
elif st.session_state.pagina == "gerir_perguntas":
    st.markdown("<h2>📝 Gestão de Perguntas</h2>", unsafe_allow_html=True)
    
    with st.form("form_pergunta"):
        nova_p = st.text_input("Enunciado da Pergunta:")
        op1 = st.text_input("Opção 1:")
        op2 = st.text_input("Opção 2:")
        op3 = st.text_input("Opção 3:")
        op4 = st.text_input("Opção 4:")
        correta = st.text_input("Texto exato da Resposta Correta (igual a uma das opções):")
        
        submitted = st.form_submit_button("💾 Salvar Nova Pergunta")
        if submitted:
            if nova_p and op1 and op2 and op3 and op4 and correta:
                ops = [op1, op2, op3, op4]
                if correta in ops:
                    perguntas.append({"pergunta": nova_p, "opcoes": ops, "resposta": correta})
                    salvar_dados(perguntas, participantes, historico)
                    st.success("Pergunta adicionada com sucesso!")
                else:
                    st.error("A resposta correta tem de coincidir exatamente com uma das 4 opções.")
            else:
                st.warning("Preencha todos os campos.")
                
    st.write("### Perguntas Cadastradas:")
    for idx, item in enumerate(perguntas):
        st.write(f"**{idx+1}. {item['pergunta']}** (Resp: {item['resposta']})")
        
    st.write("")
    if st.button("⬅️ Voltar ao Menu"):
        st.session_state.pagina = "menu"
        st.rerun()
