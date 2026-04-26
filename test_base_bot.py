import random

def coups_possibles(ouvrier):
    coups = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx = ouvrier.x + dx
            ny = ouvrier.y + dy
            if not ouvrier.jeu.est_dans_plateau(nx, ny):
                continue
            if not case_libre(nx, ny):
                continue
            if ouvrier.jeu.mat[nx][ny] > ouvrier.jeu.mat[ouvrier.x][ouvrier.y] + 1:
                continue
            for dx2 in [-1, 0, 1]:
                for dy2 in [-1, 0, 1]:
                    bx = nx + dx2
                    by = ny + dy2
                    if not ouvrier.jeu.est_dans_plateau(bx, by):
                        continue
                    if not case_libre(bx, by):
                        continue
                    if ouvrier.jeu.mat[bx][by] < 4:
                        coups.append((nx, ny, bx, by))
    return coups

def jouer_aleatoire(ouvrier):
    coups = coups_possibles(ouvrier)
    if not coups:
        print("Aucun coup possible")
        return

    coup = random.choice(coups)
    nx, ny, bx, by = coup
    ouvrier.deplacer(nx, ny)
    ouvrier.construire(bx, by)

for i in range(10):  # c'est le nombre de tour de la partie en aléatoire
    print("Tour", i)
    jouer_aleatoire(ouvrier1)
    jouer_aleatoire(ouvrier2)
    jeu.afficher()




import ast
import random

data = ast.literal_eval(input())

pos = {0: (0, 0), 1: (4, 4)}
print(f"PLACER {pos}")

if not data:
    adv = ast.literal_eval(input())

while True:
    try:
        ligne = input()
    except EOFError:
        break

    if ligne == "END":
        break

    if ligne.startswith("PLAY "):
        w, dep, con = ast.literal_eval(ligne[5:])


ouvrier = random.choice([0, 1])
nx = random.randint(0, 4)
ny = random.randint(0, 4)
bx = random.randint(0, 4)
by = random.randint(0, 4)

print(f"PLAY ({ouvrier}, ({nx}, {ny}), ({bx}, {by}))")


ouvrier = random.choice([0, 1])
coups = coups_possibles(ouvrier_obj)  
if coups:
    nx, ny, bx, by = random.choice(coups)
    print(f"PLAY ({ouvrier}, ({nx}, {ny}), ({bx}, {by}))")
else:
    print("PLAY (0, (0, 0), (0, 0))")  
