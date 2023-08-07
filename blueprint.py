from os import path
from random import seed
from random import randint

#este modulo trabalha apenas quando um jogo é iniciado ou quando um jogo é salvo
#se for novo, as celulas precisam ser preenchidas genericamente. Se carregado, ele lê os dados salvos.


def salvar(lista, jogo):
    pass


def carregar(lista, jogo):
    pass


def iniciar_generico(lista, dados):         #enviar apenas dados do menu ou todo o jogo? Pq aqui que vai ser salvo ne

    aleatorios = []
    seed()
    #aleatorizar quais celulas terao pedras

    if dados.dificuldade == "facil": quantidade_pedras = 15
    elif dados.dificuldade == "dificil": quantidade_pedras = 30

    for _ in range(quantidade_pedras):
        parar = False

        while parar == False:
            value = randint(1, 147)
            if (value >=1 and value <= 7) or (value >=22 and value <= 26):
                parar = False
            else:
                parar = True
        
        aleatorios.append(value)

    #preencher celulas com dados genericos

    parar = False
    ide = 1

    while parar == False:

        a = ((ide-1) // 21) #representa o i na matriz
        b = (ide-1) % 21 #representa o j na matriz
        b = b * 51 #o j na matriz representa a largura
        a = a * 93 #o i na matriz representa a altura
        lista[ide-1].coordenadas = b, a

        if (ide >=1 and ide <= 7) or (ide >=22 and ide <= 26):
            lista[ide-1].bloqueada = True
        else:
            lista[ide-1].bloqueada = False
            lista[ide-1].vazio = True
            lista[ide-1].consumo = 0
            lista[ide-1].pretendente = "nenhuma"

            #as coordenadas ficavam aqui

        if ide in aleatorios and lista[ide-1].bloqueada == False: lista[ide-1].pedra = True
        else: lista[ide-1].pedra = False
        
        lista[ide-1].tipo = None
        lista[ide-1].situacao = None
        lista[ide-1].lvl = None
        lista[ide-1].id = ide

        ide += 1
        if ide > 147: parar = True

    lista[0].coordenadas = (0,0)
    lista[0].imagem()

    #a partir aqui vamos preencher os dados corretos pra porta, quarto e elevador que vem de padrão

    entrada = 26
    while entrada >= 26 and entrada <= 30:

        lista[entrada].pedra = False
        lista[entrada].vazio = False
        lista[entrada].tipo = "porta"   #lembrando que a porta e indestrutivel
        lista[entrada].consumo = 25     #ainda em testes esse valor, mas lembrando que aqui corresponde a uma celula sozinha
        lista[entrada].lvl = '1'
        entrada += 1

    lista[26].situacao = "_1-4"   #nao ha o denominador porque so existe uma maneira de organizar a porta
    lista[27].situacao = "_2-4"     #tive q colocar por causa do metodo q estou usando pra ver o tamanho da sala
    lista[28].situacao = "_3-4"
    lista[29].situacao = "_4-4"

    lista[30].tipo = "elevador"
    lista[30].consumo = 20
    lista[30].situacao = "_1-1" #ele nao tem imagens diferentes
    lista[30].lvl = '0'

    if lista[30-21].pedra == False:     #quando quebra uma pedra é preciso checar se se torna pretendente
        lista[30-21].pretendente = "vertical"
    if lista[30+21].pedra == False:
        lista[30+21].pretendente = "vertical"

    quartos = 31
    while quartos >= 31 and quartos <= 36:
        lista[quartos].pedra = False
        lista[quartos].vazio = False
        lista[quartos].tipo = "quarto"
        lista[quartos].consumo = 150

        if dados.dificuldade == "facil": lista[quartos].lvl = '2'
        elif dados.dificuldade == "dificil": lista[quartos].lvl = '1'
        quartos += 1

    lista[31].situacao = "_1-6" #esse quarto esja junto a outros 5
    lista[32].situacao = "_2-6"
    lista[33].situacao = "_3-6"
    lista[34].situacao = "_4-6"
    lista[35].situacao = "_5-6"
    lista[36].situacao = "_6-6"

    if lista[37].pedra == False:
        lista[37].pretendente = "total"

    #teste pra visualizar o que ha na lista dos objetos (lista de todas as celulas) e criar seus objetos
    contagem = 0
    while contagem < 147:

        lista[contagem].imagem()
        print(vars(lista[contagem]))            #teste
        contagem += 1
    
