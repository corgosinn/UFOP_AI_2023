#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-

"""
Inteligência Artificial - CSI457
Thiago Corgosinho Silva 20.2.8117
Ruan Tiengo Rocha
"""

#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.
"""

# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)

HUMANO = -1
COMP = +1

numero_de_ratos = 6
numero_de_gatos = 1

tabuleiro = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, -1, 0, 0, 0, 0],
]

"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: +1 se o computador vence; -1 se o HUMANOo vence; 0 empate
 """


def avaliacao(estado):

    if vitoria(estado, COMP):
        placar = +1
    elif vitoria(estado, HUMANO):
        placar = -1
    else:
        placar = 0

    return placar


""" fim avaliacao (estado)------------------------------------- """


def vitoria(estado, jogador):

    win_estado = [  # toda ultima linha
        estado[7][0], estado[7][1], estado[7][2], estado[7][3],
        estado[7][4], estado[7][5], estado[7][6], estado[7][7],
    ]
    # Se os jogadores forem os ratos
    if jogador == COMP:
        # Se o rato estiver na ultima posição, os ratos vencem
        if jogador in win_estado:
            return True
        # Se capturaram o gato, os ratos vencem
        elif numero_de_gatos == 0:
            return True
        else:
            return False
    else:
        # Se o gato capturou todos os ratos
        if numero_de_ratos == 0:
            return True
        else:
            return False


""" ---------------------------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""


def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)


""" ---------------------------------------------------------- """

"""
Verifica celular vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""


def celulas_vazias(estado):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0:
                celulas.append([x, y])
    return celulas


""" ---------------------------------------------------------- """

"""
Um movimento é valido se a célula escolhida está vazia.
:param (x): coordenada X
:param (y): coordenada Y
:return: True se o tabuleiro[x][y] está vazio
"""


def movimento_valido(x, y):
    if [x, y] in celulas_vazias(tabuleiro):
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Executa o movimento no tabuleiro se as coordenadas são válidas
:param (x): coordenadas X
:param (y): coordenadas Y
:param (jogador): o jogador da vez
"""


def exec_movimento(x, y, jogador):
    if movimento_valido(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False


""" ---------------------------------------------------------- """

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
mas nunca será nove neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""


def minimax(estado, profundidade, jogador):

    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado)
        return [-1, -1, placar]

    for cell in celulas_vazias(estado):
        x, y = cell[0], cell[1]
        estado[x][y] = jogador
        placar = minimax(estado, profundidade - 1, -jogador)
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == COMP:
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN
    return melhor


""" ---------------------------------------------------------- """

"""
Limpa o console para SO Windows
"""


def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


""" ---------------------------------------------------------- """

"""
Imprime o tabuleiro no console
:param. (estado): estado atual do tabuleiro
"""


def exibe_tabuleiro(estado, comp_escolha, humano_escolha):
    print('----------------')
    for row in estado:
        print('\n----------------')
        for cell in row:
            if cell == +1:
                print('|', comp_escolha, '|', end='')
            elif cell == -1:
                print('|', humano_escolha, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n----------------')


""" ---------------------------------------------------------- """

"""
Chama a função minimax se a profundidade < 9,
ou escolhe uma coordenada aleatória.
:param (comp_escolha): Computador escolhe X ou O
:param (humano_escolha): HUMANO escolhe X ou O
:return:
"""


def IA_vez(comp_escolha, humano_escolha):
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    if profundidade == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(tabuleiro, profundidade, COMP)
        x, y = move[0], move[1]

    exec_movimento(x, y, COMP)
    time.sleep(1)


""" ---------------------------------------------------------- """


def HUMANO_vez(comp_escolha, humano_escolha):
    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    # Dicionário de movimentos válidos
    movimento = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [0, 4], 6: [0, 5], 7: [0, 6], 8: [0, 7],
        9: [1, 0], 10: [1, 1], 11: [1, 2], 12: [1, 3], 13: [1, 4], 14: [1, 5], 15: [1, 6], 16: [1, 7],
        17: [2, 0], 18: [2, 1], 19: [2, 2], 20: [2, 3], 21: [2, 4], 22: [2, 5], 23: [2, 6], 24: [2, 7],
        25: [3, 0], 26: [3, 1], 27: [3, 2], 28: [3, 3], 29: [3, 4], 30: [3, 5], 31: [3, 6], 32: [3, 7],
        33: [4, 0], 34: [4, 1], 35: [4, 2], 36: [4, 3], 37: [4, 4], 38: [4, 5], 39: [4, 6], 40: [4, 7],
        41: [5, 0], 42: [5, 1], 43: [5, 2], 44: [5, 3], 45: [5, 4], 46: [5, 5], 47: [5, 6], 48: [5, 7],
        49: [6, 0], 50: [6, 1], 51: [6, 2], 52: [6, 3], 53: [6, 4], 54: [6, 5], 55: [6, 6], 56: [6, 7],
        57: [7, 0], 58: [7, 1], 59: [7, 2], 60: [7, 3], 61: [7, 4], 62: [7, 5], 63: [7, 6], 64: [7, 7],

    }

    limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    while (movimento < 1 or movimento > 9):
        try:
            movimento = int(input('Use numero (1..9): '))
            coord = movimentos[movimento]
            tenta_movimento = exec_movimento(coord[0], coord[1], HUMANO)

            if tenta_movimento == False:
                print('Movimento Inválido')
                movimento = -1
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')


""" ---------------------------------------------------------- """

"""
Funcao Principal que chama todas funcoes
"""


def main():

    limpa_console()
    humano_escolha = 'G'  # Pode ser Rato ou Gato
    comp_escolha = 'R'  # Pode ser Rato ou Gato
    primeiro = 'S'  # S se HUMANO primeiro e N caso o computador é o primeiro

    # Laço principal do jogo
    while len(celulas_vazias(tabuleiro)) > 0 and not fim_jogo(tabuleiro):
        if primeiro == 'N':
            IA_vez(comp_escolha, humano_escolha)
            primeiro = ''

        HUMANO_vez(comp_escolha, humano_escolha)
        IA_vez(comp_escolha, humano_escolha)

    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Perdeu!')
    else:
        limpa_console()
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Empate!')

    exit()


if __name__ == '__main__':
    main()
