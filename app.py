# ==============================================================================
# QUIZ CATÓLICO DOS FESTEJOS - VERSÃO WEB (STREAMLIT) ⛪🎵🎲
# ==============================================================================

import streamlit as st
import random
import json
import os

ARQUIVO_DADOS = "dados_quiz_igreja.json"
ARQUIVO_CONFIG = "config_quiz.json"

st.set_page_config(page_title="Quiz Católico - Imaculada Conceição", page_icon="⛪", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #0B2545;
        color: white;
    }
    .stButton>button {
        background-color: #134074;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        padding: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1F618D;
        color: white;
    }
    h1, h2, h3 {
        color: #FFFFFF;
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

perguntas, participantes, historico = carregar_dados()

# ==============================================================================
# 1. MENU PRINCIPAL
# ==============================================================================
if st.session_state.pagina == "menu":
    st.markdown("<h1 style='text-align: center;'>⛪ Festejos da Imaculada Conceição ⛪</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #8DA9C4;'>Sistema Oficial de Quiz Paroquial (Versão Web)</h4>", unsafe_allow_html=True)
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
# 2. SELECIONAR / INSERIR PARTICIPANTE
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    st.markdown("<h2>👤 Identificação do Participante</h2>", unsafe_allow_html=True)
    
    nome_digitado = st.text_input("Digite o nome do participante:")
    
    if participantes:
        escolha_lista = st.selectbox("Ou escolha da lista cadastrada:", ["-- Selecione da lista --"] + participantes)
    else:
        escolha_lista = "-- Selecione da lista --"
        
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
# 3. TELA DO JOGO (QUIZ)
# ==============================================================================
elif st.session_state.pagina == "jogo":
    p_idx = st.session_state.pergunta_idx
    total_p = len(st.session_state.perguntas_sessao)
    
    col_a, col_b, col_c = st.columns(3)
    col_a.markdown(f"**Participante:** {st.session_state.participante}")
    col_b.markdown(f"**Pontos:** {st.session_state.pontuacao}")
    col_c.markdown(f"**Acertos:** {st.session_state.acertos}/3")
    st.divider()
    
    if p_idx < total_p:
        pergunta_atual = st.session_state.perguntas_sessao[p_idx]
        
        st.markdown(f"### Q{p_idx + 1}: {pergunta_atual['pergunta']}")
        st.write("")
        
        escolha = st.radio("Escolha a alternativa correta:", pergunta_atual["opcoes"], key=f"q_{p_idx}")
        
        st.write("")
        if st.button("✅ Confirmar Resposta"):
            if escolha == pergunta_atual["resposta"]:
                st.success("Resposta Correta! 🎉 (+100 pontos)")
                st.session_state.pontuacao += 100
                st.session_state.acertos += 1
                
                if st.session_state.acertos >= 3:
                    st.session_state.acertos = 0
                    st.session_state.pergunta_idx += 1
                    st.session_state.pagina = "dado"
                    st.rerun()
            else:
                st.error(f"Resposta Incorreta! A correta era: {pergunta_atual['resposta']}")
                
            st.session_state.pergunta_idx += 1
            if st.session_state.pergunta_idx >= total_p:
                st.session_state.pagina = "fim"
            st.rerun()
            
        if st.button("🚪 Parar e Sair para o Menu"):
            st.session_state.pagina = "menu"
            st.rerun()
    else:
        st.session_state.pagina = "fim"
        st.rerun()

# ==============================================================================
# 4. SALA DO DADO PREMIADO
# ==============================================================================
elif st.session_state.pagina == "dado":
    st.markdown("<h2 style='text-align: center;'>🎲 SALA DO DADO PREMIADO! 🎲</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center; color: #8DA9C4;'>Parabéns, {st.session_state.participante}! Acertaste 3 perguntas seguidas!</h4>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 GIRAR O DADO AGORA"):
            resultado = random.randint(1, 6)
            st.markdown(f"<h1 style='text-align: center; color: #2ECC71;'>【 {resultado} 】</h1>", unsafe_allow_html=True)
            
            reg = f"Participante: {st.session_state.participante} | Ganhou o Dado (Resultado: {resultado})"
            historico.append(reg)
            salvar_dados(perguntas, participantes, historico)
            
            if st.button("➡️ Continuar Quiz / Finalizar"):
                if st.session_state.pergunta_idx < len(st.session_state.perguntas_sessao):
                    st.session_state.pagina = "jogo"
                else:
                    st.session_state.pagina = "fim"
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
    st.markdown(f"<h3 style='text-align: center;'>Participante: {st.session_state.participante}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #F4D35E;'>Pontuação Final: {st.session_state.pontuacao} Pontos</h3>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<p style='text-align: center; font-style: italic;'>Que Nossa Senhora Imaculada Conceição abençoe grandemente a tua família!</p>", unsafe_allow_html=True)
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
