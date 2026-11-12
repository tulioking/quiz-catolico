        
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
# 9. PAINEL DE CONFIGURAÇÕES (IMAGEM, TAMANHO & TEMPOS)
# ==============================================================================
elif st.session_state.pagina == "configuracoes":
    st.markdown("<h2>⚙️ Painel de Configurações (Imagem & Tempos)</h2>", unsafe_allow_html=True)
    st.write("Gere a imagem institucional, o tamanho dela na tela e os tempos do quiz.")
    st.write("")
    
    col_cfg1, col_cfg2 = st.columns([2, 1])
    
    with col_cfg1:
        tempo_perg_val = st.number_input("Tempo por pergunta (seg):", value=config.get("tempo_pergunta", 30))
        tempo_alerta_val = st.number_input("Tempo Alerta Vermelho (seg):", value=config.get("tempo_alerta", 4))
        tamanho_img_val = st.slider("Tamanho da Imagem da Santa (Largura em Pixels):", min_value=200, max_value=600, value=config.get("tamanho_imagem", 360), step=10)
        
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
            config["tamanho_imagem"] = int(tamanho_img_val)
            salvar_config(config)
            st.success("Configurações salvas com sucesso! As alterações já estão aplicadas.")
            st.rerun()
            
    with col_bot2:
        if st.button("⬅️ Voltar ao Menu"):
            st.session_state.pagina = "menu"
            st.rerun()
