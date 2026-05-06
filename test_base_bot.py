def score_coup(ouvrier, nx, ny, bx, by):
    score = 0
    jeu = ouvrier.jeu

    hauteur_actuelle = jeu.mat[ouvrier.x][ouvrier.y]
    hauteur_nouvelle = jeu.mat[nx][ny]

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


def jouer_intelligent(ouvrier):
    coups = coups_possibles(ouvrier)

    if not coups:
        print("Aucun coup possible")
        return

    # Trier les coups selon leur score
    meilleurs_coups = []
    meilleur_score = -float("inf")

    for coup in coups:
        nx, ny, bx, by = coup
        s = score_coup(ouvrier, nx, ny, bx, by)

        if s > meilleur_score:
            meilleur_score = s
            meilleurs_coups = [coup]
        elif s == meilleur_score:
            meilleurs_coups.append(coup)

    # Choisir parmi les meilleurs coups
    nx, ny, bx, by = random.choice(meilleurs_coups)

    ouvrier.deplacer(nx, ny)
    ouvrier.construire(bx, by)
