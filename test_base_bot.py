import random
from Main import *
def coups_possibles(ouvrier):
    coups = []
    jeu = ouvrier.jeu
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            for bx in (-1,0,1):
                for by in (-1,0,1):
                    if jeu.est_dans_plateau(ouvrier.x + dx, ouvrier.y + dy) and jeu.mat[ouvrier.x + bx][ouvrier.y + by] < 4: #validité de la construction et de la position
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
    for adv in ouvrier.jeu.ouvriers_adverses():
        if abs(adv.x - bx) <= 1 and abs(adv.y - by) <= 1:
            score -= 5

    return score


def jouer_intelligent():
    for ouvrier in jeu.ouvriers:
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
