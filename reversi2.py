import Reversi
from random import choice
import time
import os

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles.'''
    return choice([m for m in b.legal_moves()])

def minValue(b, alpha, beta, profondeur):
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

def maxValue(b, alpha, beta, profondeur):
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

def IAAlphaBeta(b, alpha, beta, profondeur):
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
    ''' Les angles sont des positions stratégiques, au contraite les cases autour de l'angle de ne le sont pas car elles permettent au joueur suivant de se positionner dans l'angle.'''
    if player is None : 
        player = b._nextPlayer
    score = 0 
    val_case = {(0,0): 100, (b._boardsize-1,0): 100, (0,b._boardsize-1): 100, (b._boardsize-1,b._boardsize-1): 100,
                (1,0):-50,(0,1):-50,(1,1):-100,(0,b._boardsize-2):-50,(b._boardsize-1,1):-50,(b._boardsize-2,1):-100,(0,b._boardsize-2):-50,(1,b._boardsize-1):-50,(1,b._boardsize-2):-100,(b._boardsize-2,b._boardsize-1):-50,(b._boardsize-1,b._boardsize-2):-50,(b._boardsize-2,b._boardsize-2):-100}
    for position, value in val_case.items():
        if b._board[position[0]][position[1]] == player:
            score += value
        else:
            score -= value
    return score

def heuristique2(b, player=None):
    if player is None:
        player = b._nextPlayer
    h = b.heuristique()
    a = nbAngle(b)
    #t = nbTourAJouer(b)
    return h+a

# Print the menu and ask what the player wants to do
def menu() :
    print("=====================================")
    print("    M E N U     P R I N C I P A L    ")
    print("=====================================")
    print("1 - Règles du jeu")
    print("2 - Observer une partie IA vs Random")
    print("3 - Observer une partie IA vs IA")
    print("4 - Regarder les stats d'IA vs Random")
    print("0 - Quitter")
    print("=====================================")
    return input(">>>>> Que voulez-vous faire ? ")

# print the game's rules
def rgame_rules():
    os.system('clear')
    os.system('cls')
    print("=====================================")
    print("    R E G L E S     D U     J E U    ")
    print("=====================================")
    print("Le plateau de jeu représente un damier de 100 cases. "\
        "Chaque joueur dispose de 50 tuiles. L'objectif est d'avoir plus de tuiles de sa couleur que l'adversaire à la fin de la partie. "\
        "Celle-ci s'achèvera lorsqu'aucun des deux joueur ne peut plus jouer de coup légal. "\
        "Cela intervient généralement lorsque les 100 cases sont occupées.\n\n"\
 
        "Au départ, 2 tuiles de chaque couleur sont disposés sur les 4 cases centrales. "\
        "A tour de rôle, chacun pose une tuile avec l'obligation "\
        "de prendre au moins une tuile adverse. (Votre jeton doit être posé "\
        "de manière à entourer 1 ou plusieurs jetons adverses.)\n")
 
    print("  +-----+-----+-----+-----+                     +-----+-----+-----+-----+ ")                  
    print("  |     |     |     |     |                     |     |     |     |     | ")
    print("  +-----+-----+-----+-----+                     +-----+-----+-----+-----+ ")
    print("  |     |  R  |  V  |     |         ->          |     |  R  |  V  |     | ")    
    print("  +-----+-----+-----+-----+                     +-----+-----+-----+-----+ ")
    print("  |     |  V  |  R  |     |                     |     |  V  |  V  |  V  | ")
    print("  +-----+-----+-----+-----+                     +-----+-----+-----+-----+ ")
    print("  |     |     |     |     |                     |     |     |     |     | ")
    print("  +-----+-----+-----+-----+                     +-----+-----+-----+-----+ \n")
   
    print("Une piece peut être posée dans les direction horizontales, "\
        "verticales et diagonales.\n"\
        "La partie se termine quand tous le jetons sont posés, ou si aucun "\
        "joueur ne peut plus jouer.\n"\
        "Le vainqueur est celui qui possède le plus de tuiles de sa couleur "\
        "sur le plateau.\n"\
        " \n"\
 
        "Comment jouer :\n"\
        "Pour jouer une tuile, regardez les numeros de lignes et de colonnes et indiquez dans le terminal la case où vous souhaitez jouer.\n"
        "Les cases que vous pouvez jouer peuvent être indiqué par un O selon l'option de jeu.\n")
    print("=====================================")
    rep=(input("Tapez 0 pour retourner au menu principal : "))
    while rep!="0":
        rep=(input("Tapez 0 pour retourner au menu principal : "))
    print("===== Retour au menu principal ...")
    time.sleep(2)

# Compare the scores of the two players
def winner(board):
    nb_W, nb_B = board.get_nb_pieces()
    if nb_B>nb_W:
        print ("Black gagne")
        return 'Black'
    if nb_W>nb_B: 
        print("White gagne")
        return 'White'
    else : 
        print("Ex aequo")
        return 'Execo'
        

def partie_IA_Random(board):
    alpha= -2000
    beta= 2000
    profondeur=5

    # print(board)

    while not board.is_game_over():
        coup = randomMove(board)
        board.push(coup)
        # print('-------Random joue : ', coup)
        # print(board)

        if board.is_game_over():
            break

        coup = IAAlphaBeta(board, alpha, beta, profondeur=profondeur)
        board.push(coup)
        # print('-------IAAlphaBeta joue : ', coup)
        # print(board)
    return (winner(board))

def partie_IA_IA(board):
    alpha= -2000
    beta= 2000
    profondeur=5
    print(board)
    while not board.is_game_over():
        coup = IAAlphaBeta(board, alpha, beta, profondeur=profondeur)
        board.push(coup)
        print('-------IAAALphaBeta_1 joue : ', coup)
        print(board)
        if board.is_game_over():
            break
        coup = IAAlphaBeta(board, alpha, beta, profondeur=profondeur)
        board.push(coup)
        print('-------IAAlphaBeta_2 joue : ', coup)
        print(board)
    return (winner(board))

'''def partie_IA_Humain(board):
    alpha= -2000
    beta= 2000
    profondeur=3
    print(board)
    while not board.is_game_over():

        print("Dans quelle case voulez vous jouer ?")
        global ligne
        ligne=input("Ligne : ")
        global colonne
        colonne=input("Colonne : ")
        while ligne.isdigit()==False or int(ligne) not in range(0,board._boardsize-1):
            print("Dans quelle case voulez vous jouer ?")
            ligne=input("Ligne : ")
        while colonne.isdigit()==False or int(colonne) not in range(1,9):
            print("Dans quelle case voulez vous jouer ?")
            colonne=input("Colonne : ")
        if board.is_valid_move(board._nextPlayer, ligne, colonne):
            coup = [board._nextPlayer,ligne,colonne]
        board.push(coup)
        print('-------l Humain joue : ', coup)
        print(board)
        if board.is_game_over():
            break
        coup = IAAlphaBeta(board, alpha, beta, profondeur=profondeur)
        board.push(coup)
        print('-------IAAlphaBeta_2 joue : ', coup)
        print(board)
    winner(board)'''

def stat(nbr_partie):
    alpha= -2000
    beta= 2000
    profondeur=5

    score_B = 0
    score_W = 0
    exec = 0

    n=0

    while n < nbr_partie : 
        board = Reversi.Board()
        winner = partie_IA_Random(board)

        n=n+1
        if winner == 'Black' :
            score_B += 1
        if winner == 'White' : 
            score_W += 1
        if winner == 'Exec': 
            exec += 1
        
    print("Black gagne : ", score_B, " fois")
    print("White gagne : ", score_W, " fois")
    print("Il y a eu : ", exec, "egalite")

def main():

    os.system('clear') #for Linux
    #os.system('cls')   #for Windows
    print("===================================")    
    print("    B I E N V E N U E   D A N S    ")
    print("           R E V E R S I           ")
    print("===================================")
    time.sleep(3)
    os.system('clear')
    #os.system('cls')

    choice=menu()
    h=False

    while(choice!="0") :
        if (choice=="1") :
            rgame_rules()
        if (choice=="2"):
            board = Reversi.Board()
            print("===== Début de la partie Random vx IA...")
            partie_IA_Random(board)
            print(board)
        if (choice=="3"):
            board = Reversi.Board()
            print("===== Début de la partie IA vs IA...")
            partie_IA_IA(board)
        if (choice=="4"):
            val = int(input("Vous voulez des stats sur quel nombre de partie ? "))
            stat(val)
        #if (choice=="4"): # A rajouter dans le menu
            #board = Reversi.Board()
            #print("===== Début de la partie...")
            #partie_IA_Humain(board)
        choice=menu()

if __name__ == "__main__":
    main()
