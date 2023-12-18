import Reversi
from random import choice
import time
import os


def menu() :
    """Affiche le menu principal et demande au joueur ce qu'il veut faire.

    Returns:
        input: Demande le choix du joueur.
    """
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


def return_menu() :
    """Permet de retourner au menu principal.
    """
    print("=====================================")
    rep=(input("Tapez 0 pour retourner au menu principal : "))
    while rep!="0":
        rep=(input("Tapez 0 pour retourner au menu principal : "))
    print("===== Retour au menu principal ...")
    time.sleep(1)
    os.system('clear')
    os.system('cls')


def rgame_rules():
    """Affiche les règles du jeu.
    """
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
        " \n")


def randomMove(b):
    """Renvoie un mouvement au hasard sur la liste des mouvements possibles.

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.

    Returns:
        list: Mouvement au hasard dans la liste des mouvements possibles [nextPlayer,x,y]
    """
    return choice([m for m in b.legal_moves()])


def minValue(b, alpha, beta, profondeur):
    """Cherche à minimiser la valeur dans l'arbre de recherche.  

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.
        alpha (int): Valeur alpha de l'élagage alpha-beta.
        beta (int): Valeur beta de l'élagage alpha-beta.
        profondeur (int): Profondeur de recherche de l'algorithme.

    Returns:
        int: Valeur minimale ou évaluation heuristique. 
    """
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
    """Cherche à maximiser la valeur dans l'arbre de recherche.

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.
        alpha (int): Valeur alpha de l'élagage alpha-beta.
        beta (int): Valeur beta de l'élagage alpha-beta.
        profondeur (int): Profondeur de recherche de l'algorithme.

    Returns:
        int: Valeur maximale ou évaluation heuristique.
    """
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
    """Recherche du meilleur mouvement à jouer 

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.
        alpha (int): Valeur alpha de l'élagage alpha-beta.
        beta (int): Valeur beta de l'élagage alpha-beta.
        profondeur (int): Profondeur de recherche de l'algorithme.

    Returns:
        list: Meilleur mouvement à jouer [nextPlayer,x,y]
    """
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
    """Donne un score en fonction des positions stratégiques sur le plateau. 
    Les angles sont des positions stratégiques. 
    Au contraire les cases autour de l'angle de ne le sont pas car elles permettent au joueur suivant de se positionner dans l'angle.

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.
        player (int, optional): Prochain joueur à jouer. Defaults to None.

    Returns:
        int: Score en fonction des positions stratégiques sur le plateau.
    """
    if player is None : 
        player = b._nextPlayer
    score = 0 
    val_case = {(0,0): 100, (b._boardsize-1,0): 100, (0,b._boardsize-1): 100, (b._boardsize-1,b._boardsize-1): 100, 
                (1,0):-50,(0,1):-50,(1,1):-100,
                (0,b._boardsize-2):-50,(b._boardsize-1,1):-50,(b._boardsize-2,1):-100,
                (0,b._boardsize-2):-50,(1,b._boardsize-1):-50,(1,b._boardsize-2):-100,
                (b._boardsize-2,b._boardsize-1):-50,(b._boardsize-1,b._boardsize-2):-50,(b._boardsize-2,b._boardsize-2):-100}
    for position, value in val_case.items():
        if b._board[position[0]][position[1]] == player:
            score += value
        else:
            score -= value
    return score


def heuristique2(b, player=None):
    """Implémente une heuristique en fonction du nombre de pièce et des positions stratégiques du plateau. 

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.
        player (int, optional): Prochain joueur à jouer. Defaults to None.

    Returns:
        int: Score de l'heuristique
    """
    if player is None:
        player = b._nextPlayer
    h = b.heuristique()
    a = nbAngle(b)
    return h+a


def winner(b):
    """Compare les scores des deux joueurs et affiche le gagnant.

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.

    Returns:
        str: winner
    """
    nb_W, nb_B = b.get_nb_pieces()
    winner = ""
    if nb_B>nb_W:
        print ("Victoire de Black")
        winner = "black"
    elif nb_W>nb_B: 
        print("Victoire de White")
        winner = 'white'
    else :
        print("Egalité")
        winner = "egalite"
    return winner
        

def partie_IA_Random(b, profondeur = 5, affichage = True):
    """Création d'une partie entre notre IA et un joueur random.

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.
        profondeur (int): profondeur de recherche de l'algorithme. Defaults to 5.
        affichage (bool): Affichage du déroulement de la partie. Defaults to True.

    Returns:
        str: winner
    """
    alpha= -2000
    beta= 2000

    while not b.is_game_over():
        coup = randomMove(b)
        b.push(coup)
        if affichage :
            print('-------Random joue : ', coup)
            print(b)
        if b.is_game_over():
            break

        coup = IAAlphaBeta(b, alpha, beta, profondeur=profondeur)
        b.push(coup)
        if affichage : 
            print('-------IA AlphaBeta joue : ', coup)
            print(b)       

    print(f'====FIN DE LA PARTIE. Résultat :')
    win = winner(b)
    return win


def partie_IA_IA(b, profondeur = 5, affichage = True):
    """Création d'une partie entre deux joueurs IA.

    Args:
        b (Reversi.Board): Implémentation du jeu Reversi.
        profondeur (int): profondeur de recherche de l'algorithme. Defaults to 5.
        affichage (bool): Affichage du déroulement de la partie. Defaults to True.

    Returns:
        str: winner
    """
    alpha= -2000
    beta= 2000

    while not b.is_game_over():
        coup = IAAlphaBeta(b, alpha, beta, profondeur=profondeur)
        b.push(coup)
        if affichage :
            print('-------IAAALphaBeta_1 joue : ', coup)
            print(b)
        if b.is_game_over():
            break

        coup = IAAlphaBeta(b, alpha, beta, profondeur=profondeur)
        b.push(coup)
        if affichage : 
            print('-------IAAlphaBeta_2 joue : ', coup)
            print(b)

    print(f'FIN DE LA PARTIE. Résultat :')
    win = winner(b)
    return win


def stat(nbr_partie,profondeur):
    """Permet de générer plusieurs partie contre un joueur random pour obtenir des statistiques sur le nombre
    de partie gagnées par l'IA.

    Args:
        nbr_partie (int): nombre de parties à générer
    """
    score_B = 0
    score_W = 0
    egal = 0
    n=0
    while n < nbr_partie : 
        board = Reversi.Board()
        winner = partie_IA_Random(board, profondeur= profondeur, affichage= False)

        n=n+1
        if winner == 'black' :
            score_B += 1
        if winner == 'white' : 
            score_W += 1
        if winner == 'egalite': 
            egal += 1
        
    print("Black gagne : ", score_B, " fois")
    print("White gagne : ", score_W, " fois")
    print("Il y a eu : ", egal, "egalite")



def main():
    os.system('clear') 
    os.system('cls')
    print("===================================")    
    print("    B I E N V E N U E   D A N S    ")
    print("           R E V E R S I           ")
    print("===================================")
    time.sleep(3)
    os.system('clear')
    os.system('cls')
    choice=menu()

    while(choice!="0") :
        if (choice=="1") :
            rgame_rules()
            return_menu()

        if (choice=="2"):
            board = Reversi.Board()
            print("===== Début de la partie Random vs IA...")
            partie_IA_Random(board)
            return_menu()

        if (choice=="3"):
            board = Reversi.Board()
            print("===== Début de la partie IA vs IA...")
            partie_IA_IA(board)
            return_menu()
            
        if (choice=="4"):
            val = int(input("Vous voulez des stats sur quel nombre de partie ? "))
            prof = int(input("Quelle profondeur voulez vous tester? "))
            stat(val,prof)
            return_menu()
            
        choice=menu()

if __name__ == "__main__":
    main()
