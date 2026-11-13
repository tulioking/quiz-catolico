# ==============================================================================
# SUPER QUIZ MULTI-TEMAS (COM MODO MOBILE / PAISAGEM E 2.100 PERGUNTAS) 📱🖥️🎲
# ==============================================================================

import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time
import base64
import re

ARQUIVO_DADOS = "dados_quiz_geral.json"
ARQUIVO_CONFIG = "config_quiz_geral.json"

TEMAS_COM_DIFICULDADE = ["⛪ Igreja", "🦸 Super-Heróis", "🎨 Desenhos", "⚔️ Animes"]
NIVEIS_DIFICULDADE = ["🟢 Fácil", "🟡 Normal", "🟠 Hard", "🔴 Impossível"]

MULTIPLICADOR_PONTOS = {
    "🟢 Fácil": 1.0,
    "🟡 Normal": 1.5,
    "🟠 Hard": 2.5,
    "🔴 Impossível": 5.0
}

# ==============================================================================
# PALETAS DE CORES, PÔSTERES E FRASES FINAIS EXCLUSIVAS DE CADA MODO DE JOGO
# ==============================================================================
INFO_MODOS = {
    "⛪ Igreja": {
        "cor_fundo": "#0B2545", "cor_card": "#134074", "cor_texto": "#FFFFFF",
        "cor_destaque": "#F4D35E", "cor_botao": "#134074", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#1F618D",
        "icone": "⛪", "titulo_card": "🌸 Imaculada Conceição", "sub_card": "Fé, História, Santos e Sagradas Escrituras",
        "img_padrao": "nossa_senhora.png",
        "msg_final": "Que Nossa Senhora Imaculada Conceição abençoe grandemente a você e toda a sua família! 🙏✨"
    },
    "🦸 Super-Heróis": {
        "cor_fundo": "#0A1128", "cor_card": "#1C2541", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFD166", "cor_botao": "#B80C09", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#FFD166",
        "icone": "🦸‍♂️", "titulo_card": "⚡ Universo dos Heróis", "sub_card": "Marvel, DC, Quadrinhos e Superpoderes",
        "img_padrao": "tema_herois.png",
        "msg_final": "Missão cumprida, herói! Você mostrou que tem superpoderes de conhecimento e salvou o multiverso! 🦸‍♂️⚡"
    },
    "🍎 Frutas": {
        "cor_fundo": "#1B4332", "cor_card": "#2D6A4F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFD166", "cor_botao": "#40916C", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#95D5B2",
        "icone": "🍉", "titulo_card": "🍎 Pomar Tropical", "sub_card": "Frutas, Vitaminas, Sabores e Natureza",
        "img_padrao": "tema_frutas.png",
        "msg_final": "Que desempenho refrescante! Você colheu os melhores resultados no nosso pomar de conhecimentos! 🍉🍍"
    },
    "🍔 Comidas": {
        "cor_fundo": "#370617", "cor_card": "#6A040F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFBA08", "cor_botao": "#9D0208", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#F48C06",
        "icone": "🍔", "titulo_card": "👨‍🍳 Mestre da Culinária", "sub_card": "Pratos Típicos, Sabores do Brasil e do Mundo",
        "img_padrao": "tema_comidas.png",
        "msg_final": "Parabéns, Mestre-Cuca! Você temperou essa partida com muito talento e deu um show de gastronomia! 👨‍🍳🍔"
    },
    "📺 Novelas": {
        "cor_fundo": "#3C096C", "cor_card": "#5A189A", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FF9E00", "cor_botao": "#7B2CBF", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#E0AAFF",
        "icone": "📺", "titulo_card": "🎭 Clássicos da TV", "sub_card": "Vilãs Icônicas, Bordões e Grandes Tramas",
        "img_padrao": "tema_novelas.png",
        "msg_final": "Cena digna de último capítulo em horário nobre! Você brilhou como protagonista nessa novela! 📺🌟"
    },
    "🎬 Filmes": {
        "cor_fundo": "#121212", "cor_card": "#1F1F1F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#D4AF37", "cor_botao": "#292929", "cor_texto_botao": "#D4AF37", "cor_borda_botao": "#D4AF37",
        "icone": "🎬", "titulo_card": "🍿 Sessão de Cinema", "sub_card": "Sucessos de Bilheteria, Oscar e Clássicos",
        "img_padrao": "tema_filmes.png",
        "msg_final": "E o Oscar vai para... VOCÊ! Uma atuação digna de tapete vermelho e recorde de bilheteria! 🎬🏆"
    },
    "🎨 Desenhos": {
        "cor_fundo": "#003049", "cor_card": "#00507A", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FCBF49", "cor_botao": "#F77F00", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#FCBF49",
        "icone": "🎨", "titulo_card": "🎈 Mundo Animado", "sub_card": "Desenhos Clássicos, Nostalgia e Diversão",
        "img_padrao": "tema_desenhos.png",
        "msg_final": "Isso é tudo, pessoal! Você mandou super bem e garantiu a diversão com gostinho de infância! 🎨🎈"
    },
    "⚔️ Animes": {
        "cor_fundo": "#10002B", "cor_card": "#240046", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00F5D4", "cor_botao": "#7209B7", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#F72585",
        "icone": "⚔️", "titulo_card": "🐉 Arena Otaku", "sub_card": "400 Perguntas Únicas: Fácil, Normal, Hard e Impossível!",
        "img_padrao": "tema_animes.png",
        "msg_final": "O seu poder de luta passou de 8.000! Você despertou o instinto superior e dominou a Arena Otaku! ⚔️🔥"
    },
    "💼 Trabalhos & Profissões": {
        "cor_fundo": "#1B263B", "cor_card": "#283845", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00B4D8", "cor_botao": "#415A77", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#90E0EF",
        "icone": "💼", "titulo_card": "🛠️ Mundo das Profissões", "sub_card": "Tecnologia, Saúde, Engenharia e Ofícios",
        "img_padrao": "tema_trabalhos.png",
        "msg_final": "Trabalho de excelência! Você mostrou competência máxima e merece uma promoção com louvor! 💼🚀"
    },
    "🎲 Misturadão (Todos os Temas)": {
        "cor_fundo": "#1F1147", "cor_card": "#341F6F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00F5D4", "cor_botao": "#4E2A84", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#00F5D4",
        "icone": "🎲", "titulo_card": "🌟 Desafio Misturadão", "sub_card": "Todas as 2.100 Perguntas Juntas num Só Jogo!",
        "img_padrao": "tema_misturadao.png",
        "msg_final": "Incrível! Você encarou o desafio supremo de todos os temas e provou que sabe de tudo um pouco! 🎲👑"
    }
}

# ==============================================================================
# GERADOR DE PERGUNTAS (COM 400 FATOS 100% ÚNICOS E SEM REPETIÇÃO EM ANIMES!)
# ==============================================================================
def montar_100_perguntas(fatos, templates):
    todas_respostas = list(dict.fromkeys([f[2] for f in fatos]))
    perguntas_geradas = []
    rng = random.Random(42)
    
    for idx in range(100):
        item, sub, certa = fatos[idx % len(fatos)]
        molde = templates[idx % len(templates)]
        enunciado = molde.format(item=item, sub=sub)
        
        pool_erradas = [r for r in todas_respostas if r != certa]
        distratores = rng.sample(pool_erradas, min(3, len(pool_erradas)))
        opcoes_brutas = [certa] + distratores
        
        letras = ["A)", "B)", "C)", "D)"]
        opcoes_finais = [f"{letras[i]} {opcoes_brutas[i]}" for i in range(4)]
        perguntas_geradas.append({
            "pergunta": enunciado,
            "opcoes": opcoes_finais,
            "resposta": f"A) {certa}"
        })
    return perguntas_geradas

def construir_bancos_completos():
    tpl_padrao = [
        "Sobre {item}, qual alternativa indica corretamente {sub}?",
        "Qual das opções abaixo corresponde a {sub} em {item}?",
        "No universo de {item}, o que define corretamente {sub}?",
        "Assinale a alternativa verdadeira sobre {sub} referente a {item}:"
    ]

    # ⚔️ ANIMES — 400 FATOS 100% ÚNICOS (100 POR NÍVEL, ZERO REPETIÇÕES!)
    animes_facil_100 = [
        ("Dragon Ball Z", "o nome do protagonista criado na Terra que adora lutar", "Son Goku"),
        ("Dragon Ball Z", "a quantidade de Esferas do Dragão necessárias para invocar Shenlong", "7 Esferas do Dragão"),
        ("Dragon Ball Z", "o golpe de energia azul mais famoso lançado por Goku com as duas mãos", "Kamehameha"),
        ("Dragon Ball Z", "o príncipe orgulhoso da raça Saiyajin que é o maior rival de Goku", "Vegeta"),
        ("Dragon Ball Z", "o nome do primeiro filho de Goku com Chi-Chi", "Son Gohan"),
        ("Dragon Ball Z", "o melhor amigo careca de Goku desde o treino com o Mestre Kame", "Kuririn"),
        ("Dragon Ball Z", "o guerreiro de pele verde da raça Namekuseijin que treinou Gohan", "Piccolo"),
        ("Dragon Ball Z", "a transformação lendária de cabelos dourados e olhos verdes", "Super Saiyajin"),
        ("Dragon Ball Z", "a semente mágica cultivada pelo Mestre Karin que cura ferimentos na hora", "Semente dos Deuses"),
        ("Dragon Ball Z", "a cientista genial de cabelos azuis criadora do Radar do Dragão", "Bulma"),
        ("Naruto", "o grande sonho de infância de Naruto Uzumaki na Vila da Folha", "Tornar-se o Hokage"),
        ("Naruto", "a criatura gigante de nove caudas selada dentro de Naruto", "Raposa de Nove Caudas (Kurama)"),
        ("Naruto", "o rival de Naruto e sobrevivente do massacre do clã Uchiha", "Sasuke Uchiha"),
        ("Naruto", "a kunoichi de cabelos rosas integrante do Time 7", "Sakura Haruno"),
        ("Naruto", "o ninja copiador de cabelos grisalhos e máscara que lidera o Time 7", "Kakashi Hatake"),
        ("Naruto", "o prato de macarrão japonês favorito de Naruto no Ichiraku", "Lámen (Ramen)"),
        ("Naruto", "a técnica básica que Naruto usa para criar várias cópias físicas de si mesmo", "Jutsu Clone das Sombras"),
        ("Naruto", "a esfera espiral de chakra azul giratória criada na palma da mão", "Rasengan"),
        ("Naruto", "o poder ocular de olhos vermelhos exclusivo do clã Uchiha", "Sharingan"),
        ("Naruto", "a vila oculta onde Naruto nasceu e cresceu", "Aldeia da Folha (Konoha)"),
        ("One Piece", "o grande sonho de Monkey D. Luffy ao navegar pelos mares", "Ser o Rei dos Piratas"),
        ("One Piece", "o acessório inseparável que Shanks entregou para Luffy usar na cabeça", "Chapéu de Palha"),
        ("One Piece", "o poder que o corpo de Luffy ganhou após comer uma Akuma no Mi", "Corpo elástico de borracha"),
        ("One Piece", "a grande fraqueza de qualquer pessoa que come uma Fruta do Diabo", "Perder as forças ao entrar na água do mar"),
        ("One Piece", "o espadachim de cabelos verdes que luta usando três espadas", "Roronoa Zoro"),
        ("One Piece", "a navegadora ruiva do bando apaixonada por mapas e dinheiro", "Nami"),
        ("One Piece", "o cozinheiro loiro do bando que luta apenas usando chutes", "Sanji"),
        ("One Piece", "o atirador narigudo e contador de histórias do bando", "Usopp"),
        ("One Piece", "a pequena rena de nariz azul que é o médico da tripulação", "Tony Tony Chopper"),
        ("One Piece", "a bandeira negra com caveira usada pelos navios piratas", "Jolly Roger"),
        ("Pokémon", "o primeiro Pokémon amarelo do tipo elétrico parceiro de Ash Ketchum", "Pikachu"),
        ("Pokémon", "o objeto esférico vermelho e branco usado para capturar Pokémon", "Pokébola"),
        ("Pokémon", "a dupla de vilões atrapalhados da Equipe Rocket acompanhados por Meowth", "Jessie e James"),
        ("Pokémon", "o Pokémon inicial de fogo com a ponta do rabo em chamas em Kanto", "Charmander"),
        ("Pokémon", "o Pokémon inicial do tipo água em formato de tartaruga azul", "Squirtle"),
        ("Pokémon", "o Pokémon inicial do tipo planta que carrega um bulbo nas costas", "Bulbasaur"),
        ("Pokémon", "a evolução final em formato de dragão alado de fogo do Charmander", "Charizard"),
        ("Pokémon", "o Pokémon psíquico lendário criado em laboratório a partir do DNA de Mew", "Mewtwo"),
        ("Cavaleiros do Zodíaco", "a constelação protetora da armadura de bronze de Seiya", "Pégaso"),
        ("Cavaleiros do Zodíaco", "a deusa grega da sabedoria que os Cavaleiros juraram proteger", "Deusa Atena (Saori Kido)"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Bronze que ficou cego para derrotar Algol de Perseu", "Shiryu de Dragão"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Bronze que domina o gelo e o Pó de Diamante", "Hyoga de Cisne"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Bronze gentil que usa correntes rosadas como arma", "Shun de Andrômeda"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro solitário cuja armadura renasce das cinzas", "Ikki de Fênix"),
        ("Cavaleiros do Zodíaco", "a classe de elite formada pelos 12 guerreiros que protegem as 12 Casas", "Cavaleiros de Ouro"),
        ("Death Note", "o que acontece com a pessoa cujo nome é escrito no Death Note", "Ela morre (geralmente de parada cardíaca)"),
        ("Death Note", "o estudante brilhante que encontra o caderno e passa a ser chamado de Kira", "Light Yagami"),
        ("Death Note", "a fruta favorita que o Shinigami Ryuk é completamente viciado em comer", "Maçã"),
        ("Death Note", "o detetive genial que senta agachado e adora comer doces", "L"),
        ("Demon Slayer", "o jovem bondoso de olfato apurado que vende carvão no início da obra", "Tanjiro Kamado"),
        ("Demon Slayer", "a irmã de Tanjiro que foi transformada em Oni mas não ataca humanos", "Nezuko Kamado"),
        ("Demon Slayer", "onde Tanjiro carrega sua irmã Nezuko durante o dia para protegê-la do sol", "Dentro de uma caixa de madeira nas costas"),
        ("Demon Slayer", "o espadachim medroso de cabelos amarelos que luta dormindo com trovões", "Zenitsu Agatsuma"),
        ("Demon Slayer", "o espadachim selvagem que usa uma cabeça de javali como máscara", "Inosuke Hashibira"),
        ("Attack on Titan", "os monstros gigantes devoradores de humanos fora das muralhas", "Titãs"),
        ("Attack on Titan", "o protagonista determinado a exterminar todos os Titãs do mundo", "Eren Yeager"),
        ("Attack on Titan", "a guerreira habilidosa de cachecol vermelho que protege Eren", "Mikasa Ackerman"),
        ("Attack on Titan", "o amigo estrategista loiro de Eren e Mikasa que sonhava em ver o mar", "Armin Arlert"),
        ("Attack on Titan", "o ponto fraco fatal no corpo de qualquer Titã comum", "A nuca"),
        ("One Punch Man", "a característica visual marcante da cabeça do herói Saitama", "Ele é totalmente careca"),
        ("One Punch Man", "como Saitama derrota seus inimigos mais poderosos", "Com apenas um único soco"),
        ("One Punch Man", "o ciborgue loiro que se torna discípulo fiel de Saitama", "Genos"),
        ("My Hero Academia", "o jovem protagonista que nasceu sem individualidade num mundo de heróis", "Izuku Midoriya (Deku)"),
        ("My Hero Academia", "o herói número 1 conhecido como o Símbolo da Paz", "All Might"),
        ("My Hero Academia", "o rival explosivo de infância de Deku que cria explosões pelas mãos", "Katsuki Bakugo"),
        ("Jujutsu Kaisen", "o estudante de cabelos rosas que engole um dedo amaldiçoado", "Yuji Itadori"),
        ("Jujutsu Kaisen", "o professor de cabelos brancos e venda nos olhos dos alunos do 1º ano", "Satoru Gojo"),
        ("Spy x Family", "a garotinha adotada por Loid e Yor que possui o poder de ler mentes", "Anya Forger"),
        ("Spy x Family", "a verdadeira profissão secreta do pai adotivo Loid Forger (Twilight)", "Espião secreto"),
        ("Spy x Family", "a verdadeira profissão secreta da mãe adotiva Yor Forger", "Assassina profissional (Princesa Espinho)"),
        ("Solo Leveling", "o protagonista que começa a história como o caçador mais fraco da humanidade", "Sung Jin-Woo"),
        ("Solo Leveling", "a classificação inicial mais baixa de todas que Jin-Woo tinha na Associação", "Caçador de Rank E"),
        ("Black Clover", "o jovem protagonista órfão que grita muito e sonha em ser o Rei Mago", "Asta"),
        ("Black Clover", "o livro mágico que cada mago recebe aos 15 anos na cerimônia da torre", "Grimório"),
        ("Bleach", "o adolescente de cabelos laranjas que consegue ver fantasmas desde criança", "Ichigo Kurosaki"),
        ("Bleach", "a Shinigami que transfere seus poderes para Ichigo no primeiro episódio", "Rukia Kuchiki"),
        ("Tokyo Revengers", "o jovem protagonista que descobre a habilidade de voltar no tempo", "Takemichi Hanagaki"),
        ("Mashle: Magia e Músculos", "o que Mash faz todos os dias na floresta já que não possui magia", "Musculação e levantamento de peso"),
        ("Slime (Tensura)", "a criatura gelatinosa azul em que Satoru Mikami reencarna no outro mundo", "Um Slime"),
        ("Cyberpunk: Edgerunners", "o jovem estudante de jaqueta amarela que entra para o mundo dos mercenários", "David Martinez"),
        ("Yu-Gi-Oh!", "o objeto egípcio dourado em forma de pirâmide que Yugi usa no pescoço", "Enigma do Milênio"),
        ("Digimon Adventure", "o monstrinho amarelo parecido com um pequeno dinossauro parceiro de Tai", "Agumon"),
        ("Beyblade", "o brinquedo usado nas batalhas de estádio pelos competidores", "Piões de batalha (Beyblades)"),
        ("Sailor Moon", "o animal falante com uma meia-lua na testa que entrega o broche a Usagi", "Uma gata preta chamada Luna"),
        ("Sakura Card Captors", "o guardião amarelo com asas parecido com um bichinho de pelúcia", "Kerberos (Kero)"),
        ("InuYasha", "a metade não-humana do protagonista InuYasha de orelhas brancas", "Meio-Youkai cão"),
        ("Yu Yu Hakusho", "o adolescente rebelde que morre salvando uma criança e vira Detetive Espiritual", "Yusuke Urameshi"),
        ("Fullmetal Alchemist", "a ciência mística usada pelos irmãos Elric batendo as palmas das mãos", "Alquimia"),
        ("Hunter x Hunter", "o garoto de roupas verdes que sai da Ilha da Baleia para procurar seu pai", "Gon Freecss"),
        ("Blue Lock", "o esporte em que 300 jovens atacantes competem dentro do projeto Blue Lock", "Futebol"),
        ("Haikyuu!!", "o esporte de quadra com rede pelo qual Shoyo Hinata é apaixonado", "Voleibol"),
        ("Captain Tsubasa (Super Campeões)", "a posição de ataque e liderança de Oliver Tsubasa em campo", "Camisa 10 e capitão do time"),
        ("Chainsaw Man", "a arma em que a cabeça e os braços de Denji se transformam ao puxar a corda", "Motosserras"),
        ("Chainsaw Man", "o pequeno demônio cachorrinho laranja com uma motosserra na testa", "Pochita"),
        ("Dr. Stone", "o que aconteceu misteriosamente com todos os seres humanos da Terra no início", "Foram transformados em estátuas de pedra"),
        ("Dr. Stone", "o jovem gênio cientista que conta os segundos por 3.700 anos", "Senku Ishigami"),
        ("The Seven Deadly Sins (Nanatsu no Taizai)", "o capitão loiro baixinho dono da taverna Chapéu de Javali", "Meliodas, o Pecado da Ira do Dragão"),
        ("Fairy Tail", "o tipo de magia elemental dominada por Natsu Dragneel, criado por Igneel", "Magia de Dragon Slayer do Fogo"),
        ("Baki", "o objetivo de Baki Hanma ao treinar artes marciais extremas desde criança", "Derrotar seu pai Yujiro Hanma, a criatura mais forte da Terra"),
        ("Dandadan", "as duas coisas em que Momo Ayase e Okarun acreditavam no começo da história", "Fantasmas e Alienígenas")
    ]

    animes_normal_100 = [
        ("Solo Leveling", "a palavra de comando que Sung Jin-Woo pronuncia para extrair sombras", "Erga-se (Arise)"),
        ("Solo Leveling", "o melhor amigo rico de Jin-Woo que usa uma armadura caríssima e escudo", "Yoo Jin-Ho"),
        ("Solo Leveling", "a caçadora de Rank S loira que sente um cheiro diferente e agradável em Jin-Woo", "Cha Hae-In"),
        ("Black Clover", "o número de folhas no trevo do grimório de Asta que representa um demônio", "Trevo de Cinco Folhas"),
        ("Black Clover", "o irmão de criação e rival prodígio de Asta que recebeu o grimório de 4 folhas", "Yuno"),
        ("Black Clover", "o esquadrão mais bagunceiro dos Cavaleiros Mágicos no qual Asta entra", "Touros Negros"),
        ("Black Clover", "a nobre da família Silva que usa magia de água e não controlava seu poder no início", "Noelle Silva"),
        ("Bleach", "o nome da espada gigante de Ichigo Kurosaki em sua forma liberada inicial (Shikai)", "Zangetsu"),
        ("Bleach", "o amigo de óculos de Ichigo que pertence ao clã de arqueiros espirituais Quincy", "Uryu Ishida"),
        ("Bleach", "a amiga de classe de Ichigo que possui os grampos mágicos Shun Shun Rikka", "Orihime Inoue"),
        ("Bleach", "a organização militar dividida em 13 divisões que protege a Soul Society", "Gotei 13"),
        ("Tokyo Revengers", "o nome verdadeiro completo do líder invencível Mikey da Toman", "Manjiro Sano"),
        ("Tokyo Revengers", "o vice-líder alto da Toman que tem uma tatuagem de dragão na têmpora", "Draken (Ken Ryuguji)"),
        ("Tokyo Revengers", "a namorada de adolescência que Takemichi tenta salvar da morte no futuro", "Hinata Tachibana"),
        ("Mashle: Magia e Músculos", "o doce recheado de creme que Mash come o tempo inteiro", "Profiteroles (bombinhas de creme)"),
        ("Mashle: Magia e Músculos", "o nome da famosa escola de magia onde Mash precisa se tornar Visionário Divino", "Academia de Magia Easton"),
        ("Slime (Tensura)", "o Dragão da Tempestade que se torna o primeiro amigo de Rimuru na caverna", "Veldora Tempest"),
        ("Slime (Tensura)", "o nome da nação de monstros fundada e governada por Rimuru", "Federação Jura Tempest"),
        ("Cyberpunk: Edgerunners", "o implante militar na coluna que deixa David com reflexos em câmera lenta", "Sandevistan"),
        ("Cyberpunk: Edgerunners", "o líder veterano de braços gigantes que acolhe David no seu grupo", "Maine"),
        ("Cyberpunk: Edgerunners", "a pistoleira baixinha e explosiva de pele azulada do grupo de Maine", "Rebecca"),
        ("Dragon Ball Z", "o imperador galáctico que destruiu o Planeta Vegeta e matou Kuririn em Namekusei", "Freeza"),
        ("Dragon Ball Z", "o bioandroide perfeito criado pelo computador do Dr. Gero que organizou um torneio", "Cell"),
        ("Dragon Ball Z", "o monstro rosado mágico despertado pelo mago Babidi que transforma pessoas em doce", "Majin Boo"),
        ("Dragon Ball Z", "a dança ou técnica que une Goku e Vegeta num único guerreiro superpoderoso", "Fusão (Gogeta na dança / Vegetto nos brincos Potara)"),
        ("Dragon Ball Z", "o jovem vindo do futuro com uma espada nas costas para avisar sobre os Androides", "Trunks do Futuro"),
        ("Dragon Ball Super", "o Deus da Destruição do Sétimo Universo que tem aparência de gato roxo", "Bills (Beerus)"),
        ("Naruto", "o mestre lendário Sannin conhecido como Sábio Tarado que treinou Naruto", "Jiraiya"),
        ("Naruto", "o irmão mais velho de Sasuke que aniquilou o clã e entrou para a Akatsuki", "Itachi Uchiha"),
        ("Naruto", "o Jinchuuriki da Areia que controla a areia com sua cabaça nas costas", "Gaara do Deserto"),
        ("Naruto", "o ninja de sobrancelhas grossas e macacão verde que usa apenas Taijutsu", "Rock Lee"),
        ("Naruto", "o estrategista preguiçoso do clã Nara que controla sombras e tem QI acima de 200", "Shikamaru Nara"),
        ("Naruto", "a garota tímida do clã Hyuga que possui o olho Byakugan e sempre amou Naruto", "Hinata Hyuga"),
        ("Naruto", "o vilão Sannin das cobras obcecado pela imortalidade que marcou Sasuke", "Orochimaru"),
        ("Naruto Shippuden", "o líder da Akatsuki que possui o olho Rinnegan e destruiu Konoha com o Shinra Tensei", "Pain (Nagato)"),
        ("One Piece", "o primeiro navio com cabeça de ovelha que o bando ganhou na vila de Kaya", "Going Merry"),
        ("One Piece", "o irmão mais velho adotivo de Luffy que comeu a Fruta do Fogo (Mera Mera no Mi)", "Portgas D. Ace"),
        ("One Piece", "a arqueóloga do bando capaz de ler as pedras históricas chamadas Poneglyphs", "Nico Robin"),
        ("One Piece", "o esqueleto músico afro que voltou à vida graças à Fruta da Ressurreição", "Brook"),
        ("One Piece", "o pirata lendário executado em Loguetown que deixou o tesouro One Piece", "Gol D. Roger"),
        ("One Piece", "o espadachim número 1 do mundo que carrega a espada negra Yoru nas costas", "Dracule Mihawk"),
        ("One Piece", "o cirurgião da morte capitão dos Piratas Heart que comeu a Ope Ope no Mi", "Trafalgar Law"),
        ("Attack on Titan", "o comandante da Tropa de Exploração famoso pelo grito 'Shinzou wo Sasageyo!'", "Erwin Smith"),
        ("Attack on Titan", "o capitão baixinho considerado o soldado mais forte da humanidade", "Levi Ackerman"),
        ("Attack on Titan", "as três grandes muralhas concêntricas que protegiam o reino humano", "Muralhas Maria, Rose e Sina"),
        ("Attack on Titan", "o aparelho com cabos de aço e gás usado pelos soldados para voar entre prédios", "Equipamento de Manobra Tridimensional (DMT)"),
        ("Attack on Titan", "os dois guerreiros infiltrados que se revelaram o Titã Blindado e o Titã Colossal", "Reiner Braun e Bertholdt Hoover"),
        ("Demon Slayer", "o rei progenitor de todos os Onis que tem aparência semelhante a Michael Jackson", "Muzan Kibutsuji"),
        ("Demon Slayer", "o Hashira das Chamas que protegeu todos os passageiros no Trem Infinito", "Kyojuro Rengoku"),
        ("Demon Slayer", "o Hashira da Água calmo que salvou Tanjiro e Nezuko no primeiro episódio", "Giyu Tomioka"),
        ("Demon Slayer", "a Hashira dos Insetos que usa veneno de glicínia na ponta da espada", "Shinobu Kocho"),
        ("Demon Slayer", "o minério especial que absorve luz solar usado para forjar as espadas dos caçadores", "Minério Escarlate para Espadas Nichirin"),
        ("Jujutsu Kaisen", "o aluno do 1º ano do clã Zenin que invoca shikigamis através das Dez Sombras", "Megumi Fushiguro"),
        ("Jujutsu Kaisen", "a aluna do 1º ano que luta usando um martelo, pregos e bonecos de palha", "Nobara Kugisaki"),
        ("Jujutsu Kaisen", "o feiticeiro de Grau 1 ex-assalariado que usa gravata e a técnica de proporção 7:3", "Kento Nanami"),
        ("Jujutsu Kaisen", "o estudante grandalhão de Kyoto que pergunta 'Qual é o seu tipo de mulher?'", "Aoi Todo"),
        ("My Hero Academia", "o estudante que tem metade do corpo de gelo e metade de fogo, filho de Endeavor", "Shoto Todoroki"),
        ("My Hero Academia", "a estudante que remove a gravidade das coisas que toca com as pontas dos dedos", "Ochaco Uraraka"),
        ("My Hero Academia", "o professor cansado da Turma 1-A que apaga individualidades com o olhar", "Shota Aizawa (Eraser Head)"),
        ("My Hero Academia", "o líder da Liga dos Vilões que desintegra tudo o que toca com os cinco dedos", "Tomura Shigaraki"),
        ("Death Note", "a modelo famosa apaixonada por Light que também possui um Death Note e os olhos de Shinigami", "Misa Amane"),
        ("Death Note", "o acordo que um humano pode fazer com um Shinigami em troca de metade do seu tempo de vida", "Acordo dos Olhos de Shinigami (para ver o nome e tempo de vida)"),
        ("Fullmetal Alchemist", "o que os irmãos Elric tentaram fazer na infância quebrando o maior tabu da alquimia", "Transmutação Humana para reviver a mãe Trisha"),
        ("Fullmetal Alchemist", "onde a alma de Alphonse Elric foi selada por Edward após perder o corpo físico", "Dentro de uma grande armadura de ferro"),
        ("Fullmetal Alchemist", "o Alquimista das Chamas que cria explosões estalando os dedos com luvas especiais", "Coronel Roy Mustang"),
        ("Hunter x Hunter", "o sobrevivente do clã Kurta cujos olhos ficam escarlates quando sente fortes emoções", "Kurapika"),
        ("Hunter x Hunter", "o amigo de Gon que entrou no Exame Hunter com o objetivo de pagar a faculdade de medicina", "Leorio Paradinight"),
        ("Hunter x Hunter", "o mágico psicopata que usa cartas de baralho e a habilidade elástica Bungee Gum", "Hisoka Morow"),
        ("Yu Yu Hakusho", "o guerreiro baixinho de três olhos que domina as Chamas Negras Mortais", "Hiei"),
        ("Yu Yu Hakusho", "o Youkai raposa reencarnado como humano ruivo que controla plantas e chicote de rosas", "Kurama (Shuichi Minamino)"),
        ("Yu Yu Hakusho", "o valentão ruivo amigo de Yusuke que cria uma espada espiritual de energia", "Kazuma Kuwabara"),
        ("Yu Yu Hakusho", "a mestra idosa da Doutrina Genkai que treinou Yusuke e lhe passou a Onda Espiritual", "Mestra Genkai"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Ouro de Áries que conserta as armaduras em Jamiel", "Mu de Áries"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Ouro brasileiro que protege a segunda casa do Santuário", "Aldebaran de Touro"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Ouro de Leão, irmão mais novo do herói Aiolos de Sagitário", "Aiolia de Leão"),
        ("One Punch Man", "a heroína de Classe S Rank 2 conhecida como Tornado do Terror que usa telecinese", "Tatsumaki"),
        ("One Punch Man", "o vilão caçador de heróis discípulo rebelde de Bang (Silver Fang)", "Garou"),
        ("One Punch Man", "o homem considerado o mais forte da Terra que na verdade só tem sorte e joga videogame", "King (e o Motor King)"),
        ("Spy x Family", "o cachorro branco grande adotado pelos Forger que consegue prever o futuro", "Bond Forger"),
        ("Chainsaw Man", "a mulher misteriosa de olhos amarelos em anéis que chefia a Divisão Especial 4", "Makima"),
        ("Chainsaw Man", "a Infernal de Sangue com chifres vermelhos que divide apartamento com Denji e Aki", "Power"),
        ("Blue Lock", "o protagonista que possui excelente visão espacial e o chute direto de primeira", "Yoichi Isagi"),
        ("Blue Lock", "o gênio preguiçoso de cabelos brancos que domina qualquer bola com controle absurdo", "Seishiro Nagi"),
        ("Haikyuu!!", "o levantador prodígio chamado de Rei da Quadra que faz a dupla rápida com Hinata", "Tobio Kageyama"),
        ("Haikyuu!!", "a escola de uniforme preto associada a corvos onde Hinata e Kageyama jogam", "Colégio Karasuno"),
        ("InuYasha", "o meio-irmão mais velho de InuYasha, um Youkai completo elegante e poderoso", "Sesshomaru"),
        ("InuYasha", "a espada forjada a partir do dente do pai de InuYasha capaz de cortar 100 Youkais", "Tessaiga"),
        ("Code Geass", "o nome falso adotado pelo príncipe exilado Lelouch na Academia Ashford", "Lelouch Lamperouge"),
        ("Sword Art Online", "o espadachim negro que zerou o jogo mortal Aincrad usando duas espadas", "Kirito (Kazuto Kirigaya)"),
        ("The Seven Deadly Sins", "o Pecado do Orgulho do Leão que fica invencível quando o sol atinge o meio-dia", "Escanor"),
        ("Dr. Stone", "o líquido químico feito com ácido nítrico e álcool que desfaz a petrificação", "Fluido de Revivamento (Água Milagrosa)"),
        ("Mob Psycho 100", "o charlatão sem poderes psíquicos que é o chefe e mentor de Shigeo Kageyama (Mob)", "Arataka Reigen"),
        ("Fire Force", "o jovem bombeiro que solta fogo pelos pés e sorri quando fica nervoso", "Shinra Kusakabe"),
        ("Frieren e a Jornada para o Além", "a raça longeva da maga Frieren que vive milhares de anos", "Elfa"),
        ("Bocchi the Rock!", "o instrumento musical que a tímida Hitori Gotoh toca com maestria na banda Kessoku", "Guitarra elétrica"),
        ("Oshi no Ko", "a idol lendária do grupo B-Komachi que teve os gêmeos Aqua e Ruby", "Ai Hoshino"),
        ("Re:Zero", "a maldição/habilidade que faz Subaru Natsuki voltar a um ponto salvo toda vez que morre", "Retorno através da Morte"),
        ("Konosuba", "a deusa da água inútil que Kazuma escolheu levar consigo para o outro mundo", "Aqua"),
        ("Overlord", "o esqueleto mago supremo líder da Grande Tumba de Nazarick", "Ainz Ooal Gown (Momonga)"),
        ("Vinland Saga", "o jovem guerreiro islandês que busca duelo contra Askeladd para vingar seu pai Thors", "Thorfinn")
    ]

    animes_hard_100 = [
        ("Solo Leveling", "o cavaleiro vermelho-sangue comandante que Jin-Woo derrota na missão de troca de classe", "Igris, o Comandante Vermelho-Sangue"),
        ("Solo Leveling", "o rei formiga alado nascido na Ilha de Jeju que Jin-Woo transforma em sua sombra mais fiel", "Beru"),
        ("Solo Leveling", "o alto orc xamã que Jin-Woo renomeia ao transformar em general do seu exército de sombras", "Tusk (Presa)"),
        ("Solo Leveling", "o título oficial da classe oculta que o Sistema concede a Sung Jin-Woo", "Monarca das Sombras (inicialmente Necromante)"),
        ("Solo Leveling", "o caçador norte-americano de Nível Nacional conhecido como Golias e líder da Guilda Scavenger", "Thomas Andre"),
        ("Solo Leveling", "o nome do pai de Sung Jin-Woo que ficou desaparecido dentro de um portal por 10 anos", "Sung Il-Hwan"),
        ("Bleach: Thousand-Year Blood War", "o nome da Bankai de chamas supremas do Comandante Genryusai Yamamoto", "Zanka no Tachi"),
        ("Bleach: Thousand-Year Blood War", "a verdadeira identidade da Capitã da 4ª Divisão Retsu Unohana no passado", "Yachiru Unohana, a primeira Kenpachi da história"),
        ("Bleach: Thousand-Year Blood War", "o nome da Bankai de gelo absoluto verdadeiro de Rukia Kuchiki", "Hakka no Togame"),
        ("Bleach: Thousand-Year Blood War", "o nome da Shikai e da Bankai finalmente despertadas por Kenpachi Zaraki", "Nozarashi (Shikai) e transformação berserk demoníaca (Bankai)"),
        ("Bleach: Thousand-Year Blood War", "o nome da Bankai teatral em atos sombrios do Capitão Shunsui Kyoraku", "Katen Kyokotsu: Karamatsu Shinju"),
        ("Bleach", "o grupo de 10 Arrancars de elite numerados de 1 a 10 comandados por Sosuke Aizen", "Os Espada"),
        ("Bleach", "o Espada de número 4 que enfrenta Ichigo no domo de Las Noches com a Segunda Etapa", "Ulquiorra Cifer"),
        ("Black Clover", "o capitão estrangeiro dos Touros Negros que usa Magia de Escuridão e katana", "Yami Sukehiro"),
        ("Black Clover", "o capitão do Alvorecer Dourado que dividia o mesmo corpo com o líder dos elfos Patry", "William Vangeance"),
        ("Black Clover", "o 28º Rei Mago do Reino de Clover que possui Magia do Tempo", "Julius Novachrono"),
        ("Black Clover", "a irmã mais velha de Fuegoleon que domina a zona de mana Calidus Brachium", "Mereoleona Vermillion"),
        ("Black Clover", "o vice-capitão dos Touros Negros que fez um pacto com quatro demônios diferentes", "Nacht Faust"),
        ("Tokyo Revengers", "o fundador da 1ª geração da Black Dragons e irmão mais velho de Mikey", "Shinichiro Sano"),
        ("Tokyo Revengers", "o capitão da 1ª divisão da Toman e amigo de infância que deu o amuleto a Chifuyu", "Keisuke Baji"),
        ("Tokyo Revengers", "o líder implacável da gangue Tenjiku em Yokohama e meio-irmão adotivo de Mikey", "Izana Kurokawa"),
        ("Mashle: Magia e Músculos", "o estudante de duas linhas que controla gravidade e vira rival/amigo de Mash", "Lance Crown"),
        ("Mashle: Magia e Músculos", "o líder do grupo Magia Lupus que usa Magia de Marionetes e três linhas", "Abel Walker"),
        ("Mashle: Magia e Músculos", "o Visionário Divino da Areia considerado o mais forte entre os estudantes", "Orter Madl"),
        ("Slime (Tensura)", "a Habilidade Única inicial de Rimuru que analisa tudo e depois evolui para o Senhor da Sabedoria", "Grande Sábio (que evolui para Rafael)"),
        ("Slime (Tensura)", "a Lorde Demônio mais antiga de cabelos rosas conhecida como a Destruidora", "Milim Nava"),
        ("Slime (Tensura)", "o espadachim Kijin mestre de Rimuru cujo golpe corta até o espírito do oponente", "Hakurou"),
        ("Slime (Tensura)", "a aventureira japonesa dona da máscara anti-magia que deixou sua vontade para Rimuru", "Shizue Izawa (Shizu)"),
        ("Cyberpunk: Edgerunners", "o lendário mercenário 96% ciborgue segurança da Arasaka que derrota David", "Adam Smasher"),
        ("Cyberpunk: Edgerunners", "o transtorno mental causado pelo excesso de implantes cibernéticos no corpo", "Ciberpsicose (Cyberpsychosis)"),
        ("Cyberpunk: Edgerunners", "o fixer traidor de quatro olhos cibernéticos que contratava a equipe de Maine e David", "Faraday"),
        ("Dragon Ball Z", "o cientista da Patrulha Vermelha que criou os Androides 16, 17, 18 e Cell", "Dr. Maki Gero (Androide 20)"),
        ("Dragon Ball Z", "o planeta cujos habitantes ensinaram a técnica do Teletransporte para Goku", "Planeta Yardrat"),
        ("Dragon Ball Z", "o guerreiro do Outro Mundo do Oeste que enfrentou Goku na final do Torneio do Outro Mundo", "Paikuhan (Pikkon)"),
        ("Dragon Ball Super", "o guerreiro mortal do Universo 11 cujo poder supera o de um Deus da Destruição", "Jiren, o Cinzento"),
        ("Dragon Ball Super", "o Kaioshin do Universo 10 que roubou o corpo de Goku para executar o Plano Zero Mortais", "Zamasu (Goku Black)"),
        ("Naruto", "o nome verdadeiro do Quarto Hokage, criador do Rasengan e pai de Naruto", "Minato Namikaze"),
        ("Naruto", "a mãe de Naruto que foi a segunda Jinchuuriki da Kyuubi antes dele nascer", "Kushina Uzumaki"),
        ("Naruto Shippuden", "o último estágio proibido dos Oito Portões Internos usado por Might Guy contra Madara", "Oitavo Portão: Portão da Morte (Formação da Noite / Guy Noturno)"),
        ("Naruto Shippuden", "a técnica ocular suprema de espaço-tempo do Mangekyou Sharingan de Obito e Kakashi", "Kamui"),
        ("Naruto Shippuden", "os nomes dos dois irmãos fundadores de Konoha dos clãs Senju e Uchiha", "Hashirama Senju e Madara Uchiha"),
        ("Naruto Shippuden", "a espada lendária sem lâmina de Kisame Hoshigaki que absorve chakra", "Samehada (Pele de Tubarão)"),
        ("One Piece", "os três tipos de Haki existentes no mundo de One Piece", "Haki da Observação, Haki do Armamento e Haki do Rei (Conquistador)"),
        ("One Piece", "a antiga organização de 7 grandes piratas corsários aliados ao Governo Mundial", "Os Shichibukai"),
        ("One Piece", "o nome do cientista mais genial do mundo que trabalhava para a Marinha em Egghead", "Dr. Vegapunk"),
        ("One Piece", "o verdadeiro nome da Akuma no Mi de Luffy revelado no Despertar do Gear 5", "Hito Hito no Mi, Modelo: Nika (Deus do Sol)"),
        ("One Piece", "o carpinteiro mestre de Water 7 que construiu o navio Oro Jackson de Gol D. Roger", "Tom"),
        ("One Piece", "o primeiro imediato da tripulação de Gol D. Roger conhecido como o Rei das Trevas", "Silvers Rayleigh"),
        ("Attack on Titan", "o meio-irmão mais velho de Eren Yeager que possuía o poder do Titã Bestial", "Zeke Yeager"),
        ("Attack on Titan", "o nome da nação continental onde os Eldianos viviam presos na zona de internamento de Liberio", "Marley"),
        ("Attack on Titan", "a maldição que limita o tempo de vida de qualquer portador dos Nove Titãs", "Maldição de Ymir (máximo de 13 anos de vida após herdar o poder)"),
        ("Attack on Titan", "o evento apocalíptico ativado por Eren marchando com milhões de Titãs das Muralhas", "O Estrondo (The Rumbling)"),
        ("Demon Slayer", "o Lua Superior Número 1 de seis olhos que usa a Respiração da Lua", "Kokushibo (Michikatsu Tsugikuni)"),
        ("Demon Slayer", "o Lua Superior Número 3 mestre em artes marciais Soryu que matou Rengoku", "Akaza (Hakuji)"),
        ("Demon Slayer", "o lendário espadachim criador da Respiração do Sol original da Era Sengoku", "Yoriichi Tsugikuni"),
        ("Demon Slayer", "o ferreiro de máscara Hyottoko que fica furioso toda vez que Tanjiro quebra a espada", "Hotaru Haganezuka"),
        ("Jujutsu Kaisen", "o nome da Expansão de Domínio de Ryomen Sukuna que não possui barreira fechada", "Santuário Malevolente (Fukuma Mizushi)"),
        ("Jujutsu Kaisen", "o assassino de feiticeiros do clã Zenin sem nenhuma energia amaldiçoada e pai de Megumi", "Toji Fushiguro (Toji Zenin)"),
        ("Jujutsu Kaisen", "o artefato amaldiçoado de Grau Especial usado para selar Satoru Gojo em Shibuya", "Reino da Prisão (Prison Realm / Gokumonkyo)"),
        ("Jujutsu Kaisen", "o estudante do 3º ano cuja Expansão de Domínio funciona como um jogo de pachinko com jackpot imortal", "Kinji Hakari"),
        ("My Hero Academia", "o antigo inimigo de All Might e vilão mestre por trás da Liga dos Vilões", "All For One"),
        ("My Hero Academia", "o estudante do 3º ano do Big 3 da U.A. que atravessa paredes com a individualidade Permeação", "Mirio Togata (Lemillion)"),
        ("My Hero Academia", "a mestra de All Might e sétima portadora do One For All", "Nana Shimura"),
        ("Death Note", "os dois jovens prodígios criados no orfanato Wammy's House como sucessores de L", "Near (Nate River) e Mello (Mihael Keehl)"),
        ("Death Note", "a agente do FBI noiva de Raye Penber que quase descobriu a identidade de Kira no início", "Naomi Misora"),
        ("Fullmetal Alchemist: Brotherhood", "o criador original dos 7 Homúnculos que nasceu dentro de um frasco de vidro", "Pai (O Homúnculo no Frasco)"),
        ("Fullmetal Alchemist: Brotherhood", "o melhor amigo de Roy Mustang que foi assassinado por Inveja numa cabine telefônica", "Maes Hughes"),
        ("Hunter x Hunter", "os seis tipos de aura do sistema de Nen ensinados por Wing", "Reforço, Emissão, Transformação, Materialização, Manipulação e Especialização"),
        ("Hunter x Hunter", "o presidente da Associação Hunter que enfrentou o Rei Formiga Quimera Meruem", "Isaac Netero"),
        ("Hunter x Hunter", "o jogo de videogame criado por Ging Freecss que na verdade ficava no mundo real", "Greed Island"),
        ("Yu Yu Hakusho", "o ex-Detetive Espiritual que abriu o buraco para o Makai e possui sete personalidades", "Shinobu Sensui"),
        ("Yu Yu Hakusho", "o líder da equipe adversária na final do Torneio das Trevas que controla 100% dos seus músculos", "Toguro Mais Jovem"),
        ("Cavaleiros do Zodíaco", "o golpe supremo proibido por Atena executado por três Cavaleiros de Ouro juntos", "Exclamação de Atena"),
        ("Cavaleiros do Zodíaco", "o sentido além dos seis sentidos que permite aos Cavaleiros atingirem a velocidade da luz", "O Sétimo Sentido"),
        ("Cavaleiros do Zodíaco", "o sentido necessário para descer vivo ao Mundo dos Mortos (Submundo de Hades)", "O Oitavo Sentido (Arayashiki)"),
        ("One Punch Man", "o conquistador alienígena líder dos ladrões da Matéria Escura que enfrentou Saitama na nave", "Lord Boros"),
        ("One Punch Man", "o herói número 1 da Classe S que raramente aparece na Associação de Heróis", "Blast"),
        ("Chainsaw Man", "o Demônio das Armas que matou a família de Aki Hayakawa em poucos segundos", "Demônio da Pistola (Gun Devil)"),
        ("Chainsaw Man", "o caçador de demônios veterano considerado o mais forte da Divisão 4 que treinou Denji e Power", "Kishibe"),
        ("Blue Lock", "o idealizador excêntrico de óculos que criou e comanda todo o projeto Blue Lock", "Jinpachi Ego"),
        ("Blue Lock", "o irmão mais novo prodígio de Sae Itoshi e rival número 1 dentro do Blue Lock", "Rin Itoshi"),
        ("Haikyuu!!", "o capitão e levantador da escola Aoba Johsai conhecido pelo saque viagem devastador", "Toru Oikawa"),
        ("Haikyuu!!", "o capitão canhoto da academia Shiratorizawa considerado um dos três melhores atacantes do Japão", "Wakatoshi Ushijima"),
        ("Code Geass", "o robô mecha Knightmare Frame branco de 7ª geração pilotado por Suzaku Kururugi", "Lancelot"),
        ("Steins;Gate", "o verdadeiro nome da viajante do tempo John Titor que na verdade era filha de Daru", "Suzuha Amane"),
        ("InuYasha", "o vilão principal meio-Youkai nascido da junção de centenas de demônios com o bandido Onigumo", "Naraku"),
        ("InuYasha", "a sacerdotisa guardiã da Joia de Quatro Almas que selou InuYasha na árvore há 50 anos", "Kikyo"),
        ("Evangelion", "as criaturas misteriosas gigantes que atacam Tokyo-3 após o Segundo Impacto", "Anjos (Angels)"),
        ("Cowboy Bebop", "o caçador de recompensas ex-membro do sindicato Red Dragon que pilota a nave Swordfish II", "Spike Spiegel"),
        ("Berserk", "o bando mercenário lendário liderado por Griffith durante a Era de Ouro", "Bando do Falcão"),
        ("Vinland Saga", "o líder astuto do bando viking que matou Thors numa emboscada nas Ilhas Faroé", "Askeladd"),
        ("Dr. Stone", "o primata colegial mais forte que queria destruir as estátuas dos adultos corruptos", "Tsukasa Shishio"),
        ("Mob Psycho 100", "o espírito maligno de bochechas vermelhas que vira parceiro flutuante de Mob", "Covinhas (Ekubo / Dimple)"),
        ("Frieren", "o herói humano do grupo original cuja morte de velhice motivou a nova jornada de Frieren", "Himmel, o Herói"),
        ("Re:Zero", "a Bruxa da Inveja que deu a Subaru a habilidade de Retorno através da Morte", "Satella"),
        ("Overlord", "a supervisora dos Guardiões de Andar de Nazarick que tem asas negras na cintura e ama Ainz", "Albedo"),
        ("The Seven Deadly Sins", "o irmão mais novo de Meliodas que possui o mandamento da Piedade", "Zeldris"),
        ("Fairy Tail", "o mago negro imortal criador dos demônios do livro de Zeref e irmão mais velho de Natsu", "Zeref Dragneel"),
        ("Dandadan", "o espírito de alta velocidade que possuiu Okarun dentro do túnel abandonado", "Vovó Turbo (Turbo Granny)"),
        ("Kaiju No. 8", "o trabalhador de limpeza de monstros de 32 anos que engole um parasita e vira o Kaiju Nº 8", "Kafka Hibino")
    ]

    animes_impossivel_100 = [
        ("Solo Leveling", "o nome verdadeiro do Monarca das Sombras original e ex-Fragmento da Luz Brilhante", "Ashborn"),
        ("Solo Leveling", "o nome do arquiteto demoníaco da Estátua de Deus do Templo Cartenon que criou o Sistema", "Kandiaru"),
        ("Solo Leveling", "o nome do Monarca da Destruição e Rei dos Dragões que é o inimigo final da obra", "Antares"),
        ("Solo Leveling", "o cálice divino usado pelos Governantes para voltar 10 anos no tempo toda vez que a Terra era destruída", "Cálice da Reencarnação"),
        ("Solo Leveling", "o nome da doença do sono causada pela exposição excessiva à mana que afetou a mãe de Jin-Woo", "Sono Eterno (Eternal Slumber)"),
        ("Solo Leveling", "as adagas lendárias criadas a partir da presa do próprio Rei dos Dragões Kamish", "Ira de Kamish (Kamish's Wrath)"),
        ("Bleach: Thousand-Year Blood War", "a letra e o nome do Schrift do Imperador Quincy Yhwach e de Uryu Ishida", "Letra 'A' — The Almighty (Yhwach) e The Antithesis (Uryu)"),
        ("Bleach: Thousand-Year Blood War", "o membro da Guarda Real (Divisão Zero) que batizou tudo o que existe na Soul Society", "Ichibe Hyosube (Monge que chama o Nome Verdadeiro)"),
        ("Bleach: Thousand-Year Blood War", "o Sternritter de letra 'V' (The Visionary) que transforma qualquer imaginação em realidade", "Gremmy Thoumeaux"),
        ("Bleach: Thousand-Year Blood War", "o Sternritter de letra 'M' (The Miracle) que é o próprio coração do Rei das Almas", "Gerard Valkyrie"),
        ("Bleach: Thousand-Year Blood War", "o nome da Bankai de Kisuke Urahara que reconstrói tudo o que toca com costuras", "Kannonbiraki Benihime Aratame"),
        ("Bleach", "o número e nome do Hado de nível 90 sem encantamento favorito de Sosuke Aizen", "Hado #90: Kurohitsugi (Sarcófago Negro)"),
        ("Black Clover", "o nome do demônio sem mana que foi criado pela mãe de Asta (Licita) dentro do grimório", "Liebe"),
        ("Black Clover", "os três irmãos Zogratis da Tríade Negra do Reino de Spade e seus respectivos demônios", "Dante (Lucifero), Vanica (Megicula) e Zenon (Beelzebub)"),
        ("Black Clover", "o verdadeiro nome do primeiro Rei Mago da história que derrotou o demônio ancestral Licht", "Lemiel Silvamillion Clover"),
        ("Black Clover", "o demônio de nível supremo que manipulou elfos e humanos por 500 anos usando Magia de Kotodama (Palavra)", "Zagred"),
        ("Tokyo Revengers", "quem foi o primeiro viajante do tempo original antes de passar o poder para Takemichi", "Shinichiro Sano"),
        ("Tokyo Revengers", "o nome da gangue de Mikey no arco final após a dissolução da Toman e a Guerra das Três Divindades", "Kanto Manji Gang"),
        ("Mashle: Magia e Músculos", "o vilão principal pai de Mash que buscava fundir o coração de seus seis filhos para virar um deus", "Innocent Zero (Cyril Marcus)"),
        ("Mashle: Magia e Músculos", "o filho mais velho de Innocent Zero que usa a espada Caladbolg e domina 100% da força", "Doom"),
        ("Slime (Tensura)", "os nomes das quatro cores dos Demônios Primordiais que passam a servir Rimuru", "Diablo (Noir/Preto), Testarossa (Blanc/Branco), Ultima (Violet/Roxo) e Carrera (Jaune/Amarelo)"),
        ("Slime (Tensura)", "o nome do Dragão Verdadeiro criador do mundo e pai de Milim Nava", "Veldanava"),
        ("Slime (Tensura)", "o nome da entidade consciente Manas que nasce quando Rimuru dá um nome para a habilidade Rafael", "Ciel"),
        ("Cyberpunk: Edgerunners", "a dupla de estúdio japonês e diretor responsável pela criação do anime para a CD Projekt Red", "Studio Trigger, dirigido por Hiroyuki Imaishi"),
        ("Cyberpunk: Edgerunners", "o nome da música de Rosa Walton que virou o hino emocional de David e Lucy na Lua", "I Really Want to Stay at Your House"),
        ("Dragon Ball", "o ano exato em que Akira Toriyama publicou o capítulo 1 do mangá Dragon Ball na Weekly Shonen Jump", "1984"),
        ("Dragon Ball Z", "o nome da mãe biológica Saiyajin de Goku mostrada em Dragon Ball Minus e no filme de Broly", "Gine"),
        ("Dragon Ball Z", "o nome do avô adotivo terráqueo que encontrou Goku bebê na montanha Paozu", "Son Gohan (Avô Gohan)"),
        ("Dragon Ball Super", "o nome do Sumo Sacerdote pai de Whis e Vados e conselheiro de Zeno", "Daishinkan (Grand Priest)"),
        ("Dragon Ball Z", "o poder de luta exato que o rastreador de Raditz marcou ao medir o fazendeiro com espingarda no episódio 1", "Poder de luta igual a 5"),
        ("Naruto", "o nome do Sábio dos Seis Caminhos e do seu irmão gêmeo que foi morar na Lua", "Hagoromo Otsutsuki e Hamura Otsutsuki"),
        ("Naruto", "os nomes verdadeiros das nove Bijuus de 1 a 9 caudas", "Shukaku, Matatabi, Isobu, Son Goku, Kokuo, Saiken, Chomei, Gyuki e Kurama"),
        ("Naruto", "o nome da técnica de teletransporte instantâneo criada por Tobirama Senju e aperfeiçoada por Minato", "Hiraishin no Jutsu (Deus Voador do Trovão)"),
        ("Naruto", "o nome verdadeiro do pai de Kakashi Hatake conhecido como o Canino Branco de Konoha", "Sakumo Hatake"),
        ("One Piece", "o nome do incidente lendário há 38 anos onde Garp e Roger se uniram para derrotar Rocks D. Xebec", "Incidente de God Valley"),
        ("One Piece", "o nome completo do infame pirata capitão dos Piratas Rocks antes da era de Roger", "Rocks D. Xebec"),
        ("One Piece", "os nomes das três Armas Ancestrais capazes de destruir o mundo de One Piece", "Pluton, Poseidon e Uranus"),
        ("One Piece", "o soberano secreto que senta no Trono Vazio em Mary Geoise acima dos Cinco Anciões (Gorosei)", "Imu-sama"),
        ("One Piece", "a ilha final da Grand Line batizada por Gol D. Roger ao ler a história de Joy Boy", "Laugh Tale"),
        ("Attack on Titan", "o nome da fundadora original que entrou na árvore gigante e tocou a criatura da vida há 2.000 anos", "Ymir Fritz"),
        ("Attack on Titan", "o sobrenome da família que governava dentro das muralhas escondendo a linhagem real Fritz", "Família Reiss"),
        ("Attack on Titan", "o nome da cidade natal de Eren, Mikasa e Armin localizada no sul da Muralha Maria", "Distrito de Shiganshina"),
        ("Demon Slayer", "a flor rara que floresce apenas poucos dias por ano à luz do sol e que Muzan procurava à noite", "Lírio da Aranha Azul"),
        ("Demon Slayer", "a idade máxima que um espadachim que desperta a Marca do Caçador consegue viver (com exceção de Yoriichi)", "25 anos de idade"),
        ("Demon Slayer", "o período histórico japonês em que Muzan Kibutsuji foi transformado em Oni há mais de mil anos", "Era Heian"),
        ("Jujutsu Kaisen", "o feiticeiro milenar que troca de corpos transplantando o cérebro e gerou Yuji Itadori", "Kenjaku"),
        ("Jujutsu Kaisen", "o nome completo do Shikigami supremo não domado das Dez Sombras invocado por Megumi em Shibuya", "General Divino Oito Cabos Divergente Sila Mahoraga"),
        ("Jujutsu Kaisen", "o cântico completo recitado por Satoru Gojo para amplificar o Vazio Roxo a 200%", "Nove Cordas, Luz Polarizada, Corvo e Shomyo, a Lacuna entre o Dentro e o Fora"),
        ("My Hero Academia", "o nome completo do primeiro portador do One For All, irmão mais novo do vilão All For One", "Yoichi Shigaraki"),
        ("My Hero Academia", "o verdadeiro nome civil de All Might", "Toshinori Yagi"),
        ("Death Note", "o nome verdadeiro completo de L revelado pelo autor Tsugumi Ohba no volume 13", "L Lawliet"),
        ("Death Note", "o nome do Shinigami que amava Misa Amane e se sacrificou matando L para salvar a vida dela", "Rem"),
        ("Fullmetal Alchemist", "a frase e a data exata gravadas na tampa interna do relógio de bolso de Alquimista Federal de Edward", "Don't Forget 3.Oct.11 (Não esqueça 3 de outubro de 1911)"),
        ("Fullmetal Alchemist", "o nome do país oriental de onde vieram Ling Yao, Lan Fan e a arte da Alkahestria", "Império de Xing"),
        ("Hunter x Hunter", "o nome da habilidade de Nen de Kurapika que só pode ser usada contra a Trupe Fantasma sob pena de morte", "Chain Jail (Corrente de Prisão)"),
        ("Hunter x Hunter", "o jogo de estratégia de tabuleiro do Leste Gorteau no qual Meruem jamais derrotou a cega Komugi", "Gungi"),
        ("Hunter x Hunter", "a irmã mais nova de Killua Zoldyck que abriga a entidade misteriosa capaz de realizar qualquer desejo", "Alluka Zoldyck (Nanika)"),
        ("Yu Yu Hakusho", "o nome do pai ancestral Youkai de Yusuke Urameshi que era um dos três reis do Makai", "Raizen"),
        ("Cavaleiros do Zodíaco", "o nome do autor do mangá original Saint Seiya publicado em 1986", "Masami Kurumada"),
        ("Cavaleiros do Zodíaco", "os dois sobreviventes da Guerra Santa anterior de 1743 que se tornaram o Mestre Ancião e o Grande Mestre", "Dohko de Libra e Shion de Áries"),
        ("One Punch Man", "o pseudônimo do autor original que criou a webcomic One Punch Man e Mob Psycho 100", "ONE (e redesenhado por Yusuke Murata)"),
        ("Chainsaw Man", "o autor do mangá Chainsaw Man, também criador de Fire Punch e Look Back", "Tatsuki Fujimoto"),
        ("Chainsaw Man", "o Demônio Primordial que aparece com uma fila de astronautas cortados ao meio na escuridão do Inferno", "Demônio da Escuridão (Darkness Devil)"),
        ("Blue Lock", "o atacante francês número 1 do mundo no qual Jinpachi Ego se inspirou e que joga no Bastard München", "Noel Noa"),
        ("Haikyuu!!", "o time profissional da Divisão 1 da V.League do Japão onde Hinata entra após treinar vôlei de praia no Brasil", "MSBY Black Jackals"),
        ("Evangelion", "de quem era a alma que habitava dentro do núcleo da Unidade Evangelion-01 de Shinji", "Yui Ikari (a mãe de Shinji)"),
        ("Evangelion", "o significado literal da palavra alemã NERV e seu lema completo", "Nervo (Deus está em seu céu, tudo está bem com o mundo)"),
        ("Code Geass", "o nome do plano final de Lelouch e Suzaku para concentrar todo o ódio do mundo nele mesmo", "Zero Requiem"),
        ("Steins;Gate", "o número exato da divergência da linha de mundo Steins Gate onde Kurisu e Mayuri sobrevivem", "1.048596%"),
        ("Berserk", "o nome que Griffith recebe ao renascer como o quinto membro da Mão de Deus durante o Eclipse", "Femto, o Falcão da Escuridão"),
        ("Berserk", "o nome do autor lendário de Berserk que dedicou mais de 30 anos de vida à obra", "Kentaro Miura"),
        ("Monster", "o nome do livro infantil ilustrado tcheco usado no seminário 511 Kinderheim que influenciou Johan Liebert", "O Monstro Sem Nome (de Emil Sebe / Franz Bonaparta)"),
        ("Vinland Saga", "o navegador nórdico histórico que falou para Thorfinn sobre a terra pacífica de Vinland", "Leif Erikson"),
        ("Dr. Stone", "a verdadeira natureza do 'Why-Man' na Lua que enviava o código Morse WHY", "Uma colônia de dispositivos mecânicos parasitas inteligentes (Medusas)"),
        ("Frieren", "a Grande Maga elfa da era mítica líder da Associação Mágica Continental e mestra de Flamme", "Serie"),
        ("Re:Zero", "o nome do Grande Espírito do Fogo na forma de gatinho cinza que acompanha Emilia", "Puck"),
        ("Overlord", "o nome do jogo DMMORPG de realidade virtual do ano 2138 que deu origem ao mundo de Ainz", "YGGDRASIL"),
        ("InuYasha", "o nome da autora consagrada de InuYasha, Ranma 1/2 e Urusei Yatsura", "Rumiko Takahashi"),
        ("Fairy Tail", "o verdadeiro significado do acrônimo E.N.D., o demônio mais forte do livro de Zeref", "Etherious Natsu Dragneel"),
        ("The Seven Deadly Sins", "a entidade suprema primordial que criou a Divindade Suprema, o Rei dos Demônios e a Árvore Sagrada", "O Caos"),
        ("Cowboy Bebop", "a frase final icônica que aparece no canto da tela no encerramento do último episódio", "You're Gonna Carry That Weight (Você vai carregar esse peso)"),
        ("Akira", "o ano exato em que se passa a história de Kaneda e Tetsuo em Neo-Tokyo", "Ano de 2019"),
        ("Ghost in the Shell", "o nome da Major ciborgue protagonista da Seção 9 de Segurança Pública", "Major Motoko Kusanagi"),
        ("Hellsing Ultimate", "a identidade histórica real do vampiro supremo Alucard que serve a Integra Hellsing", "Conde Drácula (Vlad, o Empalador)"),
        ("JoJo's Bizarre Adventure", "o nome do Stand de DIO na Parte 3 capaz de parar o tempo por alguns segundos", "The World (Za Warudo)"),
        ("JoJo's Bizarre Adventure", "o Stand evoluído de Giorno Giovanna na Parte 5 que anula qualquer ação de volta ao zero", "Gold Experience Requiem"),
        ("Gurren Lagann", "a frase clássica de Kamina para Simon sobre a sua broca", "A sua broca é a broca que vai perfurar os céus!"),
        ("Kill la Kill", "o nome da espada em forma de metade de tesoura vermelha empunhada por Ryuko Matoi", "Lâmina Decapitadora (Scissor Blade)"),
        ("Fate/stay night", "a verdadeira identidade histórica lendária da serva da classe Saber invocada por Shirou Emiya", "Rei Artur Pendragon (Artoria Pendragon)"),
        ("Made in Abyss", "a maldição da 6ª Camada do Abismo que atinge quem tenta subir de volta", "Perda da humanidade (transformação em Narehate) ou morte"),
        ("The Promised Neverland", "os números de identificação tatuados no pescoço de Emma, Norman e Ray em Grace Field", "63194 (Emma), 22194 (Norman) e 81194 (Ray)"),
        ("Tokyo Ghoul", "a conta matemática regressiva que Jason obrigava Kaneki a repetir durante a tortura", "1000 menos 7 (993, 986, 979...)"),
        ("Parasyte (Kiseijuu)", "o nome do parasita alienígena que se alojou na mão direita de Shinichi Izumi", "Migi (que significa Direita em japonês)"),
        ("Assassination Classroom", "a velocidade máxima em Mach que o professor polvo amarelo Koro-sensei consegue atingir", "Mach 20"),
        ("Haikyuu!!", "a frase escrita na faixa preta da torcida da escola Inarizaki dos irmãos Miya", "Não precisamos das memórias de ontem"),
        ("Slam Dunk", "o número da camisa vermelha do time Shohoku usada pelo protagonista ruivo Hanamichi Sakuragi", "Camisa número 10"),
        ("Hajime no Ippo", "o golpe assinatura de Ippo Makunouchi que gira o tronco em forma de oito infinito", "Dempsey Roll"),
        ("Baki", "a marca demoníaca que aparece nos músculos das costas dos membros puros da família Hanma", "As Costas de Ogro (Demon Back)"),
        ("Yu-Gi-Oh!", "o nome verdadeiro do Faraó do Antigo Egito cuja alma habitava o Enigma do Milênio", "Faraó Atem"),
        ("Dragon Ball Z", "os nomes verdadeiros humanos dos Androides gêmeos Nº 17 e Nº 18 antes de serem modificados", "Lapis (Nº 17) e Lazuli (Nº 18)")
    ]

    # DEMAIS TEMAS (IGREJA, HERÓIS, DESENHOS, FRUTAS, COMIDAS, NOVELAS, FILMES, TRABALHOS)
    igreja_facil = [
        ("o Natal", "o grande acontecimento celebrado em 25 de dezembro", "Nascimento de Jesus em Belém"),
        ("a Páscoa", "o acontecimento central da fé cristã", "Ressurreição de Jesus Cristo"),
        ("São José", "a sua missão na Sagrada Família", "Pai adotivo de Jesus e Esposo de Maria"),
        ("Maria Santíssima", "o seu papel na história da salvação", "Mãe de Jesus Cristo"),
        ("o Batismo", "a sua importância na caminhada cristã", "Primeiro Sacramento da vida cristã"),
        ("a Arca de Noé", "o motivo pelo qual Deus pediu sua construção", "Salvar a família de Noé e os animais do Dilúvio"),
        ("Davi e Golias", "o objeto que o jovem Davi usou para vencer o gigante", "Uma funda e uma pedra"),
        ("Jonas", "o que aconteceu com o profeta no mar", "Passou três dias no ventre de um grande peixe"),
        ("o Pai-Nosso", "a importância desta oração", "A oração que o próprio Jesus ensinou aos Apóstolos"),
        ("São Pedro", "a missão que ele recebeu diretamente de Jesus", "Primeiro Papa da Igreja"),
        ("São Francisco de Assis", "o título pelo qual é conhecido mundialmente", "Padroeiro dos Animais e da Ecologia"),
        ("Nossa Senhora Aparecida", "o título que ela possui no nosso país", "Rainha e Padroeira do Brasil"),
        ("a Bíblia Sagrada", "as duas grandes partes em que ela se divide", "Antigo Testamento e Novo Testamento"),
        ("Adão e Eva", "o jardim onde viviam no início da Criação", "Jardim do Éden"),
        ("Moisés", "o milagre famoso ocorrido na saída do Egito", "Abertura do Mar Vermelho"),
        ("os Dez Mandamentos", "onde foram entregues por Deus a Moisés", "Em duas tábuas de pedra no Monte Sinai"),
        ("Judas Iscariotes", "o valor pelo qual entregou Jesus", "Trinta moedas de prata"),
        ("a Santa Missa", "o que acontece com o pão e o vinho no altar", "Tornam-se o Corpo e o Sangue de Cristo"),
        ("o Domingo de Ramos", "o que recordamos nesta celebração", "A entrada triunfal de Jesus em Jerusalém"),
        ("a Sexta-Feira Santa", "o que a Igreja recorda em silêncio e oração", "A Paixão e Morte de Jesus na Cruz")
    ]
    igreja_normal = [
        ("o Dogma da Imaculada Conceição", "o significado desta verdade de fé", "Maria foi concebida sem a mancha do pecado original"),
        ("Nossa Senhora de Fátima", "os nomes dos três pastorinhos videntes em Portugal", "Lúcia, Francisco e Jacinta"),
        ("Nossa Senhora de Lourdes", "a jovem santa para quem ela apareceu na França", "Santa Bernadette Soubirous"),
        ("Pentecostes", "o evento celebrado 50 dias após a Páscoa", "Descida do Espírito Santo em línguas de fogo"),
        ("São Paulo Apóstolo", "o nome que ele tinha antes da conversão na estrada de Damasco", "Saulo de Tarso"),
        ("os Sete Sacramentos", "os três sacramentos da Iniciação Cristã", "Batismo, Eucaristia e Crisma"),
        ("o Santo Rosário", "os quatro grupos de mistérios meditados", "Gozosos, Luminosos, Dolorosos e Gloriosos"),
        ("os quatro Evangelistas", "os nomes dos autores dos Evangelhos", "Mateus, Marcos, Lucas e João"),
        ("o livro do Gênesis", "a posição que ocupa na Sagrada Escritura", "Primeiro livro da Bíblia"),
        ("o livro do Apocalipse", "a posição que ocupa no Novo Testamento", "Último livro da Bíblia"),
        ("Santa Rita de Cássia", "a devoção popular pela qual é invocada", "Santa das Causas Impossíveis"),
        ("Santo Antônio de Pádua", "o título popular além de Doutor da Igreja", "Santo Casamenteiro e Padroeiro dos Pobres"),
        ("São João Batista", "o parentesco que tinha com Jesus e sua missão", "Primo de Jesus que batizava no Rio Jordão"),
        ("a Quaresma", "o dia em que se inicia este tempo penitencial", "Quarta-Feira de Cinzas"),
        ("o Advento", "a cor litúrgica utilizada nas quatro semanas de preparação", "Roxo (e Rosa no Domingo Gaudete)"),
        ("as Bodas de Caná", "o que Jesus realizou nesta festa de casamento", "Seu primeiro milagre, transformando água em vinho"),
        ("São Miguel, São Gabriel e São Rafael", "a categoria angélica a que pertencem", "Os três Arcanjos citados na Bíblia"),
        ("São João Paulo II", "o país de origem deste santo Papa", "Polônia"),
        ("Santa Luzia", "a proteção pela qual é invocada pelos fiéis", "Protetora dos olhos e da visão"),
        ("São Cristóvão", "a classe de trabalhadores de quem é padroeiro", "Padroeiro dos motoristas e viajantes")
    ]
    igreja_hard = [
        ("o Dogma da Imaculada Conceição", "o Papa e o ano exato da proclamação solene", "Papa Pio IX em 8 de dezembro de 1854"),
        ("o Dogma da Assunção de Maria", "o Papa que o proclamou em 1950", "Papa Pio XII"),
        ("Nossa Senhora Aparecida", "os nomes dos três pescadores que encontraram a imagem em 1717", "Domingos Garcia, Filipe Pedroso e João Alves"),
        ("Nossa Senhora de Guadalupe", "o indígena vidente no México em 1531", "São Juan Diego Cuauhtlatoatzin"),
        ("São Tomás de Aquino", "a sua maior obra teológica e filosófica", "Suma Teológica"),
        ("Santo Agostinho de Hipona", "a santa mãe que rezou anos por sua conversão", "Santa Mônica"),
        ("São Jerônimo", "a famosa tradução da Bíblia para o latim que ele realizou", "A Vulgata Latina"),
        ("o Concílio de Niceia em 325", "a heresia que foi combatida dando origem ao Credo", "O Arianismo (que negava a divindade de Cristo)"),
        ("Santa Teresinha do Menino Jesus", "o mosteiro carmelita na França onde viveu", "Carmelo de Lisieux"),
        ("São Padre Pio de Pietrelcina", "o fenômeno místico que carregou no corpo por 50 anos", "Os Estigmas da Paixão de Cristo"),
        ("a Transubstanciação", "o significado teológico deste termo na Eucaristia", "Conversão de toda a substância do pão e do vinho no Corpo e Sangue de Cristo"),
        ("o livro dos Atos dos Apóstolos", "o autor sagrado que o escreveu como continuação do seu Evangelho", "São Lucas Evangelista"),
        ("São Maximiliano Maria Kolbe", "o ato heroico que realizou no campo de Auschwitz", "Deu a própria vida no lugar de um pai de família"),
        ("Santa Catarina de Sena", "o grande feito histórico em que convenceu o Papa no século XIV", "O retorno do Papado de Avignon para Roma"),
        ("São Bento de Núrsia", "o lema famoso da Regra Beneditina", "Ora et Labora (Reza e Trabalha)"),
        ("São Lourenço", "o seu cargo na Igreja de Roma antes do martírio na grelha", "Um dos sete diáconos de Roma"),
        ("Santo Estêvão", "a sua marca na história do cristianismo primitivo", "Primeiro mártir (Protomártir) da Igreja"),
        ("o Concílio Vaticano II", "o Papa que o convocou em 1962 e o Papa que o encerrou em 1965", "São João XXIII e São Paulo VI"),
        ("São Francisco Xavier", "a região do mundo onde ficou conhecido como grande missionário", "Ásia (Índia e Japão)"),
        ("Santa Teresa d'Ávila", "o santo espanhol com quem reformou a Ordem do Carmo", "São João da Cruz")
    ]
    igreja_impossivel = [
        ("a Bula Ineffabilis Deus", "o conteúdo deste documento papal de 1854", "Documento oficial que definiu o Dogma da Imaculada Conceição"),
        ("a Constituição Munificentissimus Deus", "o dogma mariano definido por Pio XII neste texto de 1950", "Dogma da Assunção de Nossa Senhora ao Céu em corpo e alma"),
        ("o Concílio de Éfeso no ano 431", "o título grego proclamado para Maria contra Nestório", "Theotokos (Mãe de Deus)"),
        ("a Didaqué", "a importância deste documento cristão do século I", "O Catecismo mais antigo conhecido, chamado Doutrina dos Doze Apóstolos"),
        ("São Policarpo de Esmirna", "de qual Apóstolo de Jesus ele foi discípulo direto", "Discípulo direto do Apóstolo São João"),
        ("Santo Irineu de Lyon", "a obra famosa que escreveu no século II contra o gnosticismo", "Adversus Haereses (Contra as Heresias)"),
        ("o Código de Direito Canônico atual", "o ano em que foi promulgado por São João Paulo II", "Promulgado em 25 de janeiro de 1983"),
        ("a Encíclica Rerum Novarum de 1891", "o Papa autor e o tema central deste marco histórico", "Papa Leão XIII, inaugurando a Doutrina Social da Igreja"),
        ("a Encíclica Fides et Ratio", "as duas asas que elevam o espírito humano à verdade segundo João Paulo II", "A Fé e a Razão"),
        ("as Doutoras da Igreja", "as três primeiras mulheres proclamadas Doutoras da Igreja", "Santa Teresa d'Ávila, Santa Catarina de Sena e Santa Teresinha de Lisieux"),
        ("o Concílio de Calcedônia no ano 451", "a definição cristológica central estabelecida pelos bispos", "Cristo é uma só Pessoa em duas naturezas: verdadeiro Deus e verdadeiro Homem"),
        ("o papiro Rylands P52", "a importância arqueológica deste fragmento bíblico", "O fragmento mais antigo do Novo Testamento (Evangelho de São João)"),
        ("a Oração Eucarística II", "o santo teólogo do século III em cujos escritos ela se baseia", "Santo Hipólito de Roma"),
        ("o Triságio Angélico (Santo, Santo, Santo)", "o livro e capítulo do Antigo Testamento onde os Serafins o proclamam", "Profeta Isaías, capítulo 6"),
        ("Melquisedeque no livro do Gênesis", "a oferta que este rei de Salém trouxe prefigurando a Eucaristia", "Pão e Vinho, por ser sacerdote do Deus Altíssimo"),
        ("o Murmúrio de Elias no Monte Horeb", "onde Deus se manifestou ao profeta em 1 Reis 19", "Na brisa suave e silenciosa, e não no vento forte nem no terremoto"),
        ("o Papa São Silvestre I", "o imperador romano que governava durante o Édito de Milão em 313", "Imperador Constantino Magno"),
        ("São Cirilo de Jerusalém", "as famosas instruções que escreveu no século IV para os recém-batizados", "As Catequeses Mistagógicas"),
        ("a Cruz de São Damião", "o pedido que o Crucificado fez a São Francisco de Assis em 1205", "Francisco, vai e reconstrói a minha Igreja"),
        ("o Tratado da Verdadeira Devoção à Santíssima Virgem", "o santo francês que escreveu esta obra-prima mariana", "São Luís Maria Grignion de Montfort")
    ]

    herois_facil = [
        ("o Homem-Aranha", "o animal que picou Peter Parker e lhe deu superpoderes", "Uma aranha radioativa"),
        ("o Batman", "a cidade sombria que ele jurou proteger do crime", "Gotham City"),
        ("o Superman", "o símbolo famoso estampado no peito do seu uniforme azul", "Um grande S vermelho e amarelo"),
        ("o Hulk", "a cor da pele do herói quando Bruce Banner fica furioso", "Verde"),
        ("o Homem de Ferro", "o que Tony Stark veste para voar e combater os vilões", "Uma armadura tecnológica de metal"),
        ("o Capitão América", "a arma de defesa que ele carrega no braço com uma estrela", "Um escudo redondo indestrutível"),
        ("o deus Thor", "o elemento da natureza que ele controla com seu martelo", "Raios e trovões"),
        ("a Mulher-Maravilha", "o objeto dourado que obriga qualquer pessoa a dizer a verdade", "Laço da Verdade"),
        ("o Flash", "o superpoder principal que o torna famoso no mundo inteiro", "Supervelocidade para correr na velocidade da luz"),
        ("o Aquaman", "a habilidade especial que ele possui nos oceanos", "Respirar debaixo d'água e comandar criaturas marinhas"),
        ("o Wolverine", "o que sai das mãos dele quando vai para a batalha", "Três garras afiadas de metal em cada mão"),
        ("o Batman", "o veículo famoso todo preto e cheio de armas que ele dirige", "Batmóvel"),
        ("o Homem-Aranha", "a frase famosa que seu Tio Ben lhe ensinou sobre responsabilidade", "Com grandes poderes vêm grandes responsabilidades"),
        ("o Superman", "a pedra verde espacial que tira todas as forças dele", "Kryptonita"),
        ("o parceiro do Batman", "o jovem ajudante acrobata que luta ao lado do Homem-Morcego", "Robin"),
        ("o vilão Coringa", "a aparência característica do maior inimigo do Batman", "Cabelo verde, rosto branco e um sorriso de palhaço"),
        ("os Vingadores", "a equipe de heróis formada por Homem de Ferro, Thor, Hulk e Capitão América", "Os Heróis Mais Poderosos da Terra da Marvel"),
        ("a Liga da Justiça", "a equipe formada por Superman, Batman, Mulher-Maravilha e Flash", "A principal equipe de super-heróis da DC"),
        ("o Pantera Negra", "o traje escuro com garras que o rei de Wakanda utiliza", "Uniforme da Pantera Negra"),
        ("o Groot", "a única frase que essa árvore alienígena dos Guardiões da Galáxia fala", "Eu sou o Groot!")
    ]
    herois_normal = [
        ("o Homem de Ferro", "a identidade secreta bilionária do herói na Marvel", "Tony Stark"),
        ("o Batman", "o nome do mordomo fiel que cuida de Bruce Wayne na Mansão Wayne", "Alfred Pennyworth"),
        ("o Homem-Aranha", "o nome do jornal onde Peter Parker trabalhava tirando fotos", "Clarim Diário, chefiado por J. Jonah Jameson"),
        ("o Superman", "o planeta natal que explodiu quando ele ainda era um bebê", "Planeta Krypton"),
        ("o deus Thor", "o nome do seu martelo mágico e do seu irmão adotivo trapaceiro", "Mjolnir e Loki"),
        ("o Pantera Negra", "o metal raríssimo que caiu em Wakanda num meteoro", "Vibranium"),
        ("o vilão Thanos", "quantas Joias do Infinito existem para completar a Manopla", "6 Joias: Espaço, Mente, Realidade, Poder, Tempo e Alma"),
        ("os X-Men", "o líder telepata cadeirante e seu rival que controla o magnetismo", "Professor Charles Xavier e Magneto"),
        ("a série The Boys", "o líder arrogante dos Sete que tem poderes parecidos com o Superman", "Capitão Pátria (Homelander)"),
        ("a animação Invencível (Invincible)", "o nome do pai alienígena Viltrumita de Mark Grayson", "Omni-Man (Nolan Grayson)"),
        ("o Doutor Estranho", "a profissão que Stephen Strange exercia antes de sofrer o acidente nas mãos", "Neurocirurgião renomado"),
        ("a Viúva Negra e o Gavião Arqueiro", "os nomes verdadeiros dessa dupla de agentes da S.H.I.E.L.D.", "Natasha Romanoff e Clint Barton"),
        ("o Deadpool", "o nome verdadeiro do mercenário tagarela que se regenera de tudo", "Wade Wilson"),
        ("o Quarteto Fantástico", "os quatro integrantes da família de heróis", "Sr. Fantástico, Mulher Invisível, Tocha Humana e o Coisa"),
        ("o Lanterna Verde", "o piloto de testes que foi o primeiro humano da Tropa dos Lanternas Verdes", "Hal Jordan"),
        ("o Demolidor (Daredevil)", "a profissão que o herói cego Matt Murdock exerce durante o dia", "Advogado em Hell's Kitchen"),
        ("o Homem-Formiga", "o ex-ladrão carismático que assume o traje nos filmes da Marvel", "Scott Lang"),
        ("o Feiticeiro Shazam", "o nome do garoto órfão que grita a palavra mágica para virar adulto", "Billy Batson"),
        ("os Guardiões da Galáxia", "o guaxinim geneticamente modificado mestre em armas e tecnologia", "Rocket Raccoon"),
        ("a Feiticeira Escarlate", "o nome verdadeiro da heroína Wanda e do androide por quem ela se apaixona", "Wanda Maximoff e Visão")
    ]
    herois_hard = [
        ("o Soldado Invernal", "o nome completo do melhor amigo de infância de Steve Rogers", "James Buchanan 'Bucky' Barnes"),
        ("o Batman", "os nomes dos quatro primeiros jovens que assumiram o manto de Robin nos quadrinhos", "Dick Grayson, Jason Todd, Tim Drake e Damian Wayne"),
        ("a saga Guerra Civil da Marvel", "o motivo da divisão entre o time do Capitão América e o time do Homem de Ferro", "A Lei de Registro de Super-Humanos após a tragédia em Stamford"),
        ("a série The Boys", "a substância química azul criada pela Vought que dá superpoderes aos bebês", "Composto V"),
        ("Invencível (Invincible)", "a regra brutal do Império Viltrumita revelada por Omni-Man", "Conquistar planetas para expandir o império onde apenas os fortes sobrevivem"),
        ("o Wolverine", "o nome verdadeiro de nascimento de Logan no século XIX no Canadá", "James Howlett"),
        ("Vingadores: Guerra Infinita", "o machado real forjado em Nidavellir para Thor enfrentar Thanos", "Rompe-Tormentas (Stormbreaker)"),
        ("a Batgirl / Oráculo", "o vilão que atirou em Barbara Gordon na obra 'A Piada Mortal'", "O Coringa"),
        ("a queda do Morcego", "o vilão estrategista movido pela droga Veneno que quebrou a coluna do Batman", "Bane"),
        ("a morte do Superman", "o monstro pré-histórico kryptoniano que matou o Superman nos quadrinhos de 1992", "Apocalipse (Doomsday)"),
        ("a saga Ponto de Ignição (Flashpoint)", "quem se torna o Batman nessa linha do tempo alterada por Barry Allen", "Thomas Wayne (o pai de Bruce Wayne)"),
        ("Watchmen", "o físico nuclear azul quase onipotente criado em um acidente de laboratório", "Doutor Manhattan (Jon Osterman)"),
        ("o Homem-Aranha", "o primeiro grande amor de Peter Parker que morreu na ponte George Washington", "Gwen Stacy, jogada pelo Duende Verde"),
        ("o simbionte Venom", "o jornalista rival de Peter Parker que se tornou o primeiro hospedeiro famoso do Venom", "Eddie Brock"),
        ("o Cavaleiro da Lua (Moon Knight)", "o deus egípcio da Lua de quem Marc Spector se torna o avatar", "Khonshu"),
        ("o Justiceiro (Punisher)", "o nome verdadeiro do ex-fuzileiro naval que combate o crime sem piedade", "Frank Castle"),
        ("o Surfista Prateado", "o devorador de mundos gigante de quem Norrin Radd era arauto", "Galactus"),
        ("o Doutor Destino (Doctor Doom)", "o país fictício do leste europeu governado com mão de ferro por Victor Von Doom", "Latvéria"),
        ("a inteligência artificial Ultron", "quem criou o robô Ultron originalmente nos quadrinhos clássicos da Marvel", "Hank Pym (o Homem-Formiga original)"),
        ("a Tropa dos Lanternas", "as emoções que alimentam os anéis Amarelo, Vermelho e Azul", "Medo (Amarelo/Sinestro), Ira (Vermelho/Atrocitus) e Esperança (Azul)")
    ]
    herois_impossivel = [
        ("a estreia do Superman", "a revista e o ano exato em que o primeiro super-herói da história apareceu", "Action Comics #1, publicada em junho de 1938"),
        ("a estreia do Batman", "a revista de 1939 e a dupla de criadores (incluindo o coautor injustiçado por décadas)", "Detective Comics #27, criado por Bob Kane e Bill Finger"),
        ("a estreia do Homem-Aranha", "a revista antológica de 1962 onde Stan Lee e Steve Ditko lançaram o herói", "Amazing Fantasy #15"),
        ("o Universo Principal da Marvel", "o número oficial da Terra principal onde ocorrem as histórias canônicas dos quadrinhos", "Terra-616"),
        ("o nome de batismo kryptoniano", "o nome original do Superman dado por seu pai biológico Jor-El e sua mãe Lara", "Kal-El"),
        ("o mordomo do Homem de Ferro", "o nome do mordomo humano da família Stark que inspirou a sigla J.A.R.V.I.S. e o Visão", "Edwin Jarvis"),
        ("o segundo Robin (Jason Todd)", "como a DC Comics decidiu o destino de Jason Todd em 1988 na saga 'Morte em Família'", "Através de uma votação por telefone feita pelos próprios leitores"),
        ("a primeira aparição do Wolverine", "em qual revista de outro herói o Wolverine estreou em 1974 antes de entrar nos X-Men", "The Incredible Hulk #180 e #181"),
        ("o criador de Invencível (Invincible)", "o roteirista que criou tanto 'Invincible' quanto 'The Walking Dead'", "Robert Kirkman (com arte de Cory Walker e Ryan Ottley)"),
        ("os criadores de The Boys", "o roteirista e o desenhista dos quadrinhos originais lançados em 2006", "Garth Ennis e Darick Robertson"),
        ("Watchmen", "o roteirista lendário britânico autor de Watchmen, V de Vingança e A Piada Mortal", "Alan Moore"),
        ("O Cavaleiro das Trevas (1986)", "o autor e desenhista que revolucionou o Batman e o Demolidor nos anos 80", "Frank Miller"),
        ("o Rei dos Quadrinhos", "o lendário desenhista cocriador do Capitão América, Quarteto Fantástico, X-Men, Hulk e Novos Deuses", "Jack Kirby"),
        ("a Equação Antivida", "o tirano governante do planeta Apokolips obcecado por essa equação na DC", "Darkseid (Uxas)"),
        ("Guerras Secretas (1984)", "a entidade cósmica que sequestrou heróis e vilões para lutarem no Mundo Bélico", "Beyonder"),
        ("Crise nas Infinitas Terras (1985)", "o vilão cósmico devorador de universos que destruiu o multiverso original da DC", "Anti-Monitor"),
        ("o escudo do Capitão América nos quadrinhos", "a liga metálica exata do escudo redondo nos quadrinhos (diferente do cinema)", "Uma liga única de Vibranium com Ferro/Aço (Proto-Adamantium)"),
        ("a inscrição no martelo Mjolnir", "o encantamento exato gravado por Odin na lateral do martelo de Thor", "Aquele que empunhar este martelo, se for digno, possuirá o poder de Thor"),
        ("o nome verdadeiro do Coringa", "o pseudônimo de comediante fracassado sugerido em 'A Piada Mortal' e o filme de 1989", "Jack Napier / Capuz Vermelho"),
        ("a entidade suprema da Marvel", "o ser onipotente que está acima do Tribunal Vivo e de todas as entidades cósmicas", "The One Above All (Aquele Acima de Tudo)")
    ]

    desenhos_facil = [
        ("Bob Esponja", "o formato da casa onde ele mora no fundo do mar", "Um abacaxi"),
        ("Patrick Estrela", "o seu parentesco e amizade com Bob Esponja", "Uma estrela-do-mar rosa e melhor amigo do Bob Esponja"),
        ("Scooby-Doo", "o seu melhor amigo humano que está sempre com fome", "Salsicha"),
        ("Tom e Jerry", "os animais que protagonizam essa dupla clássica", "Um gato e um rato"),
        ("Pica-Pau", "a cor das penas da cabeça desse pássaro famoso", "Vermelha"),
        ("Pernalonga", "o vegetal que ele está sempre mastigando", "Uma cenoura"),
        ("Turma da Mônica", "o personagem que troca a letra R pela letra L ao falar", "Cebolinha"),
        ("Cascão", "aquilo de que ele foge de todas as maneiras possíveis", "Água e banho"),
        ("Magali", "a característica mais famosa da personagem e sua fruta favorita", "Muito comilona e apaixonada por melancia"),
        ("Mickey Mouse", "o nome do seu cachorro de estimação", "Pluto"),
        ("Pato Donald", "os nomes dos seus três sobrinhos trigêmeos", "Huguinho, Zezinho e Luisinho"),
        ("Popeye", "o alimento que ele come para ficar superforte na hora", "Espinafre"),
        ("Os Simpsons", "a cor da pele dos personagens dessa família", "Amarela"),
        ("Peppa Pig", "o nome do irmãozinho mais novo dela que adora dinossauros", "George"),
        ("Patrulha Canina", "o garoto líder da equipe de filhotes socorristas", "Ryder"),
        ("Dora, a Aventureira", "o macaquinho de botas vermelhas que a acompanha", "Botas"),
        ("As Meninas Superpoderosas", "os nomes das três irmãs heroínas", "Florzinha, Lindinha e Docinho"),
        ("Ben 10", "o objeto que ele usa no pulso para virar alienígenas", "Um relógio alienígena chamado Omnitrix"),
        ("Piu-Piu e Frajola", "a frase famosa que o passarinho amarelo sempre diz", "Eu acho que vi um gatinho!"),
        ("Papa-Léguas", "o vilão que tenta capturá-lo no deserto usando produtos ACME", "Wile E. Coyote (Coioite)")
    ]
    desenhos_normal = [
        ("Bob Esponja", "o restaurante onde ele trabalha fazendo hambúrgueres de siri", "Siri Cascudo, do chefe Seu Siriguejo"),
        ("Scooby-Doo", "os cinco integrantes da Mistério S/A", "Fred, Daphne, Velma, Salsicha e Scooby-Doo"),
        ("Os Flintstones", "o melhor amigo vizinho de Fred e sua esposa", "Barney e Betty Rubble"),
        ("Os Jetsons", "a época em que vive a família de George Jetson", "No futuro espacial cheio de robôs e carros voadores"),
        ("Os Padrinhos Mágicos", "os nomes das duas fadas padrinhos de Timmy Turner", "Cosmo e Wanda"),
        ("Hora de Aventura", "os nomes do garoto humano e do cão mágico amarelo", "Finn e Jake"),
        ("Apenas um Show (Regular Show)", "as espécies dos amigos protagonistas Mordecai e Rigby", "Um gaio-azul e um guaxinim"),
        ("O Incrível Mundo de Gumball", "o irmão adotivo de Gumball que era um peixinho dourado com pernas", "Darwin Watterson"),
        ("Gravity Falls", "o tio-avô dono da Cabana do Mistério", "Tio-avô Stan (Stanley Pines)"),
        ("Avatar: A Lenda de Aang", "a tribo de origem de Katara e Sokka", "Tribo da Água do Sul"),
        ("Phineas e Ferb", "a irmã mais velha que tenta dedurá-los para a mãe todo dia", "Candace Flynn"),
        ("Coragem, o Cão Covarde", "os nomes dos dois idosos donos do Coragem", "Muriel e Eustácio Resmungão"),
        ("O Laboratório de Dexter", "o rival de Dexter que tem uma risada estridente", "Mandark"),
        ("Jovens Titãs", "os cinco heróis da torre em formato de T", "Robin, Estelar, Mutano, Ciborgue e Ravena"),
        ("As Três Espiãs Demais", "o chefe da organização WOOHP que envia as missões", "Jerry"),
        ("Caverna do Dragão", "o vilão de um chifre só que persegue os jovens no Reino", "Vingador"),
        ("Corrida Maluca", "a motorista charmosa do Carrinho Pra Frente (número 5)", "Penélope Charmosa"),
        ("Manda-Chuva", "o guarda policial que tenta colocar ordem no beco", "Guarda Belo"),
        ("Johnny Bravo", "a característica física e personalidade do protagonista", "Topete loiro gigante, óculos escuros e músculos"),
        ("Du, Dudu e Edu", "o doce gigante que eles fazem de tudo para conseguir comprar", "Bala de caramelo gigante")
    ]
    desenhos_hard = [
        ("Bob Esponja", "o nome do caracol de estimação dele que mia como gato", "Gary"),
        ("Bob Esponja", "o nome completo do vilão microscópico dono do Balde de Lixo", "Sheldon J. Plankton"),
        ("Ben 10 Clássico", "quantos alienígenas iniciais vinham no Omnitrix no 1º episódio", "10 alienígenas (Chama, Quatro Braços, XLR8, Diamante, etc.)"),
        ("Avatar: A Lenda de Aang", "o nome do bisão voador de seis patas e do lêmure de Aang", "Appa e Momo"),
        ("Gravity Falls", "o nome do demônio triangular amarelo de um olho só e cartola", "Bill Cipher"),
        ("Hora de Aventura", "o nome verdadeiro do Rei Gelado antes de colocar a coroa mágica", "Simon Petrikov"),
        ("Steven Universo", "as três Crystal Gems que criaram o jovem Steven", "Garnet, Ametista e Pérola"),
        ("KND: A Turma do Bairro", "o codinome do líder careca de óculos escuros do Setor V", "Número 1 (Nigel Uno)"),
        ("As Aventuras de Jackie Chan", "o que o Tio sempre dizia dando um peteleco na testa", "Mais uma coisa! (One more thing!)"),
        ("Super Choque (Static Shock)", "o nome civil do herói Virgil e seu melhor amigo", "Virgil Hawkins e Richie Foley (Gear)"),
        ("X-Men: Evolution", "o instituto onde os jovens mutantes moravam com o Professor Xavier", "Instituto Xavier em Bayville"),
        ("Danny Phantom", "o acidente que deu poderes fantasmas ao jovem Danny Fenton", "Entrou no portal fantasma construído por seus pais"),
        ("Jimmy Neutron", "o nome do seu cachorro robótico inteligente", "Goddard"),
        ("Kim Possible", "o melhor amigo desastrado de Kim e a toupeira-pelada dele", "Ron Stoppable e Rufus"),
        ("Samurai Jack", "o demônio metamorfo que enviou Jack para o futuro", "Aku (Abu)"),
        ("Mansão Foster para Amigos Imaginários", "o melhor amigo azul de Mac", "Bloo"),
        ("Os Simpsons", "o nome do dono bilionário da Usina Nuclear de Springfield", "Sr. Montgomery Burns"),
        ("Futurama", "o nome do robô dobrador amigo de Fry", "Bender Bending Rodríguez"),
        ("Pinky e o Cérebro", "o objetivo deles em absolutamente todas as noites", "Tentar dominar o mundo"),
        ("ThunderCats", "o nome da espada mágica empunhada por Lion-O", "Espada Justiceira (com o Olho de Thundera)")
    ]
    desenhos_impossivel = [
        ("Bob Esponja", "o nome do criador da série que era biólogo marinho na vida real", "Stephen Hillenburg"),
        ("Gravity Falls", "quem escreveu de verdade os 3 Diários misteriosos na história", "Stanford Pines (o irmão gêmeo de seis dedos do Tio Stan)"),
        ("Ben 10", "o nome do gênio da raça Galvaniana que criou o Omnitrix", "Azmuth"),
        ("Avatar: A Lenda de Aang", "a sociedade secreta da qual o Tio Iroh era Grão-Mestre", "Ordem do Lótus Branco"),
        ("As Meninas Superpoderosas", "o nome do ingrediente acidental que deu superpoderes a elas", "Elemento X"),
        ("O Laboratório de Dexter", "o criador desta série que também criou Samurai Jack e Primal", "Genndy Tartakovsky"),
        ("Caverna do Dragão", "os nomes das 6 armas mágicas recebidas pelos jovens", "Arco, Tacape, Escudo, Bastão, Capa da Invisibilidade e Chapéu de Mago"),
        ("Scooby-Doo", "o nome verdadeiro completo do Salsicha na versão original", "Norville Rogers"),
        ("Turma da Mônica", "qual foi o primeiro personagem criado por Mauricio de Sousa em 1959", "O cãozinho Bidu e seu dono Franjinha"),
        ("Pica-Pau", "o nome do cartunista norte-americano que criou o personagem em 1940", "Walter Lantz"),
        ("Tom e Jerry", "a dupla lendária de criadores que dirigiu os curtas originais na MGM", "William Hanna e Joseph Barbera"),
        ("Hora de Aventura", "o conflito apocalíptico ocorrido 1.000 anos antes da série", "A Grande Guerra dos Cogumelos"),
        ("Apenas um Show", "o nome do criador da série que fazia a voz original do Mordecai", "J. G. Quintel"),
        ("Os Simpsons", "o nome completo do criador da família Simpson", "Matt Groening"),
        ("Coragem, o Cão Covarde", "o estado norte-americano onde fica a cidade fictícia de Lugar Nenhum", "Kansas"),
        ("Os Padrinhos Mágicos", "o nome do professor de Timmy obcecado em provar que fadas existem", "Sr. Denzel Crocker"),
        ("Jovens Titãs", "o nome do pai demônio interdimensional da heroína Ravena", "Trigon"),
        ("Corrida Maluca", "quem pilotava o Carro-Tronco (número 10) na corrida", "Rufus Lenhador e o castor Dentes-de-Serra"),
        ("Os Flintstones", "o nome do pequeno alienígena verde que apenas Fred e Barney viam", "Gazoo"),
        ("He-Man e os Mestres do Universo", "o verdadeiro nome do Príncipe de Eternia e do seu tigre", "Príncipe Adam e Pacato (Gato Guerreiro)")
    ]

    fatos_frutas = [
        ("o Abacaxi", "a característica visual famosa no topo da fruta", "Possui uma coroa de folhas espinhosas"),
        ("a Melancia", "a sua composição ideal para hidratação no verão", "Mais de 90% de água e polpa vermelha"),
        ("a Banana", "o mineral famoso que ajuda a evitar cãibras musculares", "Rica em Potássio"),
        ("a Laranja", "o nutriente famoso por fortalecer a imunidade", "Rica em Vitamina C"),
        ("o Abacate", "o prato mexicano famoso feito com sua polpa amassada", "Ingrediente principal do Guacamole"),
        ("o Caju", "a parte curiosa onde fica a verdadeira semente da fruta", "A castanha-de-caju na ponta externa"),
        ("a Jabuticaba", "o modo curioso como ela nasce na árvore brasileira", "Nasce grudada diretamente no tronco"),
        ("o Coco Verde", "o líquido refrescante encontrado dentro da fruta", "Água de coco isotônica natural"),
        ("o Morango", "o detalhe curioso sobre seus pontinhos externos", "As sementes ficam do lado de fora"),
        ("o Açaí", "a região brasileira de onde essa palmeira é nativa", "Região Amazônica / Norte do Brasil"),
        ("a Uva", "a bebida milenar produzida a partir da sua fermentação", "Vinho e suco integral"),
        ("a Manga", "as variedades muito doces e sem fiapos famosas no Brasil", "Manga Tommy e Manga Palmer"),
        ("o Mamão", "a enzima natural que auxilia na digestão", "Papaína, que ajuda no funcionamento intestinal"),
        ("o Maracujá", "o efeito popularmente associado ao seu suco e folhas", "Propriedades calmantes e relaxantes"),
        ("o Limão", "o componente responsável pelo seu sabor azedo característico", "Ácido cítrico natural"),
        ("a Maçã", "a princesa dos contos de fadas associada a esta fruta", "Branca de Neve"),
        ("a Goiaba", "o doce em barra tradicional feito com sua polpa", "Goiabada, famosa na sobremesa Romeu e Julieta"),
        ("a Acerola", "o seu maior destaque nutricional entre as frutas tropicais", "Altíssima concentração de Vitamina C"),
        ("o Pequi", "o bioma brasileiro onde é símbolo da culinária regional", "Cerrado brasileiro"),
        ("a Pitaya", "o apelido exótico pelo formato da sua casca escamosa", "Fruta-do-Dragão"),
        ("o Kiwi", "a aparência característica da sua casca e polpa", "Casca marrom peluda e polpa verde brilhante"),
        ("a Carambola", "o formato geométrico que aparece quando cortada em fatias", "Formato de estrela de cinco pontas"),
        ("a Jaca", "o seu recorde entre as frutas que nascem em árvores", "Uma das maiores e mais pesadas frutas de árvore"),
        ("a Tâmara", "a região do mundo onde é cultivada há milênios", "Desertos do Oriente Médio e Norte da África"),
        ("a Romã", "o significado popular associado às suas sementes no Ano-Novo", "Simboliza prosperidade e fartura")
    ]
    fatos_comidas = [
        ("o Baião de Dois", "os ingredientes principais desse clássico nordestino", "Arroz, feijão-de-corda ou verde e queijo coalho"),
        ("a Feijoada Brasileira", "a base principal usada no preparo tradicional", "Feijão-preto cozido com carnes salgadas"),
        ("a Pamonha", "o ingrediente agrícola ralado para fazer a massa", "Milho verde fresco"),
        ("a Tapioca", "o ingrediente extraído da mandioca para fazer a goma", "Fécula e goma de mandioca hidratada"),
        ("o Acarajé", "a base da massa frita no azeite de dendê na Bahia", "Feijão-fradinho temperado com cebola"),
        ("o Pão de Queijo", "o estado brasileiro mundialmente famoso pela receita", "Minas Gerais"),
        ("a Pizza Napolitana", "o país europeu onde surgiu a receita clássica", "Itália"),
        ("o Sushi", "a base principal combinada com peixe na culinária japonesa", "Arroz temperado com vinagre e alga nori"),
        ("o Churrasco", "o corte bovino com capa de gordura mais pedido no Brasil", "Picanha na brasa"),
        ("a Moqueca", "o ingrediente principal cozido na panela de barro", "Peixe e frutos do mar"),
        ("o Brigadeiro", "os ingredientes essenciais do doce mais famoso das festas", "Leite condensado, chocolate em pó e manteiga"),
        ("a Coxinha", "o recheio tradicional mais pedido nas lanchonetes", "Frango desfiado, muitas vezes com catupiry"),
        ("o Vatapá", "os ingredientes que dão sabor e cremosidade ao prato", "Pão ou farinha, leite de coco, amendoim, castanha e camarão"),
        ("a Carne de Sol com Macaxeira", "o acompanhamento clássico nos restaurantes do Nordeste", "Manteiga da terra e queijo coalho"),
        ("a Lasanha à Bolonhesa", "o recheio intercalado com a massa nesse prato italiano", "Molho de carne moída, presunto, queijo e molho branco"),
        ("a Paella", "o país europeu famoso por esse prato de arroz com frutos do mar", "Espanha"),
        ("os Tacos e Burritos", "a culinária tradicional onde esses pratos são reis", "Culinária Mexicana"),
        ("o Croissant", "o país famoso por essa massa folhada em formato de meia-lua", "França"),
        ("a Bacalhoada", "o país europeu que eternizou as receitas com bacalhau e azeite", "Portugal"),
        ("o Cuscuz Nordestino", "o ingrediente amarelo hidratado e cozido na cuscuzeira", "Flocão de milho cozido no vapor"),
        ("a Farofa", "o ingrediente tostado na manteiga que acompanha o churrasco", "Farinha de mandioca ou de milho"),
        ("o Pudim de Leite", "a calda clássica que cobre a forma antes de assar", "Calda de caramelo feita com açúcar derretido"),
        ("o Strogonoff", "os ingredientes que formam o molho rosado clássico no Brasil", "Creme de leite, molho de tomate e champignon"),
        ("a Canjica e o Mungunzá", "a época festiva do ano em que esses pratos são tradição", "Festas Juninas de São João"),
        ("o Pastel de Feira", "a bebida gelada que forma a dupla perfeita nas feiras livres", "Caldo de cana moído na hora")
    ]
    fatos_novelas = [
        ("a novela Avenida Brasil", "a vilã icônica interpretada por Adriana Esteves", "Carminha"),
        ("a novela Senhora do Destino", "a vilã famosa pelos memes da escada e por roubar Lindalva", "Nazaré Tedesco"),
        ("a novela O Clone", "a protagonista muçulmana que vivia um grande amor com Lucas", "Jade, vivida por Giovanna Antonelli"),
        ("a novela Vale Tudo", "o grande mistério que parou o Brasil em 1988", "Quem matou Odete Roitman?"),
        ("a novela Pantanal", "a personagem mítica que se transforma em onça-pintada", "Juma Marruá"),
        ("a novela O Rei do Gado", "as duas famílias rivais italianas no início da trama", "Mezenga e Berdinazzi"),
        ("a novela Chocolate com Pimenta", "a protagonista dona da fábrica de chocolates em Ventura", "Ana Francisca, vivida por Mariana Ximenes"),
        ("a novela Alma Gêmea", "a jovem indígena que reencarna após o amor com Rafael", "Serena, vivida por Priscila Fantin"),
        ("a novela Mulheres de Areia", "os nomes das irmãs gêmeas de personalidades opostas", "Ruth e Raquel, vividas por Glória Pires"),
        ("a novela A Viagem", "o espírito revoltado que assombrava os vivos na trama", "Alexandre, vivido por Guilherme Fontes"),
        ("a novela O Cravo e a Rosa", "o casal que vivia brigando como cão e gato nos anos 1920", "Petruchio e Catarina"),
        ("a novela Caminho das Índias", "o casal indiano principal da história", "Maya, Bahuan e Raj"),
        ("a novela Terra Nostra", "o imigrante italiano que se apaixona por Giuliana no navio", "Matteo, vivido por Thiago Lacerda"),
        ("a novela Laços de Família", "a cena emocionante de Camila durante o tratamento de saúde", "Raspou os cabelos ao som de Love by Grace"),
        ("a novela Roque Santeiro", "a viúva exuberante que nunca chegou a casar de verdade", "Viúva Porcina, vivida por Regina Duarte"),
        ("a novela Tieta", "a protagonista que volta rica para Santana do Agreste", "Tieta do Agreste, vivida por Betty Faria"),
        ("a novela Da Cor do Pecado", "a vilã loira obcecada pela fortuna de Afonso Lambertini", "Bárbara, vivida por Giovanna Antonelli"),
        ("a novela Cheias de Charme", "o trio musical formado pelas três domésticas protagonistas", "As Empreguetes: Penha, Rosário e Cida"),
        ("a novela Totalmente Demais", "a diretora implacável da revista de moda na trama", "Carolina Castilho, vivida por Juliana Paes"),
        ("a novela A Usurpadora", "os nomes das irmãs gêmeas mexicanas na história", "Paola Bracho e Paulina Martins"),
        ("a novela Maria do Bairro", "a vilã dramática que gritava frases inesquecíveis", "Soraya Montenegro"),
        ("a novela Rebelde", "o colégio de elite onde os seis jovens formaram a banda RBD", "Elite Way School"),
        ("a novela Carrossel", "a professora doce e querida pelos alunos da Escola Mundial", "Professora Helena"),
        ("a novela Império", "o título pelo qual era chamado o protagonista José Alfredo", "Comendador"),
        ("a novela Verdades Secretas", "o apelido da jovem modelo Arlete nas passarelas", "Angel")
    ]
    fatos_filmes = [
        ("o filme Titanic", "o casal protagonista interpretado por Leonardo DiCaprio e Kate Winslet", "Jack Dawson e Rose DeWitt Bukater"),
        ("a saga Harry Potter", "o nome da escola de magia e bruxaria onde a história acontece", "Hogwarts"),
        ("O Senhor dos Anéis", "o pequeno hobbit encarregado de destruir o Um Anel", "Frodo Bolseiro"),
        ("a saga Star Wars", "a famosa revelação feita por Darth Vader a Luke Skywalker", "Eu sou o seu pai"),
        ("o filme O Rei Leão", "o filhote de leão herdeiro da Pedra do Rei", "Simba"),
        ("a franquia Toy Story", "a dupla principal de brinquedos do garoto Andy", "Xerife Woody e patrulheiro Buzz Lightyear"),
        ("o filme Jurassic Park", "as criaturas pré-históricas recriadas a partir do DNA no âmbar", "Dinossauros"),
        ("o filme Matrix", "a escolha de pílulas oferecida por Morpheus a Neo", "Pílula Azul ou Pílula Vermelha"),
        ("o filme Avatar", "a lua exuberante habitada pelo povo azul Na'vi", "Pandora"),
        ("De Volta para o Futuro", "o carro famoso transformado em máquina do tempo pelo Dr. Brown", "DeLorean"),
        ("O Poderoso Chefão", "o sobrenome da família mafiosa liderada por Don Vito", "Família Corleone"),
        ("Velozes e Furiosos", "o personagem de Vin Diesel que valoriza a família acima de tudo", "Dominic Toretto"),
        ("Piratas do Caribe", "o capitão excêntrico apaixonado pelo navio Pérola Negra", "Capitão Jack Sparrow"),
        ("a animação Shrek", "o melhor amigo falante que acompanha o ogro no pântano", "Burro Falante"),
        ("a animação Frozen", "a irmã mais velha com poderes mágicos de gelo e neve", "Rainha Elsa"),
        ("Procurando Nemo", "a espécie de peixe laranja com listras brancas do protagonista", "Peixe-palhaço"),
        ("o filme Tropa de Elite", "o personagem imortalizado por Wagner Moura no BOPE", "Capitão Nascimento"),
        ("O Auto da Compadecida", "a dupla de amigos nordestinos espertos e inseparáveis", "João Grilo e Chicó"),
        ("o filme Cidade de Deus", "o jovem morador que sonha em se tornar fotógrafo profissional", "Buscapé"),
        ("o filme Central do Brasil", "a ocupação de Dora, vivida por Fernanda Montenegro, na estação", "Escrevedora de cartas para pessoas analfabetas"),
        ("o filme Forrest Gump", "a frase clássica sobre a vida dita pelo protagonista no banco de praça", "A vida é como uma caixa de chocolates"),
        ("o filme Gladiador", "o general romano que se torna gladiador na arena do Coliseu", "Maximus Decimus Meridius"),
        ("o filme Rocky, um Lutador", "o esporte em que Rocky Balboa enfrenta Apollo Creed", "Boxe"),
        ("Homem-Aranha no Aranhaverso", "o jovem do Brooklyn que assume o manto do herói", "Miles Morales"),
        ("Vingadores: Ultimato", "a frase final dita por Tony Stark antes de estalar os dedos", "Eu sou o Homem de Ferro")
    ]
    fatos_trabalhos = [
        ("Analista de Suporte e TI", "a função essencial desempenhada nas empresas modernas", "Resolver problemas técnicos de computadores, sistemas e usuários"),
        ("Administrador de Redes", "os equipamentos que ele configura para conectar a empresa", "Roteadores, Switches, Firewalls e servidores de rede"),
        ("Técnico de Fibra Óptica", "a ferramenta usada para unir dois fios de vidro com precisão", "Máquina de fusão de fibra óptica"),
        ("Médico Cardiologista", "o órgão do corpo humano do qual ele cuida", "Coração e sistema circulatório"),
        ("Engenheiro Civil", "a responsabilidade técnica principal numa construção", "Cálculo estrutural e execução segura de obras e pontes"),
        ("Eletricista", "o instrumento usado para medir tensão, corrente e resistência elétrica", "Multímetro"),
        ("Advogado", "o exame nacional obrigatório para exercer a profissão no Brasil", "Exame da Ordem dos Advogados do Brasil (OAB)"),
        ("Professor", "a missão principal dentro da sala de aula", "Ensinar, formar cidadãos e compartilhar conhecimento"),
        ("Bombeiro", "o número de telefone de emergência no Brasil para chamá-lo", "193"),
        ("Chef de Cozinha", "a responsabilidade principal dentro de um restaurante", "Criar o cardápio, preparar pratos e coordenar a equipe"),
        ("Mecânico Automotivo", "a manutenção preventiva mais comum feita no motor", "Troca de óleo e filtros do veículo"),
        ("Enfermeiro", "a atuação direta no cuidado diário dos pacientes", "Administrar medicamentos, aferir sinais vitais e assistir o paciente"),
        ("Contador", "a declaração anual que ele ajuda pessoas e empresas a entregar", "Imposto de Renda e balanço patrimonial"),
        ("Arquiteto", "o foco do seu trabalho ao planejar um ambiente", "Conforto, estética, iluminação e aproveitamento do espaço"),
        ("Farmacêutico", "a sua responsabilidade técnica nas drogarias", "Orientar sobre o uso correto de medicamentos e receitas"),
        ("Militar das Forças Armadas", "o dever constitucional da sua função", "Defesa da Pátria e garantia da soberania nacional"),
        ("Desenvolvedor de Software", "as linguagens muito usadas em automação, dados e web", "Python, JavaScript e bancos de dados SQL"),
        ("Dentista", "o cuidado preventivo recomendado a cada 6 meses", "Limpeza dentária e prevenção de cáries"),
        ("Médico Veterinário", "o público atendido em sua clínica ou fazenda", "Animais domésticos, silvestres e de produção"),
        ("Motorista Profissional", "o documento obrigatório com categoria específica para dirigir", "Carteira Nacional de Habilitação (CNH)"),
        ("Padeiro e Confeiteiro", "o ingrediente biológico que faz a massa do pão crescer", "Fermento biológico"),
        ("Fotógrafo Profissional", "os três pilares básicos para controlar a luz numa câmera", "ISO, Abertura do Diafragma e Velocidade do Obturador"),
        ("Psicólogo", "o foco do atendimento clínico no consultório", "Saúde mental, escuta qualificada e comportamento humano"),
        ("Pedreiro e Mestre de Obras", "a ferramenta usada para garantir que a parede suba reta", "Prumo e Nível de bolha"),
        ("Designer Gráfico", "o formato de arquivo vetorial usado em corte a laser e logotipos", "SVG e curvas vetoriais")
    ]

    return {
        "⛪ Igreja": {
            "🟢 Fácil": montar_100_perguntas(igreja_facil, tpl_padrao),
            "🟡 Normal": montar_100_perguntas(igreja_normal, tpl_padrao),
            "🟠 Hard": montar_100_perguntas(igreja_hard, tpl_padrao),
            "🔴 Impossível": montar_100_perguntas(igreja_impossivel, tpl_padrao)
        },
        "🦸 Super-Heróis": {
            "🟢 Fácil": montar_100_perguntas(herois_facil, tpl_padrao),
            "🟡 Normal": montar_100_perguntas(herois_normal, tpl_padrao),
            "🟠 Hard": montar_100_perguntas(herois_hard, tpl_padrao),
            "🔴 Impossível": montar_100_perguntas(herois_impossivel, tpl_padrao)
        },
        "🎨 Desenhos": {
            "🟢 Fácil": montar_100_perguntas(desenhos_facil, tpl_padrao),
            "🟡 Normal": montar_100_perguntas(desenhos_normal, tpl_padrao),
            "🟠 Hard": montar_100_perguntas(desenhos_hard, tpl_padrao),
            "🔴 Impossível": montar_100_perguntas(desenhos_impossivel, tpl_padrao)
        },
        "⚔️ Animes": {
            "🟢 Fácil": montar_100_perguntas(animes_facil_100, tpl_padrao),
            "🟡 Normal": montar_100_perguntas(animes_normal_100, tpl_padrao),
            "🟠 Hard": montar_100_perguntas(animes_hard_100, tpl_padrao),
            "🔴 Impossível": montar_100_perguntas(animes_impossivel_100, tpl_padrao)
        },
        "🍎 Frutas": montar_100_perguntas(fatos_frutas, tpl_padrao),
        "🍔 Comidas": montar_100_perguntas(fatos_comidas, tpl_padrao),
        "📺 Novelas": montar_100_perguntas(fatos_novelas, tpl_padrao),
        "🎬 Filmes": montar_100_perguntas(fatos_filmes, tpl_padrao),
        "💼 Trabalhos & Profissões": montar_100_perguntas(fatos_trabalhos, tpl_padrao)
    }

BANCOS_PADRAO = construir_bancos_completos()
LISTA_MODOS_JOGO = list(INFO_MODOS.keys())

# ==============================================================================
# CONFIGURAÇÕES SIMPLIFICADAS E DIRETAS
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
        "txt_titulo_menu": "🎲 SUPER QUIZ MULTI-TEMAS (2.100 PERGUNTAS) 🎲",
        "txt_subtitulo_menu": "Escolha o seu tema, selecione a dificuldade e desafie os seus conhecimentos! (F11 para tela cheia)",
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

# Inicialização de Estados da Sessão (Incluindo o Modo Mobile!)
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
    "modo_mobile": False, "forcar_paisagem_js": False
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
# GERADOR DE CSS DINÂMICO (ADAPTA AUTOMATICAMENTE PARA MODO MOBILE OU TELÃO!)
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
    
    # Escalas inteligentes para Celular vs Telão
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
        /* BOTÕES COMPACTOS DA BARRA DE DISPOSITIVO NO TOPO */
        .st-key-btn_toggle_mob button, .st-key-btn_girar_paisagem button {{
            font-size: 14px !important;
            padding: 6px 12px !important;
            max-width: 240px !important;
            margin: 2px auto !important;
            border-radius: 20px !important;
            background-color: rgba(255,255,255,0.12) !important;
            border: 1px solid {paleta['cor_destaque']} !important;
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
# IMAGEM DINÂMICA DA COLUNA DIREITA (TAMANHO REDUZIDO NO MODO MOBILE!)
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
# FUNÇÕES DE DADOS
# ==============================================================================
def copiar_bancos_padrao():
    copia = {}
    for k, v in BANCOS_PADRAO.items():
        if isinstance(v, dict):
            copia[k] = {niv: list(lista_p) for niv, lista_p in v.items()}
        else:
            copia[k] = list(v)
    return copia

def carregar_dados():
    bancos_atuais = copiar_bancos_padrao()
    participantes_atuais = []
    historico_atual = []
    precisa_salvar = False
    
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if not dados.get("animes_400_unicos_v5", False):
                    precisa_salvar = True
                elif "bancos_perguntas" in dados and isinstance(dados["bancos_perguntas"], dict):
                    for k, val_salvo in dados["bancos_perguntas"].items():
                        if k in TEMAS_COM_DIFICULDADE:
                            if isinstance(val_salvo, dict):
                                for niv in NIVEIS_DIFICULDADE:
                                    if niv in val_salvo and len(val_salvo[niv]) >= 10:
                                        bancos_atuais[k][niv] = val_salvo[niv]
                                    else:
                                        precisa_salvar = True
                            else:
                                precisa_salvar = True
                        elif k in BANCOS_PADRAO:
                            if isinstance(val_salvo, list) and len(val_salvo) >= 10:
                                bancos_atuais[k] = val_salvo
                            else:
                                precisa_salvar = True
                else:
                    precisa_salvar = True
                
                participantes_atuais = dados.get("participantes", [])
                historico_atual = dados.get("historico", [])
        except Exception:
            precisa_salvar = True
    else:
        precisa_salvar = True
        
    if precisa_salvar:
        salvar_dados(bancos_atuais, participantes_atuais, historico_atual)
        
    return bancos_atuais, participantes_atuais, historico_atual

def salvar_dados(bancos_perguntas, participantes, historico):
    dados = {
        "animes_400_unicos_v5": True,
        "bancos_perguntas": bancos_perguntas,
        "participantes": participantes,
        "historico": historico
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def contar_todas_perguntas(bancos_dict):
    total = 0
    for v in bancos_dict.values():
        if isinstance(v, dict):
            for lista_n in v.values():
                total += len(lista_n)
        elif isinstance(v, list):
            total += len(v)
    return total

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

bancos_perguntas, participantes, historico = carregar_dados()

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
# BARRA RÁPIDA NO TOPO: ALTERNAR MODO MOBILE (VERTICAL) E MODO PAISAGEM (TELÃO)
# ==============================================================================
col_bar1, col_bar2 = st.columns([1, 1])
with col_bar1:
    txt_toggle_mob = "🖥️ Mudar para Modo Telão / Paisagem" if st.session_state.modo_mobile else "📱 Mudar para Versão Celular (Vertical)"
    if st.button(txt_toggle_mob, key="btn_toggle_mob"):
        st.session_state.modo_mobile = not st.session_state.modo_mobile
        st.rerun()

with col_bar2:
    if st.button("🔄 Tela Cheia / Girar Paisagem", key="btn_girar_paisagem"):
        st.session_state.modo_mobile = False
        st.session_state.forcar_paisagem_js = True
        st.rerun()

if st.session_state.get("forcar_paisagem_js", False):
    st.session_state.forcar_paisagem_js = False
    components.html("""
        <script>
        (async function() {
            try {
                const docEl = window.parent.document.documentElement;
                if (docEl.requestFullscreen) {
                    await docEl.requestFullscreen();
                } else if (docEl.webkitRequestFullscreen) {
                    await docEl.webkitRequestFullscreen();
                }
                if (window.parent.screen && window.parent.screen.orientation && window.parent.screen.orientation.lock) {
                    await window.parent.screen.orientation.lock('landscape');
                }
            } catch (err) {
                console.log("Rotação automática depende do desbloqueio do aparelho:", err);
            }
        })();
        </script>
    """, height=0)
    st.toast("🔄 Modo Paisagem ativado! Se estiver no celular, vire o aparelho na horizontal.", icon="📱")

# ==============================================================================
# SLOTS DE CONTEÚDO INDEPENDENTES
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
# 1. MENU PRINCIPAL
# ==============================================================================
if st.session_state.pagina == "menu":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        st.session_state.modo_jogo_ativo = None
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
# 2. SELECIONAR PARTICIPANTE + MODO + DIFICULDADE (ADAPTÁVEL MOBILE / TELÃO)
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

            pts_base_cfg = config.get("pontos_por_acerto", 100)
            if modo_escolhido in TEMAS_COM_DIFICULDADE:
                idx_dif = NIVEIS_DIFICULDADE.index(st.session_state.dificuldade_ativa) if st.session_state.dificuldade_ativa in NIVEIS_DIFICULDADE else 0
                dif_escolhida = st.selectbox(
                    "3️⃣ Escolha o Nível de Dificuldade:",
                    NIVEIS_DIFICULDADE,
                    index=idx_dif,
                    key="sel_dif_jogo_sel"
                )
                st.session_state.dificuldade_ativa = dif_escolhida
                pts_partida = int(pts_base_cfg * MULTIPLICADOR_PONTOS.get(dif_escolhida, 1.0))
                qtd_disp = len(bancos_perguntas.get(modo_escolhido, {}).get(dif_escolhida, []))
                resumo_badge = f"🎯 {modo_escolhido} ({dif_escolhida}) — {qtd_disp} perguntas | ⭐ {pts_partida} pts"
                txt_botao_ini = f"▶️ Iniciar: {modo_escolhido} ({dif_escolhida})"
            else:
                dif_escolhida = None
                st.session_state.dificuldade_ativa = None
                pts_partida = pts_base_cfg
                if modo_escolhido == "🎲 Misturadão (Todos os Temas)":
                    qtd_disp = contar_todas_perguntas(bancos_perguntas)
                else:
                    qtd_disp = len(bancos_perguntas.get(modo_escolhido, []))
                resumo_badge = f"🎯 Tema: {modo_escolhido} — {qtd_disp} perguntas!"
                txt_botao_ini = f"▶️ Iniciar Quiz: {modo_escolhido}"
                
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
                        salvar_dados(bancos_perguntas, participantes, historico)
                
                if nome_final:
                    if modo_escolhido == "🎲 Misturadão (Todos os Temas)":
                        lista_base = []
                        for val_b in bancos_perguntas.values():
                            if isinstance(val_b, dict):
                                for l_niv in val_b.values():
                                    lista_base.extend(l_niv)
                            elif isinstance(val_b, list):
                                lista_base.extend(val_b)
                    elif modo_escolhido in TEMAS_COM_DIFICULDADE:
                        lista_base = list(bancos_perguntas.get(modo_escolhido, {}).get(dif_escolhida, []))
                    else:
                        lista_base = list(bancos_perguntas.get(modo_escolhido, []))
                        
                    if not lista_base:
                        st.error("Este modo/nível ainda não possui perguntas cadastradas!")
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
# 3. TELA DO JOGO (LAYOUT RESPONSIVO PARA CELULAR VERTICAL OU TELÃO PAISAGEM!)
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
        dif_atual = st.session_state.get("dificuldade_ativa")
        mult = MULTIPLICADOR_PONTOS.get(dif_atual, 1.0) if dif_atual else 1.0
        pts_acerto = int(config.get("pontos_por_acerto", 100) * mult)
        paleta = obter_paleta_ativa()
        
        if p_idx >= total_p:
            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
            ir_para_pagina("fim")

        if not st.session_state.respondido:
            tocar_audio_invisivel(SOM_TIC_TAK, loop=True)

        # No modo mobile, usa coluna única direta para caber tudo na tela do celular sem espremer!
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
                salvar_dados(bancos_perguntas, participantes, historico)
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
            salvar_dados(bancos_perguntas, participantes, historico)
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
                salvar_dados(bancos_perguntas, participantes, historico)
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
                    salvar_dados(bancos_perguntas, participantes, historico)
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
                salvar_dados(bancos_perguntas, participantes, historico)
                st.rerun()
            if st.button("🗑️ Limpar Todo o Histórico"):
                historico.clear()
                salvar_dados(bancos_perguntas, participantes, historico)
                st.rerun()
        else:
            st.info("Ainda não existem registos no histórico.")

# ==============================================================================
# 8. GERIR / EDITAR AS 2.100 PERGUNTAS SEPARADAS POR TEMA & NÍVEL
# ==============================================================================
elif st.session_state.pagina == "gerir_perguntas":
    slot_selecao.empty()
    slot_jogo.empty()
    with slot_outros.container():
        st.markdown("<h2 style='text-align: center;'>📝 Gestão de Perguntas (2.100 Perguntas)</h2>", unsafe_allow_html=True)
        
        if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_topo", use_container_width=True):
            st.session_state.editando_idx = None
            st.session_state.modo_jogo_ativo = None
            ir_para_pagina("menu")
        if st.button("➕ Nova Pergunta neste Banco", key="btn_nova_perg_topo", use_container_width=True):
            st.session_state.editando_idx = -1
            st.rerun()
        if st.button("🔄 Restaurar 100 Perguntas deste Banco", key="btn_reset_tema", use_container_width=True):
            tema_atual = st.session_state.tema_gerir_selecionado
            niv_atual = st.session_state.nivel_gerir_selecionado
            if tema_atual in TEMAS_COM_DIFICULDADE:
                bancos_perguntas[tema_atual][niv_atual] = list(BANCOS_PADRAO[tema_atual][niv_atual])
            else:
                bancos_perguntas[tema_atual] = list(BANCOS_PADRAO[tema_atual])
            salvar_dados(bancos_perguntas, participantes, historico)
            st.success("As 100 perguntas deste banco foram restauradas!")
            st.rerun()

        temas_disponiveis = list(BANCOS_PADRAO.keys())
        idx_t = temas_disponiveis.index(st.session_state.tema_gerir_selecionado) if st.session_state.tema_gerir_selecionado in temas_disponiveis else 0
        tema_sel_gerir = st.selectbox("📂 1. Selecione o Modo de Jogo:", temas_disponiveis, index=idx_t)
        
        if tema_sel_gerir != st.session_state.tema_gerir_selecionado:
            st.session_state.tema_gerir_selecionado = tema_sel_gerir
            st.session_state.modo_jogo_ativo = tema_sel_gerir
            st.session_state.editando_idx = None
            st.rerun()

        if tema_sel_gerir in TEMAS_COM_DIFICULDADE:
            idx_n = NIVEIS_DIFICULDADE.index(st.session_state.nivel_gerir_selecionado) if st.session_state.nivel_gerir_selecionado in NIVEIS_DIFICULDADE else 0
            niv_sel_gerir = st.selectbox("🎯 2. Selecione o Nível de Dificuldade:", NIVEIS_DIFICULDADE, index=idx_n)
            if niv_sel_gerir != st.session_state.nivel_gerir_selecionado:
                st.session_state.nivel_gerir_selecionado = niv_sel_gerir
                st.session_state.editando_idx = None
                st.rerun()
            perguntas_do_tema = bancos_perguntas.get(tema_sel_gerir, {}).get(niv_sel_gerir, [])
            rotulo_banco = f"{tema_sel_gerir} ({niv_sel_gerir})"
        else:
            niv_sel_gerir = None
            perguntas_do_tema = bancos_perguntas.get(tema_sel_gerir, [])
            rotulo_banco = tema_sel_gerir

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
                
                btn_sub = st.form_submit_button("💾 Salvar Pergunta")
                if btn_sub:
                    if nova_p and op1 and op2 and op3 and op4 and correta:
                        ops = [op1, op2, op3, op4]
                        if correta in ops:
                            item_novo = {"pergunta": nova_p, "opcoes": ops, "resposta": correta}
                            if is_novo:
                                perguntas_do_tema.insert(0, item_novo)
                            else:
                                perguntas_do_tema[idx_edit] = item_novo
                            if tema_sel_gerir in TEMAS_COM_DIFICULDADE:
                                bancos_perguntas[tema_sel_gerir][niv_sel_gerir] = perguntas_do_tema
                            else:
                                bancos_perguntas[tema_sel_gerir] = perguntas_do_tema
                            salvar_dados(bancos_perguntas, participantes, historico)
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
        st.markdown(f"<h3 style='text-align: center;'>📋 Perguntas de {rotulo_banco} ({len(perguntas_do_tema)} cadastradas)</h3>", unsafe_allow_html=True)
        
        busca_txt = st.text_input("🔍 Filtrar / Pesquisar pergunta neste banco:", "")
        
        for idx, item in enumerate(perguntas_do_tema):
            if busca_txt.strip().lower() in item["pergunta"].lower() or busca_txt.strip().lower() in item["resposta"].lower():
                col_txt, col_edit, col_del = st.columns([5, 1, 1])
                with col_txt:
                    st.write(f"**{idx+1}. {item['pergunta']}** *(Resp: {item['resposta']})*")
                with col_edit:
                    if st.button("✏️", key=f"edit_p_{rotulo_banco}_{idx}"):
                        st.session_state.editando_idx = idx
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_p_{rotulo_banco}_{idx}"):
                        perguntas_do_tema.pop(idx)
                        if tema_sel_gerir in TEMAS_COM_DIFICULDADE:
                            bancos_perguntas[tema_sel_gerir][niv_sel_gerir] = perguntas_do_tema
                        else:
                            bancos_perguntas[tema_sel_gerir] = perguntas_do_tema
                        salvar_dados(bancos_perguntas, participantes, historico)
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
            st.markdown("<h3 style='text-align: center;'>📏 Ajuste de Tamanho (Modo Telão/PC)</h3>", unsafe_allow_html=True)
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
            st.markdown("<h3 style='text-align: center;'>♻️ Restaurar Padrão de Fábrica</h3>", unsafe_allow_html=True)
            if st.button("🔄 Restaurar Todas as Configurações e as 2.100 Perguntas", key="btn_restaurar_orig"):
                salvar_config(obter_config_padrao())
                salvar_dados(copiar_bancos_padrao(), participantes, historico)
                st.session_state.up_cnt += 1
                st.session_state.msg_upload_ok = "🔄 Configurações e banco de 2.100 perguntas restaurados com sucesso!"
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
