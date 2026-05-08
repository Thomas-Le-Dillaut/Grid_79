import random
from Main import *
bot_joueur = 1  # Définir le joueur contrôlé par le bot
def coups_possibles(ouvrier):
    coups = []
    jeu = ouvrier.jeu
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            for bx in (-1,0,1):
                for by in (-1,0,1):
                    if jeu.est_dans_plateau(ouvrier.x + dx, ouvrier.y + dy) and jeu.est_dans_plateau(ouvrier.x + bx, ouvrier.y + by):
                        if jeu.mat[ouvrier.x + bx][ouvrier.y + by] < 4: # pas de construction sur un dome
                            if jeu.case_libre(ouvrier.x + dx, ouvrier.y + dy) and jeu.mat[ouvrier.x + dx][ouvrier.y + dy]-jeu.mat[ouvrier.x][ouvrier.y] <= 1: #pas d'autres joueur + pas trop haut
                                coups.append((ouvrier.x + dx, ouvrier.y + dy, ouvrier.x + bx, ouvrier.y + by))
    return coups
def score_coup(ouvrier, dx, dy, bx, by):
    score = 0
    jeu = ouvrier.jeu

    hauteur_actuelle = jeu.mat[ouvrier.x][ouvrier.y]
    hauteur_nouvelle = jeu.mat[dx][dy]

    # Priorité : gagner
    if hauteur_nouvelle == 3:
        return 1000

    # bonus s'il monte
    score += (hauteur_nouvelle - hauteur_actuelle) * 10

    # bonus s'il construit haut
    score += jeu.mat[bx][by]

    # Essaie de ne pas aider l'adversaire
    adversaires = [o for o in jeu.ouvriers if o.joueur != ouvrier.joueur]
    for adv in adversaires:
        if abs(adv.x - bx) <= 1 and abs(adv.y - by) <= 1:
            score -= 5

    return score


def jouer_intelligent():
    for ouvrier in jeu.ouvriers:
        if ouvrier.joueur == jeu.joueur_actuel:
            coups = coups_possibles(ouvrier)

            if not coups:
                print("Aucun coup possible")
                return

            # Trier les coups selon leur score
            meilleurs_coups = []
            meilleur_score = -float("inf")

            for coup in coups:
                dx, dy, bx, by = coup
                s = score_coup(ouvrier, dx, dy, bx, by)

                if s > meilleur_score:
                    meilleur_score = s
                    meilleurs_coups = [coup]
                elif s == meilleur_score:
                    meilleurs_coups.append(coup)

            # Choisir parmi les meilleurs coups
            dx, dy, bx, by = random.choice(meilleurs_coups)

            ouvrier.deplacer(dx, dy)
            ouvrier.construire(bx, by)


# Début de la partie

jeu = Game()

Ouvrier(0, 0, 0, 0, jeu)
Ouvrier(1, 0, 1, 0, jeu)
Ouvrier(2, 4, 4, 1, jeu)
Ouvrier(3, 4, 3, 1, jeu)



# Boucle du jeu = nombre de tours

while True:
    jeu.afficher()  # Affiche l’état actuel du jeu.

    if jeu.verifier_defaite():
        break  # Arrête la partie si un joueur ne peut plus jouer.

    if jeu.joueur_actuel == bot_joueur:  # Si c’est le tour du bot, il joue automatiquement.
        jouer_intelligent()  # Si c’est le tour du bot, il joue automatiquement.
        jeu.changer_joueur()  # Passe au joueur suivant.
        continue

    oid_str = input("Choisir ouvrier id : ")  # Demande quel ouvrier jouer.

    if not oid_str.isdigit():
        print("Veuillez entrer un nombre")  # Vérifie la validité de l’entrée.
        continue

    oid = int(oid_str)

    ouvrier = None
    for o in jeu.ouvriers:
        if o.id == oid:
            ouvrier = o  # Recherche l’ouvrier correspondant.
            break

    if ouvrier is None:
        print("Ouvrier introuvable")  # Vérifie que l’ouvrier existe.
        continue

    mx_str = input("Move x : ")
    my_str = input("Move y : ")

    if not mx_str.isdigit() or not my_str.isdigit():
        print("Coordonnées invalides")  # Vérifie la saisie.
        continue

    mx = int(mx_str)
    my = int(my_str)

    if ouvrier.deplacer(mx, my):

        bx_str = input("Build x : ")
        by_str = input("Build y : ")

        if not bx_str.isdigit() or not by_str.isdigit():
            print("Coordonnées invalides")  # Vérifie la construction.
            continue

        bx = int(bx_str)
        by = int(by_str)

        if ouvrier.construire(bx, by):
            jeu.changer_joueur()  # Passe au joueur suivant.
