#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-

"""
Inteligência Artificial - CSI457
Thiago Corgosinho Silva 20.2.8117
Ruan Tiengo Rocha 19.2.8050
"""

#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
Trabalho prático 1
"""

# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)

HUMANO = -1
COMP = +1

numero_de_ratos = 6
numero_de_gatos = 1
pos_gato = [7, 3]
pos_ratos = {1: [1, 0], 2: [1, 1], 3: [1, 2], 4: [1, 5], 5: [1, 6], 6: [1, 7]}

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
:returna: +1 se o computador vence; -1 se o HUMANOo vence;
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
        elif numero_de_gatos == 0:  # se capturarem o rato
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


def jogadas_possiveis_gato(estado):
    moves = []
    row = pos_gato[0]
    col = pos_gato[1]
    # movimentos para frente
    print("Entra nas jogados possiveis do gato")
    i = row + 1
    while i < len(estado) and estado[i][col] >= 0:
        if estado[i][col] > 0:
            break
        moves.append((i, col))
        i = i + 1

    # movimentos para trás
    i = row - 1
    while i >= 0 and estado[i][col] >= 0:
        if estado[i][col] > 0:
            break
        moves.append((i, col))
        i = i - 1

    # movimentos para a esquerda
    j = col - 1
    while j >= 0 and estado[row][j] >= 0:
        if estado[row][j] > 0:
            break
        moves.append((row, j))
        j = j - 1

    # movimentos para a direita
    j = col + 1
    while j < len(estado[0]) and estado[row][j] >= 0:
        if estado[row][j] > 0:
            break
        moves.append((row, j))
        j = j + 1

    return moves

#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, 0, 0, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, -1, 0, 0, 0, 0],
#


def jogadas_possiveis_ratos(estado):
    jogadas = []
    for numero_rato in pos_ratos.keys():
        jogadas.append(jogadas_possiveis_rato(estado, pos_ratos[numero_rato]))
    return jogadas


def jogadas_possiveis_rato(estado, rato):
    celulas = []
    linha = rato[0]
    coluna = rato[1]

    if linha + 1 <= 7:
        # diagonal para esquerda
        if coluna - 1 >= 0:
            if estado[linha+1][coluna - 1] == -1:
                celulas.append([linha+1, coluna-1])
    # diagonal para direita
        if coluna + 1 <= 7:
            if estado[linha+1][coluna + 1] == -1:
                celulas.append([linha + 1, coluna + 1])
    # Se o movemento a frente está livre
        if estado[linha+1][coluna] <= 0:
            celulas.append([linha + 1, coluna])
    # Primeiro movimento do rato pode ser 2 linhas

    if linha + 2 <= 7 and linha == 1:
        if estado[linha + 2][coluna] <= 0:
            celulas.append([linha + 2, coluna])
    return celulas


def movimento_valido(x, y, jogador):
    if jogador == -1:
        print("entrei")
        print(f"JOGADAS GATO: {jogadas_possiveis_gato(tabuleiro)}")
        if (x, y) in jogadas_possiveis_gato(tabuleiro):
            return True
        else:
            return False
    else:
        print(f"JOGADAS RATO: {jogadas_possiveis_gato(tabuleiro,jogador)}")
        if [x, y] in jogadas_possiveis_ratos(tabuleiro, jogador):
            return True
        else:
            return False


def exec_movimento(x, y, jogador):
    if movimento_valido(x, y, jogador):
        print("movimento valido")
        if (jogador == -1):
            if (tabuleiro[x][y] == 1):
                numero_de_ratos = numero_de_ratos - 1
            tabuleiro[pos_gato[0]][pos_gato[1]] = 0
            tabuleiro[x][y] = -1
            pos_gato[0] = x
            pos_gato[1] = y
        else:
            if (tabuleiro[x][y] == -1):
                numero_de_gatos = numero_de_gatos - 1
            tabuleiro[x][y] = 1

        tabuleiro[x][y] = jogador
        return True
    else:
        print("movimento invalido")
        return False


def minimax(estado, profundidade, jogador):
    # Valor minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]
    # Valor minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(estado):
        placar = avaliacao(estado)
        return [-1, -1, placar]
    if jogador == COMP:
        jogadas = jogadas_possiveis_gato(estado)
        for cell in jogadas:
            x = cell[0]
            y = cell[1]
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
    else:
        jogadas = jogadas_possiveis_ratos(estado)
        for indice_rato, jogadas_possiveis in enumerate(jogadas):
            for cell in jogadas_possiveis:
                x = cell[0]
                y = cell[1]
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


def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def exibe_tabuleiro(estado, comp_escolha, humano_escolha):
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            print(f"{estado[x][y]}", end=' ')
        print()


def IA_vez(comp_escolha, humano_escolha):
    profundidade = len(jogadas_possiveis_gato(tabuleiro))
    if fim_jogo(tabuleiro):
        return

    # limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    move = minimax(tabuleiro, profundidade, COMP)
    x, y = move[0], move[1]

    exec_movimento(x, y, COMP)
    time.sleep(1)


""" ---------------------------------------------------------- """


def HUMANO_vez(comp_escolha, humano_escolha):
    if fim_jogo(tabuleiro):
        return

    # Dicionário de movimentos válidos
    linha = -1
    coluna = -1
    # limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)

    while (linha < 1 or linha > 8 or coluna < 1 or coluna > 8):
        try:
            linha = int(input('Digite o numero da linha ( 1 a 8 ): '))
            coluna = int(input('Digite o numero da coluna ( 1 a 8 ): '))
            coord = (linha - 1, coluna - 1)
            tenta_movimento = exec_movimento(coord[0], coord[1], HUMANO)

            if tenta_movimento == False:
                print('Movimento Inválido')
                linha = -1
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Inválida!')
            linha = -1
            coluna = -1


def main():
    # limpa_console()
    humano_escolha = 'G'  # Pode ser Rato ou Gato
    comp_escolha = 'R'  # Pode ser Rato ou Gato
    primeiro = 'S'  # S se HUMANO primeiro e N caso o computador é o primeiro

    # Laço principal do jogo
    while not fim_jogo(tabuleiro):
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
    exit()


if __name__ == '__main__':
    main()
