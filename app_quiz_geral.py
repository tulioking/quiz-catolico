# ==============================================================================
# SUPER QUIZ MULTI-TEMAS (900 PERGUNTAS + CORES CAMALEÃO POR MODO) 🎲🎨🚀
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
# PALETAS DE CORES AUTOMÁTICAS PARA CADA MODO DE JOGO
# ==============================================================================
CORES_POR_MODO = {
    "⛪ Igreja": {
        "cor_fundo": "#0B2545", "cor_card": "#134074", "cor_texto": "#FFFFFF",
        "cor_destaque": "#F4D35E", "cor_botao": "#134074", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#1F618D"
    },
    "🦸 Super-Heróis": {
        "cor_fundo": "#0A1128", "cor_card": "#1C2541", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFD166", "cor_botao": "#B80C09", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#FFD166"
    },
    "🍎 Frutas": {
        "cor_fundo": "#1B4332", "cor_card": "#2D6A4F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFD166", "cor_botao": "#40916C", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#95D5B2"
    },
    "🍔 Comidas": {
        "cor_fundo": "#370617", "cor_card": "#6A040F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FFBA08", "cor_botao": "#9D0208", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#F48C06"
    },
    "📺 Novelas": {
        "cor_fundo": "#3C096C", "cor_card": "#5A189A", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FF9E00", "cor_botao": "#7B2CBF", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#E0AAFF"
    },
    "🎬 Filmes": {
        "cor_fundo": "#121212", "cor_card": "#1F1F1F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#D4AF37", "cor_botao": "#292929", "cor_texto_botao": "#D4AF37", "cor_borda_botao": "#D4AF37"
    },
    "🎨 Desenhos": {
        "cor_fundo": "#003049", "cor_card": "#00507A", "cor_texto": "#FFFFFF",
        "cor_destaque": "#FCBF49", "cor_botao": "#F77F00", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#FCBF49"
    },
    "⚔️ Animes": {
        "cor_fundo": "#10002B", "cor_card": "#240046", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00F5D4", "cor_botao": "#7209B7", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#F72585"
    },
    "💼 Trabalhos & Profissões": {
        "cor_fundo": "#1B263B", "cor_card": "#283845", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00B4D8", "cor_botao": "#415A77", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#90E0EF"
    },
    "🎲 Misturadão (Todos os Temas)": {
        "cor_fundo": "#1F1147", "cor_card": "#341F6F", "cor_texto": "#FFFFFF",
        "cor_destaque": "#00F5D4", "cor_botao": "#4E2A84", "cor_texto_botao": "#FFFFFF", "cor_borda_botao": "#00F5D4"
    }
}

# ==============================================================================
# GERADOR AUTOMÁTICO DE 900 PERGUNTAS (100 POR CATEGORIA)
# ==============================================================================
def montar_100_perguntas(fatos, templates):
    """Gera exatamente 100 perguntas variadas e únicas a partir de uma matriz de fatos reais."""
    todas_respostas = list(dict.fromkeys([f[2] for f in fatos]))
    perguntas_geradas = []
    rng = random.Random(42)
    
    for idx in range(100):
        item, sub, certa = fatos[idx % len(fatos)]
        Ciclo = idx // len(fatos)
        molde = templates[Ciclo % len(templates)]
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
    # 1. IGREJA (25 fatos x 4 variações = 100 perguntas)
    fatos_igreja = [
        ("o Dogma da Imaculada Conceição", "proclamado pelo Papa Pio IX", "1854"),
        ("Nossa Senhora de Lourdes", "a jovem vidente na França", "Santa Bernadette"),
        ("Nossa Senhora de Fátima", "o país das aparições em 1917", "Portugal"),
        ("Nossa Senhora Aparecida", "o rio onde a imagem foi encontrada", "Rio Paraíba do Sul"),
        ("São Pedro", "a função recebida diretamente de Jesus", "Primeiro Papa da Igreja"),
        ("São Francisco de Assis", "o título pelo qual é conhecido mundialmente", "Padroeiro dos Animais e da Ecologia"),
        ("o Batismo", "o significado na vida cristã", "Primeiro Sacramento da iniciação cristã"),
        ("a Eucaristia", "o mistério celebrado na Santa Missa", "Corpo e Sangue de Cristo"),
        ("o Natal", "a celebração litúrgica de 25 de dezembro", "Nascimento de Jesus em Belém"),
        ("a Páscoa", "o acontecimento central da fé cristã", "Ressurreição de Jesus Cristo"),
        ("Pentecostes", "o evento celebrado 50 dias após a Páscoa", "Descida do Espírito Santo sobre os Apóstolos"),
        ("São Paulo Apóstolo", "o nome que tinha antes da sua conversão", "Saulo de Tarso"),
        ("Santa Teresinha do Menino Jesus", "o título espiritual da sua doutrina", "Doutora da Pequena Via"),
        ("São João Paulo II", "o país de origem deste santo Papa", "Polônia"),
        ("o Santo Rosário", "o conjunto de mistérios rezados na tradição mariana", "Gozosos, Luminosos, Dolorosos e Gloriosos"),
        ("a Quaresma", "o tempo de preparação espiritual antes da Páscoa", "40 dias de oração, jejum e caridade"),
        ("o Advento", "o período litúrgico de quatro semanas", "Preparação para a chegada do Natal"),
        ("São José", "a missão confiada por Deus na Sagrada Família", "Pai adotivo de Jesus e Esposo de Maria"),
        ("o Arcanjo São Gabriel", "a missão bíblica no Evangelho de Lucas", "Anunciar a Maria que ela seria Mãe do Salvador"),
        ("São Miguel Arcanjo", "o significado do seu nome hebraico", "Quem como Deus?"),
        ("o livro do Gênesis", "a posição que ocupa na Sagrada Escritura", "Primeiro livro da Bíblia"),
        ("o livro do Apocalipse", "a posição que ocupa no Novo Testamento", "Último livro da Bíblia"),
        ("os quatro Evangelistas", "os autores dos Evangelhos canônicos", "Mateus, Marcos, Lucas e João"),
        ("Santa Rita de Cássia", "a devoção popular pela qual é invocada", "Santa das Causas Impossíveis"),
        ("Santo Antônio", "o título popular além de Doutor da Igreja", "Santo Casamenteiro e Padroeiro dos Pobres")
    ]
    tpl_igreja = [
        "Na tradição e história católica, sobre {item} ({sub}), qual é a resposta correta?",
        "Conhecimentos da Fé: Qual alternativa corresponde corretamente a {item} ({sub})?",
        "Desafio Bíblico e Mariano: O que está diretamente ligado a {item} ({sub})?",
        "Pergunta dos Festejos: Assinale a opção verdadeira a respeito de {item} ({sub}):"
    ]

    # 2. SUPER-HERÓIS (25 fatos x 4 = 100 perguntas)
    fatos_herois = [
        ("Homem de Ferro", "identidade secreta nos quadrinhos", "Tony Stark"),
        ("Batman", "identidade secreta e protetor de Gotham", "Bruce Wayne"),
        ("Homem-Aranha", "jovem fotógrafo do Clarim Diário", "Peter Parker"),
        ("Superman", "nome de batismo na Terra e jornalista", "Clark Kent"),
        ("Capitão América", "soldado que recebeu o soro do supersoldado", "Steve Rogers"),
        ("Mulher-Maravilha", "princesa guerreira de Themyscira", "Diana Prince"),
        ("Hulk", "cientista exposto aos raios gama", "Bruce Banner"),
        ("Thor", "martelo mágico forjado pelos anões", "Mjolnir"),
        ("Pantera Negra", "nação africana rica em Vibranium", "Wakanda"),
        ("Wolverine", "metal indestrutível que reveste suas garras", "Adamantium"),
        ("Flash", "velocista escarlate da Liga da Justiça", "Barry Allen"),
        ("Aquaman", "reino submerso que ele governa nos oceanos", "Atlântida"),
        ("Lanterna Verde", "fonte de poder usada pela Tropa espacial", "Anel do Poder movido pela força de vontade"),
        ("Doutor Estranho", "título místico que protege a Terra", "Mago Supremo"),
        ("Viúva Negra", "nome verdadeiro da espiã russa dos Vingadores", "Natasha Romanoff"),
        ("Gavião Arqueiro", "arma principal usada com precisão absoluta", "Arco e flechas especiais"),
        ("Thanos", "artefato usado para reunir as 6 Joias do Infinito", "Manopla do Infinito"),
        ("Coringa", "maior arqui-inimigo que ele enfrenta nas histórias", "Batman"),
        ("Lex Luthor", "maior rival que ele tenta derrotar em Metrópolis", "Superman"),
        ("Professor Xavier", "equipe de mutantes que ele fundou", "X-Men"),
        ("Quarteto Fantástico", "líder elástico conhecido como Sr. Fantástico", "Reed Richards"),
        ("Deadpool", "nome verdadeiro do mercenário tagarela", "Wade Wilson"),
        ("Homem-Formiga", "cientista original que descobriu as partículas de encolhimento", "Hank Pym"),
        ("Shazam", "palavra mágica gritada por Billy Batson para se transformar", "SHAZAM!"),
        ("Guardiões da Galáxia", "líder humano conhecido como Senhor das Estrelas", "Peter Quill")
    ]
    tpl_herois = [
        "Universo dos Heróis: Em relação a {item} ({sub}), qual é a resposta certa?",
        "Quiz Marvel & DC: Qual alternativa identifica corretamente {item} ({sub})?",
        "Superpoderes em Ação: O que corresponde exatamente a {item} ({sub})?",
        "Desafio Geek: Sobre {item} ({sub}), marque a opção correta:"
    ]

    # 3. FRUTAS (25 fatos x 4 = 100 perguntas)
    fatos_frutas = [
        ("Abacaxi", "característica visual famosa no topo da fruta", "Possui uma coroa de folhas espinhosas"),
        ("Melancia", "composição nutricional para hidratação no verão", "Mais de 90% de água e polpa vermelha"),
        ("Banana", "mineral famoso que ajuda a evitar cãibras musculares", "Rica em Potássio"),
        ("Laranja", "nutriente famoso para fortalecer a imunidade", "Rica em Vitamina C"),
        ("Abacate", "prato mexicano famoso feito com sua polpa amassada", "Ingrediente principal do Guacamole"),
        ("Caju", "parte curiosa onde fica a verdadeira semente da fruta", "A castanha-de-caju na ponta externa"),
        ("Jabuticaba", "modo curioso como nasce na árvore brasileira", "Nasce grudada diretamente no tronco"),
        ("Coco", "líquido natural encontrado dentro da fruta verde", "Água de coco isotônica natural"),
        ("Morango", "detalhe botânico sobre seus pontinhos externos", "As sementes ficam do lado de fora"),
        ("Açaí", "região brasileira de onde essa palmeira é nativa", "Região Amazônica / Norte do Brasil"),
        ("Uva", "bebida milenar produzida a partir da sua fermentação", "Vinho e suco integral"),
        ("Manga", "variedade muito doce e sem fiapos famosa no Brasil", "Manga Tommy e Manga Palmer"),
        ("Mamão", "enzima natural que auxilia na digestão", "Papaína (ajuda no funcionamento intestinal)"),
        ("Maracujá", "efeito popularmente associado ao seu suco e folhas", "Propriedades calmantes e relaxantes"),
        ("Limão", "sabor característico devido à alta presença de ácido", "Ácido cítrico (sabor azedo refrescante)"),
        ("Maçã", "personagem de conto de fadas associada a esta fruta", "Branca de Neve"),
        ("Goiaba", "doce em barra tradicional feito com sua polpa", "Goiabada (par perfeito com queijo no Romeu e Julieta)"),
        ("Acerola", "destaque nutricional entre as frutas tropicais", "Altíssima concentração de Vitamina C"),
        ("Pequi", "bioma brasileiro onde é símbolo da culinária regional", "Cerrado brasileiro (cuidado com os espinhos internos)"),
        ("Pitaya", "apelido exótico pelo formato da casca escamosa", "Fruta-do-Dragão"),
        ("Kiwi", "aparência da casca e da polpa interna", "Casca marrom peluda e polpa verde brilhante"),
        ("Carambola", "formato geométrico quando cortada em fatias", "Formato de estrela de cinco pontas"),
        ("Jaca", "recorde entre as frutas que nascem em árvores", "Uma das maiores e mais pesadas frutas de árvore"),
        ("Tâmara", "região do mundo onde é cultivada há milênios", "Desertos do Oriente Médio e Norte da África"),
        ("Romã", "tradição popular de fim de ano associada às suas sementes", "Simboliza prosperidade e fartura")
    ]
    tpl_frutas = [
        "Quiz das Frutas: Sobre a fruta {item} ({sub}), qual é a alternativa correta?",
        "Natureza e Saúde: O que caracteriza perfeitamente a fruta {item} ({sub})?",
        "Pomar de Perguntas: Assinale o fato verdadeiro sobre {item} ({sub}):",
        "Curiosidade Frutícola: Quando falamos em {item} ({sub}), a resposta certa é:"
    ]

    # 4. COMIDAS (25 fatos x 4 = 100 perguntas)
    fatos_comidas = [
        ("Baião de Dois", "ingredientes principais desse clássico nordestino", "Arroz, feijão-de-corda (ou verde) e queijo coalho"),
        ("Feijoada Brasileira", "grão principal usado no preparo tradicional", "Feijão-preto com carnes salgadas"),
        ("Pamonha", "base agrícola ralada para fazer a massa", "Milho verde fresco"),
        ("Tapioca", "ingrediente extraído da mandioca para hidratar a goma", "Fécula / goma de mandioca (polvilho)"),
        ("Acarajé", "massa frita no azeite de dendê típica da Bahia", "Feijão-fradinho temperado com cebola"),
        ("Pão de Queijo", "estado brasileiro mundialmente famoso pela receita", "Minas Gerais"),
        ("Pizza Napolitana", "país europeu onde surgiu a receita clássica", "Itália"),
        ("Sushi", "base principal combinada com peixe fresco na culinária japonesa", "Arroz temperado com vinagre e alga nori"),
        ("Churrasco Gaúcho", "corte bovino com capa de gordura muito querido no Brasil", "Picanha na brasa"),
        ("Moqueca", "ingrediente principal cozido na panela de barro", "Peixe e frutos do mar com leite de coco ou azeite"),
        ("Brigadeiro", "ingredientes essenciais do doce mais famoso das festas", "Leite condensado, chocolate em pó e manteiga"),
        ("Coxinha", "recheio tradicional mais pedido nas lanchonetes", "Frango desfiado (muitas vezes com catupiry)"),
        ("Vatapá", "ingredientes que dão cremosidade ao prato", "Pão ou farinha, leite de coco, amendoim, castanha e camarão"),
        ("Carne de Sol com Macaxeira", "acompanhamento clássico nos restaurantes do Nordeste", "Manteiga da terra (manteiga de garrafa) e queijo coalho"),
        ("Lasanha à Bolonhesa", "camadas intercaladas com massa nesse prato italiano", "Molho de carne moída, presunto, queijo e molho branco"),
        ("Paella", "país europeu famoso por esse prato de arroz com frutos do mar", "Espanha"),
        ("Tacos e Burritos", "culinária tradicional da América do Norte onde são reis", "Culinária Mexicana"),
        ("Croissant", "país famoso por essa massa folhada em formato de meia-lua", "França"),
        ("Bacalhoada", "país europeu que eternizou as receitas com bacalhau e azeite", "Portugal"),
        ("Cuscuz Nordestino", "ingrediente amarelo hidratado e cozido na cuscuzeira", "Flocão de milho cozido no vapor"),
        ("Farofa", "ingrediente tostado na manteiga que acompanha o churrasco", "Farinha de mandioca ou de milho"),
        ("Pudim de Leite", "calda clássica que cobre a forma antes de assar em banho-maria", "Calda de caramelo feita com açúcar derretido"),
        ("Strogonoff", "ingredientes que formam o molho rosado clássico no Brasil", "Creme de leite, ketchup/tomate e champignon"),
        ("Canjica / Mungunzá", "época festiva do ano em que esse prato de milho é tradição", "Festas Juninas (São João)"),
        ("Pastel de Feira", "bebida gelada que forma a dupla perfeita nas feiras livres", "Caldo de cana (Garapa)")
    ]
    tpl_comidas = [
        "Show de Gastronomia: Sobre o prato {item} ({sub}), qual é a resposta certa?",
        "Sabores da Cozinha: Qual alternativa descreve corretamente {item} ({sub})?",
        "Mestre Cuca: O que está diretamente associado a {item} ({sub})?",
        "Cardápio do Quiz: A respeito de {item} ({sub}), marque a opção correta:"
    ]

    # 5. NOVELAS (25 fatos x 4 = 100 perguntas)
    fatos_novelas = [
        ("Avenida Brasil", "vilã icônica interpretada por Adriana Esteves", "Carminha"),
        ("Senhora do Destino", "vilã famosa pelos memes da escada e por roubar Lindalva", "Nazaré Tedesco"),
        ("O Clone", "protagonista muçulmana que vivia um amor com Lucas", "Jade (Giovanna Antonelli)"),
        ("Vale Tudo", "grande mistério que parou o Brasil em 1988", "Quem matou Odete Roitman?"),
        ("Pantanal", "personagem mítica que se transforma em onça-pintada", "Juma Marruá"),
        ("O Rei do Gado", "famílias rivais italianas no início da trama", "Mezenga e Berdinazzi"),
        ("Chocolate com Pimenta", "protagonista dona da fábrica de chocolates em Ventura", "Ana Francisca (Mariana Ximenes)"),
        ("Alma Gêmea", "índia protagonista que reencarna após o amor com Rafael", "Serena (Priscila Fantin)"),
        ("Mulheres de Areia", "irmãs gêmeas idênticas de personalidades opostas", "Ruth e Raquel (Glória Pires)"),
        ("A Viagem", "personagem revoltado que assombrava os vivos no Vale dos Suicidas", "Alexandre (Guilherme Fontes)"),
        ("Cravo e a Rosa", "casal que vivia brigando como cão e gato na década de 1920", "Petruchio e Catarina"),
        ("Caminho das Índias", "casal indiano separado pelas castas sociais", "Maya e Bahuan (e Raj)"),
        ("Terra Nostra", "imigrante italiano que se apaixona por Giuliana no navio", "Matteo (Thiago Lacerda)"),
        ("Laços de Família", "atitude emocionante de Camila durante o tratamento de leucemia", "Raspou os cabelos ao som de 'Love by Grace'"),
        ("Roque Santeiro", "viúva exuberante que nunca chegou a casar de verdade", "Viúva Porcina (Regina Duarte)"),
        ("Tieta", "protagonista que volta rica para Santana do Agreste", "Tieta do Agreste (Betty Faria)"),
        ("Da Cor do Pecado", "vilã loira obcecada pela fortuna de Afonso Lambertini", "Bárbara (Giovanna Antonelli)"),
        ("Cheias de Charme", "trio musical formado pelas três domésticas protagonistas", "As Empreguetes (Penha, Rosário e Cida)"),
        ("Totalmente Demais", "cantora de Chay Suede / vilã da revista de moda", "Carolina Castilho (Juliana Paes)"),
        ("A Usurpadora", "irmãs gêmeas mexicanas interpretadas por Gabriela Spanic", "Paola Bracho e Paulina Martins"),
        ("Maria do Bairro", "vilã dramática que gritava 'Maldita Marginal!'", "Soraya Montenegro"),
        ("Rebelde (RBD)", "colégio de elite onde os seis jovens formaram a banda", "Elite Way School"),
        ("Carrossel", "professora doce e querida pelos alunos da Escola Mundial", "Professora Helena"),
        ("Império", "apelido do protagonista José Alfredo vestido sempre de preto", "Comendador"),
        ("Verdades Secretas", "apelido da jovem modelo Arlete nas passarelas", "Angel")
    ]
    tpl_novelas = [
        "Quiz das Novelas: Na trama {item} ({sub}), qual é a resposta correta?",
        "Memória da TV: Qual alternativa corresponde ao clássico {item} ({sub})?",
        "Dramaturgia na Tela: Quem ou o que ficou marcado em {item} ({sub})?",
        "Vale a Pena Lembrar: Sobre a novela {item} ({sub}), assinale a opção certa:"
    ]

    # 6. FILMES (25 fatos x 4 = 100 perguntas)
    fatos_filmes = [
        ("Titanic", "casal protagonista interpretado por Leonardo DiCaprio e Kate Winslet", "Jack Dawson e Rose DeWitt Bukater"),
        ("Harry Potter", "escola de magia e bruxaria onde a saga acontece", "Hogwarts"),
        ("O Senhor dos Anéis", "pequeno hobbit encarregado de destruir o Um Anel", "Frodo Bolseiro"),
        ("Star Wars", "revelação famosa feita por Darth Vader a Luke Skywalker", "Eu sou o seu pai"),
        ("O Rei Leão", "filhote de leão herdeiro da Pedra do Rei", "Simba"),
        ("Toy Story", "dupla principal de brinquedos de Andy", "Xerife Woody e patrulheiro Buzz Lightyear"),
        ("Jurassic Park", "criaturas pré-históricas recriadas a partir de DNA no âmbar", "Dinossauros"),
        ("Matrix", "escolha de pílulas oferecida por Morpheus a Neo", "Pílula Azul ou Pílula Vermelha"),
        ("Avatar", "lua exuberante habitada pelo povo azul Na'vi", "Pandora"),
        ("De Volta para o Futuro", "carro transformado em máquina do tempo pelo Dr. Brown", "DeLorean"),
        ("O Poderoso Chefão", "sobrenome da família mafiosa liderada por Don Vito", "Família Corleone"),
        ("Velozes e Furiosos", "personagem de Vin Diesel que valoriza a 'família' acima de tudo", "Dominic Toretto"),
        ("Piratas do Caribe", "capitão excêntrico apaixonado pelo navio Pérola Negra", "Capitão Jack Sparrow"),
        ("Shrek", "melhor amigo falante que acompanha o ogro no pântano", "Burro Falante"),
        ("Frozen", "irmã mais velha com poderes mágicos de gelo e neve", "Rainha Elsa"),
        ("Procurando Nemo", "espécie de peixe laranja com listras brancas do protagonista", "Peixe-palhaço"),
        ("Tropa de Elite", "personagem imortalizado por Wagner Moura no BOPE", "Capitão Nascimento"),
        ("O Auto da Compadecida", "dupla de amigos nordestinos espertos e inseparáveis", "João Grilo e Chicó"),
        ("Cidade de Deus", "jovem morador que sonha em se tornar fotógrafo profissional", "Buscapé"),
        ("Central do Brasil", "profissão de Dora (Fernanda Montenegro) na estação de trem", "Escrevedora de cartas para pessoas analfabetas"),
        ("Forrest Gump", "frase clássica sobre a vida dita pelo protagonista no banco de praça", "A vida é como uma caixa de chocolates"),
        ("Gladiador", "general romano que se torna gladiador na arena do Coliseu", "Maximus Decimus Meridius"),
        ("Rocky, um Lutador", "esporte em que Rocky Balboa enfrenta Apollo Creed", "Boxe"),
        ("Homem-Aranha no Aranhaverso", "jovem do Brooklyn que assume o manto do herói", "Miles Morales"),
        ("Vingadores: Ultimato", "frase final dita por Tony Stark antes de estalar os dedos", "Eu sou o Homem de Ferro")
    ]
    tpl_filmes = [
        "Sessão de Cinema: No filme {item} ({sub}), qual é a resposta correta?",
        "Quiz de Hollywood & Cinema: O que se destaca em {item} ({sub})?",
        "Luz, Câmera, Ação: Assinale a opção certa sobre {item} ({sub}):",
        "Clássicos da Telona: Sobre a produção {item} ({sub}), a alternativa correta é:"
    ]

    # 7. DESENHOS (25 fatos x 4 = 100 perguntas)
    fatos_desenhos = [
        ("Bob Esponja", "formato da casa onde ele mora na Fenda do Biquíni", "Um abacaxi no fundo do mar"),
        ("Scooby-Doo", "nome da van colorida usada pela turma para investigar mistérios", "Máquina de Mistério"),
        ("Tom e Jerry", "espécies dos dois rivais clássicos dos desenhos animados", "Um gato doméstico e um ratinho esperto"),
        ("Os Simpsons", "cidade norte-americana onde mora a família amarela", "Springfield"),
        ("As Meninas Superpoderosas", "nomes das três irmãs criadas pelo Professor Utônio", "Florzinha, Lindinha e Docinho"),
        ("Pica-Pau", "característica sonora mais famosa do personagem", "Sua risada inconfundível"),
        ("Pernalonga", "frase clássica que ele diz enquanto mastiga uma cenoura", "O que que há, velhinho?"),
        ("Os Flintstones", "período histórico em que vivem Fred Flintstone e Barney", "Idade da Pedra (em Bedrock)"),
        ("Ben 10", "dispositivo alienígena em formato de relógio preso ao pulso", "Omnitrix"),
        ("Padrinhos Mágicos", "nomes do casal de fadas de cabelos rosa e verde de Timmy", "Cosmo e Wanda"),
        ("Hora de Aventura", "dupla de protagonistas que vive na Terra de Ooo", "Finn (o humano) e Jake (o cão mágico)"),
        ("Gravity Falls", "irmãos gêmeos que passam o verão na Cabana do Mistério", "Dipper e Mabel Pines"),
        ("Avatar: A Lenda de Aang", "quatro elementos dominados pelo Avatar", "Água, Terra, Fogo e Ar"),
        ("Phineas e Ferb", "animal de estimação deles que é um agente secreto", "Perry, o Ornitorrinco (Agente P)"),
        ("Coragem, o Cão Covarde", "lugar isolado onde ele mora com Muriel e Eustácio", "Lugar Nenhum"),
        ("Laboratório de Dexter", "irmã mais velha que sempre invade e bagunça o laboratório", "Dee Dee"),
        ("Jovens Titãs", "líder da equipe que não possui superpoderes, mas usa artes marciais", "Robin"),
        ("Turma da Mônica", "objeto inseparável que a Mônica usa para correr atrás do Cebolinha", "Coelhinho de pelúcia azul Sansão"),
        ("Chaves (Desenho)", "comida favorita que o Chaves sempre sonha em comer na vila", "Sanduíche de presunto"),
        ("Popeye", "alimento enlatado que lhe dá força instantânea nos músculos", "Espinafre"),
        ("Manda-Chuva", "grupo de animais de rua que ele lidera no beco", "Gangue de gatos de Nova York"),
        ("Corrida Maluca", "vilão trapaceiro acompanhado pelo cachorro risonho Muttley", "Dick Vigarista"),
        (" Ursinhos Carinhosos", "poder especial disparado pela barriga dos ursinhos", "Raio de sentimentos e arco-íris"),
        ("Caverna do Dragão", "guia misterioso baixinho de manto vermelho que dá conselhos", "Mestre dos Magos"),
        ("Três Espiãs Demais", "nomes das três amigas estudantes de Beverly Hills", "Sam, Clover e Alex")
    ]
    tpl_desenhos = [
        "Mundo dos Desenhos: Em {item} ({sub}), qual é a resposta certa?",
        "Nostalgia Animada: Qual alternativa descreve corretamente {item} ({sub})?",
        "TV Globinho & Clássicos: O que é verdadeiro sobre {item} ({sub})?",
        "Quiz de Animação: A respeito do desenho {item} ({sub}), marque a opção correta:"
    ]

    # 8. ANIMES (25 fatos x 4 = 100 perguntas)
    fatos_animes = [
        ("Dragon Ball Z", "transformação lendária de cabelos dourados alcançada por Goku em Namekusei", "Super Saiyajin"),
        ("Naruto", "raposa de nove caudas selada dentro do protagonista", "Kurama"),
        ("One Piece", "grande sonho de Monkey D. Luffy ao navegar pela Grand Line", "Encontrar o One Piece e ser o Rei dos Piratas"),
        ("Solo Leveling", "comando que Sung Jin-Woo usa para erguer seu exército de sombras", "Erga-se (Arise)"),
        ("Bleach", "espada espiritual empunhada por Ichigo Kurosaki como Shinigami", "Zanpakuto (Zangetsu)"),
        ("Attack on Titan (Shingeki no Kyojin)", "três muralhas que protegiam a humanidade dos Titãs", "Muralhas Maria, Rose e Sina"),
        ("Black Clover", "característica única do protagonista Asta num mundo onde todos têm magia", "Ele nasceu sem mana e usa Anti-Magia"),
        ("Tokyo Revengers", "gangue de motoqueiros onde Takemichi tenta salvar o futuro de Mikey", "Tokyo Manji (Toman)"),
        ("Mashle: Magia e Músculos", "como Mash Burnedead supera os magos mesmo sem ter magia", "Com força física pura e treino muscular absurdo"),
        ("That Time I Got Reincarnated as a Slime", "criatura em que o protagonista reencarna com o nome de Rimuru Tempest", "Um Slime azul superpoderoso"),
        ("Cyberpunk: Edgerunners", "implante militar cibernético nas costas usado por David Martinez", "Sandevistan (supervelocidade)"),
        ("Demon Slayer (Kimetsu no Yaiba)", "motivo da jornada de Tanjiro Kamado", "Transformar sua irmã Nezuko de volta em humana"),
        ("Jujutsu Kaisen", "feiticeiro de venda nos olhos conhecido como o mais forte", "Satoru Gojo"),
        ("Death Note", "regra principal do caderno encontrado por Light Yagami", "A pessoa cujo nome for escrito nele morre"),
        ("Cavaleiros do Zodíaco", "golpe principal disparado por Seiya de Pégaso", "Meteoro de Pégaso"),
        ("Pokémon", "primeiro parceiro elétrico de Ash Ketchum da cidade de Pallet", "Pikachu"),
        ("Fullmetal Alchemist", "lei fundamental da alquimia seguida pelos irmãos Elric", "Lei da Troca Equivalente"),
        ("My Hero Academia (Boku no Hero)", "individualidade passada de All Might para Izuku Midoriya", "One For All"),
        ("Hunter x Hunter", "energia vital aprendida por Gon e Killua após o Exame Hunter", "Nen"),
        ("Yu Yu Hakusho", "técnica espiritual disparada pela ponta do dedo de Yusuke Urameshi", "Leigan"),
        ("InuYasha", "joia poderosa em pedaços procurada no Japão Feudal", "Joia de Quatro Almas"),
        ("One Punch Man", "rotina de treino que deixou Saitama careca e invencível", "100 flexões, 100 abdominais, 100 agachamentos e 10 km por dia"),
        ("Spy x Family", "poder secreto da pequena Anya Forger", "Telepatia (ela lê a mente das pessoas)"),
        ("Blue Lock", "esporte competitivo que busca criar o maior atacante do Japão", "Futebol"),
        ("Haikyuu!!", "posição na quadra de vôlei em que o baixinho Hinata Shoyo brilha", "Central de bloqueio com salto gigante")
    ]
    tpl_animes = [
        "Quiz Otaku & Animes: Na obra {item} ({sub}), qual é a resposta correta?",
        "Desafio dos Animes: O que corresponde exatamente a {item} ({sub})?",
        "Cultura Japonesa & Mangás: Sobre o anime {item} ({sub}), marque a certa:",
        "Batalha de Conhecimento: Em {item} ({sub}), qual alternativa está correta?"
    ]

    # 9. TRABALHOS & PROFISSÕES (25 fatos x 4 = 100 perguntas)
    fatos_trabalhos = [
        ("Analista de Suporte / TI", "função essencial nas empresas modernas", "Resolver problemas técnicos de computadores, sistemas e usuários"),
        ("Administrador de Redes", "equipamentos que ele configura para conectar a empresa", "Roteadores, Switches, Firewalls e servidores de rede"),
        ("Técnico de Fibra Óptica", "ferramenta usada para unir dois fios de vidro com precisão", "Máquina de fusão de fibra óptica"),
        ("Médico Cardiologista", "órgão do corpo humano do qual ele cuida", "Coração e sistema circulatório"),
        ("Engenheiro Civil", "responsabilidade técnica numa construção", "Cálculo estrutural e execução segura de obras e pontes"),
        ("Eletricista", "instrumento usado para medir tensão, corrente e resistência elétrica", "Multímetro"),
        ("Advogado", "exame nacional obrigatório para exercer a profissão no Brasil", "Exame da Ordem dos Advogados do Brasil (OAB)"),
        ("Professor", "missão principal dentro da sala de aula", "Ensinar, formar cidadãos e compartilhar conhecimento"),
        ("Bombeiro", "número de telefone de emergência no Brasil para chamá-los", "193"),
        ("Chef de Cozinha / Cozinheiro", "responsabilidade principal dentro de um restaurante", "Criar o cardápio, preparar pratos e coordenar a brigada"),
        ("Mecânico Automotivo", "manutenção preventiva mais comum feita no motor", "Troca de óleo e filtros do veículo"),
        ("Enfermeiro", "atuação direta no cuidado diário dos pacientes", "Administrar medicamentos, aferir sinais vitais e assistir o paciente"),
        ("Contador / Contabilista", "declaração anual que ele ajuda pessoas e empresas a entregar", "Imposto de Renda e balanço patrimonial"),
        ("Arquiteto", "foco do seu trabalho ao planejar um ambiente", "Conforto, estética, iluminação e aproveitamento do espaço"),
        ("Farmacêutico", "profissional responsável técnico nas drogarias", "Orientar sobre o uso correto de medicamentos e receitas"),
        ("Soldado / Militar", "dever constitucional das Forças Armadas", "Defesa da Pátria e garantia da soberania nacional"),
        ("Desenvolvedor de Software / Programador", "linguagem muito usada em automação, dados e sistemas web", "Python, JavaScript e bancos de dados SQL"),
        ("Dentista (Odontologista)", "cuidado preventivo recomendado a cada 6 meses", "Limpeza dentária (profilaxia) e prevenção de cáries"),
        ("Veterinário", "público atendido em sua clínica ou fazenda", "Animais domésticos, silvestres e de produção"),
        ("Motorista Profissional", "documento obrigatório com categoria específica para dirigir no Brasil", "Carteira Nacional de Habilitação (CNH)"),
        ("Padeiro / Confeiteiro", "ingrediente biológico que faz a massa do pão crescer", "Fermento biológico"),
        ("Fotógrafo", "três pilares básicos para controlar a luz numa câmera", "ISO, Abertura do Diafragma e Velocidade do Obturador"),
        ("Psicólogo", "foco do atendimento clínico no consultório", "Saúde mental, escuta qualificada e comportamento humano"),
        ("Pedreiro / Mestre de Obras", "ferramenta usada para garantir que a parede suba perfeitamente reta", "Prumo e Nível de bolha"),
        ("Designer Gráfico", "formato de arquivo vetorial usado em corte a laser e logotipos", "SVG (Scalable Vector Graphics) e curvas vetoriais")
    ]
    tpl_trabalhos = [
        "Mundo do Trabalho: Sobre a profissão de {item} ({sub}), qual é a resposta certa?",
        "Quiz das Profissões: O que faz parte do dia a dia de um {item} ({sub})?",
        "Carreira & Ofícios: Assinale a opção correta sobre {item} ({sub}):",
        "Conhecimento Profissional: Quando falamos em {item} ({sub}), a resposta é:"
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
# CONFIGURAÇÕES PADRÃO E TEMAS PRÉ-DEFINIDOS
# ==============================================================================
TEMAS_PRONTOS = {
    "Personalizado (Livre)": None,
    "Azul Mariano (Padrão)": CORES_POR_MODO["⛪ Igreja"],
    "Herói Épico (Azul & Vermelho)": CORES_POR_MODO["🦸 Super-Heróis"],
    "Verde Tropical (Frutas & Natureza)": CORES_POR_MODO["🍎 Frutas"],
    "Vermelho Gourmet (Comidas & Festa)": CORES_POR_MODO["🍔 Comidas"],
    "Roxo Glamour (Novelas & TV)": CORES_POR_MODO["📺 Novelas"],
    "Noite de Oscar (Filmes & Gala)": CORES_POR_MODO["🎬 Filmes"],
    "Cartoon Vibrante (Desenhos)": CORES_POR_MODO["🎨 Desenhos"],
    "Neon Cyberpunk (Animes & Geek)": CORES_POR_MODO["⚔️ Animes"],
    "Corporativo Tech (Trabalhos & TI)": CORES_POR_MODO["💼 Trabalhos & Profissões"]
}

def obter_config_padrao():
    return {
        "imagem_ns": "nossa_senhora.png",
        "tamanho_imagem": 360,
        "borda_imagem": 12,
        "usar_fundo_img": False,
        "imagem_fundo": "fundo_quiz_geral.png",
        "opacidade_fundo": 0.7,
        "cor_auto_por_modo": True,
        
        "tempo_pergunta": 30,
        "tempo_alerta": 5,
        "acertos_para_dado": 3,
        "pontos_por_acerto": 100,
        "ativar_sons": True,
        "ativar_baloes": True,
        
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
        
        "tam_fonte_titulo": 46,
        "tam_fonte_pergunta": 30,
        "tam_fonte_opcoes": 24,
        "tam_fonte_placar": 20,
        "tam_fonte_botao": 22,
        "largura_botao": 500,
        "altura_botao": 16,
        "raio_borda_botao": 10,
        
        "titulo_aba": "Super Quiz 900 Perguntas",
        "icone_aba": "🎲",
        "txt_titulo_menu": "🎲 SUPER QUIZ MULTI-TEMAS (900 PERGUNTAS) 🎲",
        "txt_subtitulo_menu": "Escolha um dos 10 modos de jogo e desafie os seus conhecimentos! (F11 para tela cheia)",
        "txt_titulo_imagem": "🌸 Destaque do Quiz",
        "txt_btn_jogar": "▶️ Jogar / Escolher Modo de Jogo",
        "txt_btn_participantes": "👥 Cadastrar Participantes",
        "txt_btn_perguntas": "📝 Gerir as 900 Perguntas por Tema",
        "txt_btn_historico": "📊 Histórico de Acertos e Prêmios",
        "txt_btn_config": "⚙️ Estúdio de Personalização (Configurações)",
        "txt_btn_sair": "🚪 Sair / Fechar Sistema",
        "txt_sala_dado": "🎲 SALA DO DADO PREMIADO! 🎲",
        "txt_sub_dado": "Parabéns! Chegou a hora de lançar o dado!",
        "txt_titulo_fim": "🎉 FIM DA PARTIDA! PARABÉNS! 🎉",
        "txt_msg_final": "Obrigado por participar! Que Deus abençoe grandemente a todos!"
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
    page_title=config.get("titulo_aba", "Super Quiz"),
    page_icon=config.get("icone_aba", "🎲"),
    layout="wide"
)

# ==============================================================================
# GERADOR DE CSS DINÂMICO (MUDA DE COR CONFORME O MODO DE JOGO SELECIONADO!)
# ==============================================================================
def obter_paleta_ativa():
    modo_atual = st.session_state.get("modo_jogo_ativo")
    if config.get("cor_auto_por_modo", True) and modo_atual in CORES_POR_MODO:
        return CORES_POR_MODO[modo_atual]
    return {
        "cor_fundo": config["cor_fundo"],
        "cor_card": config["cor_card"],
        "cor_texto": config["cor_texto"],
        "cor_destaque": config["cor_destaque"],
        "cor_botao": config["cor_botao"],
        "cor_texto_botao": config["cor_texto_botao"],
        "cor_borda_botao": config["cor_borda_botao"]
    }

def aplicar_estilos_dinamicos():
    paleta = obter_paleta_ativa()
    bg_css = f"background-color: {paleta['cor_fundo']};"
    
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
        }}
        .placar-alerta {{
            font-size: {config['tam_fonte_placar'] + 2}px !important;
            font-weight: bold !important;
            color: #FF4B4B !important;
        }}
        .badge-modo {{
            background-color: {paleta['cor_botao']};
            color: {paleta['cor_destaque']};
            padding: 6px 16px;
            border-radius: 20px;
            border: 2px solid {paleta['cor_destaque']};
            font-weight: bold;
            font-size: 18px;
            display: inline-block;
            margin-bottom: 10px;
        }}
        .main-card {{
            background-color: {paleta['cor_card']};
            padding: 28px;
            border-radius: 14px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.45);
            margin-bottom: 22px;
            border: 2px solid {paleta['cor_borda_botao']};
        }}
        .main-card h3 {{
            font-size: {config['tam_fonte_pergunta']}px !important;
            line-height: 1.4 !important;
            color: {paleta['cor_texto']} !important;
            margin: 0 !important;
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
            max-width: {config['largura_botao']}px !important;
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
            color: {paleta['cor_texto']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# FUNÇÕES DE DADOS (GARANTE 100 PERGUNTAS EM CADA BANCO AUTOMATICAMENTE)
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
                if "bancos_perguntas" in dados and isinstance(dados["bancos_perguntas"], dict):
                    for k, lista_p in dados["bancos_perguntas"].items():
                        # Se o banco salvo tinha menos de 100 perguntas (ex: versão antiga de 3 perguntas), completa com as 100!
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

def mostrar_santa(largura_custom=None, borda_custom=None, titulo_custom=None):
    img_path = config.get("imagem_ns", "nossa_senhora.png")
    if not os.path.exists(img_path) and os.path.exists("nossa_senhora.png"):
        img_path = "nossa_senhora.png"
        
    largura = largura_custom if largura_custom is not None else config.get("tamanho_imagem", 360)
    borda = borda_custom if borda_custom is not None else config.get("borda_imagem", 12)
    titulo = titulo_custom if titulo_custom is not None else config.get("txt_titulo_imagem", "🌸 Destaque do Quiz")
    
    paleta = obter_paleta_ativa()
    html_bloco = "<div style='text-align: center; width: 100%;'>"
    if titulo.strip():
        html_bloco += f"<h3 style='margin-bottom: 15px; color: {paleta['cor_texto']};'>{titulo}</h3>"
    
    if os.path.exists(img_path):
        try:
            with open(img_path, "rb") as f:
                b64_img = base64.b64encode(f.read()).decode("utf-8")
            html_bloco += (
                f"<img src='data:image/png;base64,{b64_img}' "
                f"style='width: {largura}px; max-width: 100%; height: auto; "
                f"margin: 0 auto; display: block; border-radius: {borda}px; "
                f"border: 3px solid {paleta['cor_destaque']}; "
                f"box-shadow: 0 4px 15px rgba(0,0,0,0.45);' />"
            )
        except Exception:
            html_bloco += "<p style='color: #F4D35E;'>Erro ao ler imagem.</p>"
    else:
        html_bloco += f"<p style='color: #8DA9C4;'>Imagem '{img_path}' não encontrada.</p>"
        
    html_bloco += "</div>"
    st.markdown(html_bloco, unsafe_allow_html=True)

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
    "up_cnt": 0, "msg_upload_ok": "", "tema_gerir_selecionado": "⛪ Igreja"
}
for chave, valor_padrao in estados_iniciais.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor_padrao

# Aplica o CSS dinâmico (já sabendo qual é o modo_jogo_ativo da sessão!)
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
# 1. MENU PRINCIPAL
# ==============================================================================
if st.session_state.pagina == "menu":
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
            st.warning("Para fechar o sistema no navegador, basta fechar esta aba ou janela.")

# ==============================================================================
# 2. SELECIONAR PARTICIPANTE + MODO DE JOGO (MUDA A COR NA HORA!)
# ==============================================================================
elif st.session_state.pagina == "selecionar_participante":
    st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>👤 Participante & Modo de Jogo</h2>", unsafe_allow_html=True)
    
    col_esq, col_dir = st.columns([2, 1])
    
    with col_dir:
        mostrar_santa()
        
    with col_esq:
        nome_digitado = st.text_input("1️⃣ Digite o nome do Participante:")
        escolha_lista = st.selectbox(
            "Ou escolha da lista cadastrada:",
            ["-- Selecione da lista --"] + participantes
        ) if participantes else "-- Selecione da lista --"
        
        st.write("")
        idx_modo_atual = LISTA_MODOS_JOGO.index(st.session_state.modo_jogo_ativo) if st.session_state.modo_jogo_ativo in LISTA_MODOS_JOGO else 0
        modo_escolhido = st.selectbox(
            "2️⃣ Escolha o Modo de Jogo / Tema das Perguntas (A cor da tela muda com o tema!):",
            LISTA_MODOS_JOGO,
            index=idx_modo_atual
        )
        
        # Assim que o utilizador muda o modo de jogo no seletor, atualiza a cor da tela ao vivo!
        if modo_escolhido != st.session_state.modo_jogo_ativo:
            st.session_state.modo_jogo_ativo = modo_escolhido
            st.rerun()
            
        if modo_escolhido == "🎲 Misturadão (Todos os Temas)":
            qtd_disp = sum(len(v) for v in bancos_perguntas.values())
        else:
            qtd_disp = len(bancos_perguntas.get(modo_escolhido, []))
            
        st.markdown(
            f"<div class='badge-modo'>🎯 Tema selecionado: {modo_escolhido} — {qtd_disp} perguntas disponíveis!</div>",
            unsafe_allow_html=True
        )
        
        st.write("")
        col_btn1, col_btn2, col_btn3 = st.columns([0.5, 2, 0.5])
        with col_btn2:
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
                    # Seleciona o banco de perguntas do modo escolhido
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
                        st.session_state.pagina = "jogo"
                        st.rerun()
                else:
                    st.warning("⚠️ Por favor, digite ou selecione o nome do participante!")
                    
            if st.button("⬅️ Voltar ao Menu", use_container_width=True):
                st.session_state.modo_jogo_ativo = None
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
    paleta = obter_paleta_ativa()
    
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
        
        st.markdown(
            f"<div class='badge-modo'>Modo: {st.session_state.modo_jogo_ativo} &nbsp;|&nbsp; Pergunta {p_idx + 1} de {total_p}</div>",
            unsafe_allow_html=True
        )
        
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
    paleta = obter_paleta_ativa()
    if st.session_state.tempo_final_congelado is None:
        st.session_state.tempo_final_congelado = obter_tempo_decorrido()
        
    tempo_final_fmt = formatar_tempo_partida(st.session_state.tempo_final_congelado)
    
    if not st.session_state.historico_salvo_partida:
        reg_final = (
            f"Participante: {st.session_state.participante} | "
            f"Modo: {st.session_state.modo_jogo_ativo} | "
            f"Pontos: {st.session_state.pontuacao} | "
            f"Acertos: {st.session_state.total_acertos_partida} | "
            f"Erros: {st.session_state.total_erros_partida} | "
            f"Tempo Total: {tempo_final_fmt}"
        )
        historico.append(reg_final)
        salvar_dados(bancos_perguntas, participantes, historico)
        st.session_state.historico_salvo_partida = True
        
    st.markdown(f"<h1 style='text-align: center;'>{config['txt_titulo_fim']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Participante: {st.session_state.participante} ({st.session_state.modo_jogo_ativo})</h2>", unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='text-align: center; color: {paleta['cor_destaque']};'>"
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
            st.session_state.modo_jogo_ativo = None
            st.session_state.pagina = "menu"
            st.rerun()

# ==============================================================================
# 6. CADASTRAR PARTICIPANTES
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
            salvar_dados(bancos_perguntas, participantes, historico)
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
                    salvar_dados(bancos_perguntas, participantes, historico)
                    st.success(f"Participante '{p}' removido!")
                    st.rerun()
    else:
        st.info("Nenhum participante cadastrado.")
        
    st.write("")
    if st.button("⬅️ Voltar ao Menu", key="voltar_part_fim"):
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 7. HISTÓRICO
# ==============================================================================
elif st.session_state.pagina == "historico":
    col_top_h1, col_top_h2 = st.columns([2, 1])
    with col_top_h1:
        st.markdown("<h2>📊 Histórico de Acertos, Tempos e Prêmios</h2>", unsafe_allow_html=True)
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
                salvar_dados(bancos_perguntas, participantes, historico)
                st.success("Itens selecionados apagados com sucesso!")
                st.rerun()
        with col_h2:
            if st.button("🗑️ Limpar Todo o Histórico"):
                historico.clear()
                salvar_dados(bancos_perguntas, participantes, historico)
                st.rerun()
    else:
        st.info("Ainda não existem registos no histórico.")
        
    st.write("")
    if st.button("⬅️ Voltar ao Menu", key="voltar_hist_fim"):
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 8. GERIR / EDITAR AS 900 PERGUNTAS SEPARADAS POR TEMA
# ==============================================================================
elif st.session_state.pagina == "gerir_perguntas":
    st.markdown("<h2>📝 Gestão de Perguntas por Modo de Jogo (900 Perguntas)</h2>", unsafe_allow_html=True)
    
    col_topo_esq, col_topo_meio, col_topo_dir = st.columns([1, 1, 1])
    with col_topo_esq:
        if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_topo", use_container_width=True):
            st.session_state.editando_idx = None
            st.session_state.modo_jogo_ativo = None
            st.session_state.pagina = "menu"
            st.rerun()
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
        st.write(f"### {titulo_form}")
        
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
    st.write(f"### 📋 Perguntas de {tema_sel_gerir} ({len(perguntas_do_tema)} cadastradas):")
    
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
                
    st.write("")
    if st.button("⬅️ Voltar ao Menu", key="btn_voltar_perg_rodape", use_container_width=True):
        st.session_state.editando_idx = None
        st.session_state.modo_jogo_ativo = None
        st.session_state.pagina = "menu"
        st.rerun()

# ==============================================================================
# 9. ESTÚDIO DE PERSONALIZAÇÃO TOTAL
# ==============================================================================
elif st.session_state.pagina == "configuracoes":
    st.session_state.modo_jogo_ativo = None
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

    aba_cores, aba_botoes, aba_textos, aba_img_regras, aba_sons = st.tabs([
        "🎨 1. Cores & Fundo",
        "🔘 2. Botões & Tamanhos",
        "✍️ 3. Textos & Títulos",
        "🖼️ 4. Imagem & Regras",
        "🔊 5. Sons & Restauro"
    ])
    
    with aba_cores:
        st.subheader("🎨 Paleta de Cores e Troca Automática por Modo")
        cor_auto_val = st.checkbox(
            "🦎 Mudar as cores da tela automaticamente conforme o Modo de Jogo escolhido (Super-Heróis, Frutas, Animes, etc.)",
            value=config.get("cor_auto_por_modo", True)
        )
        
        opcoes_temas = list(TEMAS_PRONTOS.keys())
        idx_tema = opcoes_temas.index(config.get("tema_escolhido", "Azul Mariano (Padrão)")) if config.get("tema_escolhido") in opcoes_temas else 0
        tema_sel = st.selectbox("Cor Padrão do Menu Principal (ou de todo o jogo se desmarcar a opção acima):", opcoes_temas, index=idx_tema)
        
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
            tam_f_perg_val = st.slider("Tamanho da Letra da Pergunta (px):", 20, 50, int(config.get("tam_fonte_pergunta", 30)), 1)
            tam_f_opc_val = st.slider("Tamanho da Letra das Alternativas A, B, C, D (px):", 16, 42, int(config.get("tam_fonte_opcoes", 24)), 1)
            tam_f_plac_val = st.slider("Tamanho da Letra do Placar no Topo (px):", 14, 36, int(config.get("tam_fonte_placar", 20)), 1)

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

    with aba_img_regras:
        col_ir1, col_ir2 = st.columns([1.5, 1])
        with col_ir1:
            st.subheader("🖼️ Imagem Principal / Lateral")
            tamanho_img_val = st.slider("Largura da Imagem Lateral (px):", 150, 650, int(config.get("tamanho_imagem", 360)), 10)
            borda_img_val = st.slider("Arredondamento da Moldura da Imagem (px):", 0, 200, int(config.get("borda_imagem", 12)), 4)
            
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
        if st.button("🔄 Restaurar Todas as Configurações e as 900 Perguntas", key="btn_restaurar_orig"):
            salvar_config(obter_config_padrao())
            salvar_dados(construir_bancos_900(), participantes, historico)
            st.session_state.up_cnt += 1
            st.session_state.msg_upload_ok = "🔄 Configurações e banco de 900 perguntas restaurados com sucesso!"
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
                "cor_auto_por_modo": bool(cor_auto_val),
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
