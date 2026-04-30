mat=[[0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]
pos={}#en gros ca stoque les endroits ou tu peux pas move et pour les ouvriers tu peux choper leurs coord avec pos[l'id de l'ouvrier](si on update bien pos à chaque move)
class Game:
    def __init__(self):
        self.mat = [[0]*5 for _ in range(5)]
        self.positions = {}
        self.ouvriers = []
        self.joueur_actuel = 0

    def est_dans_plateau(self, x, y):
        return 0 <= x < 5 and 0 <= y < 5

    def case_libre(self, x, y):
        return (x, y) not in self.positions.values()

    def afficher(self):
        print("\nPlateau :")
        for i in range(5):
            for j in range(5):
                print(self.mat[i][j], end=" ")
            print()
        print("Positions :", self.positions)
        print("Joueur actuel :", self.joueur_actuel)
        print()

    def changer_joueur(self):
        self.joueur_actuel = 1 - self.joueur_actuel

    def peut_bouger(self, ouvrier):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = ouvrier.x + dx
                y = ouvrier.y + dy

                if not self.est_dans_plateau(x, y):
                    continue
                if (x, y) == (ouvrier.x, ouvrier.y):
                    continue
                if not self.case_libre(x, y):
                    continue
                if self.mat[x][y] <= self.mat[ouvrier.x][ouvrier.y] + 1:
                    return True
        return False

    def verifier_defaite(self):
        for o in self.ouvriers:
            if o.joueur == self.joueur_actuel:
                if self.peut_bouger(o):
                    return False
        print(f"Le joueur {self.joueur_actuel} ne peut plus jouer. Défaite !")
        return True


class Ouvrier:
    def __init__(self, identifiant, x, y, joueur, jeu):
        self.id = identifiant
        self.x = x
        self.y = y
        self.joueur = joueur
        self.jeu = jeu

        self.jeu.positions[self.id] = (x, y)
        self.jeu.ouvriers.append(self)

    def deplacer(self, x, y):
        if self.joueur != self.jeu.joueur_actuel:
            print("Ce n'est pas ton tour")
            return False

        if not self.jeu.est_dans_plateau(x, y):
            print("Hors plateau")
            return False

        if (x, y) == (self.x, self.y):
            print("Pas de déplacement")
            return False

        if abs(x - self.x) <= 1 and abs(y - self.y) <= 1:
            if self.jeu.case_libre(x, y):
                if self.jeu.mat[x][y] <= self.jeu.mat[self.x][self.y] + 1:

                    if self.jeu.mat[x][y] == 3:
                        print(f"🎉 Joueur {self.joueur} gagne !")
                        exit()

                    self.x = x
                    self.y = y
                    self.jeu.positions[self.id] = (x, y)
                    return True
                else:
                    print("Trop haut")
            else:
                print("Case occupée")
        else:
            print("Déplacement invalide")
        return False

    def construire(self, x, y):
        if not self.jeu.est_dans_plateau(x, y):
            print("Hors plateau")
            return False

        if abs(x - self.x) <= 1 and abs(y - self.y) <= 1:
            if self.jeu.case_libre(x, y):
                if self.jeu.mat[x][y] < 4:
                    self.jeu.mat[x][y] += 1
                    return True
                else:
                    print("Dôme déjà présent")
            else:
                print("Impossible de construire ici")
        else:
            print("Construction invalide")
        return False


# Début de la partie

jeu = Game()

Ouvrier(0, 0, 0, 0, jeu)
Ouvrier(1, 0, 1, 0, jeu)
Ouvrier(2, 4, 4, 1, jeu)
Ouvrier(3, 4, 3, 1, jeu)



# Boucle du jeu = nombre de tours

while True:
    jeu.afficher()

    if jeu.verifier_defaite():
        break

    # choisir ouvrier
    oid_str = input("Choisir ouvrier id : ")

    if not oid_str.isdigit():
        print("Veuillez entrer un nombre")
        continue

    oid = int(oid_str)

    ouvrier = None
    for o in jeu.ouvriers:
        if o.id == oid:
            ouvrier = o
            break

    if ouvrier is None:
        print("Ouvrier introuvable")
        continue

    # déplacement
    mx_str = input("Move x : ")
    my_str = input("Move y : ")

    if not mx_str.isdigit() or not my_str.isdigit():
        print("Coordonnées invalides")
        continue

    mx = int(mx_str)
    my = int(my_str)

    if ouvrier.deplacer(mx, my):

        # construction
        bx_str = input("Build x : ")
        by_str = input("Build y : ")

        if not bx_str.isdigit() or not by_str.isdigit():
            print("Coordonnées invalides")
            continue

        bx = int(bx_str)
        by = int(by_str)

        if ouvrier.construire(bx, by):
            jeu.changer_joueur()
