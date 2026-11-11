# ==============================================================================
# QUIZ CATÓLICO DOS FESTEJOS - VERSÃO DEFINITIVA (CAMPO LIMPO E ENTER PARA INICIAR) ⛪🎵🎲
# ==============================================================================

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import random
import json
import os

try:
    import pygame
    PYGAME_DISPONIVEL = True
except ImportError:
    PYGAME_DISPONIVEL = False

try:
    import winsound
except ImportError:
    winsound = None

ARQUIVO_DADOS = "dados_quiz_igreja.json"
ARQUIVO_CONFIG = "config_quiz.json"

class QuizSistemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Católico - Festejos Imaculada Conceição")
        
        try:
            self.root.option_add('*Button.takeFocus', 0)
        except Exception:
            pass
        
        # Tela Cheia Automática para o Projetor
        self.root.attributes("-fullscreen", True)
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        
        # Inicializar Pygame para áudio MP3/WAV
        if PYGAME_DISPONIVEL:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception:
                pass

        # Paleta de Cores (Azul Celeste e Branco)
        self.COR_BG = "#0B2545"         
        self.COR_CARD = "#134074"       
        self.COR_AZUL_CLARO = "#8DA9C4"
        self.COR_AZUL_SELECIONADO = "#1F618D" 
        self.COR_BRANCO = "#FFFFFF"
        self.COR_VERDE = "#2ECC71"      
        self.COR_VERMELHO = "#E74C3C"   
        
        self.root.config(bg=self.COR_BG)
        
        # Configurações padrão
        self.configuracoes = {
            "imagem_ns": "nossa_senhora.png",
            "musica_menu": "",
            "musica_jogo": "",
            "musica_dado": "",
            "musica_comemoracao": "",
            "som_clique_botao": "Silencioso",
            "tipo_som_acerto": "Campainha Alegre",
            "tipo_som_erro": "Bife Grave",
            "tipo_som_tempo": "Alarme Contínuo",
            "som_acerto": "",
            "som_erro": "",
            "som_tempo_esgotado": "",
            "tempo_limite": 30,
            "tempo_alarme": 4
        }
        self.carregar_configuracoes()
        
        self.musica_tocando = True
        self.musica_atual_caminho = ""
        
        # Dados padrão de perguntas
        self.perguntas = [
            {
                "pergunta": "Em que ano foi proclamado o Dogma da Imaculada Conceição pelo Papa Pio IX?",
                "opcoes": ["A) 1854", "B) 1950", "C) 1891", "D) 1250"],
                "resposta": "A) 1854"
            },
            {
                "pergunta": "Qual é a cor litúrgica principal associada às festividades de Nossa Senhora?",
                "opcoes": ["A) Vermelho", "B) Azul / Branco", "C) Verde", "D) Roxo"],
                "resposta": "B) Azul / Branco"
            },
            {
                "pergunta": "Quem foi a jovem santa a quem Nossa Senhora apareceu em Lourdes, França?",
                "opcoes": ["A) Santa Teresinha", "B) Santa Clara", "C) Santa Bernadette", "D) Santa Rita"],
                "resposta": "C) Santa Bernadette"
            }
        ]
        
        self.participantes = []
        self.historico = []
        self.carregar_dados()
        
        self.participante_atual = "Geral"
        self.pergunta_atual = 0
        self.pontuacao = 0
        self.total_acertos = 0  
        self.respondido = False
        self.escolha_selecionada = None
        self.perguntas_sessao = []
        
        self.tempo_restante = 0
        self.timer_id = None
        
        self.tocar_musica_loop(self.configuracoes.get("musica_menu", ""))
        self.mostrar_menu_principal()

    def carregar_dados(self):
        if os.path.exists(ARQUIVO_DADOS):
            try:
                with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    self.perguntas = dados.get("perguntas", self.perguntas)
                    self.participantes = dados.get("participantes", [])
                    self.historico = dados.get("historico", [])
            except Exception:
                pass

    def salvar_dados(self):
        try:
            dados = {
                "perguntas": self.perguntas,
                "participantes": self.participantes,
                "historico": self.historico
            }
            with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar os dados: {e}")

    def carregar_configuracoes(self):
        if os.path.exists(ARQUIVO_CONFIG):
            try:
                with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                    self.configuracoes.update(json.load(f))
            except Exception:
                pass

    def salvar_configuracoes(self):
        try:
            with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
                json.dump(self.configuracoes, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")

    def limpar_tela(self):
        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass
        for widget in self.root.winfo_children():
            widget.destroy()

    def alternar_play_pause_musica(self):
        self.musica_tocando = not self.musica_tocando
        if PYGAME_DISPONIVEL:
            try:
                if not self.musica_tocando:
                    pygame.mixer.music.pause()
                else:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.unpause()
                    elif self.musica_atual_caminho:
                        self.tocar_musica_loop(self.musica_atual_caminho)
            except Exception:
                pass
                
        for w in self.root.winfo_children():
            self._atualizar_botoes_musica_recursivo(w)

    def _atualizar_botoes_musica_recursivo(self, widget):
        try:
            if isinstance(widget, tk.Button) and ("🎶 Tocar Música" in widget.cget("text") or "⏸️ Pausar Música" in widget.cget("text")):
                if self.musica_tocando:
                    widget.config(text="⏸️ Pausar Música", bg="#C0392B")
                else:
                    widget.config(text="🎶 Tocar Música", bg="#27AE60")
            for filho in widget.winfo_children():
                self._atualizar_botoes_musica_recursivo(filho)
        except Exception:
            pass

    def tocar_musica_loop(self, caminho):
        self.musica_atual_caminho = caminho
        if not self.musica_tocando or not PYGAME_DISPONIVEL:
            return
        if caminho and os.path.exists(caminho):
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(caminho)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Erro ao tocar música loop: {e}")
        else:
            self.parar_musica()

    def parar_musica(self):
        if PYGAME_DISPONIVEL:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

    def tocar_som_clique(self):
        if not self.musica_tocando:
            return
        tipo_clique = self.configuracoes.get("som_clique_botao", "Silencioso")
        if tipo_clique == "Silencioso":
            return
        
        if winsound:
            try:
                if tipo_clique == "Clique Leve":
                    winsound.Beep(1000, 30)
                elif tipo_clique == "Bipe do Sistema":
                    winsound.Beep(800, 50)
            except Exception:
                pass

    def tocar_som_efeito(self, tipo):
        if not self.musica_tocando:
            return
        
        caminho = self.configuracoes.get(f"som_{tipo}", "")
        if caminho and os.path.exists(caminho) and PYGAME_DISPONIVEL:
            try:
                sound = pygame.mixer.Sound(caminho)
                sound.play()
                return
            except Exception as e:
                print(f"Erro ao reproduzir efeito {tipo}: {e}")
        
        tipo_escolhido = self.configuracoes.get(f"tipo_som_{tipo}", "")
        if winsound:
            try:
                if tipo_escolhido == "Campainha Alegre":
                    winsound.Beep(880, 100)
                    winsound.Beep(1174, 200)
                elif tipo_escolhido == "Bife Grave":
                    winsound.Beep(250, 300)
                elif tipo_escolhido == "Alarme Contínuo":
                    winsound.Beep(500, 100)
                    winsound.Beep(300, 200)
                elif tipo_escolhido == "Som Curto Simples":
                    winsound.Beep(600, 120)
            except Exception:
                pass

    def testar_som_arquivo(self, caminho, tipo_padrao=""):
        caminho_limpo = caminho.strip()
        if caminho_limpo and os.path.exists(caminho_limpo) and PYGAME_DISPONIVEL:
            try:
                sound = pygame.mixer.Sound(caminho_limpo)
                sound.play()
                return
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao reproduzir áudio: {e}")
        
        if winsound:
            try:
                if tipo_padrao == "Campainha Alegre":
                    winsound.Beep(880, 100)
                    winsound.Beep(1174, 200)
                elif tipo_padrao == "Bife Grave":
                    winsound.Beep(250, 300)
                elif tipo_padrao == "Alarme Contínuo":
                    winsound.Beep(500, 100)
                    winsound.Beep(300, 200)
                elif tipo_padrao == "Som Curto Simples":
                    winsound.Beep(600, 120)
                elif tipo_padrao == "Clique Leve":
                    winsound.Beep(1000, 30)
                elif tipo_padrao == "Bipe do Sistema":
                    winsound.Beep(800, 50)
                else:
                    messagebox.showwarning("Aviso", "Selecione um arquivo de áudio válido ou escolha uma opção na lista.")
            except Exception:
                pass

    def carregar_imagem_segura(self, caminho, largura, altura):
        if not caminho or not os.path.exists(caminho):
            return None
        try:
            from PIL import Image, ImageTk
            img = Image.open(caminho)
            img = img.resize((largura, altura), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except ImportError:
            try:
                img = tk.PhotoImage(file=caminho)
                return img
            except Exception:
                return None

    def criar_botao_customizado(self, parent, **kwargs):
        comando_original = kwargs.pop("command", None)
        
        kwargs.pop("takefocus", None)
        kwargs.pop("highlightthickness", None)
        
        btn = tk.Button(parent, **kwargs)
        
        def acao_ao_soltar(event):
            if str(btn.cget("state")) != "disabled":
                self.tocar_som_clique()
                if comando_original:
                    comando_original()
                    
        btn.bind("<ButtonRelease-1>", acao_ao_soltar)
        return btn

    def criar_barra_topo(self, parent):
        top_bar = tk.Frame(parent, bg=self.COR_BG)
        top_bar.pack(fill=tk.X, pady=(0, 10))
        
        texto_musica = "⏸️ Pausar Música" if self.musica_tocando else "🎶 Tocar Música"
        cor_musica = "#C0392B" if self.musica_tocando else "#27AE60"
        btn_som = self.criar_botao_customizado(top_bar, text=texto_musica, font=("Segoe UI", 11, "bold"), bg=cor_musica, fg=self.COR_BRANCO, relief=tk.FLAT, command=self.alternar_play_pause_musica, cursor="hand2")
        btn_som.pack(side=tk.RIGHT, ipadx=10, ipady=3)
        return top_bar

    # =========================================================================
    # 1. MENU PRINCIPAL
    # =========================================================================
    def mostrar_menu_principal(self):
        self.parar_musica()
        self.tocar_musica_loop(self.configuracoes.get("musica_menu", ""))
        self.limpar_tela()
        
        frame = tk.Frame(self.root, bg=self.COR_BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=40)
        
        self.criar_barra_topo(frame)

        tk.Label(frame, text="⛪ Festejos da Imaculada Conceição ⛪", font=("Segoe UI", 28, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(pady=5)
        tk.Label(frame, text="Quiz da Imaculada (Pressione F11 para tela cheia)", font=("Segoe UI", 12), bg=self.COR_BG, fg=self.COR_AZUL_CLARO).pack(pady=(0, 20))
        
        btn_estilo = {"font": ("Segoe UI", 13, "bold"), "bg": self.COR_CARD, "fg": self.COR_BRANCO, "activebackground": self.COR_AZUL_SELECIONADO, "activeforeground": self.COR_BRANCO, "relief": tk.FLAT, "width": 35, "cursor": "hand2"}
        
        self.criar_botao_customizado(frame, text="▶️ Jogar / Iniciar Quiz", command=self.selecionar_participante_popup, **btn_estilo).pack(pady=6, ipady=6)
        self.criar_botao_customizado(frame, text="👥 Cadastrar Participantes", command=self.tela_cadastro_participantes, **btn_estilo).pack(pady=6, ipady=6)
        self.criar_botao_customizado(frame, text="📝 Cadastrar / Gerir / Editar Perguntas", command=self.tela_gerir_perguntas, **btn_estilo).pack(pady=6, ipady=6)
        self.criar_botao_customizado(frame, text="📊 Histórico de Acertos e Prêmios", command=self.tela_historico, **btn_estilo).pack(pady=6, ipady=6)
        self.criar_botao_customizado(frame, text="⚙️ Configurações (Músicas, Imagem e Sons)", command=self.tela_configuracoes, **btn_estilo).pack(pady=6, ipady=6)
        
        self.criar_botao_customizado(frame, text="⏻ Sair / Fechar Sistema", command=self.root.destroy, font=("Segoe UI", 13, "bold"), bg=self.COR_VERMELHO, fg=self.COR_BRANCO, activebackground="#C0392B", relief=tk.FLAT, width=35, cursor="hand2").pack(pady=15, ipady=6)

    # =========================================================================
    # 1.1 TELA DE CONFIGURAÇÕES
    # =========================================================================
    def tela_configuracoes(self):
        self.limpar_tela()
        
        frame = tk.Frame(self.root, bg=self.COR_BG, padx=40, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.criar_barra_topo(frame)

        tk.Label(frame, text="⚙️ Painel de Configurações (Músicas, Imagem & Sons)", font=("Segoe UI", 20, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(anchor=tk.W, pady=5)
        
        conteudo_f = tk.Frame(frame, bg=self.COR_BG)
        conteudo_f.pack(fill=tk.BOTH, expand=True, pady=10)
        
        col_esq = tk.Frame(conteudo_f, bg=self.COR_BG)
        col_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        col_dir = tk.Frame(conteudo_f, bg=self.COR_CARD, width=280, padx=15, pady=15)
        col_dir.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        col_dir.pack_propagate(False)
        
        tk.Label(col_dir, text="🖼️ Pré-visualização da Imagem", font=("Segoe UI", 12, "bold"), bg=self.COR_CARD, fg="#F4D35E").pack(pady=(5, 10))
        
        lbl_previa_img = tk.Label(col_dir, bg=self.COR_BG)
        lbl_previa_img.pack(fill=tk.BOTH, expand=True, pady=5)

        def atualizar_previa(caminho):
            img_prev = self.carregar_imagem_segura(caminho, 220, 260)
            if img_prev:
                lbl_previa_img.config(image=img_prev, text="")
                lbl_previa_img.image = img_prev
            else:
                lbl_previa_img.config(image="", text="[ Imagem Inválida\nou Não Encontrada ]", fg=self.COR_AZUL_CLARO, font=("Segoe UI", 10))

        atualizar_previa(self.configuracoes.get("imagem_ns", ""))

        def criar_seletor_com_botoes(label_txt, config_key, filetypes, tipo_teste="musica"):
            f = tk.Frame(col_esq, bg=self.COR_BG)
            f.pack(fill=tk.X, pady=3)
            tk.Label(f, text=label_txt, font=("Segoe UI", 10, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, width=24, anchor="w").pack(side=tk.LEFT)
            
            ent = tk.Entry(f, font=("Segoe UI", 10), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
            ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=2)
            ent.insert(0, self.configuracoes.get(config_key, ""))
            
            def procurar():
                caminho = filedialog.askopenfilename(filetypes=filetypes)
                if caminho:
                    ent.delete(0, tk.END)
                    ent.insert(0, caminho)
                    if config_key == "imagem_ns":
                        atualizar_previa(caminho)
                    
            def remover():
                ent.delete(0, tk.END)
                if config_key == "imagem_ns":
                    atualizar_previa("")

            self.criar_botao_customizado(f, text="📂 Procurar", font=("Segoe UI", 9), bg=self.COR_CARD, fg=self.COR_BRANCO, command=procurar, relief=tk.FLAT).pack(side=tk.RIGHT, ipadx=4)
            self.criar_botao_customizado(f, text="🗑️ Remover", font=("Segoe UI", 9), bg=self.COR_VERMELHO, fg=self.COR_BRANCO, command=remover, relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=4)
            
            if tipo_teste == "som":
                self.criar_botao_customizado(f, text="▶ Testar", font=("Segoe UI", 9, "bold"), bg="#27AE60", fg=self.COR_BRANCO, command=lambda: self.testar_som_arquivo(ent.get()), relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=4)
                
            return ent

        ent_img = criar_seletor_com_botoes("Imagem N. Senhora:", "imagem_ns", [("Imagens", "*.jpeg *.jpg *.png")], "imagem")
        ent_m_menu = criar_seletor_com_botoes("Música Menu:", "musica_menu", [("Áudio", "*.mp3 *.wav")], "som")
        ent_m_jogo = criar_seletor_com_botoes("Fundo Jogo:", "musica_jogo", [("Áudio", "*.mp3 *.wav")], "som")
        ent_m_dado = criar_seletor_com_botoes("Durante Dado:", "musica_dado", [("Áudio", "*.mp3 *.wav")], "som")
        ent_m_comem = criar_seletor_com_botoes("Comemoração Dado:", "musica_comemoracao", [("Áudio", "*.mp3 *.wav")], "som")
        
        ent_s_acerto = criar_seletor_com_botoes("Som Acerto (Ficheiro):", "som_acerto", [("Áudio", "*.mp3 *.wav")], "som")
        
        opcoes_sons = ["Campainha Alegre", "Bife Grave", "Alarme Contínuo", "Som Curto Simples", "Silencioso"]
        
        f_acerto_tipo = tk.Frame(col_esq, bg=self.COR_BG)
        f_acerto_tipo.pack(fill=tk.X, pady=3)
        tk.Label(f_acerto_tipo, text="↳ Tipo Som Acerto:", font=("Segoe UI", 9, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, width=24, anchor="w").pack(side=tk.LEFT)
        combo_acerto = ttk.Combobox(f_acerto_tipo, values=opcoes_sons, font=("Segoe UI", 10), state="readonly")
        combo_acerto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        combo_acerto.set(self.configuracoes.get("tipo_som_acerto", "Campainha Alegre"))
        self.criar_botao_customizado(f_acerto_tipo, text="▶ Testar Tipo", font=("Segoe UI", 9, "bold"), bg="#27AE60", fg=self.COR_BRANCO, command=lambda: self.testar_som_arquivo("", combo_acerto.get()), relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=4)

        ent_s_erro = criar_seletor_com_botoes("Som Erro (Ficheiro):", "som_erro", [("Áudio", "*.mp3 *.wav")], "som")
        
        f_erro_tipo = tk.Frame(col_esq, bg=self.COR_BG)
        f_erro_tipo.pack(fill=tk.X, pady=3)
        tk.Label(f_erro_tipo, text="↳ Tipo Som Erro:", font=("Segoe UI", 9, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, width=24, anchor="w").pack(side=tk.LEFT)
        combo_erro = ttk.Combobox(f_erro_tipo, values=opcoes_sons, font=("Segoe UI", 10), state="readonly")
        combo_erro.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        combo_erro.set(self.configuracoes.get("tipo_som_erro", "Bife Grave"))
        self.criar_botao_customizado(f_erro_tipo, text="▶ Testar Tipo", font=("Segoe UI", 9, "bold"), bg="#27AE60", fg=self.COR_BRANCO, command=lambda: self.testar_som_arquivo("", combo_erro.get()), relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=4)

        ent_s_tempo = criar_seletor_com_botoes("Tempo Esgotado (Ficheiro):", "som_tempo_esgotado", [("Áudio", "*.mp3 *.wav")], "som")
        
        f_tempo_tipo = tk.Frame(col_esq, bg=self.COR_BG)
        f_tempo_tipo.pack(fill=tk.X, pady=3)
        tk.Label(f_tempo_tipo, text="↳ Tipo Tempo Esgotado:", font=("Segoe UI", 9, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, width=24, anchor="w").pack(side=tk.LEFT)
        combo_tempo = ttk.Combobox(f_tempo_tipo, values=opcoes_sons, font=("Segoe UI", 10), state="readonly")
        combo_tempo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        combo_tempo.set(self.configuracoes.get("tipo_som_tempo", "Alarme Contínuo"))
        self.criar_botao_customizado(f_tempo_tipo, text="▶ Testar Tipo", font=("Segoe UI", 9, "bold"), bg="#27AE60", fg=self.COR_BRANCO, command=lambda: self.testar_som_arquivo("", combo_tempo.get()), relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=4)

        f_clique = tk.Frame(col_esq, bg=self.COR_BG)
        f_clique.pack(fill=tk.X, pady=3)
        tk.Label(f_clique, text="Som ao Clicar nos Botões:", font=("Segoe UI", 10, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, width=24, anchor="w").pack(side=tk.LEFT)
        opcoes_clique = ["Silencioso", "Clique Leve", "Bipe do Sistema"]
        combo_clique = ttk.Combobox(f_clique, values=opcoes_clique, font=("Segoe UI", 10), state="readonly")
        combo_clique.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        combo_clique.set(self.configuracoes.get("som_clique_botao", "Silencioso"))
        self.criar_botao_customizado(f_clique, text="▶ Testar", font=("Segoe UI", 9, "bold"), bg="#27AE60", fg=self.COR_BRANCO, command=lambda: self.testar_som_arquivo("", combo_clique.get()), relief=tk.FLAT).pack(side=tk.RIGHT, padx=2, ipadx=4)

        f_t = tk.Frame(col_esq, bg=self.COR_BG)
        f_t.pack(fill=tk.X, pady=4)
        tk.Label(f_t, text="Tempo por pergunta (seg):", font=("Segoe UI", 10, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, width=24, anchor="w").pack(side=tk.LEFT)
        ent_tempo = tk.Entry(f_t, font=("Segoe UI", 10), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
        ent_tempo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=2)
        ent_tempo.insert(0, str(self.configuracoes.get("tempo_limite", 30)))

        f_al = tk.Frame(col_esq, bg=self.COR_BG)
        f_al.pack(fill=tk.X, pady=4)
        tk.Label(f_al, text="Tempo Alerta Vermelho (seg):", font=("Segoe UI", 10, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, width=24, anchor="w").pack(side=tk.LEFT)
        ent_alarme = tk.Entry(f_al, font=("Segoe UI", 10), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
        ent_alarme.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=2)
        ent_alarme.insert(0, str(self.configuracoes.get("tempo_alarme", 4)))

        def salvar_configs():
            try:
                self.configuracoes["imagem_ns"] = ent_img.get().strip()
                self.configuracoes["musica_menu"] = ent_m_menu.get().strip()
                self.configuracoes["musica_jogo"] = ent_m_jogo.get().strip()
                self.configuracoes["musica_dado"] = ent_m_dado.get().strip()
                self.configuracoes["musica_comemoracao"] = ent_m_comem.get().strip()
                self.configuracoes["som_acerto"] = ent_s_acerto.get().strip()
                self.configuracoes["som_erro"] = ent_s_erro.get().strip()
                self.configuracoes["som_tempo_esgotado"] = ent_s_tempo.get().strip()
                self.configuracoes["tipo_som_acerto"] = combo_acerto.get()
                self.configuracoes["tipo_som_erro"] = combo_erro.get()
                self.configuracoes["tipo_som_tempo"] = combo_tempo.get()
                self.configuracoes["som_clique_botao"] = combo_clique.get()
                self.configuracoes["tempo_limite"] = int(ent_tempo.get().strip())
                self.configuracoes["tempo_alarme"] = int(ent_alarme.get().strip())
                self.salvar_configuracoes()
                messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
                self.mostrar_menu_principal()
            except ValueError:
                messagebox.showerror("Erro", "Os campos de tempo devem ser números inteiros válidos.")

        btn_f = tk.Frame(frame, bg=self.COR_BG)
        btn_f.pack(fill=tk.X, pady=10)
        
        self.criar_botao_customizado(btn_f, text="💾 Salvar Configurações", font=("Segoe UI", 12, "bold"), bg=self.COR_AZUL_SELECIONADO, fg=self.COR_BRANCO, relief=tk.FLAT, command=salvar_configs).pack(side=tk.LEFT, ipady=5, ipadx=10)
        self.criar_botao_customizado(btn_f, text="⬅️ Voltar ao Menu", font=("Segoe UI", 12), bg="#333333", fg=self.COR_BRANCO, relief=tk.FLAT, command=self.mostrar_menu_principal).pack(side=tk.RIGHT, ipady=5, ipadx=10)

    # =========================================================================
    # 2. SELECIONAR PARTICIPANTE (COM CAMPO DE NOME LIMPO E SUPORTE A ENTER)
    # =========================================================================
    def selecionar_participante_popup(self):
        if not self.perguntas:
            messagebox.showwarning("Aviso", "Não há perguntas cadastradas!")
            return
            
        top = tk.Toplevel(self.root)
        top.title("Escolher Participante")
        top.geometry("450x480")
        top.config(bg=self.COR_BG)
        top.grab_set()
        
        tk.Label(top, text="Selecione ou Insira o Participante:", font=("Segoe UI", 14, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(pady=15)
        
        ent_novo = tk.Entry(top, font=("Segoe UI", 12), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
        ent_novo.pack(fill=tk.X, padx=20, pady=5, ipady=5)
        ent_novo.focus_set() # Já foca diretamente no campo limpo para digitar
        
        tk.Label(top, text="Ou escolha da lista cadastrada:", font=("Segoe UI", 11), bg=self.COR_BG, fg=self.COR_AZUL_CLARO).pack(anchor=tk.W, padx=20, pady=(10, 2))
        
        lb_frame = tk.Frame(top, bg=self.COR_CARD)
        lb_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        lb = tk.Listbox(lb_frame, font=("Segoe UI", 11), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT)
        lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for p in self.participantes:
            lb.insert(tk.END, p)
            
        def confirmar(event=None):
            nome = ""
            selection = lb.curselection()
            if selection:
                nome = lb.get(selection[0])
            else:
                val = ent_novo.get().strip()
                if val:
                    nome = val
                    if nome not in self.participantes:
                        self.participantes.append(nome)
                        self.salvar_dados()
            
            if nome:
                self.participante_atual = nome
                top.destroy()
                self.pergunta_atual = 0
                self.pontuacao = 0
                self.total_acertos = 0
                
                self.perguntas_sessao = []
                for p in self.perguntas:
                    ops = list(p["opcoes"])
                    random.shuffle(ops)
                    self.perguntas_sessao.append({
                        "pergunta": p["pergunta"],
                        "opcoes": ops,
                        "resposta": p["resposta"]
                    })
                random.shuffle(self.perguntas_sessao)
                
                self.tocar_musica_loop(self.configuracoes.get("musica_jogo", ""))
                self.iniciar_tela_jogo()
            else:
                messagebox.showwarning("Aviso", "Selecione ou digite um nome válido.")

        # Permite pressionar Enter para confirmar direto
        ent_novo.bind("<Return>", confirmar)

        self.criar_botao_customizado(top, text="▶️ Iniciar com este Participante", font=("Segoe UI", 12, "bold"), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT, command=confirmar).pack(fill=tk.X, padx=20, pady=15, ipady=8)

    # =========================================================================
    # 3. CADASTRAR PARTICIPANTES
    # =========================================================================
    def tela_cadastro_participantes(self):
        self.limpar_tela()
        frame = tk.Frame(self.root, bg=self.COR_BG, padx=50, pady=40)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.criar_barra_topo(frame)

        tk.Label(frame, text="👥 Cadastro de Participantes", font=("Segoe UI", 22, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(anchor=tk.W, pady=10)
        
        entry_nome = tk.Entry(frame, font=("Segoe UI", 14), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
        entry_nome.pack(fill=tk.X, pady=10, ipady=8)
        
        def adicionar(event=None):
            nome = entry_nome.get().strip()
            if nome:
                if nome not in self.participantes:
                    self.participantes.append(nome)
                    self.salvar_dados()
                    messagebox.showinfo("Sucesso", f"Participante '{nome}' cadastrado!")
                    entry_nome.delete(0, tk.END)
                    atualizar_lista()
                else:
                    messagebox.showwarning("Aviso", "Participante já cadastrado.")
            else:
                messagebox.showwarning("Aviso", "Digite um nome válido.")

        entry_nome.bind("<Return>", adicionar)

        self.criar_botao_customizado(frame, text="Adicionar Participante", font=("Segoe UI", 12, "bold"), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT, command=adicionar).pack(anchor=tk.W, pady=5, ipady=6)
        
        tk.Label(frame, text="Participantes Cadastrados:", font=("Segoe UI", 13, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO).pack(anchor=tk.W, pady=(20, 5))
        
        listbox_frame = tk.Frame(frame, bg=self.COR_CARD)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        listbox = tk.Listbox(listbox_frame, font=("Segoe UI", 12), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT, height=10)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def atualizar_lista():
            listbox.delete(0, tk.END)
            for p in self.participantes:
                listbox.insert(tk.END, p)
        atualizar_lista()
        
        self.criar_botao_customizado(frame, text="⬅️ Voltar ao Menu", font=("Segoe UI", 12), bg="#333333", fg=self.COR_BRANCO, relief=tk.FLAT, command=lambda: [self.tocar_musica_loop(self.configuracoes.get("musica_menu", "")), self.mostrar_menu_principal()]).pack(anchor=tk.W, pady=20, ipady=6)

    # =========================================================================
    # 4. GERIR PERGUNTAS
    # =========================================================================
    def tela_gerir_perguntas(self):
        self.limpar_tela()
        frame = tk.Frame(self.root, bg=self.COR_BG, padx=40, pady=30)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.criar_barra_topo(frame)

        tk.Label(frame, text="📝 Gestão e Edição de Perguntas", font=("Segoe UI", 22, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(anchor=tk.W, pady=5)
        
        list_f = tk.Frame(frame, bg=self.COR_CARD)
        list_f.pack(fill=tk.BOTH, expand=True, pady=10)
        
        listbox_p = tk.Listbox(list_f, font=("Segoe UI", 11), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT, height=12)
        listbox_p.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def atualizar_lista_p():
            listbox_p.delete(0, tk.END)
            for idx, item in enumerate(self.perguntas):
                listbox_p.insert(tk.END, f"{idx+1}. {item['pergunta']}")
        atualizar_lista_p()
        
        def abrir_janela_cadastro(pergunta_obj=None, index=None):
            top = tk.Toplevel(self.root)
            top.title("Cadastrar / Editar Pergunta")
            top.geometry("600x520")
            top.config(bg=self.COR_BG)
            top.grab_set()
            
            tk.Label(top, text="Enunciado da Pergunta:", font=("Segoe UI", 12, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(anchor=tk.W, padx=20, pady=10)
            ent_p = tk.Entry(top, font=("Segoe UI", 12), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
            ent_p.pack(fill=tk.X, padx=20, ipady=5)
            
            tk.Label(top, text="Digite as 4 opções e escreva EXATAMENTE qual é a resposta correta:", font=("Segoe UI", 11, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO).pack(anchor=tk.W, padx=20, pady=(15, 5))
            
            ent_ops = []
            for i in range(4):
                f_sub = tk.Frame(top, bg=self.COR_BG)
                f_sub.pack(fill=tk.X, padx=20, pady=3)
                tk.Label(f_sub, text=f"Opção {i+1}:", font=("Segoe UI", 10), bg=self.COR_BG, fg=self.COR_BRANCO, width=8).pack(side=tk.LEFT)
                e = tk.Entry(f_sub, font=("Segoe UI", 11), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
                e.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=3)
                ent_ops.append(e)
                
            tk.Label(top, text="Texto exato da Resposta Correta:", font=("Segoe UI", 11, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO).pack(anchor=tk.W, padx=20, pady=(10, 2))
            ent_correta = tk.Entry(top, font=("Segoe UI", 11), bg=self.COR_CARD, fg=self.COR_BRANCO, insertbackground="white")
            ent_correta.pack(fill=tk.X, padx=20, ipady=5)
                
            if pergunta_obj:
                ent_p.insert(0, pergunta_obj["pergunta"])
                ent_correta.insert(0, pergunta_obj["resposta"])
                for i, op_val in enumerate(pergunta_obj["opcoes"]):
                    if i < len(ent_ops):
                        ent_ops[i].insert(0, op_val)
                    
            def salvar():
                texto = ent_p.get().strip()
                ops = [e.get().strip() for e in ent_ops]
                correta_txt = ent_correta.get().strip()
                
                if not texto or any(not o for o in ops) or not correta_txt:
                    messagebox.showwarning("Aviso", "Preencha todos os campos e a resposta correta.")
                    return
                
                if correta_txt not in ops:
                    messagebox.showwarning("Aviso", "O texto da resposta correta deve ser exatamente igual a uma das 4 opções inseridas!")
                    return
                
                nova = {
                    "pergunta": texto,
                    "opcoes": ops,
                    "resposta": correta_txt
                }
                
                if index is not None:
                    self.perguntas[index] = nova
                else:
                    self.perguntas.append(nova)
                    
                self.salvar_dados()
                messagebox.showinfo("Sucesso", "Pergunta salva com sucesso!")
                top.destroy()
                atualizar_lista_p()

            self.criar_botao_customizado(top, text="Salvar Pergunta", font=("Segoe UI", 12, "bold"), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT, command=salvar).pack(pady=20, ipady=6, ipadx=15)

        def editar_selecionada():
            selected = listbox_p.curselection()
            if selected:
                idx = selected[0]
                abrir_janela_cadastro(self.perguntas[idx], idx)
            else:
                messagebox.showwarning("Aviso", "Selecione uma pergunta para editar.")

        def apagar_selecionada():
            selected = listbox_p.curselection()
            if selected:
                idx = selected[0]
                self.perguntas.pop(idx)
                self.salvar_dados()
                atualizar_lista_p()
                messagebox.showinfo("Apagado", "Pergunta removida com sucesso.")
            else:
                messagebox.showwarning("Aviso", "Selecione uma pergunta para apagar.")

        btn_f = tk.Frame(frame, bg=self.COR_BG)
        btn_f.pack(fill=tk.X, pady=10)
        
        self.criar_botao_customizado(btn_f, text="➕ Nova Pergunta", font=("Segoe UI", 11, "bold"), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT, command=lambda: abrir_janela_cadastro()).pack(side=tk.LEFT, ipady=6, ipadx=10)
        self.criar_botao_customizado(btn_f, text="✏️ Editar Selecionada", font=("Segoe UI", 11, "bold"), bg="#2980B9", fg=self.COR_BRANCO, relief=tk.FLAT, command=editar_selecionada).pack(side=tk.LEFT, padx=10, ipady=6, ipadx=10)
        self.criar_botao_customizado(btn_f, text="🗑️ Apagar Selecionada", font=("Segoe UI", 11, "bold"), bg=self.COR_VERMELHO, fg=self.COR_BRANCO, relief=tk.FLAT, command=apagar_selecionada).pack(side=tk.LEFT, ipady=6, ipadx=10)
        self.criar_botao_customizado(btn_f, text="⬅️ Voltar ao Menu", font=("Segoe UI", 11), bg="#333333", fg=self.COR_BRANCO, relief=tk.FLAT, command=lambda: [self.tocar_musica_loop(self.configuracoes.get("musica_menu", "")), self.mostrar_menu_principal()]).pack(side=tk.RIGHT, ipady=6, ipadx=10)

    # =========================================================================
    # 5. HISTÓRICO
    # =========================================================================
    def tela_historico(self):
        self.limpar_tela()
        frame = tk.Frame(self.root, bg=self.COR_BG, padx=50, pady=40)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.criar_barra_topo(frame)

        tk.Label(frame, text="📊 Histórico de Acertos e Prêmios", font=("Segoe UI", 22, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(anchor=tk.W, pady=10)
        
        listbox_frame = tk.Frame(frame, bg=self.COR_CARD)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        listbox = tk.Listbox(listbox_frame, font=("Segoe UI", 12), bg=self.COR_CARD, fg=self.COR_BRANCO, relief=tk.FLAT, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for h in self.historico:
            listbox.insert(tk.END, h)
        if not self.historico:
            listbox.insert(tk.END, "Nenhum registo no histórico ainda.")
            
        def apagar_historico():
            sel = listbox.curselection()
            if sel:
                idx = sel[0]
                if idx < len(self.historico):
                    self.historico.pop(idx)
                    self.salvar_dados()
                    listbox.delete(idx)
                    messagebox.showinfo("Sucesso", "Registo removido do histórico.")
            else:
                messagebox.showwarning("Aviso", "Selecione um item do histórico para apagar.")

        btn_f = tk.Frame(frame, bg=self.COR_BG)
        btn_f.pack(fill=tk.X, pady=15)
        
        self.criar_botao_customizado(btn_f, text="🗑️ Apagar Selecionado", font=("Segoe UI", 11, "bold"), bg=self.COR_VERMELHO, fg=self.COR_BRANCO, relief=tk.FLAT, command=apagar_historico).pack(side=tk.LEFT, ipady=6, ipadx=10)
        self.criar_botao_customizado(btn_f, text="⬅️ Voltar ao Menu", font=("Segoe UI", 11), bg="#333333", fg=self.COR_BRANCO, relief=tk.FLAT, command=lambda: [self.tocar_musica_loop(self.configuracoes.get("musica_menu", "")), self.mostrar_menu_principal()]).pack(side=tk.RIGHT, ipady=6, ipadx=10)

    # =========================================================================
    # 6. FLUXO DO JOGO
    # =========================================================================
    def iniciar_tela_jogo(self):
        self.limpar_tela()
        
        main_frame = tk.Frame(self.root, bg=self.COR_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        col_esq = tk.Frame(main_frame, bg=self.COR_BG)
        col_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 30))
        
        info_frame = tk.Frame(col_esq, bg=self.COR_BG)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(info_frame, text=f"Participante: {self.participante_atual}", font=("Segoe UI", 16, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(side=tk.LEFT)
        
        texto_musica = "⏸️ Pausar Música" if self.musica_tocando else "🎶 Tocar Música"
        cor_musica = "#C0392B" if self.musica_tocando else "#27AE60"
        self.btn_som = self.criar_botao_customizado(info_frame, text=texto_musica, font=("Segoe UI", 11, "bold"), bg=cor_musica, fg=self.COR_BRANCO, relief=tk.FLAT, command=self.alternar_play_pause_musica, cursor="hand2")
        self.btn_som.pack(side=tk.LEFT, padx=20, ipadx=10, ipady=3)
        
        self.lbl_timer = tk.Label(info_frame, text="⏱️ Tempo: --", font=("Segoe UI", 14, "bold"), bg=self.COR_BG, fg="#F4D35E")
        self.lbl_timer.pack(side=tk.LEFT, padx=15)
        
        self.lbl_score = tk.Label(info_frame, text=f"Pontos: 0 | Acertos: {self.total_acertos}/3", font=("Segoe UI", 14, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO)
        self.lbl_score.pack(side=tk.RIGHT)
        
        self.lbl_pergunta = tk.Label(col_esq, text="", font=("Segoe UI", 18, "bold"), bg=self.COR_CARD, fg=self.COR_BRANCO, 
                                     wraplength=800, justify=tk.LEFT, padx=30, pady=30, relief=tk.FLAT)
        self.lbl_pergunta.pack(fill=tk.X, pady=(0, 20))
        
        self.botoes_opcoes = []
        for i in range(4):
            btn = self.criar_botao_customizado(col_esq, text="", font=("Segoe UI", 14, "bold"), bg=self.COR_AZUL_CLARO, fg=self.COR_BG, 
                            activebackground=self.COR_AZUL_SELECIONADO, activeforeground=self.COR_BRANCO, relief=tk.FLAT, anchor="w", padx=20,
                            command=lambda idx=i: self.selecionar_opcao(idx))
            btn.pack(fill=tk.X, pady=8, ipady=12)
            self.botoes_opcoes.append(btn)
            
        self.btn_confirmar = self.criar_botao_customizado(col_esq, text="✅ Confirmar Resposta", font=("Segoe UI", 14, "bold"), bg=self.COR_CARD, fg="#888888", 
                                       relief=tk.FLAT, state=tk.DISABLED, command=self.confirmar_resposta, cursor="hand2")
        self.btn_confirmar.pack(fill=tk.X, pady=(15, 0), ipady=10)
        
        self.btn_proxima = self.criar_botao_customizado(col_esq, text="➡️ Próxima Pergunta", font=("Segoe UI", 14, "bold"), bg=self.COR_CARD, fg="#888888", 
                                     relief=tk.FLAT, state=tk.DISABLED, command=self.carregar_proxima_pergunta, cursor="hand2")
        self.btn_proxima.pack(fill=tk.X, pady=(10, 0), ipady=10)
            
        ctrl_frame = tk.Frame(col_esq, bg=self.COR_BG)
        ctrl_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.criar_botao_customizado(ctrl_frame, text="🚪 Parar e Voltar ao Menu", font=("Segoe UI", 12), bg="#C0392B", fg=self.COR_BRANCO, relief=tk.FLAT, command=lambda: [self.tocar_musica_loop(self.configuracoes.get("musica_menu", "")), self.mostrar_menu_principal()]).pack(side=tk.LEFT, ipadx=15, ipady=6)

        col_dir = tk.Frame(main_frame, bg=self.COR_CARD, width=350, padx=20, pady=20)
        col_dir.pack(side=tk.RIGHT, fill=tk.Y)
        col_dir.pack_propagate(False)
        
        tk.Label(col_dir, text="🌸 Imaculada Conceição", font=("Segoe UI", 18, "bold"), bg=self.COR_CARD, fg=self.COR_BRANCO).pack(pady=(10, 10))
        
        self.btn_rolar_dado = self.criar_botao_customizado(col_dir, text="🎲 Rolar Dado Premiado", font=("Segoe UI", 13, "bold"), bg="#555555", fg="#888888", 
                                        relief=tk.FLAT, state=tk.DISABLED, command=self.tela_cheia_dado, cursor="arrow")
        self.btn_rolar_dado.pack(fill=tk.X, pady=15, ipady=10)
        
        self.img_ns = None
        nome_img = self.configuracoes.get("imagem_ns", "nossa_senhora.png")
        self.img_ns = self.carregar_imagem_segura(nome_img, 260, 320)
                
        if self.img_ns:
            tk.Label(col_dir, image=self.img_ns, bg=self.COR_CARD).pack(fill=tk.BOTH, expand=True, pady=10)
        else:
            tk.Label(col_dir, text=f"[ Imagem '{nome_img}'\nnão encontrada na pasta ]", font=("Segoe UI", 11, "italic"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO, justify=tk.CENTER, height=12).pack(fill=tk.BOTH, expand=True, pady=10)

        self.carregar_proxima_pergunta()

    def carregar_proxima_pergunta(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        self.respondido = False
        self.escolha_selecionada = None
        self.btn_confirmar.config(state=tk.DISABLED, bg=self.COR_CARD, fg="#888888")
        self.btn_proxima.config(state=tk.DISABLED, bg=self.COR_CARD, fg="#888888")
        
        self.pergunta_atual += 1
        if self.pergunta_atual <= len(self.perguntas_sessao):
            p = self.perguntas_sessao[self.pergunta_atual - 1]
            self.lbl_pergunta.config(text=f"Q{self.pergunta_atual}: {p['pergunta']}")
            for i, opcao in enumerate(p["opcoes"]):
                self.botoes_opcoes[i].config(text=opcao, bg=self.COR_AZUL_CLARO, fg=self.COR_BG, state=tk.NORMAL)
            
            limite = self.configuracoes.get("tempo_limite", 30)
            if limite > 0:
                self.tempo_restante = limite
                self.atualizar_cronometro()
            else:
                self.lbl_timer.config(text="⏱️ Tempo: Ilimitado")
        else:
            self.fim_do_jogo_participante()

    def atualizar_cronometro(self):
        if self.respondido:
            return
        if self.tempo_restante > 0:
            self.lbl_timer.config(text=f"⏱️ Tempo: {self.tempo_restante}s")
            self.tempo_restante -= 1
            self.timer_id = self.root.after(1000, self.atualizar_cronometro)
        else:
            self.lbl_timer.config(text="⏱️ Tempo Esgotado!")
            self.tocar_som_efeito("tempo_esgotado")
            self.tempo_esgotado_alarme_tela_cheia()

    def tempo_esgotado_alarme_tela_cheia(self):
        if self.respondido:
            return
        self.respondido = True
        
        self.limpar_tela()
        frame_alarme = tk.Frame(self.root, bg=self.COR_VERMELHO)
        frame_alarme.pack(fill=tk.BOTH, expand=True)
        
        self.criar_barra_topo(frame_alarme)

        tk.Label(frame_alarme, text="⚠️ TEMPO ESGOTADO! ⚠️", font=("Segoe UI", 40, "bold"), bg=self.COR_VERMELHO, fg=self.COR_BRANCO).pack(pady=60)
        tk.Label(frame_alarme, text="O tempo para responder esta pergunta terminou.", font=("Segoe UI", 22), bg=self.COR_VERMELHO, fg=self.COR_BRANCO).pack(pady=20)
        
        duracao_alarme = self.configuracoes.get("tempo_alarme", 4) * 1000
        
        def piscar(restante):
            if restante > 0:
                cor_atual = frame_alarme.cget("bg")
                nova_cor = "#0B2545" if cor_atual == self.COR_VERMELHO else self.COR_VERMELHO
                frame_alarme.config(bg=nova_cor)
                for w in frame_alarme.winfo_children():
                    w.config(bg=nova_cor)
                self.tocar_som_efeito("tempo_esgotado")
                self.root.after(300, lambda: piscar(restante - 300))
            else:
                self.tocar_musica_loop(self.configuracoes.get("musica_menu", ""))
                self.mostrar_menu_principal()

        self.root.after(100, lambda: piscar(duracao_alarme))

    def selecionar_opcao(self, idx):
        if self.respondido:
            return
        self.escolha_selecionada = idx
        for i, btn in enumerate(self.botoes_opcoes):
            if i == idx:
                btn.config(bg=self.COR_AZUL_SELECIONADO, fg=self.COR_BRANCO)
            else:
                btn.config(bg=self.COR_AZUL_CLARO, fg=self.COR_BG)
        self.btn_confirmar.config(state=tk.NORMAL, bg=self.COR_AZUL_SELECIONADO, fg=self.COR_BRANCO)

    def confirmar_resposta(self):
        if self.respondido or self.escolha_selecionada is None:
            return
        self.respondido = True
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        self.btn_confirmar.config(state=tk.DISABLED, bg=self.COR_CARD, fg="#888888")
        self.btn_proxima.config(state=tk.NORMAL, bg=self.COR_AZUL_SELECIONADO, fg=self.COR_BRANCO)
        
        p = self.perguntas_sessao[self.pergunta_atual - 1]
        texto_escolhido = p["opcoes"][self.escolha_selecionada]
        correta_txt = p["resposta"]
        
        for i, btn in enumerate(self.botoes_opcoes):
            if p["opcoes"][i] == correta_txt:
                btn.config(bg=self.COR_VERDE, fg=self.COR_BRANCO)
            elif i == self.escolha_selecionada and texto_escolhido != correta_txt:
                btn.config(bg=self.COR_VERMELHO, fg=self.COR_BRANCO)
            btn.config(state=tk.DISABLED)
            
        if texto_escolhido == correta_txt:
            self.pontuacao += 100
            self.total_acertos += 1
            self.tocar_som_efeito("acerto")
            self.lbl_score.config(text=f"Pontos: {self.pontuacao} | Acertos: {self.total_acertos}/3")
            
            if self.total_acertos >= 3:
                self.total_acertos = 0  
                self.btn_rolar_dado.config(state=tk.NORMAL, bg=self.COR_AZUL_SELECIONADO, fg=self.COR_BRANCO, cursor="hand2")
        else:
            self.tocar_som_efeito("erro")
            self.lbl_score.config(text=f"Pontos: {self.pontuacao} | Acertos: {self.total_acertos}/3")

    # =========================================================================
    # 7. TELA CHEIA PARA O DADO COM BOTÃO GIRAR E MÚSICAS ESPECÍFICAS
    # =========================================================================
    def tela_cheia_dado(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        self.tocar_musica_loop(self.configuracoes.get("musica_dado", ""))
        
        self.limpar_tela()
        
        frame_dado = tk.Frame(self.root, bg=self.COR_BG)
        frame_dado.pack(fill=tk.BOTH, expand=True, padx=80, pady=60)
        
        self.criar_barra_topo(frame_dado)

        tk.Label(frame_dado, text="🎲 SALA DO DADO PREMIADO! 🎲", font=("Segoe UI", 32, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(pady=20)
        tk.Label(frame_dado, text=f"Participante: {self.participante_atual}", font=("Segoe UI", 22), bg=self.COR_BG, fg=self.COR_AZUL_CLARO).pack(pady=10)
        tk.Label(frame_dado, text="Clique no botão abaixo para girar o dado!", font=("Segoe UI", 18), bg=self.COR_BG, fg=self.COR_BRANCO).pack(pady=15)
        
        lbl_num = tk.Label(frame_dado, text="🎲", font=("Segoe UI", 90, "bold"), bg=self.COR_CARD, fg=self.COR_BRANCO, padx=60, pady=20)
        lbl_num.pack(pady=30)
        
        def iniciar_giro():
            btn_girar.config(state=tk.DISABLED, bg="#555555")
            passos = [random.randint(1, 6) for _ in range(12)]
            resultado_final = random.randint(1, 6)
            passos.append(resultado_final)
            
            def animar(index):
                if index < len(passos):
                    num = passos[index]
                    lbl_num.config(text=f"【 {num} 】", fg=self.COR_AZUL_CLARO)
                    tempo_espera = 80 + (index * 30)
                    self.root.after(tempo_espera, lambda: animar(index + 1))
                else:
                    self.tocar_musica_loop(self.configuracoes.get("musica_comemoracao", ""))
                    lbl_num.config(text=f"【 {resultado_final} 】", fg=self.COR_VERDE)
                    
                    self.historico.append(f"Participante: {self.participante_atual} | Ganhou o Dado (Resultado: {resultado_final})")
                    self.salvar_dados()
                    
                    self.root.after(3500, self.fim_do_jogo_participante)

            animar(0)

        btn_girar = self.criar_botao_customizado(frame_dado, text="🎲 GIRAR O DADO", font=("Segoe UI", 20, "bold"), bg=self.COR_AZUL_SELECIONADO, fg=self.COR_BRANCO, relief=tk.FLAT, command=iniciar_giro, cursor="hand2")
        btn_girar.pack(ipadx=40, ipady=15, pady=20)

    # =========================================================================
    # 8. TELA DE AGRADECIMENTO FINAL (COM BÊNÇÃO DE NOSSA SENHORA E MENU INICIAL)
    # =========================================================================
    def fim_do_jogo_participante(self):
        reg_final = f"Participante: {self.participante_atual} | Pontuação Final: {self.pontuacao} Pontos"
        if reg_final not in self.historico:
            self.historico.append(reg_final)
            self.salvar_dados()
        
        self.limpar_tela()
        
        self.tocar_musica_loop(self.configuracoes.get("musica_comemoracao", ""))
        
        frame = tk.Frame(self.root, bg=self.COR_BG, padx=60, pady=60)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.criar_barra_topo(frame)

        tk.Label(frame, text="🎉 PARABÉNS! 🎉", font=("Segoe UI", 32, "bold"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(pady=15)
        tk.Label(frame, text=f"Participante: {self.participante_atual} | Pontuação: {self.pontuacao} Pontos", font=("Segoe UI", 22, "bold"), bg=self.COR_BG, fg=self.COR_AZUL_CLARO).pack(pady=10)
        
        nome_img = self.configuracoes.get("imagem_ns", "nossa_senhora.png")
        img_final = self.carregar_imagem_segura(nome_img, 180, 220)
        if img_final:
            tk.Label(frame, image=img_final, bg=self.COR_BG).pack(pady=10)
            self.img_final_ref = img_final
            
        tk.Label(frame, text="Que Nossa Senhora Imaculada Conceição abençoe grandemente a tua família!", font=("Segoe UI", 18, "italic"), bg=self.COR_BG, fg=self.COR_BRANCO).pack(pady=20)
        
        self.criar_botao_customizado(frame, text="🏠 Voltar ao Menu Inicial", font=("Segoe UI", 16, "bold"), bg=self.COR_AZUL_SELECIONADO, fg=self.COR_BRANCO, relief=tk.FLAT, command=lambda: [self.tocar_musica_loop(self.configuracoes.get("musica_menu", "")), self.mostrar_menu_principal()]).pack(ipadx=30, ipady=15, pady=20)

def main():
    root = tk.Tk()
    app = QuizSistemaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()