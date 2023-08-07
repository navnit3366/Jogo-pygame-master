import pygame
from pygame import mixer
mixer.init()
pygame.init()

from os import path
import sys
#import dwellers
from random import seed
from random import randint

def animacao(jogo, lista, flipar):

    #jogo.sobresalas.testeduplas = []

    preto = 0, 0, 0
    coleta = None
    jogo.janela.fill(preto)
    jogo.janela.blit(jogo.fuso,(0,0))
    jogo.janela.blit(jogo.fundo, (0,0))
    jogo.janela.blit(jogo.iconesistema, (0,0))

    mano = pygame.image.load(path.join('personagens', 'mano.png'))
    mina = pygame.image.load(path.join('personagens', 'mina.png'))

    if jogo.modo == "construir":
        contorno1 = pygame.image.load(path.join('sistema', 'constrorno1.png'))
        contorno2 = pygame.image.load(path.join('sistema', 'constrorno2.png'))
        #contorno3 = pygame.image.load(path.join('sistema', 'constrorno3.png'))

    contagem = 0
    while contagem < 147:
        lista[contagem].imagem()    #sera se tem problema atualizar toda santa vez as imagens?
        if lista[contagem].obj != None:
            jogo.janela.blit(lista[contagem].obj,lista[contagem].coordenadas)


        if lista[contagem].morador != None:
            if lista[contagem].morador.sexo == "M": jogo.janela.blit(mano, lista[contagem].coordenadas)
            else: jogo.janela.blit(mina, lista[contagem].coordenadas)

        if lista[contagem].idle:
            if lista[contagem].tipo == "cozinha": coleta = pygame.image.load(path.join('sistema', 'coletacozinha.png'))
            elif lista[contagem].tipo == "gerador": coleta = pygame.image.load(path.join('sistema', 'coletagerador.png'))
            elif lista[contagem].tipo == "tratamento": coleta = pygame.image.load(path.join('sistema', 'coletatratamento.png'))
            elif lista[contagem].tipo == "renda": coleta = pygame.image.load(path.join('sistema', 'coletarenda.png'))
            elif lista[contagem].tipo == "laboratorio": coleta = pygame.image.load(path.join('sistema', 'coletalaboratorio.png'))

            if coleta != None: jogo.janela.blit(coleta,lista[contagem].coordenadas)

        if jogo.modo == "construir":
            if jogo.construirtipo == "elevador":
                if lista[contagem].pretendente == "total" or lista[contagem].pretendente == "vertical":
                    jogo.janela.blit(contorno1,lista[contagem].coordenadas)

            else:
                b = (contagem) % 21
                if lista[contagem].pretendente == "total":
                    if lista[contagem-1].vazio and not lista[contagem-1].pedra and b != 0:
                        jogo.janela.blit(contorno2,lista[contagem-1].coordenadas)

                    elif lista[contagem+1].vazio and not lista[contagem+1].pedra and b != 20:
                        jogo.janela.blit(contorno2,lista[contagem].coordenadas)

        contagem += 1
    HUD(jogo)
    if flipar == True: pygame.display.flip()


def minerar(jogo, celula):

    confirmacao = pygame.image.load(path.join('sistema', 'removerpedra.png'))
    contorno = pygame.image.load(path.join('sistema', 'contorno.png'))
    erro  = pygame.image.load(path.join('sistema', 'naopode.png'))

    jogo.janela.blit(contorno, celula.coordenadas)
    jogo.janela.blit(confirmacao,(459,186))
    pygame.display.flip()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:

                position = pos_x, pos_y = pygame.mouse.get_pos()
                if pos_y >= 372 and pos_y <= 465:
                    if pos_x >= 510 and pos_x <= 560:
                        return
                    elif pos_x >= 612 and pos_x <= 663:
                        preco = (((celula.id-1) // 21) * 50) + 50
                        if jogo.dinheiro < preco:
                            jogo.janela.blit(erro,(459,186))
                            pygame.display.flip()
                        else:
                            celula.pedra = False
                            jogo.dinheiro = jogo.dinheiro - preco
                            sucesso =  pygame.mixer.Sound(path.join('sons','minerar.wav'))
                            pygame.mixer.Sound.play(sucesso)
                            return
            
        
def achar_celula(position):

    pos_x, pos_y = position
    x = 1020
    y = 558
    achei = False
    while achei == False:
        if pos_y < y: y -= 93
        else: achei = True
    achei = False
    while achei == False:
        if pos_x < x: x -= 51
        else: achei = True
    y = (y // 93) * 21
    x = (x//51) + 1
    pos_vetor = (x + y) - 1
    return pos_vetor


def pretendencia(lista, pos_vetor, demolicao):

    if demolicao == True:   #se isso for verdade, quer dizer que uma celula foi demolida

        #se vier ide, so diminuir 1 pra ter o pos_vetor
        if lista[pos_vetor].pedra or not lista[pos_vetor].vazio: return
        a = ((pos_vetor) // 21) #representa o i na matriz
        b = (pos_vetor) % 21 #representa o j na matriz
        

        lista[pos_vetor].pretendente = None
        if a != 0:
            if not lista[pos_vetor-21].vazio and lista[pos_vetor-21].tipo == "elevador": lista[pos_vetor].pretendente = "vertical"
        if a != 6:
            if not lista[pos_vetor+21].vazio and lista[pos_vetor+21].tipo == "elevador": lista[pos_vetor].pretendente = "vertical"
        if b != 0:
            if lista[pos_vetor-1].vazio == False: lista[pos_vetor].pretendente = "total"
        if b != 20:
            if lista[pos_vetor+1].vazio == False: lista[pos_vetor].pretendente = "total"
    

    else:                                       #era bom q aqui tambem removesse, qnd destroi uma sala
        #print("plim")
        if lista[pos_vetor].vazio == False:
            a = ((pos_vetor) // 21) #representa o i na matriz
            b = (pos_vetor) % 21 #representa o j na matriz

            if a != 0:
                if lista[pos_vetor-21].vazio == True and lista[pos_vetor-21].pedra == False:
                    if lista[pos_vetor].tipo == "elevador": lista[pos_vetor-21].pretendente = "vertical"
            if a != 6:
                if lista[pos_vetor+21].vazio == True and lista[pos_vetor+21].pedra == False:
                    if lista[pos_vetor].tipo == "elevador": lista[pos_vetor+21].pretendente = "vertical"
            if b != 0:
                if lista[pos_vetor-1].vazio == True and lista[pos_vetor-1].pedra == False: lista[pos_vetor-1].pretendente = "total"
            if b != 20:
                if lista[pos_vetor+1].vazio == True and lista[pos_vetor+1].pedra == False: lista[pos_vetor+1].pretendente = "total"



def erguer(lista, pos_vetor, jogo, fundir):

    #essa funcao tbm tem obrigacao de fundir salas

    lista[pos_vetor].vazio = False
    lista[pos_vetor].pretendente = False
    lista[pos_vetor].tipo = jogo.construirtipo

    if jogo.construirtipo == "elevador":
        
        lista[pos_vetor].lvl = "0"
        lista[pos_vetor].situacao = "_1-1"
        lista[pos_vetor].consumo = jogo.sobresalas.cnsm_EQCAEDRT[0]
        jogo.dinheiro -= jogo.sobresalas.preco[0][0]
        jogo.sobresalas.aumentar_qtd(0)

    else:

        lista[pos_vetor].lvl = "1"
        lista[pos_vetor].situacao = "_1-2"

        lista[pos_vetor+1].vazio = False
        lista[pos_vetor+1].pretendente = False
        lista[pos_vetor+1].tipo = jogo.construirtipo
        lista[pos_vetor+1].lvl = "1"
        lista[pos_vetor+1].situacao = "_2-2"

        x = None
        if jogo.construirtipo == "quarto":
            jogo.dinheiro -= jogo.sobresalas.preco[0][1]
            x = 1
            jogo.lotacao += 2
        elif jogo.construirtipo == "cozinha":
            jogo.dinheiro -= jogo.sobresalas.preco[0][2]
            x = 2
        elif jogo.construirtipo == "tratamento":
            jogo.dinheiro -= jogo.sobresalas.preco[0][3]
            x = 3
        elif jogo.construirtipo == "gerador":
            jogo.dinheiro -= jogo.sobresalas.preco[1][0]
            x = 4
        elif jogo.construirtipo == "renda":
            jogo.dinheiro -= jogo.sobresalas.preco[1][1]
            x = 5
        elif jogo.construirtipo == "radio":
            jogo.dinheiro -= jogo.sobresalas.preco[1][2]
            x = 6
        elif jogo.construirtipo == "treinamento":
            jogo.dinheiro -= jogo.sobresalas.preco[1][3]
            x = 7
   
        lista[pos_vetor].consumo = jogo.sobresalas.cnsm_EQCAEDRT[x]
        jogo.sobresalas.aumentar_qtd(x)
        lista[pos_vetor+1].consumo = jogo.sobresalas.cnsm_EQCAEDRT[x]
        jogo.sobresalas.aumentar_qtd(x)



    if fundir != None: fusao(jogo,lista,pos_vetor,fundir)
    jogo.sobresalas.calcconsumo()
    sucesso =  pygame.mixer.Sound(path.join('sons','obrafinalizada.wav'))
    pygame.mixer.Sound.play(sucesso)





def preparar_obra(jogo, lista):

    voltar = pygame.image.load(path.join('sistema', 'voltar.png'))

    jogo.modo = "construir"
    while True:

        animacao(jogo, lista, False)
        jogo.janela.blit(voltar, (0,0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:

                position = pos_x, pos_y = pygame.mouse.get_pos()
                pos_vetor = achar_celula(position)

                if pos_vetor == 0:
                    jogo.modo = "espectador"
                    return True

                if jogo.construirtipo == "elevador":
                    if lista[pos_vetor].pretendente == "vertical" or lista[pos_vetor].pretendente == "total":
                        erguer(lista,pos_vetor,jogo,None)
                        jogo.modo = "espectador"
                        pretendencia(lista,pos_vetor,False)
                        jogo.construirtipo = None
                        return False

                    else: print("ai pode nao")
                else:
                    b = (pos_vetor) % 21
                    l = lista
                    p = pos_vetor
                    t = "total"
                    executar = True
                    fundir = None

                    if l[p].pretendente == t and b == 0 and not l[p+1].vazio:
                        executar = False        #caso onde tem 1 celula sozinha na margem esquerda sendo amassada
                    elif l[p].pretendente == t and b == 20 and not l[p-1].vazio:
                        executar = False        #caso onde tem 1 celula sozinha na margem direita sendo amassada
                    elif l[p].pretendente == t and b > 0 and b < 18 and not l[p-1].vazio and l[p+1].pretendente == t and not l[p+2].vazio:
                        #uma construcao entre 2 salas, uma intersseccao, onde a clicada tem uma esquerda ocupada
                        if jogo.construirtipo == l[p-1].tipo and 1 == int(l[p-1].lvl): 
                            if int(l[p-1].situacao[3]) < 6: fundir = "esquerda"
                        if jogo.construirtipo == l[p+2].tipo and 1 == int(l[p+2].lvl):
                            if int(l[p-1].situacao[3]) <= 2 and int(l[p+2].situacao[3]) <= 2: 
                                if fundir == "esquerda": fundir = "esquerda e direita"
                                else: fundir == "direita"
                    elif l[p].pretendente == t and b > 1 and b < 19 and not l[p+1].vazio and l[p-1].pretendente == t and not l[p-2].vazio:
                                #aq pode ter erro, ctrlv. Melhor ficar assim, ai a celula q vc clica pode alterar a preferencia
                        if jogo.construirtipo == l[p+1].tipo and 1 == int(l[p+1].lvl):     
                            if int(l[p-2].situacao[3]) < 6: fundir = "direita"
                        if jogo.construirtipo == l[p-2].tipo and 1 == int(l[p-2].lvl):
                            if int(l[p+1].situacao[3]) <= 2 and int(l[p-2].situacao[3]) <= 2: 
                                if fundir == "direita": fundir = "esquerda e direita"
                                else: fundir == "esquerda"
                        pos_vetor = p - 1  #uma construcao entre 2 salas, uma intersseccao, onde a clicada tem uma direita ocupada
                    elif l[p].pretendente == t and b > 0 and b < 20:        #aq quando vc clica numa pretendente, 2 casos
                        if l[p-1].pretendente != t and not l[p-1].pedra and not l[p+1].vazio:
                            if jogo.construirtipo == l[p+1].tipo and 1 == int(l[p+1].lvl):
                                if int(l[p+1].situacao[3]) < 6: fundir = "direita"
                            pos_vetor = p - 1           #vc clicou na celula que tem uma ocupada a direita
                        elif l[p+1].pretendente != t and not l[p+1].pedra and not l[p-1].vazio:
                            #vc clicou na celula que tem uma ocupada a esquerda
                            if jogo.construirtipo == l[p-1].tipo and 1 == int(l[p-1].lvl):
                                if int(l[p-1].situacao[3]) < 6: fundir = "esquerda"
                        else: executar = False
                    #a ordem das 2 condicoes a seguir representa oq vai ser escolhido no caso de um diagrama de venn
                    elif l[p].pretendente != t and not l[p].pedra:          #quando vc clica numa nao pretendente de salas normais
                        if l[p-1].pretendente == t and not l[p-2].vazio and b > 1:
                            if jogo.construirtipo == l[p-2].tipo and 1 == int(l[p-2].lvl):
                                if int(l[p-2].situacao[3]) < 6: fundir = "esquerda"
                            pos_vetor = p - 1           #se a esquerda dela tem uma sala pretendente, porque a esquerda dela e ocupado
                        elif l[p+1].pretendente == t and not l[p+2].vazio and b < 19:
                            if jogo.construirtipo == l[p+2].tipo and 1 == int(l[p+2].lvl):
                                if int(l[p+2].situacao[3]) < 6: fundir = "direita"
                            #se a direita dela tem uma pretendente porque sua direita esta ocupada
                        else: executar = False
                    else: 
                        executar = False                
                    if executar:
                        erguer(lista,pos_vetor,jogo,fundir)
                        jogo.modo = "espectador"
                        pretendencia(lista,pos_vetor,False)
                        pretendencia(lista,pos_vetor+1,False)
                        jogo.construirtipo = None
                        return False

        jogo.clock.tick(60)



def catalogo(jogo, lista, desfocar, voltar, ant, prox,livrpaginatual, flipar):
    
    anterior = pygame.image.load(path.join('sistema', ant + '.png'))
    proxima = pygame.image.load(path.join('sistema', prox + '.png'))

    opcao1 = pygame.image.load(path.join('sistema', 'comprar' + livrpaginatual[0] + '.png'))
    opcao2 = pygame.image.load(path.join('sistema', 'comprar' + livrpaginatual[1] + '.png'))
    opcao3 = pygame.image.load(path.join('sistema', 'comprar' + livrpaginatual[2] + '.png'))
    opcao4 = pygame.image.load(path.join('sistema', 'comprar' + livrpaginatual[3] + '.png'))
    
    animacao(jogo,lista, False)

    jogo.janela.blit(desfocar, (0,0))
    jogo.janela.blit(voltar, (0,0))
    jogo.janela.blit(anterior, (51,279))
    jogo.janela.blit(proxima, (969,279))

    jogo.janela.blit(opcao1, (153,279))
    jogo.janela.blit(opcao2, (357,279))
    jogo.janela.blit(opcao3, (561,279))
    jogo.janela.blit(opcao4, (765,279))

    if flipar == True: pygame.display.flip()



def texto(frase, cor, x, y):
    font = pygame.font.Font(None,30)
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(frase),True,cor)
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    display_surface.blit(debug_surf,debug_rect)


def fusao(jogo, lista, pos_vetor, fundir):

    print("teste")
    if fundir == "esquerda":
        if lista[pos_vetor-2].situacao[3] == "4":
            lista[pos_vetor-4].situacao = "_1-6"            
            lista[pos_vetor-3].situacao = "_2-6"
            lista[pos_vetor-2].situacao = "_3-6"            
            lista[pos_vetor-1].situacao = "_4-6"
            lista[pos_vetor].situacao = "_5-6"
            lista[pos_vetor+1].situacao = "_6-6"
        else:
            lista[pos_vetor-2].situacao = "_1-4"            
            lista[pos_vetor-1].situacao = "_2-4"
            lista[pos_vetor].situacao = "_3-4"
            lista[pos_vetor+1].situacao = "_4-4"

    elif fundir == "direita":
        if lista[pos_vetor+2].situacao[3] == "4":
            lista[pos_vetor].situacao = "_1-6"
            lista[pos_vetor+1].situacao = "_2-6"
            lista[pos_vetor+2].situacao = "_3-6"
            lista[pos_vetor+3].situacao = "_4-6"
            lista[pos_vetor+4].situacao = "_5-6"
            lista[pos_vetor+5].situacao = "_6-6"
        else:
            lista[pos_vetor].situacao = "_1-4"
            lista[pos_vetor+1].situacao = "_2-4"
            lista[pos_vetor+2].situacao = "_3-4"
            lista[pos_vetor+3].situacao = "_4-4"

    elif fundir == "esquerda e direita":
        lista[pos_vetor-2].situacao = "_1-6"
        lista[pos_vetor-1].situacao = "_2-6"
        lista[pos_vetor].situacao = "_3-6"
        lista[pos_vetor+1].situacao = "_4-6"
        lista[pos_vetor+2].situacao = "_5-6"
        lista[pos_vetor+3].situacao = "_6-6"
    
    lista[pos_vetor-4].obj = None            
    lista[pos_vetor-3].obj = None
    lista[pos_vetor-2].obj = None
    lista[pos_vetor-1].obj = None
    lista[pos_vetor].obj = None
    lista[pos_vetor+1].obj = None
    lista[pos_vetor+2].obj = None
    if pos_vetor <= 143:
        lista[pos_vetor+3].obj = None
        lista[pos_vetor+4].obj = None
        lista[pos_vetor+5].obj = None


def empregar_Dw_Cl(dweller,celula):

    #print("----------------------------------")

    if dweller.celula != None: 
        dweller.celula.morador = None
        #print("ola")
    if celula.morador != None: 
        celula.morador.celula = None
        #print("alo")

    dweller.celula = celula
    celula.morador = dweller



def HUD(jogo):

    icones = pygame.image.load(path.join('sistema', 'HUD.png'))
    jogo.janela.blit(icones,(0,651))

    #fundo = pygame.Surface(1071,701)

    #ja que o limite e 1000, o minimo pode diminuir inves
    energia_4pontas = ELESTE, ESUL, ELARGURA, EALTURA =  180 , 669, (jogo.energia // 10), 13 
    agua_4pontas = ALESTE, ASUL, ALARGURA, AALTURA = 360 , 669, (jogo.agua // 10), 13
    comida_4pontas = CLESTE, CSUL, CLARGURA, CALTURA = 540 , 669, (jogo.comida // 10), 13

    if jogo.agua >= (jogo.moradores * jogo.sobresalas.minimo): cor = 0, 255, 0
    else: cor = 255, 0, 0
    pygame.draw.rect(jogo.janela,cor,agua_4pontas)


    if jogo.comida >= (jogo.moradores * jogo.sobresalas.minimo): cor = 0, 255, 0
    else: cor = 255, 0, 0
    pygame.draw.rect(jogo.janela,cor,comida_4pontas)

    #if jogo.energia >= (jogo.sobresalas.consumo): cor = 0, 255, 0 #NA VDD DEVERIA SER O (CONSUMO - PRODUCAO POR HORA)
    if jogo.energia >= (jogo.sobresalas.consumo - (jogo.sobresalas.producao[4] * jogo.sobresalas.qtd_EQCAEDRT[4])): cor = 0, 255, 0 #TESTE
    else: cor = 255, 0, 0
    pygame.draw.rect(jogo.janela,cor,energia_4pontas)

    branco = 255, 255, 255
    texto(jogo.dinheiro,branco,720,665)
    frase = str(jogo.moradores) + "/" + str(jogo.lotacao)
    texto(frase,branco,885,665)


def evoluir(jogo,lista,pos_vetor):

    valeu =  pygame.mixer.Sound(path.join('sons','obrigado.wav'))

    jogo.sobresalas.preco_evoluir()
    if lista[pos_vetor].lvl == "3":
        pass #mostrar o erro e voltar.. talvez so transformar a seta em vermelha ou sla
    elif jogo.dinheiro < jogo.sobresalas.precoevoluir:
        pass #outro erro, sem dinheiro

    lista[pos_vetor].lvl = str(int(lista[pos_vetor].lvl) + 1)
    lista[pos_vetor+1].lvl = str(int(lista[pos_vetor+1].lvl) + 1)

    lista[pos_vetor].obj = None
    lista[pos_vetor+1].obj = None
    if int(lista[pos_vetor].situacao[3]) >= 4:

        lista[pos_vetor+2].lvl = str(int(lista[pos_vetor+2].lvl) + 1)
        lista[pos_vetor+3].lvl = str(int(lista[pos_vetor+3].lvl) + 1)

        lista[pos_vetor+2].obj = None
        lista[pos_vetor+3].obj = None
        print("ola")
        if lista[pos_vetor].situacao[3] == "6":
            print("ei")
            lista[pos_vetor+4].lvl = str(int(lista[pos_vetor+4].lvl) + 1)
            lista[pos_vetor+5].lvl = str(int(lista[pos_vetor+5].lvl) + 1)

            lista[pos_vetor+4].obj = None
            lista[pos_vetor+5].obj = None

            pos_max = pos_vetor + 5

        else: pos_max = pos_vetor + 3
    
    else: pos_max = pos_vetor + 1

    jogo.dinheiro = jogo.dinheiro - jogo.sobresalas.precoevoluir
    pygame.mixer.Sound.play(valeu)

    liberar_fusao(jogo,lista,pos_vetor,pos_max)
    




def demolir():
    pass



def sobrevivencia(jogo,lista,registro):


    if jogo.agua >= (jogo.moradores * jogo.sobresalas.minimo): radmais = False
    else: radmais = True

    if jogo.comida >= (jogo.moradores * jogo.sobresalas.minimo): vidamais = True
    else: vidamais = False

    max = jogo.moradores - 1
    contagem = 0
    
    while contagem <= max:

        #print("OLA")
        if registro[contagem] != None:

            if registro[contagem].xp >= 50:
                registro[contagem].xp -= 50
                registro[contagem].nivel += 1

            barreira = 100 - registro[contagem].radiacao 
            if vidamais: 
                registro[contagem].vida += 1
                if registro[contagem].vida > barreira: registro[contagem].vida = barreira
            else: registro[contagem].vida -= 2

            if radmais:
                registro[contagem].radiacao += 2
                barreira = 100 - registro[contagem].radiacao 
                if registro[contagem].vida > barreira: registro[contagem].vida = barreira
            else: 
                registro[contagem].radiacao -= 2
                if registro[contagem].radiacao < 0: registro[contagem].radiacao = 0

            if registro[contagem].vida == 0:
                if registro[contagem].celula != None:
                    id = registro[contagem].celula.id
                    #print(registro[contagem].celula)
                    #print(vars(registro[contagem].celula))
                    lista[id-1].morador = None
                #registro.pop(contagem)     #ACHO MELHOR N REMOVER DA LISTA, PRA PODER ACESSAR PELO ID..
                registro[contagem] = None
                morreu =  mixer.Sound(path.join('sons','morte.wav'))
                mixer.Sound.play(morreu)
                jogo.moradores -= 1
                #print("poxa..")
                #musica
            else: contagem += 1
        else: contagem += 1
        
        #print("SAI, ",contagem, max)

   #tirar a vida e aumentar a radiacao dos dwellers se tiver pouca comida ou agua, isso a cada hora?









def liberar_fusao(jogo,lista,pos_vetor,pm):

    #print("hm")

    b = (pos_vetor) % 21        #o pos_vetor tem que ser a direita
    l = lista
    p = pos_vetor
    fundir = None

    if l[p-1].tipo != None and l[pm+1].tipo != None and b > 0 and b < 20:
         if l[p].tipo == l[p-1].tipo and l[p].lvl == l[p-1].lvl and l[p].tipo == l[pm+1].tipo and l[p].lvl == l[pm+1].lvl:
            if l[p-1].situacao[3] != "2" and l[pm+1].situacao[3] != "2": fundir = "esquerda e direita"
            #print("1")
    elif l[p-1].tipo != None and b > 0:
        if l[p].tipo == l[p-1].tipo and l[p].lvl == l[p-1].lvl:
            if l[p-1].situacao[3] != "6": fundir = "esquerda"
            #print("2")
    elif l[pm+1].tipo != None and b < 19:
        if l[p].tipo == l[pm+1].tipo and l[p].lvl == l[pm+1].lvl:
            if l[pm+1].situacao[3] != "6": fundir = "direita"
            #print(l[p].tipo, l[p+2].tipo)
    if fundir != None: fusao(jogo,lista,pos_vetor,fundir)


def localtrabalho(jogo,lista,registro,dweller):

    voltar = pygame.image.load(path.join('sistema', 'voltar.png'))
    pode = ["porta","quarto","cozinha","tratamento","gerador","renda","laboratorio","treinamento"]

    while True:

        animacao(jogo,lista,False)
        jogo.janela.blit(voltar, (0,0))
        pygame.display.flip()

        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pos_x, pos_y = pygame.mouse.get_pos()
                    pos_vetor = achar_celula(position)

                    if pos_vetor == 0: return True

                    if lista[pos_vetor].vazio != None:
                        if not lista[pos_vetor].vazio:
                            if lista[pos_vetor].tipo in pode:
                                empregar_Dw_Cl(dweller,lista[pos_vetor])
                                return False



        
def cifra(jogo,dweller,y):
    cifra = pygame.image.load(path.join('sistema', 'cifra.png'))
    jogo.janela.blit(cifra,(620+10,y))

    teste = 33 #todos eles comecam pelo mesmo lugar no x

    carisma = CLESTE, CSUL, CLARGURA, CALTURA = 633, (y+19+(40 - (dweller.carisma*4))), 6, dweller.carisma*4
    inteligencia = ILESTE, ISUL, ILARGURA, IALTURA = 643, (y+19+(40 - (dweller.inteligencia*4))), 6, dweller.inteligencia*4
    forca = FLESTE, FSUL, FLARGURA, FALTURA = 653, (y+19+(40 - (dweller.forca*4))), 6, dweller.forca*4
    resistencia = RLESTE, RSUL, RLARGURA, RALTURA = 663, (y+19+(40 - (dweller.resistencia*4))), 6, dweller.resistencia*4
    agilidade = ALESTE, ASUL, ALARGURA, AALTURA = 673, (y+19+(40 - (dweller.agilidade*4))), 6, dweller.agilidade*4

    verde = 0, 255, 0
  
    pygame.draw.rect(jogo.janela,verde,carisma)
    pygame.draw.rect(jogo.janela,verde,inteligencia)
    pygame.draw.rect(jogo.janela,verde,forca)
    pygame.draw.rect(jogo.janela,verde,resistencia)
    pygame.draw.rect(jogo.janela,verde,agilidade)