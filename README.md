README Devoir d'intélligence articifielle
fait par : Elsa Coutaud, Esther Cros et Mallory Le Corre

Installation à faire avant de lancer le code : 
pip install : random, time, os

IA employé : 
Notre groupe à choisi de travailler avec MinMax. Ce type d'algorithme de recherche contradictoire représente les conditions gagnantes par des valeurs négatives pour un camp et par des valeurs positives pour l'autre. Les actions ultérieures seront déterminées par ces conditions, le côté minimisant essayant d'obtenir le score le plus bas, et le côté maximisant essayant d'obtenir le score le plus élevé.

Technique d'optimisation : 
Nous avons choisi d'utiliser Alpha Beta afin d'optimiser MinMax. Ayant un plateau très grand et donc de nombreuses possibilités de jeu il nous as parut judicieux de sauter certains des calculs récursifs qui sont résolument défavorables. 
En effet, après avoir établi la valeur d'une action, s'il existe une première preuve que l'action suivante peut amener l'adversaire à obtenir un meilleur score que l'action déjà établie nous n'avons pas jugé nécéssaire d'étudier plus cette action.

Heuristique : 
Nous avons utilisé l'heuristique fourni et permettant de compter les pièces. Nous l'avons amélioré en l'associant à une fonction permettant de donner plus d'importance à certaines cases. Nous avons constaté en étudiant les stratégies de jeux qu'avoir les angles était un réel avantage pour la partie. Les cases autours des angles elles au contraire ne sont pas des plus avantageuse. Sachant cela nous avons donné des valeurs aux cases. Positives lorsqu'elles sont avantageuse et négatives lorsqu'elles ne le sont pas. 

Amélioration : 
Afin de permettre une meileure intéraction avec notre code nous avons rajouté un aspect graphique à la sortie sur le terminal.
Le projet correspondant premièrement à un jeu, nous avons donc souhaiter proposer un menu permettant de choisir diverses options de jeu. 
Il est possible tout d'abord de consulter les régles de jeu. Puis d'observer une partie entre deux IA ou entre une IA et des coups random.
La dernière option propose des statistiques sur la partie opposant l'IA à des coups random. Pour cette partie nous avons simplement fait une fonction qui lance un nombre de partie à préciser et d'en donner le nombre de victoire et de défaite. 

A savoir : Le joueur 'White' correspond à l'IA pour les parties opposant IA et random. 
