# ==============================================================================
# SUPER QUIZ MULTI-TEMAS (2.100 PERGUNTAS + 4 NÍVEIS EM 4 GRANDES TEMAS) 🎲🏆🔥
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

# Temas que possuem os 4 níveis de dificuldade (400 perguntas cada!)
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
        "icone": "⚔️", "titulo_card": "🐉 Arena Otaku", "sub_card": "Dragon Ball, Naruto, One Piece, Solo Leveling e mais!",
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
# GERADOR DE PERGUNTAS NATURAIS (COM 4 NÍVEIS EM IGREJA, HERÓIS, DESENHOS E ANIMES)
# ==============================================================================
def montar_100_perguntas(fatos, templates):
    todas_respostas = list(dict.fromkeys([f[2] for f in fatos]))
    perguntas_geradas = []
    rng = random.Random(42)
    
    for idx in range(100):
        item, sub, certa = fatos[idx % len(fatos)]
        ciclo = idx // len(fatos)
        molde = templates[ciclo % len(templates)]
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
        "Qual das opções abaixo corresponde a {sub} em relação a {item}?",
        "Quando falamos sobre {item}, o que define corretamente {sub}?",
        "Assinale a alternativa verdadeira sobre {sub} referente a {item}:"
    ]

    # --------------------------------------------------------------------------
    # 1. IGREJA — 4 NÍVEIS (FÁCIL, NORMAL, HARD, IMPOSSÍVEL)
    # --------------------------------------------------------------------------
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

    # --------------------------------------------------------------------------
    # 2. SUPER-HERÓIS — 4 NÍVEIS (FÁCIL, NORMAL, HARD, IMPOSSÍVEL)
    # --------------------------------------------------------------------------
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
        ("o surfista prateado", "o devorador de mundos gigante de quem Norrin Radd era arauto", "Galactus"),
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

    # --------------------------------------------------------------------------
    # 3. DESENHOS — 4 NÍVEIS (FÁCIL, NORMAL, HARD, IMPOSSÍVEL)
    # --------------------------------------------------------------------------
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

    # --------------------------------------------------------------------------
    # 4. ANIMES — 4 NÍVEIS (FÁCIL, NORMAL, HARD, IMPOSSÍVEL)
    # --------------------------------------------------------------------------
    animes_facil = [
        ("Dragon Ball Z", "o nome do protagonista criado na Terra que busca as Esferas do Dragão", "Son Goku"),
        ("Dragon Ball Z", "quantas Esferas do Dragão existem na Terra para invocar Shenlong", "7 Esferas do Dragão"),
        ("Naruto", "o sonho principal de Naruto Uzumaki desde criança", "Tornar-se o Hokage da Vila da Folha"),
        ("One Piece", "o acessório famoso que Monkey D. Luffy usa na cabeça", "Um Chapéu de Palha"),
        ("Pokémon", "o primeiro Pokémon amarelo de tipo elétrico parceiro de Ash", "Pikachu"),
        ("Cavaleiros do Zodíaco", "a constelação protetora do protagonista Seiya", "Pégaso"),
        ("Death Note", "o que acontece quando o nome de alguém é escrito no caderno", "A pessoa morre"),
        ("One Punch Man", "como Saitama derrota praticamente qualquer inimigo", "Com apenas um soco"),
        ("Demon Slayer", "quem Tanjiro carrega dentro de uma caixa de madeira nas costas", "Sua irmã Nezuko Kamado"),
        ("Dragon Ball Z", "o príncipe orgulhoso dos Saiyajins que se torna rival de Goku", "Vegeta"),
        ("Naruto", "o melhor amigo e rival de Naruto, último sobrevivente do clã Uchiha", "Sasuke Uchiha"),
        ("One Piece", "o espadachim do bando que luta usando três espadas ao mesmo tempo", "Roronoa Zoro"),
        ("Spy x Family", "a garotinha de cabelo rosa que consegue ler mentes", "Anya Forger"),
        ("Attack on Titan", "as criaturas gigantes que devoravam humanos fora das muralhas", "Titãs"),
        ("Yu-Gi-Oh!", "o jogo que Yugi Muto domina usando o Enigma do Milênio", "Duelo de Monstros (Cartas)"),
        ("Beyblade", "o objeto giratório usado nas batalhas de arena", "Piões de batalha Beyblade"),
        ("Digimon", "o parceiro dinossauro laranja de Tai Kamiya", "Agumon"),
        ("Super Campeões (Captain Tsubasa)", "o esporte praticado por Oliver Tsubasa", "Futebol"),
        ("Sailor Moon", "a guerreira mágica que luta pelo amor e pela justiça", "Usagi Tsukino (Sailor Moon)"),
        ("Sakura Card Captors", "o que Sakura Kinomoto precisa capturar ao longo do anime", "As Cartas Clow")
    ]
    animes_normal = [
        ("Solo Leveling", "o comando que Sung Jin-Woo usa para erguer seu exército de sombras", "Erga-se (Arise)"),
        ("Black Clover", "a característica única de Asta num mundo onde todos usam magia", "Ele nasceu sem magia e usa espadas de Anti-Magia"),
        ("Bleach", "a raça de ceifadores de almas da qual Ichigo Kurosaki faz parte", "Shinigami"),
        ("Tokyo Revengers", "o apelido do líder invencível da gangue Tokyo Manji (Toman)", "Mikey (Manjiro Sano)"),
        ("Mashle: Magia e Músculos", "o doce que Mash Burnedead é completamente viciado em comer", "Profiteroles (bombinhas de creme)"),
        ("That Time I Got Reincarnated as a Slime", "o nome que o protagonista recebe do dragão Veldora ao reencarnar", "Rimuru Tempest"),
        ("Cyberpunk: Edgerunners", "a netrunner de cabelos coloridos por quem David se apaixona", "Lucy"),
        ("Jujutsu Kaisen", "o Rei das Maldições cujos dedos foram engolidos por Yuji Itadori", "Ryomen Sukuna"),
        ("My Hero Academia", "o Símbolo da Paz que passa seu poder para Izuku Midoriya", "All Might"),
        ("Naruto Shippuden", "a organização criminosa de mantos pretos com nuvens vermelhas", "Akatsuki"),
        ("Dragon Ball Z", "quem Goku derrota em Namekusei após a morte de Kuririn", "Freeza"),
        ("Dragon Ball Z", "quem derrota o vilão Cell ao atingir o Super Saiyajin 2", "Son Gohan"),
        ("One Piece", "a fruta mística que deu a Luffy um corpo de borracha", "Gomu Gomu no Mi (Hito Hito no Mi, Modelo: Nika)"),
        ("Fullmetal Alchemist", "os nomes dos dois irmãos alquimistas protagonistas", "Edward e Alphonse Elric"),
        ("Hunter x Hunter", "o melhor amigo de Gon Freecss que vem de uma família de assassinos", "Killua Zoldyck"),
        ("Yu Yu Hakusho", "os quatro amigos protagonistas que lutam no Torneio das Trevas", "Yusuke, Kuwabara, Kurama e Hiei"),
        ("InuYasha", "a estudante do presente que volta ao Japão Feudal pelo poço", "Kagome Higurashi"),
        ("Death Note", "o maior detetive do mundo que investiga o caso Kira", "L (Lawliet)"),
        ("Demon Slayer", "o título dado aos espadachins de mais alto nível da corporação", "Hashiras (Pilares)"),
        ("Attack on Titan", "o capitão da Tropa de Exploração conhecido como o mais forte da humanidade", "Capitão Levi Ackerman")
    ]
    animes_hard = [
        ("Bleach: Thousand-Year Blood War", "o nome da Bankai de Ichigo Kurosaki", "Tensa Zangetsu"),
        ("Solo Leveling", "a primeira sombra de cavaleiro vermelho-sangue que Jin-Woo extrai", "Igris, o Comandante Vermelho-Sangue"),
        ("Black Clover", "o capitão do esquadrão Touros Negros que usa Magia de Escuridão", "Yami Sukehiro"),
        ("Cyberpunk: Edgerunners", "o lendário mercenário ciborgue que David enfrenta na Arasaka Tower", "Adam Smasher"),
        ("Attack on Titan", "os nove Titãs Originais liderados pelo poder máximo de Eren", "Titã Fundador, Titã de Ataque, Colossal, Blindado, Fêmea, Bestial, Mandíbula, Quadrúpede e Martelo de Guerra"),
        ("Dragon Ball Super", "a técnica divina que Goku domina no Torneio do Poder contra Jiren", "Instinto Superior (Ultra Instinct)"),
        ("Naruto", "o nome verdadeiro do Quarto Hokage, pai de Naruto", "Minato Namikaze (Relâmpago Amarelo de Konoha)"),
        ("Jujutsu Kaisen", "o nome da Expansão de Domínio de Satoru Gojo", "Vazio Infinito (Muryokusho)"),
        ("Demon Slayer", "o primeiro usuário da Respiração do Sol que quase derrotou Muzan", "Yoriichi Tsugikuni"),
        ("That Time I Got Reincarnated as a Slime", "a habilidade suprema de inteligência que guia Rimuru desde o início", "Grande Sábio (que evolui para Rafael)"),
        ("Tokyo Revengers", "como Takemichi Hanagaki ativa sua viagem no tempo de 12 anos no passado", "Através de um aperto de mão com Naoto Tachibana"),
        ("Mashle: Magia e Músculos", "o título dado aos alunos de elite que recebem moedas de ouro em Easton", "Visionários Divinos"),
        ("One Piece", "o nome do médico rena e do carpinteiro ciborgue do bando do Chapéu de Palha", "Tony Tony Chopper e Franky"),
        ("Death Note", "o nome do Shinigami que deixou o caderno cair no mundo humano", "Ryuk"),
        ("Fullmetal Alchemist: Brotherhood", "o líder dos Homúnculos que comanda o exército de Amestris", "King Bradley (Ira / Wrath)"),
        ("Hunter x Hunter", "o líder da Trupe Fantasma (Genei Ryodan) que rouba habilidades", "Chrollo Lucilfer"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Ouro de Virgem conhecido como o homem mais próximo de Deus", "Shaka de Virgem"),
        ("Yu Yu Hakusho", "a transformação de cabelos longos prateados de Kurama", "Kurama Youko"),
        ("Code Geass", "o protagonista que recebe o poder da obediência absoluta de C.C.", "Lelouch vi Britannia (Zero)"),
        ("Steins;Gate", "o aparelho doméstico que Okabe transforma numa máquina de enviar mensagens ao passado", "Um forno de micro-ondas conectado a um celular")
    ]
    animes_impossivel = [
        ("Solo Leveling", "o título e nome do Monarca original de quem Sung Jin-Woo herdou o coração negro", "Ashborn, o Monarca das Sombras"),
        ("Bleach: Thousand-Year Blood War", "o nome do Imperador Quincy pai de todos os Quincies e sua habilidade 'A'", "Yhwach e o poder 'The Almighty' (O Onipotente)"),
        ("Black Clover", "o nome do demônio de Anti-Magia que habitava o grimório de cinco folhas de Asta", "Liebe"),
        ("Dragon Ball", "o nome verdadeiro de Goku dado por seu pai Bardock no planeta Vegeta", "Kakarotto"),
        ("Attack on Titan", "o nome da fundadora original que obteve o poder dos Titãs há 2.000 anos", "Ymir Fritz"),
        ("Cyberpunk: Edgerunners", "a música famosa de Rosa Walton que toca na cena final da Lua", "I Really Want to Stay at Your House"),
        ("That Time I Got Reincarnated as a Slime", "o nome do mordomo demônio primordial Preto invocado por Rimuru", "Diablo (Noir)"),
        ("Mashle: Magia e Músculos", "o nome do vilão principal pai de Mash que busca o coração dos 6 filhos", "Innocent Zero"),
        ("Tokyo Revengers", "o nome do irmão mais velho de Mikey que era dono de uma oficina de motos", "Shinichiro Sano"),
        ("Naruto Shippuden", "o nome do Sábio dos Seis Caminhos que criou o Ninshu", "Hagoromo Otsutsuki"),
        ("One Piece", "a ilha final da Grand Line onde Gol D. Roger deixou o grande tesouro", "Laugh Tale"),
        ("Demon Slayer", "o nome da flor rara que Muzan Kibutsuji procurou por mil anos para vencer o sol", "Lírio da Aranha Azul"),
        ("Jujutsu Kaisen", "o feiticeiro milenar que possui o corpo de Suguru Geto usando pontos na testa", "Kenjaku"),
        ("Death Note", "o nome verdadeiro completo de L revelado na enciclopédia oficial", "L Lawliet"),
        ("Hunter x Hunter", "o jogo de tabuleiro estratégico em que o Rei Meruem nunca venceu Komugi", "Gungi"),
        ("Fullmetal Alchemist", "a data gravada dentro do relógio de bolso de prata de Edward Elric", "Don't Forget 3.Oct.11 (Não esqueça 3 de outubro de 1911)"),
        ("Neon Genesis Evangelion", "o nome do comandante da NERV e pai de Shinji Ikari", "Gendo Ikari"),
        ("Cavaleiros do Zodíaco", "o Cavaleiro de Ouro de Gêmeos que assumiu o lugar do Grande Mestre", "Saga de Gêmeos"),
        ("Monster", "o nome do neurocirurgião japonês que salvou a vida do menino Johan Liebert", "Dr. Kenzo Tenma"),
        ("Berserk", "o nome do artefato em forma de rosto vermelho que ativa a Mão de Deus no Eclipse", "Behelit Carmesim (O Ovo do Rei)")
    ]

    # --------------------------------------------------------------------------
    # DEMAIS TEMAS (100 PERGUNTAS CADA)
    # --------------------------------------------------------------------------
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
            "🟢 Fácil": montar_100_perguntas(animes_facil, tpl_padrao),
            "🟡 Normal": montar_100_perguntas(animes_normal, tpl_padrao),
            "🟠 Hard": montar_100_perguntas(animes_hard, tpl_padrao),
            "🔴 Impossível": montar_100_perguntas(animes_impossivel, tpl_padrao)
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

st.set_page_config(
    page_title=config.get("titulo_aba", "Super Quiz"),
    page_icon=config.get("icone_aba", "🎲"),
    layout="wide"
)

# ==============================================================================
# GERADOR DE CSS DINÂMICO (CENTRALIZAÇÃO TOTAL)
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
    larg_max = config.get("largura_botao", 520)
    
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
        audio {{
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }}
        .placar-topo {{
            font-size: {config['tam_fonte_placar']}px !important;
            font-weight: bold !important;
            color: {paleta['cor_destaque']} !important;
            text-align: center !important;
            display: block !important;
            width: 100% !important;
        }}
        .placar-alerta {{
            font-size: {config['tam_fonte_placar'] + 2}px !important;
            font-weight: bold !important;
            color: #FF4B4B !important;
            text-align: center !important;
            display: block !important;
            width: 100% !important;
        }}
        .badge-wrapper {{
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin: 12px auto !important;
            text-align: center !important;
        }}
        .badge-modo {{
            background-color: {paleta['cor_botao']};
            color: {paleta['cor_destaque']};
            padding: 8px 22px;
            border-radius: 25px;
            border: 2px solid {paleta['cor_destaque']};
            font-weight: bold;
            font-size: 19px;
            display: inline-block;
            text-align: center !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .main-card {{
            background-color: {paleta['cor_card']};
            padding: 28px;
            border-radius: 14px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.45);
            margin-bottom: 22px;
            border: 2px solid {paleta['cor_borda_botao']};
            text-align: center !important;
        }}
        .main-card h3 {{
            font-size: {config['tam_fonte_pergunta']}px !important;
            line-height: 1.4 !important;
            color: {paleta['cor_texto']} !important;
            margin: 0 !important;
            text-align: center !important;
        }}
        div[data-testid="stTextInput"], div[data-testid="stSelectbox"] {{
            max-width: {larg_max}px !important;
            width: 100% !important;
            margin: 0 auto 12px auto !important;
        }}
        div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label {{
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            text-align: center !important;
            font-size: 18px !important;
            font-weight: bold !important;
            margin-bottom: 6px !important;
        }}
        div[data-testid="stTextInput"] label p, div[data-testid="stSelectbox"] label p {{
            font-size: 18px !important;
            font-weight: bold !important;
            text-align: center !important;
            width: 100% !important;
        }}
        div[data-testid="stTextInput"] input {{
            text-align: center !important;
            font-size: 20px !important;
            font-weight: 600 !important;
        }}
        .stRadio div[role="radiogroup"] label div p {{
            font-size: {config['tam_fonte_opcoes']}px !important;
            font-weight: 700 !important;
            color: {paleta['cor_texto']} !important;
        }}
        .stRadio div[role="radiogroup"] label {{
            padding: 10px 0px !important;
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
            padding: {config['altura_botao']}px !important;
            border: 2px solid {paleta['cor_borda_botao']} !important;
            font-size: {config['tam_fonte_botao']}px !important;
            display: block !important;
            margin: 8px auto !important;
            text-align: center !important;
            transition: all 0.2s ease !important;
        }}
        div.stButton > button:hover, [data-testid="stButton"] > button:hover {{
            filter: brightness(1.2) !important;
            border-color: {paleta['cor_destaque']} !important;
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
            font-size: {config['tam_fonte_botao'] + 2}px !important;
            max-width: {larg_max}px !important;
            width: 100% !important;
            margin: 10px auto !important;
            box-shadow: 0 0 20px rgba(244, 211, 94, 0.7) !important;
        }}
        .st-key-sair_sis button {{
            background-color: #E74C3C !important;
            border: none !important;
            color: #FFFFFF !important;
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
    
    largura = largura_custom if largura_custom is not None else config.get("tamanho_imagem", 360)
    borda = borda_custom if borda_custom is not None else config.get("borda_imagem", 14)
    titulo_topo = config.get("titulos_temas", {}).get(modo, info["titulo_card"])
    arq_img = info["img_padrao"]

    html_bloco = "<div style='text-align: center; width: 100%; display: flex; flex-direction: column; align-items: center;'>"
    if titulo_topo.strip():
        html_bloco += f"<h3 style='margin-bottom: 14px; color: {info['cor_texto']}; text-align: center;'>{titulo_topo}</h3>"

    if os.path.exists(arq_img):
        try:
            with open(arq_img, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            html_bloco += (
                f"<img src='data:image/png;base64,{b64_img}' "
                f"style='width: {largura}px; max-width: 100%; height: auto; "
                f"margin: 0 auto; display: block; border-radius: {borda}px; "
                f"border: 3px solid {info['cor_destaque']}; "
                f"box-shadow: 0 8px 25px rgba(0,0,0,0.5);' />"
            )
        except Exception:
            pass
    else:
        html_bloco += (
            f"<div style='width: {largura}px; max-width: 100%; min-height: 330px; margin: 0 auto; "
            f"background: radial-gradient(circle at top, {info['cor_botao']} 0%, {info['cor_card']} 60%, {info['cor_fundo']} 100%); "
            f"border-radius: {borda}px; border: 3px solid {info['cor_destaque']}; "
            f"box-shadow: 0 10px 28px rgba(0,0,0,0.55); display: flex; flex-direction: column; "
            f"align-items: center; justify-content: center; padding: 28px 20px; box-sizing: border-box;'>"
            f"<div style='font-size: 115px; line-height: 1.1; margin-bottom: 16px; filter: drop-shadow(0 6px 12px rgba(0,0,0,0.4));'>{info['icone']}</div>"
            f"<div style='font-size: 26px; font-weight: 800; color: {info['cor_destaque']}; margin-bottom: 10px; text-align: center;'>{modo}</div>"
            f"<div style='font-size: 16px; color: {info['cor_texto']}; opacity: 0.9; text-align: center; line-height: 1.4;'>{info['sub_card']}</div>"
            f"</div>"
        )

    html_bloco += "</div>"
    st.markdown(html_bloco, unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES DE DADOS (COM SUPORTE A NÍVEIS EM IGREJA, HERÓIS, DESENHOS E ANIMES)
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
                # Verifica a flag v4 (que inclui os 4 níveis de Super-Heróis)
                if not dados.get("niveis_dificuldade_v4", False):
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
        "niveis_dificuldade_v4": True,
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
            background: radial-gradient(circle, {paleta['cor_card']} 0%, {paleta['cor_fundo']} 90%);
            border: 3px solid {'#2ECC71' if (numero_final and not animar) else paleta['cor_destaque']};
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
    components.html(html_code, height=345)

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
    "nivel_gerir_selecionado": "🟢 Fácil", "tema_img_cfg": "⛪ Igreja", "limpar_tela_jogo": False
}
for chave, valor_padrao in estados_iniciais.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor_padrao

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
# 2. SELECIONAR PARTICIPANTE + MODO + DIFICULDADE (IGREJA, HERÓIS, DESENHOS E ANIMES!)
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    slot_jogo.empty()
    slot_outros.empty()
    with slot_selecao.container():
        st.markdown("<h2 style='text-align: center; margin-bottom: 25px;'>👤 Participante & Modo de Jogo</h2>", unsafe_allow_html=True)
        
        col_esq, col_dir = st.columns([1.8, 1.2])
        
        with col_esq:
            nome_digitado = st.text_input("1️⃣ Digite o nome do Participante:", key="input_nome_part_sel")
            escolha_lista = st.selectbox(
                "Ou escolha da lista cadastrada:",
                ["-- Selecione da lista --"] + participantes,
                key="sel_lista_part_sel"
            ) if participantes else "-- Selecione da lista --"
            
            st.write("")
            idx_modo_atual = LISTA_MODOS_JOGO.index(st.session_state.modo_jogo_ativo) if st.session_state.modo_jogo_ativo in LISTA_MODOS_JOGO else 0
            modo_escolhido = st.selectbox(
                "2️⃣ Escolha o Modo de Jogo (A cor da tela e a imagem à direita mudam na hora!):",
                LISTA_MODOS_JOGO,
                index=idx_modo_atual,
                key="sel_modo_jogo_sel"
            )
            
            if modo_escolhido != st.session_state.modo_jogo_ativo:
                st.session_state.modo_jogo_ativo = modo_escolhido
                st.rerun()

            # SE FOR IGREJA, SUPER-HERÓIS, DESENHOS OU ANIMES, EXIBE O SELETOR DE DIFICULDADE!
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
                resumo_badge = f"🎯 {modo_escolhido} ({dif_escolhida}) — {qtd_disp} perguntas | ⭐ {pts_partida} pts/acerto"
                txt_botao_ini = f"▶️ Iniciar Quiz: {modo_escolhido} ({dif_escolhida})"
            else:
                dif_escolhida = None
                st.session_state.dificuldade_ativa = None
                pts_partida = pts_base_cfg
                if modo_escolhido == "🎲 Misturadão (Todos os Temas)":
                    qtd_disp = contar_todas_perguntas(bancos_perguntas)
                else:
                    qtd_disp = len(bancos_perguntas.get(modo_escolhido, []))
                resumo_badge = f"🎯 Tema selecionado: {modo_escolhido} — {qtd_disp} perguntas disponíveis!"
                txt_botao_ini = f"▶️ Iniciar Quiz: {modo_escolhido}"
                
            st.markdown(
                f"<div class='badge-wrapper'><div class='badge-modo'>{resumo_badge}</div></div>",
                unsafe_allow_html=True
            )
            
            st.write("")
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
        dif_atual = st.session_state.get("dificuldade_ativa")
        mult = MULTIPLICADOR_PONTOS.get(dif_atual, 1.0) if dif_atual else 1.0
        pts_acerto = int(config.get("pontos_por_acerto", 100) * mult)
        paleta = obter_paleta_ativa()
        
        if p_idx >= total_p:
            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
            ir_para_pagina("fim")

        if not st.session_state.respondido:
            tocar_audio_invisivel(SOM_TIC_TAK, loop=True)

        col_jogo_esq, col_jogo_dir = st.columns([2.1, 0.9])
        
        with col_jogo_dir:
            mostrar_painel_tema()

        with col_jogo_esq:
            p = st.session_state.perguntas_sessao[p_idx]
            tempo_total_fmt = formatar_tempo_partida(obter_tempo_decorrido())
            txt_dif_badge = f" ({dif_atual})" if dif_atual else ""
            
            st.markdown(
                f"<div class='badge-wrapper'><div class='badge-modo'>Modo: {st.session_state.modo_jogo_ativo}{txt_dif_badge} &nbsp;|&nbsp; Pergunta {p_idx + 1} de {total_p}</div></div>",
                unsafe_allow_html=True
            )
            
            c1, c2, c3, c4, c5 = st.columns([1.3, 0.9, 1.1, 0.9, 1.4])
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
                
                st.write("")
                if st.button("🚪 Parar e Finalizar Partida", key=f"sair_jogo_{p_idx}", use_container_width=True):
                    st.session_state.respondido = False
                    st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                    ir_para_pagina("fim")

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
                    st.success(f"🎉 Resposta CORRETA! (+{pts_acerto} pontos)")
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
                            f"<h3 style='text-align: center; color: {paleta['cor_destaque']};'>🏆 DADO PREMIADO LIBERADO ({st.session_state.acertos} ACERTOS)!<br>"
                            f"<span style='font-size: 20px; opacity: 0.85;'>Quer continuar respondendo o desafio ou encerrar para girar o dado agora?</span></h3>",
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
                
                st.write("")
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
        st.markdown(f"<h3 style='text-align: center; opacity: 0.85;'>{st.session_state.participante} ({st.session_state.modo_jogo_ativo}{dif_str}) — {config['txt_sub_dado']}</h3>", unsafe_allow_html=True)
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
                st.write("")
                
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
        st.markdown(f"<h2 style='text-align: center;'>Participante: {st.session_state.participante} ({modo_fim}{dif_str})</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<h3 style='text-align: center; color: {paleta['cor_destaque']};'>"
            f"⭐ {st.session_state.pontuacao} Pontos &nbsp;|&nbsp; "
            f"✅ {st.session_state.total_acertos_partida} Acertos &nbsp;|&nbsp; "
            f"❌ {st.session_state.total_erros_partida} Erros &nbsp;|&nbsp; "
            f"🎯 {precisao}% Precisão &nbsp;|&nbsp; "
            f"⏱️ Tempo: {tempo_final_fmt}"
            f"</h3>",
            unsafe_allow_html=True
        )
        st.write("")
        
        mostrar_painel_tema(modo_especifico=modo_fim)
        
        frase_do_tema = config.get("msgs_finais_temas", {}).get(modo_fim, INFO_MODOS[modo_fim]["msg_final"])
        st.markdown(
            f"<p style='text-align: center; font-style: italic; font-size: 24px; font-weight: 600; "
            f"color: {paleta['cor_destaque']} !important; margin-top: 18px;'>{frase_do_tema}</p>",
            unsafe_allow_html=True
        )
        st.write("")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
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
                col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
                with col_p2:
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
            
            st.write("")
            col_h1, col_h2 = st.columns([1, 1])
            with col_h1:
                if itens_para_apagar and st.button("🗑️ Apagar Selecionados"):
                    for it in itens_para_apagar:
                        historico.remove(it)
                    salvar_dados(bancos_perguntas, participantes, historico)
                    st.rerun()
            with col_h2:
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
        st.markdown("<h2 style='text-align: center;'>📝 Gestão de Perguntas por Tema & Dificuldade (2.100 Perguntas)</h2>", unsafe_allow_html=True)
        
        col_topo_esq, col_topo_meio, col_topo_dir = st.columns([1, 1, 1])
        with col_topo_esq:
            if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_topo", use_container_width=True):
                st.session_state.editando_idx = None
                st.session_state.modo_jogo_ativo = None
                ir_para_pagina("menu")
        with col_topo_meio:
            if st.button("➕ Nova Pergunta neste Banco", key="btn_nova_perg_topo", use_container_width=True):
                st.session_state.editando_idx = -1
                st.rerun()
        with col_topo_dir:
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

        st.write("")
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
        st.markdown("<h2 style='text-align: center;'>⚙️ Painel de Configurações (Imagens por Tema, Regras & Textos)</h2>", unsafe_allow_html=True)
        if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_cfg_topo"):
            st.session_state.msg_upload_ok = ""
            st.session_state.modo_jogo_ativo = None
            ir_para_pagina("menu")

        if st.session_state.msg_upload_ok:
            st.success(st.session_state.msg_upload_ok)
            st.session_state.msg_upload_ok = ""

        aba_img, aba_regras_tam, aba_textos, aba_sons = st.tabs([
            "🖼️ 1. Imagens & Frase de cada Tema",
            "🎯 2. Regras & Tamanhos",
            "✍️ 3. Textos do Menu",
            "🔊 4. Sons & Restauro"
        ])
        
        with aba_img:
            col_im1, col_im2 = st.columns([1.5, 1])
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
                st.markdown("<h4 style='text-align: center;'>🖼️ Pré-visualização da Coluna Direita</h4>", unsafe_allow_html=True)
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
                pts_acerto_val = st.number_input("Pontos Base por Acerto (Fácil=1x, Normal=1.5x, Hard=2.5x, Impossível=5x):", 10, 1000, int(config.get("pontos_por_acerto", 100)), 10)

            st.divider()
            st.markdown("<h3 style='text-align: center;'>📏 Ajuste de Tamanho de Letras e Botões</h3>", unsafe_allow_html=True)
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
        col_bot1, col_bot2 = st.columns([1, 1])
        with col_bot1:
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
                
        with col_bot2:
            if st.button("⬅️ Voltar ao Menu Principal", key="btn_voltar_cfg_rodape", use_container_width=True):
                st.session_state.msg_upload_ok = ""
                st.session_state.modo_jogo_ativo = None
                ir_para_pagina("menu")
