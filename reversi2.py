import Reversi
from random import choice

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles.'''
    return choice([m for m in b.legal_moves()])

def minValue(b, alpha, beta, profondeur=3):
    if profondeur == 0 or b.is_game_over():
        return heuristique2(b)

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
        return heuristique2(b)

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

def nbAngle(b, player=None):
    # Position stratégiques dans les angles
    if player is None : 
        player = b._nextPlayer

    score = 0 
    # A MODIFIER, RAJOUTER CASE COTE
    val_case = {(0,0): 100, (b._boardsize-1,0): 100, (0,b._boardsize-1): 100, (b._boardsize-1,b._boardsize-1): 100}

    for position, value in val_case.items():
        if b._board[position[0]][position[1]] == player:
            score += value
        else:
            score -= value  # Pénalise les cases dans les angles occupées par l'adversaire
    return score

def nbTourAJouer(b, player=None):
    if player is None:
        player = b._nextPlayer

    # Obtenir les positions possibles pour le joueur actuel
    possible_moves = b.legal_moves()

    # Initialiser le score
    scoreTour = 0

    # Définir la valeur en fonction du joueur
    value = 1 if player == b._nextPlayer else -1

    # Calculer le score en fonction des positions possibles
    for move in possible_moves:
        x, y = move[1], move[2]
        if b._board[x][y] == player:
            scoreTour += value
        else:
            scoreTour -= value
    return scoreTour

# Implémenter quand en fonction du nombre de piece qu'on mange ?

def heuristique2(b, player=None):
    if player is None:
        player = b._nextPlayer
    h = b.heuristique()
    a = nbAngle(b)
    t = nbTourAJouer(b)
    return h+a+t

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
