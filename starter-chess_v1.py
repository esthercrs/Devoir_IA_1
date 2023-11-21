# -*- coding: utf-8 -*-
import time
import chess
from random import randint, choice

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.generate_legal_moves()])

def deroulementRandom(b):
    '''Déroulement d'une partie d'échecs au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    print(b)
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    b.push(randomMove(b))
    deroulementRandom(b)
    b.pop()

# Question 1 :
def exploreProfondeur(b, profondeur=3):
    '''Fonction qui explore l'arbre des coups possibles jusqu'à une certaine profondeur.'''
    if b.is_game_over() or profondeur == 0:
        return
    for m in b.generate_legal_moves():
        b.push(m)
        exploreProfondeur(b, profondeur-1)
        b.pop()

def exploreProfondeur(b, time_limit, profondeur=3):
    '''Fonction qui explore l'arbre des coups possibles jusqu'à une certaine profondeur et lèe ue exception dès que 
        time_limit est dépassée.
    '''
    global start
    
    if time.time() - start > time_limit:
            raise Exception("Temps dépassé")
    if b.is_game_over() or profondeur == 0:
        return
    for m in b.generate_legal_moves():
        b.push(m)
        exploreProfondeur(b, time_limit, profondeur-1)
        b.pop()

def exploreProfondeurEtCompter(b, time_limit, profondeur=3):
    '''Fonction qui explore l'arbre des coups possibles jusqu'à une certaine profondeur et lèe ue exception dès que 
        time_limit est dépassée. Elle compte aussi le nombre de noeuds
    '''
    global start
    # global nb_coups
    if time.time() - start > time_limit:
            raise Exception("Temps dépassé")
    if b.is_game_over() or profondeur == 0:
        return 1
    nb_coups = 1
    for m in b.generate_legal_moves():
        b.push(m)
        nb_coups += exploreProfondeurEtCompter(b, time_limit, profondeur-1)
        b.pop()
    return nb_coups    

# Question 2 :
def eval_board(b):
    '''Fonction qui implémente l'heuristique de Shannon. Elle affecte un poids à chaque pièce sur l'échiquier.'''
    # Poids des pièces
    val_pieces = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 200}
    score = 0
    for k, piece in b.piece_map().items():
        line = k // 8
        if piece.symbol().upper()==piece.symbol():
            score += val_pieces[piece.symbol().upper()]
        else:
            score -= val_pieces[piece.symbol().upper()]
        if piece.symbol() == 'P':
            score += 0.1 * line
        elif piece.symbol() == 'p':
            score -= 0.1 * (7-line)
    return score


# Question 3 :

def minMax(b, blanc=True, profondeur=3):
    '''Fonction qui implémente l'algorithme MinMax sans élagage alpha-beta. '''
    if b.is_game_over():
        if b.result() == '1-0':
            return 1000 if blanc else -1000
        elif b.result() == '0-1':
            return -1000 if blanc else 1000
        else:
            return 0
    if profondeur == 0:
        return eval_board(b)
    pire = 2000
    for m in b.generate_legal_moves():
        b.push(m)
        pire = min(pire, maxMin(b, not blanc, profondeur-1))
        b.pop()
    return pire

def maxMin(b, blanc=True, profondeur=3):
    '''Fonction qui implémente l'algorithme MaxMin sans élagage alpha-beta. '''
    if b.is_game_over():
        if b.result() == '1-0':
            return 1000 if blanc else -1000
        elif b.result() == '0-1':
            return -1000 if blanc else 1000
        else:
            return 0
    if profondeur == 0:
        return eval_board(b)
    meilleur = -2000
    for m in b.generate_legal_moves():
        b.push(m)
        meilleur = max(meilleur, minMax(b, not blanc, profondeur-1))
        b.pop()
    return meilleur

def IAMinMax(b, blanc=True, profondeur=3):
    '''Fonction qui implémente l'algorithme MinMax sans élagage alpha-beta et retourne le meilleur coup. '''
    meilleur = -2000
    meilleur_coup = None
    meilleurs_coup = []
    for m in b.generate_legal_moves():
        b.push(m)
        score = maxMin(b, not blanc, profondeur-1)
        if score > meilleur or meilleur_coup is None:
            meilleur = score
            meilleur_coup = m
            meilleurs_coup = [m]
        elif score == meilleur:
            meilleurs_coup.append(m)
        b.pop()

    return choice(meilleurs_coup)        

#Partie3

def minValue(b, alpha, beta, blanc=True, profondeur=3):
    if b.is_game_over():
        if b.result() == '1-0':
            return 1000 if blanc else -1000
        elif b.result() == '0-1':
            return -1000 if blanc else 1000
        else:
            return 0
    if profondeur == 0:
        return eval_board(b)

    for m in b.generate_legal_moves():
        b.push(m)
        val=maxValue(b,alpha, beta, not blanc, profondeur-1)    
        b.pop()
        if val < beta : 
            beta = val 
        if alpha >= beta : 
            return alpha
    return beta


def maxValue(b, alpha, beta, blanc=True, profondeur=3):
    if b.is_game_over():
        if b.result() == '1-0':
            return 1000 if blanc else -1000
        elif b.result() == '0-1':
            return -1000 if blanc else 1000
        else:
            return 0
    if profondeur == 0:
        return eval_board(b)

    for m in b.generate_legal_moves():
        b.push(m)
        val=minValue(b,alpha, beta, not blanc, profondeur-1)    
        b.pop()
        if val > alpha : 
            alpha = val 
        if alpha >= beta : 
            return beta
    return alpha 

def IAAlphaBeta(b, alpha, beta, blanc=True, profondeur=3):
    # alpha = -2000
    # beta = 2000
    meilleur_coup = None
    for m in b.generate_legal_moves():
        b.push(m)
        val = minValue(b, alpha, beta, not blanc, profondeur - 1)
        b.pop()
        if val > alpha or meilleur_coup is None:
            alpha = val
            meilleur_coup = m
    return meilleur_coup


board = chess.Board()
# deroulementRandom(board)
# Question 1 :
# Jusqu'à quelle profondeur on peut explorer en 30s
# for p in range(10):
#     start = time.time()
#     exploreProfondeur(board, time_limit=30, profondeur=p)
#     end = time.time()
#     print("Profondeur : ", p, " temps : ", end-start)

# Combien de noeuds à profondeurs 1, 2, 3, ... en 30s
# for p in range(1, 5):
#     start = time.time()
#     nb_coups = exploreProfondeurEtCompter(board, time_limit=30, profondeur=p)
#     end = time.time()
#     print('Profondeur : ', p, ' temps : ', end-start, ' nb_coups : ', nb_coups)
# Question 1 (Fin)

# Question 4 :
# Un match joeur aléatoire contre IA MinMax à profondeur 3
# while not board.is_game_over():
#     print(board)
#     coup = randomMove(board)
#     board.push(coup)
#     print('Joeur aléatoire joue : ', coup)
#     if board.is_game_over():
#         break
#     coup = IAMinMax(board, profondeur=3)
#     board.push(coup)
#     print('IAMinMax joue : ', coup)

# print(board.result())

#MATCH IAMiniMax à profondeur 3 contre une IAAlphaBeta à profondeur 3
alpha= -2000
beta= 2000
profondeur=3
while not board.is_game_over():
    print(board)
    coup = IAMinMax(board, blanc=True, profondeur=profondeur)
    board.push(coup)
    print('IAMiniMax joue : ', coup)
    if board.is_game_over():
        break
    coup = IAAlphaBeta(board, alpha, beta, blanc=False, profondeur=profondeur)
    board.push(coup)
    print('IAAlphaBeta joue : ', coup)

print(board.result())





