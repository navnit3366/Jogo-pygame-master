
def verificar_pytest(jogo,lista,dwellers):
    ampulheta(jogo)
    inicializacao(jogo)
    carregou_corretamente(dwellers)
    emprego_certo(lista,dwellers)
    posicoes(lista)


def carregou_corretamente(dwellers):
    contagem = 0
    while contagem < len(dwellers):
        if dwellers[contagem] != None: 
            assert dwellers[contagem].sexo != None
            assert dwellers[contagem].vida > 0
        contagem += 1
def emprego_certo(lista,dwellers):
    contagem = 0
    while contagem < len(dwellers):
        if dwellers[contagem] != None: 
            assert dwellers[contagem].celula == lista[dwellers[contagem].celula.id-1]
            contagem += 1
def ampulheta(jogo):    #esta funcao zera o horario e troca o dia
    horario = 1.0   #mas ha uma funcao antes que executa comandos
    sair = False    #a meia noite, sendo preciso garantir que 24:00 acontece
    while not sair:
        horario += jogo.passagem
        if horario > 24.3:  
            assert (horario - jogo.passagem) >= 24.0    
            sair = True
            horario = 1.0
def inicializacao(jogo):
    assert jogo.dados.dificuldade != None
    assert jogo.dados.carregar != None
    assert jogo.dados != None
    assert jogo.sobresalas != None
    assert jogo.moradores > 0
def posicoes(lista):
    contagem = 0
    while contagem < 147:
        assert lista[contagem].coordenadas != None
        contagem += 1