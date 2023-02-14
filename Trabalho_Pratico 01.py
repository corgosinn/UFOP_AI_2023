#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-

"""
Trabalho Prático 1
Inteligência Artificial - CSI457
Thiago Corgosinho Silva 20.2.8117
Ruan Tiengo Rocha 19.2.8050
"""


from math import inf as infinity
from random import choice
import platform
import time
from os import system


# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)

HUMANO = -1
COMP = +1

numero_de_ratos = 6
numero_de_gatos = 1
rato_movimentando = -1
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


def avaliacao(estado):

    if vitoria(estado, COMP):
        placar = +1
    elif vitoria(estado, HUMANO):
        placar = -1
    else:
        placar = 0

    return placar


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


def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)


def jogadas_possiveis_gato(estado):
    moves = []
    row = pos_gato[0]
    col = pos_gato[1]
    # movimentos para frente
    i = row + 1
    while i < len(estado) and estado[i][col] >= 0:
        moves.append((i, col))
        if estado[i][col] > 0:
            break
        i = i + 1

    # movimentos para trás
    i = row - 1
    while i >= 0 and estado[i][col] >= 0:
        moves.append((i, col))
        if estado[i][col] > 0:
            break
        i = i - 1

    # movimentos para a esquerda
    j = col - 1
    while j >= 0 and estado[row][j] >= 0:
        moves.append((row, j))
        if estado[row][j] > 0:
            break
        j = j - 1

    # movimentos para a direita
    j = col + 1
    while j < len(estado[0]) and estado[row][j] >= 0:
        moves.append((row, j))
        if estado[row][j] > 0:
            break
        j = j + 1

    return moves


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
        if (x, y) in jogadas_possiveis_gato(tabuleiro):
            return True
        else:
            return False
    else:
        jogadas_todos_os_ratos =  jogadas_possiveis_ratos(tabuleiro)
        for index, cood_rato in enumerate(jogadas_todos_os_ratos):
            if [x, y] in cood_rato:
                global rato_movimentando
                rato_movimentando = index
                return True
        else:
            return False


def exec_movimento(x, y, jogador):
    if movimento_valido(x, y, jogador):
        if (jogador == -1):
            if (tabuleiro[x][y] == 1):
                global numero_de_ratos
                numero_de_ratos = numero_de_ratos - 1
            tabuleiro[pos_gato[0]][pos_gato[1]] = 0
            tabuleiro[x][y] = -1
            pos_gato[0] = x
            pos_gato[1] = y
        else:
            if (tabuleiro[x][y] == -1):
                global numero_de_gatos
                numero_de_gatos = numero_de_gatos - 1
            # Linha e coluna da posição antiga do rato
            linha_rato, coluna_rato = pos_ratos.get(rato_movimentando+ 1)[0],  pos_ratos.get(rato_movimentando+ 1)[1]
            # Seta a antiga posição como 0
            tabuleiro[linha_rato][coluna_rato] = 0
            # Atualiza a nova posição
            pos_ratos.update({rato_movimentando + 1: [x,y]})
            tabuleiro[x][y] = 1
        
        return True
    else:
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
            temp = estado[x][y]
            estado[x][y] = jogador
            placar = minimax(estado, profundidade - 1, -jogador)
            estado[x][y] = temp
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
    profundidade = 3
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
