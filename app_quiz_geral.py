# ==============================================================================
# SUPER QUIZ MULTI-TEMAS - VERSÃO FINAL 100% CENTRALIZADA E LIMPA 🎲🏆✨
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
        "icone": "🎲", "titulo_card": "🌟 Desafio Misturadão", "sub_card": "Todas as 900 Perguntas Juntas num Só Jogo!",
        "img_padrao": "tema_misturadao.png",
        "msg_final": "Incrível! Você encarou o desafio supremo de todos os temas e provou que sabe de tudo um pouco! 🎲👑"
    }
}

# ==============================================================================
# GERADOR DE 900 PERGUNTAS NATURAIS (SEM PREFIXOS E SEM PARÊNTESES)
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

def construir_bancos_900():
    fatos_igreja = [
        ("o Dogma da Imaculada Conceição", "o ano em que foi proclamado pelo Papa Pio IX", "1854"),
        ("Nossa Senhora de Lourdes", "a jovem santa para quem ela apareceu na França", "Santa Bernadette"),
        ("Nossa Senhora de Fátima", "o país onde ocorreram as aparições em 1917", "Portugal"),
        ("Nossa Senhora Aparecida", "o rio onde a imagem milagrosa foi encontrada", "Rio Paraíba do Sul"),
        ("São Pedro", "a missão que ele recebeu diretamente de Jesus", "Primeiro Papa da Igreja"),
        ("São Francisco de Assis", "o título pelo qual é conhecido mundialmente", "Padroeiro dos Animais e da Ecologia"),
        ("o Batismo", "a sua importância na caminhada da fé", "Primeiro Sacramento da iniciação cristã"),
        ("a Eucaristia", "o sagrado mistério celebrado na Santa Missa", "Corpo e Sangue de Cristo"),
        ("o Natal", "o grande acontecimento celebrado em 25 de dezembro", "Nascimento de Jesus em Belém"),
        ("a Páscoa", "o acontecimento central da fé cristã", "Ressurreição de Jesus Cristo"),
        ("Pentecostes", "o evento celebrado 50 dias após a Páscoa", "Descida do Espírito Santo sobre os Apóstolos"),
        ("São Paulo Apóstolo", "o nome que ele tinha antes da sua conversão", "Saulo de Tarso"),
        ("Santa Teresinha do Menino Jesus", "o título espiritual da sua doutrina", "Doutora da Pequena Via"),
        ("São João Paulo II", "o país de origem deste santo Papa", "Polônia"),
        ("o Santo Rosário", "o conjunto de mistérios rezados na tradição mariana", "Gozosos, Luminosos, Dolorosos e Gloriosos"),
        ("a Quaresma", "o tempo de preparação espiritual antes da Páscoa", "40 dias de oração, jejum e caridade"),
        ("o Advento", "o período litúrgico de quatro semanas", "Preparação para a chegada do Natal"),
        ("São José", "a missão confiada por Deus na Sagrada Família", "Pai adotivo de Jesus e Esposo de Maria"),
        ("o Arcanjo São Gabriel", "a missão bíblica narrada no Evangelho de Lucas", "Anunciar a Maria que ela seria Mãe do Salvador"),
        ("São Miguel Arcanjo", "o significado do seu nome em hebraico", "Quem como Deus?"),
        ("o livro do Gênesis", "a posição que ocupa na Sagrada Escritura", "Primeiro livro da Bíblia"),
        ("o livro do Apocalipse", "a posição que ocupa no Novo Testamento", "Último livro da Bíblia"),
        ("os quatro Evangelistas", "os nomes dos autores dos Evangelhos canônicos", "Mateus, Marcos, Lucas e João"),
        ("Santa Rita de Cássia", "a devoção popular pela qual é invocada", "Santa das Causas Impossíveis"),
        ("Santo Antônio", "o título popular além de Doutor da Igreja", "Santo Casamenteiro e Padroeiro dos Pobres")
    ]
    tpl_igreja = [
        "Sobre {item}, qual alternativa indica corretamente {sub}?",
        "Qual das opções abaixo corresponde a {sub} em relação a {item}?",
        "Quando falamos sobre {item}, o que define corretamente {sub}?",
        "Assinale a alternativa verdadeira sobre {sub} referente a {item}:"
    ]

    fatos_herois = [
        ("o Homem de Ferro", "a identidade secreta do herói na Marvel", "Tony Stark"),
        ("o Batman", "a identidade secreta do protetor de Gotham", "Bruce Wayne"),
        ("o Homem-Aranha", "o nome do jovem fotógrafo por trás da máscara", "Peter Parker"),
        ("o Superman", "o nome terrestre adotado pelo herói em Metrópolis", "Clark Kent"),
        ("o Capitão América", "o soldado que recebeu o soro do supersoldado", "Steve Rogers"),
        ("a Mulher-Maravilha", "o nome da princesa guerreira de Themyscira", "Diana Prince"),
        ("o Hulk", "o cientista que se transforma ao ficar furioso", "Bruce Banner"),
        ("o deus Thor", "o nome do seu famoso martelo mágico", "Mjolnir"),
        ("o Pantera Negra", "o reino africano avançado que ele governa", "Wakanda"),
        ("o Wolverine", "o metal indestrutível que reveste suas garras", "Adamantium"),
        ("o herói Flash", "a identidade do velocista escarlate da Liga da Justiça", "Barry Allen"),
        ("o Aquaman", "o reino submerso que ele governa nos oceanos", "Atlântida"),
        ("o Lanterna Verde", "a fonte de poder usada pela Tropa espacial", "Anel do Poder movido pela força de vontade"),
        ("o Doutor Estranho", "o título místico que ele exerce para proteger a Terra", "Mago Supremo"),
        ("a Viúva Negra", "o nome verdadeiro da famosa espiã dos Vingadores", "Natasha Romanoff"),
        ("o Gavião Arqueiro", "a arma principal que ele domina com precisão absoluta", "Arco e flechas especiais"),
        ("o vilão Thanos", "o artefato usado para reunir as 6 Joias do Infinito", "Manopla do Infinito"),
        ("o vilão Coringa", "o super-herói que é seu maior arqui-inimigo", "Batman"),
        ("o vilão Lex Luthor", "o herói que ele tenta derrotar em Metrópolis", "Superman"),
        ("o Professor Xavier", "a famosa equipe de mutantes que ele fundou", "X-Men"),
        ("o Quarteto Fantástico", "o líder elástico conhecido como Sr. Fantástico", "Reed Richards"),
        ("o Deadpool", "o nome verdadeiro do mercenário tagarela", "Wade Wilson"),
        ("o Homem-Formiga", "o cientista que descobriu as partículas de encolhimento", "Hank Pym"),
        ("o herói Shazam", "a palavra mágica gritada por Billy Batson para se transformar", "SHAZAM!"),
        ("os Guardiões da Galáxia", "o líder humano conhecido como Senhor das Estrelas", "Peter Quill")
    ]
    tpl_herois = [
        "Sobre {item}, qual alternativa indica corretamente {sub}?",
        "Qual das opções abaixo revela {sub} em relação a {item}?",
        "Quando o assunto é {item}, qual é a resposta certa para {sub}?",
        "Marque a alternativa correta que representa {sub} de {item}:"
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
    tpl_frutas = [
        "Sobre {item}, qual alternativa indica corretamente {sub}?",
        "Qual das opções abaixo descreve {sub} em relação a {item}?",
        "Pensando nas características de {item}, qual opção responde {sub}?",
        "Assinale a alternativa correta sobre {sub} referente a {item}:"
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
    tpl_comidas = [
        "Na culinária, sobre {item}, qual opção indica {sub}?",
        "Qual alternativa descreve corretamente {sub} em relação a {item}?",
        "Quando preparamos ou saboreamos {item}, o que define {sub}?",
        "Marque a resposta certa sobre {sub} referente a {item}:"
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
    tpl_novelas = [
        "Sobre {item}, qual alternativa indica corretamente {sub}?",
        "Qual das opções abaixo corresponde a {sub} em {item}?",
        "Relembrando {item}, quem ou o que ficou marcado como {sub}?",
        "Assinale a opção verdadeira sobre {sub} em {item}:"
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
    tpl_filmes = [
        "No cinema, sobre {item}, qual alternativa indica {sub}?",
        "Qual das opções abaixo responde corretamente {sub} em {item}?",
        "Relembrando {item}, qual opção descreve {sub}?",
        "Marque a alternativa correta sobre {sub} referente a {item}:"
    ]

    fatos_desenhos = [
        ("o desenho Bob Esponja", "o formato da casa onde ele mora na Fenda do Biquíni", "Um abacaxi no fundo do mar"),
        ("o desenho Scooby-Doo", "o nome da van colorida usada pela turma para investigar mistérios", "Máquina de Mistério"),
        ("o clássico Tom e Jerry", "as espécies dos dois rivais dos desenhos animados", "Um gato doméstico e um ratinho esperto"),
        ("a série Os Simpsons", "a cidade norte-americana onde mora a família amarela", "Springfield"),
        ("As Meninas Superpoderosas", "os nomes das três irmãs criadas pelo Professor Utônio", "Florzinha, Lindinha e Docinho"),
        ("o clássico Pica-Pau", "a característica sonora mais famosa do personagem", "Sua risada inconfundível"),
        ("o coelho Pernalonga", "a frase clássica que ele diz enquanto mastiga uma cenoura", "O que que há, velhinho?"),
        ("o desenho Os Flintstones", "o período histórico em que vivem Fred Flintstone e Barney", "Idade da Pedra, na cidade de Bedrock"),
        ("o desenho Ben 10", "o dispositivo alienígena em formato de relógio preso ao pulso", "Omnitrix"),
        ("Os Padrinhos Mágicos", "os nomes do casal de fadas de cabelos rosa e verde de Timmy", "Cosmo e Wanda"),
        ("Hora de Aventura", "a dupla de protagonistas que vive na Terra de Ooo", "Finn, o humano, e Jake, o cão mágico"),
        ("o desenho Gravity Falls", "os irmãos gêmeos que passam o verão na Cabana do Mistério", "Dipper e Mabel Pines"),
        ("Avatar: A Lenda de Aang", "os quatro elementos da natureza dominados pelo Avatar", "Água, Terra, Fogo e Ar"),
        ("o desenho Phineas e Ferb", "o animal de estimação deles que atua como agente secreto", "Perry, o Ornitorrinco, conhecido como Agente P"),
        ("Coragem, o Cão Covarde", "o lugar isolado onde ele mora com Muriel e Eustácio", "Lugar Nenhum"),
        ("O Laboratório de Dexter", "a irmã mais velha que sempre invade e bagunça o laboratório", "Dee Dee"),
        ("os Jovens Titãs", "o líder da equipe que usa artes marciais e tecnologia", "Robin"),
        ("a Turma da Mônica", "o objeto inseparável que a Mônica usa para correr atrás do Cebolinha", "Coelhinho de pelúcia azul Sansão"),
        ("o Desenho do Chaves", "a comida favorita que o Chaves sempre sonha em comer na vila", "Sanduíche de presunto"),
        ("o marinheiro Popeye", "o alimento enlatado que lhe dá força instantânea nos músculos", "Espinafre"),
        ("o desenho Manda-Chuva", "o grupo de animais de rua que ele lidera no beco", "Gangue de gatos de Nova York"),
        ("a Corrida Maluca", "o vilão trapaceiro acompanhado pelo cachorro risonho Muttley", "Dick Vigarista"),
        ("os Ursinhos Carinhosos", "o poder especial disparado pela barriga dos ursinhos", "Raio de sentimentos e arco-íris"),
        ("a Caverna do Dragão", "o guia misterioso baixinho de manto vermelho que dá conselhos", "Mestre dos Magos"),
        ("o desenho Três Espiãs Demais", "os nomes das três amigas estudantes de Beverly Hills", "Sam, Clover e Alex")
    ]
    tpl_desenhos = [
        "Sobre {item}, qual alternativa indica corretamente {sub}?",
        "Qual das opções abaixo corresponde a {sub} em {item}?",
        "Quando assistimos a {item}, o que identifica {sub}?",
        "Assinale a opção correta sobre {sub} referente a {item}:"
    ]

    fatos_animes = [
        ("Dragon Ball Z", "a transformação lendária de cabelos dourados alcançada por Goku", "Super Saiyajin"),
        ("o anime Naruto", "o nome da raposa de nove caudas selada dentro do protagonista", "Kurama"),
        ("o anime One Piece", "o grande sonho de Monkey D. Luffy ao navegar pelos mares", "Encontrar o One Piece e ser o Rei dos Piratas"),
        ("o anime Solo Leveling", "o comando que Sung Jin-Woo usa para erguer seu exército de sombras", "Erga-se (Arise)"),
        ("o anime Bleach", "o nome da espada espiritual empunhada por Ichigo Kurosaki", "Zanpakuto Zangetsu"),
        ("Attack on Titan", "os nomes das três muralhas que protegiam a humanidade dos Titãs", "Muralhas Maria, Rose e Sina"),
        ("o anime Black Clover", "a característica única do protagonista Asta num mundo mágico", "Ele nasceu sem mana e usa Anti-Magia"),
        ("Tokyo Revengers", "a gangue de motoqueiros onde Takemichi tenta salvar o futuro", "Tokyo Manji (Toman)"),
        ("Mashle: Magia e Músculos", "o modo como Mash Burnedead supera os magos sem ter magia", "Com força física pura e treino muscular absurdo"),
        ("o anime do Slime (Tensura)", "a criatura em que o protagonista reencarna como Rimuru Tempest", "Um Slime azul superpoderoso"),
        ("Cyberpunk: Edgerunners", "o implante cibernético militar usado por David Martinez", "Sandevistan, que garante supervelocidade"),
        ("Demon Slayer", "o principal objetivo da jornada de Tanjiro Kamado", "Transformar sua irmã Nezuko de volta em humana"),
        ("Jujutsu Kaisen", "o feiticeiro de venda nos olhos conhecido como o mais forte", "Satoru Gojo"),
        ("o anime Death Note", "a regra principal do caderno sobrenatural de Light Yagami", "A pessoa cujo nome for escrito nele morre"),
        ("Os Cavaleiros do Zodíaco", "o golpe principal disparado por Seiya de Pégaso", "Meteoro de Pégaso"),
        ("o anime Pokémon", "o primeiro parceiro elétrico de Ash Ketchum da cidade de Pallet", "Pikachu"),
        ("Fullmetal Alchemist", "a lei fundamental da alquimia seguida pelos irmãos Elric", "Lei da Troca Equivalente"),
        ("My Hero Academia", "o poder passado de All Might para o jovem Izuku Midoriya", "One For All"),
        ("Hunter x Hunter", "a energia vital aprendida por Gon e Killua após o Exame Hunter", "Nen"),
        ("Yu Yu Hakusho", "a técnica espiritual disparada pela ponta do dedo de Yusuke", "Leigan"),
        ("o anime InuYasha", "a joia poderosa em pedaços procurada no Japão Feudal", "Joia de Quatro Almas"),
        ("One Punch Man", "a rotina de treino que deixou Saitama careca e invencível", "100 flexões, 100 abdominais, 100 agachamentos e 10 km por dia"),
        ("o anime Spy x Family", "o poder secreto da pequena Anya Forger", "Telepatia, lendo a mente das pessoas"),
        ("o anime Blue Lock", "o esporte competitivo que busca criar o maior atacante do Japão", "Futebol"),
        ("o anime Haikyuu!!", "a posição na quadra de vôlei em que o baixinho Hinata brilha", "Central de bloqueio com salto gigante")
    ]
    tpl_animes = [
        "Sobre {item}, qual alternativa indica corretamente {sub}?",
        "Qual das opções abaixo corresponde a {sub} em {item}?",
        "No universo de {item}, qual é a resposta certa para {sub}?",
        "Marque a opção correta que representa {sub} em {item}:"
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
    tpl_trabalhos = [
        "Na profissão de {item}, qual alternativa indica {sub}?",
        "Qual das opções abaixo descreve {sub} para um {item}?",
        "No dia a dia de um {item}, o que corresponde a {sub}?",
        "Assinale a alternativa correta sobre {sub} referente ao {item}:"
    ]

    return {
        "⛪ Igreja": montar_100_perguntas(fatos_igreja, tpl_igreja),
        "🦸 Super-Heróis": montar_100_perguntas(fatos_herois, tpl_herois),
        "🍎 Frutas": montar_100_perguntas(fatos_frutas, tpl_frutas),
        "🍔 Comidas": montar_100_perguntas(fatos_comidas, tpl_comidas),
        "📺 Novelas": montar_100_perguntas(fatos_novelas, tpl_novelas),
        "🎬 Filmes": montar_100_perguntas(fatos_filmes, tpl_filmes),
        "🎨 Desenhos": montar_100_perguntas(fatos_desenhos, tpl_desenhos),
        "⚔️ Animes": montar_100_perguntas(fatos_animes, tpl_animes),
        "💼 Trabalhos & Profissões": montar_100_perguntas(fatos_trabalhos, tpl_trabalhos)
    }

BANCOS_PADRAO = construir_bancos_900()
LISTA_MODOS_JOGO = list(BANCOS_PADRAO.keys()) + ["🎲 Misturadão (Todos os Temas)"]

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
        
        "titulo_aba": "Super Quiz 900 Perguntas",
        "icone_aba": "🎲",
        "txt_titulo_menu": "🎲 SUPER QUIZ MULTI-TEMAS (900 PERGUNTAS) 🎲",
        "txt_subtitulo_menu": "Escolha um dos 10 modos de jogo e desafie os seus conhecimentos! (F11 para tela cheia)",
        "txt_btn_jogar": "▶️ Jogar / Escolher Modo de Jogo",
        "txt_btn_participantes": "👥 Cadastrar Participantes",
        "txt_btn_perguntas": "📝 Gerir as 900 Perguntas por Tema",
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
# GERADOR DE CSS DINÂMICO (CENTRALIZAÇÃO TOTAL DE INPUTS, SELECTBOX, BADGES E BOTÕES)
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
        /* ETIQUETA DE TEMA 100% CENTRALIZADA */
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
        /* CENTRALIZAR CAIXAS DE TEXTO E SELECTBOX */
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
        /* OPÇÕES DO RADIO BEM VISÍVEIS */
        .stRadio div[role="radiogroup"] label div p {{
            font-size: {config['tam_fonte_opcoes']}px !important;
            font-weight: 700 !important;
            color: {paleta['cor_texto']} !important;
        }}
        .stRadio div[role="radiogroup"] label {{
            padding: 10px 0px !important;
        }}
        /* CENTRALIZAÇÃO ABSOLUTA DE TODOS OS BOTÕES */
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
        .st-key-btn_ir_dado, .st-key-btn_ir_dado > div {{
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            margin: 0 auto !important;
        }}
        .st-key-btn_ir_dado button {{
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
# IMAGEM DINÂMICA DA COLUNA DIREITA (FOTO REAL OU PÔSTER ESPECIAL DO TEMA!)
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
# FUNÇÕES DE DADOS E ATUALIZAÇÃO AUTOMÁTICA DAS PERGUNTAS LIMPAS
# ==============================================================================
def carregar_dados():
    bancos_atuais = {k: list(v) for k, v in BANCOS_PADRAO.items()}
    participantes_atuais = []
    historico_atual = []
    precisa_salvar = False
    
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                # Se for uma versão anterior sem a flag de perguntas limpas, atualiza os textos mantendo participantes e histórico!
                if not dados.get("perguntas_limpas_v2", False):
                    precisa_salvar = True
                elif "bancos_perguntas" in dados and isinstance(dados["bancos_perguntas"], dict):
                    for k, lista_p in dados["bancos_perguntas"].items():
                        if k in BANCOS_PADRAO and len(lista_p) < 10:
                            bancos_atuais[k] = list(BANCOS_PADRAO[k])
                            precisa_salvar = True
                        else:
                            bancos_atuais[k] = lista_p
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
        "perguntas_limpas_v2": True,
        "bancos_perguntas": bancos_perguntas,
        "participantes": participantes,
        "historico": historico
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

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
    """Extrai as 5 maiores pontuações registadas no histórico para exibir o Pódio."""
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
    "pergunta_idx": 0, "pontuacao": 0, "acertos": 0,
    "total_acertos_partida": 0, "total_erros_partida": 0,
    "inicio_partida": None, "tempo_final_congelado": None, "perguntas_sessao": [],
    "respondido": False, "ultima_resposta_correta": None, "dado_girado": False,
    "resultado_dado": None, "editando_idx": None, "tempo_restante": 30,
    "baloes_mostrados": False, "dado_disponivel": False, "historico_salvo_partida": False,
    "up_cnt": 0, "msg_upload_ok": "", "tema_gerir_selecionado": "⛪ Igreja",
    "tema_img_cfg": "⛪ Igreja"
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

# Container Mestre para limpar completamente o DOM entre trocas de ecrã (elimina fantasmas!)
tela_mestre = st.empty()

def ir_para_pagina(nova_pagina):
    st.session_state.pagina = nova_pagina
    tela_mestre.empty()
    st.rerun()

# ==============================================================================
# 1. MENU PRINCIPAL
# ==============================================================================
if st.session_state.pagina == "menu":
    with tela_mestre.container():
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
# 2. SELECIONAR PARTICIPANTE + MODO (100% CENTRALIZADO!)
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    with tela_mestre.container():
        st.markdown("<h2 style='text-align: center; margin-bottom: 25px;'>👤 Participante & Modo de Jogo</h2>", unsafe_allow_html=True)
        
        # Proporção exclusiva [1.8, 1.2] diferente da tela de jogo para nunca misturar elementos
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
                
            if modo_escolhido == "🎲 Misturadão (Todos os Temas)":
                qtd_disp = sum(len(v) for v in bancos_perguntas.values())
            else:
                qtd_disp = len(bancos_perguntas.get(modo_escolhido, []))
                
            # Etiqueta perfeitamente centralizada!
            st.markdown(
                f"<div class='badge-wrapper'><div class='badge-modo'>🎯 Tema selecionado: {modo_escolhido} — {qtd_disp} perguntas disponíveis!</div></div>",
                unsafe_allow_html=True
            )
            
            st.write("")
            if st.button(f"▶️ Iniciar Quiz: {modo_escolhido}", key="btn_ir_dado", use_container_width=True):
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
                        for tema_k, lista_t in bancos_perguntas.items():
                            lista_base.extend(lista_t)
                    else:
                        lista_base = list(bancos_perguntas.get(modo_escolhido, []))
                        
                    if not lista_base:
                        st.error("Este tema ainda não possui perguntas cadastradas!")
                    else:
                        st.session_state.participante = nome_final
                        st.session_state.modo_jogo_ativo = modo_escolhido
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
                        ir_para_pagina("jogo")
                else:
                    st.warning("⚠️ Por favor, digite ou selecione o nome do participante!")
                    
            if st.button("⬅️ Voltar ao Menu", key="btn_voltar_sel_part", use_container_width=True):
                st.session_state.modo_jogo_ativo = None
                ir_para_pagina("menu")

        with col_dir:
            mostrar_painel_tema(modo_especifico=modo_escolhido)

# ==============================================================================
# 3. TELA DO JOGO (ISOLADA E SEM ELEMENTOS FANTASMAS!)
# ==============================================================================
elif st.session_state.pagina == "jogo":
    with tela_mestre.container():
        p_idx = st.session_state.pergunta_idx
        total_p = len(st.session_state.perguntas_sessao)
        meta_dado = config.get("acertos_para_dado", 3)
        pts_acerto = config.get("pontos_por_acerto", 100)
        paleta = obter_paleta_ativa()
        
        if p_idx >= total_p:
            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
            ir_para_pagina("fim")

        if not st.session_state.respondido:
            tocar_audio_invisivel(SOM_TIC_TAK, loop=True)

        # Proporção [2.1, 0.9] exclusiva da tela de jogo
        col_jogo_esq, col_jogo_dir = st.columns([2.1, 0.9])
        
        with col_jogo_dir:
            mostrar_painel_tema()

        with col_jogo_esq:
            p = st.session_state.perguntas_sessao[p_idx]
            tempo_total_fmt = formatar_tempo_partida(obter_tempo_decorrido())
            
            st.markdown(
                f"<div class='badge-wrapper'><div class='badge-modo'>Modo: {st.session_state.modo_jogo_ativo} &nbsp;|&nbsp; Pergunta {p_idx + 1} de {total_p}</div></div>",
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
                            f"<h3 style='text-align: center; color: {paleta['cor_destaque']};'>🏆 DADO PREMIADO LIBERADO ({st.session_state.acertos} ACERTOS)!<br>"
                            f"<span style='font-size: 20px; opacity: 0.85;'>Quer continuar respondendo o desafio ou girar o dado agora?</span></h3>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<h3 style='text-align: center; color: {paleta['cor_destaque']};'>🏆 Fim da sequência! Mas já garantiu o seu Dado Premiado! 🏆</h3>",
                            unsafe_allow_html=True
                        )
                    
                    if st.session_state.pergunta_idx + 1 < total_p:
                        if st.button("➡️ Próxima Pergunta (Continuar Desafio)", use_container_width=True):
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
                        st.session_state.pergunta_idx += 1
                        st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                        st.session_state.dado_girado = False
                        ir_para_pagina("dado")
                else:
                    if st.button("➡️ Próxima Pergunta", use_container_width=True):
                        st.session_state.respondido = False
                        st.session_state.pergunta_idx += 1
                        st.session_state.tempo_restante = config.get("tempo_pergunta", 30)
                        
                        if st.session_state.pergunta_idx >= total_p:
                            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                            ir_para_pagina("fim")
                        else:
                            st.rerun()
                
                st.write("")
                if st.button("🚪 Parar e Finalizar Partida", key="sair_jogo_resp", use_container_width=True):
                    st.session_state.respondido = False
                    st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                    ir_para_pagina("fim")

# ==============================================================================
# 4. SALA DO DADO PREMIADO
# ==============================================================================
elif st.session_state.pagina == "dado":
    with tela_mestre.container():
        st.markdown(f"<h1 style='text-align: center;'>{config['txt_sala_dado']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; opacity: 0.85;'>{st.session_state.participante} ({st.session_state.modo_jogo_ativo}) — {config['txt_sub_dado']}</h3>", unsafe_allow_html=True)
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
                        f"Modo: {st.session_state.modo_jogo_ativo} | "
                        f"Pontos: {st.session_state.pontuacao} | "
                        f"Acertos: {st.session_state.total_acertos_partida} | "
                        f"Erros: {st.session_state.total_erros_partida} | "
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
                
                if st.session_state.pergunta_idx < len(st.session_state.perguntas_sessao):
                    if st.button("▶️ Continuar Quiz (Próxima Pergunta)", use_container_width=True):
                        st.session_state.dado_girado = False
                        st.session_state.historico_salvo_partida = False
                        ir_para_pagina("jogo")
                        
                if st.button("🏁 Encerrar Partida e Ver Resumo Final", use_container_width=True):
                    st.session_state.dado_girado = False
                    st.session_state.tempo_final_congelado = obter_tempo_decorrido()
                    ir_para_pagina("fim")

# ==============================================================================
# 5. TELA FINAL / AGRADECIMENTO (COM FRASE EXCLUSIVA DO TEMA E PRECISÃO!)
# ==============================================================================
elif st.session_state.pagina == "fim":
    with tela_mestre.container():
        modo_fim = obter_modo_visual_atual()
        paleta = obter_paleta_ativa()
        if st.session_state.tempo_final_congelado is None:
            st.session_state.tempo_final_congelado = obter_tempo_decorrido()
            
        tempo_final_fmt = formatar_tempo_partida(st.session_state.tempo_final_congelado)
        total_resp = st.session_state.total_acertos_partida + st.session_state.total_erros_partida
        precisao = int((st.session_state.total_acertos_partida / total_resp) * 100) if total_resp > 0 else 0
        
        if not st.session_state.historico_salvo_partida:
            reg_final = (
                f"Participante: {st.session_state.participante} | "
                f"Modo: {modo_fim} | "
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
        st.markdown(f"<h2 style='text-align: center;'>Participante: {st.session_state.participante} ({modo_fim})</h2>", unsafe_allow_html=True)
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
        
        # Frase Final personalizada especificamente para o modo de jogo escolhido!
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
    with tela_mestre.container():
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
    with tela_mestre.container():
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
# 8. GERIR / EDITAR AS 900 PERGUNTAS SEPARADAS POR TEMA
# ==============================================================================
elif st.session_state.pagina == "gerir_perguntas":
    with tela_mestre.container():
        st.markdown("<h2 style='text-align: center;'>📝 Gestão de Perguntas por Modo de Jogo (900 Perguntas)</h2>", unsafe_allow_html=True)
        
        col_topo_esq, col_topo_meio, col_topo_dir = st.columns([1, 1, 1])
        with col_topo_esq:
            if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_topo", use_container_width=True):
                st.session_state.editando_idx = None
                st.session_state.modo_jogo_ativo = None
                ir_para_pagina("menu")
        with col_topo_meio:
            if st.button("➕ Nova Pergunta neste Tema", key="btn_nova_perg_topo", use_container_width=True):
                st.session_state.editando_idx = -1
                st.rerun()
        with col_topo_dir:
            if st.button("🔄 Restaurar 100 Perguntas deste Tema", key="btn_reset_tema", use_container_width=True):
                tema_atual = st.session_state.tema_gerir_selecionado
                bancos_perguntas[tema_atual] = list(BANCOS_PADRAO[tema_atual])
                salvar_dados(bancos_perguntas, participantes, historico)
                st.success(f"As 100 perguntas de {tema_atual} foram restauradas!")
                st.rerun()

        st.write("")
        temas_disponiveis = list(BANCOS_PADRAO.keys())
        idx_t = temas_disponiveis.index(st.session_state.tema_gerir_selecionado) if st.session_state.tema_gerir_selecionado in temas_disponiveis else 0
        tema_sel_gerir = st.selectbox("📂 Selecione o Banco de Dados / Modo de Jogo para ver ou editar:", temas_disponiveis, index=idx_t)
        
        if tema_sel_gerir != st.session_state.tema_gerir_selecionado:
            st.session_state.tema_gerir_selecionado = tema_sel_gerir
            st.session_state.modo_jogo_ativo = tema_sel_gerir
            st.session_state.editando_idx = None
            st.rerun()

        perguntas_do_tema = bancos_perguntas.get(tema_sel_gerir, [])

        if st.session_state.editando_idx is not None:
            idx_edit = st.session_state.editando_idx
            is_novo = (idx_edit == -1)
            
            titulo_form = f"Adicionar Nova Pergunta em {tema_sel_gerir}" if is_novo else f"Editar Pergunta #{idx_edit + 1} ({tema_sel_gerir})"
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
        st.markdown(f"<h3 style='text-align: center;'>📋 Perguntas de {tema_sel_gerir} ({len(perguntas_do_tema)} cadastradas)</h3>", unsafe_allow_html=True)
        
        busca_txt = st.text_input("🔍 Filtrar / Pesquisar pergunta neste tema:", "")
        
        for idx, item in enumerate(perguntas_do_tema):
            if busca_txt.strip().lower() in item["pergunta"].lower() or busca_txt.strip().lower() in item["resposta"].lower():
                col_txt, col_edit, col_del = st.columns([5, 1, 1])
                with col_txt:
                    st.write(f"**{idx+1}. {item['pergunta']}** *(Resp: {item['resposta']})*")
                with col_edit:
                    if st.button("✏️", key=f"edit_p_{tema_sel_gerir}_{idx}"):
                        st.session_state.editando_idx = idx
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_p_{tema_sel_gerir}_{idx}"):
                        perguntas_do_tema.pop(idx)
                        bancos_perguntas[tema_sel_gerir] = perguntas_do_tema
                        salvar_dados(bancos_perguntas, participantes, historico)
                        st.rerun()

# ==============================================================================
# 9. CONFIGURAÇÕES SIMPLIFICADAS E DIRETAS (COM FRASES FINAIS POR TEMA!)
# ==============================================================================
elif st.session_state.pagina == "configuracoes":
    with tela_mestre.container():
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
                pts_acerto_val = st.number_input("Pontos ganhos por Acerto:", 10, 1000, int(config.get("pontos_por_acerto", 100)), 10)

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
            if st.button("🔄 Restaurar Todas as Configurações e as 900 Perguntas", key="btn_restaurar_orig"):
                salvar_config(obter_config_padrao())
                salvar_dados(construir_bancos_900(), participantes, historico)
                st.session_state.up_cnt += 1
                st.session_state.msg_upload_ok = "🔄 Configurações e banco de 900 perguntas restaurados com sucesso!"
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
