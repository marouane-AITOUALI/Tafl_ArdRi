# Tafl_ArdRi
ArdRi jeu de stratégie de la famille des jeux de tafl, développé avec une IA utilisant l'algorithme miniMax avec élagage Alpha-Beta

Le but est :

pour le joueur noir, de prendre le roi adverse - le pion blanc marqué d'une croix - ou
pour le joueur blanc, d'amener le roi dans une forteresse - les cases dans les coins du tablier.


# Déplacements:

Sur le jeu, un déplacement possible est affiché en bleu pour chaque pion sélectionné.
Les assaillants(pions noirs) jouent en premier.

Les pions se déplacent orthogonalement vers un emplacement libre, d'une ou plusieurs cases, comme la tour au jeu d'échecs. Toutes les cases empruntées lors du déplacement doivent être libres. Les assaillants ne peuvent accéder aux quatre forteresses situées aux coins, ni à la forteresse centrale où le roi commence la partie. Mais ils peuvent passer au-dessus de la case centrale si elle est libre.

Un pion est capturé (retiré du tablier) s'il se retrouve pris en tenaille par deux adversaires.
Cette tenaille est effectuée - lors d'un déplacement - sur les côtés opposés d'un alignement (vertical ou horizontal) jouxtant la case qu'il occupe.


# Capture Roi:
Le roi peut participer à la capture d'un pion adverse mais on ne peut pas le battre de la même façon
Pour capturer le roi, il faut l'entourer sur ses quatre côtés.
