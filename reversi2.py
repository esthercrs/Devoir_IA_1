import Reversi
from random import choice

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles.'''
    return choice([m for m in b.legal_moves()])

# def deroulementRandom(b):
#     '''Déroulement d'une partie au hasard des coups possibles. Cela illustre cependant comment on peut jouer avec la librairie
#     très simplement.'''
#     print("----------")
#     print(b)
#     if b.is_game_over():
#         return
#     b.push(randomMove(b))
#     deroulementRandom(b)
#     b.pop()


def minValue(b, alpha, beta, profondeur=3):
    if profondeur == 0 or b.is_game_over():
        return b.heuristique()

    for m in b.legal_moves():
        b.push(m)
        val = maxValue(b, alpha, beta, profondeur - 1)
        b.pop()
        if val < beta:
            beta = val
        if alpha >= beta:
            return alpha
    return beta

def maxValue(b, alpha, beta, profondeur=3):
    if profondeur == 0 or b.is_game_over():
        return b.heuristique()

    for m in b.legal_moves():
        b.push(m)
        val = minValue(b, alpha, beta, profondeur - 1)
        b.pop()
        if val > alpha:
            alpha = val
        if alpha >= beta:
            return beta
    return alpha

def IAAlphaBeta(b, alpha, beta, profondeur=3):
    meilleur_coup = None
    for m in b.legal_moves():
        b.push(m)
        val = minValue(b, alpha, beta, profondeur - 1)
        b.pop()
        if val > alpha or meilleur_coup is None:
            alpha = val
            meilleur_coup = m
    return meilleur_coup


board = Reversi.Board()

alpha= -2000
beta= 2000
profondeur=10
print(board)
while not board.is_game_over():
    coup = randomMove(board)
    board.push(coup)
    print('-------Random joue : ', coup)
    print(board)
    if board.is_game_over():
        break
    coup = IAAlphaBeta(board, alpha, beta, profondeur=profondeur)
    board.push(coup)
    print('-------IAAlphaBeta joue : ', coup)
    print(board)

