mat=[[0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]
pos={}#en gros ca stoque les endroits ou tu peux pas move et pour les ouvriers tu peux choper leurs coord avec pos[l'id de l'ouvrier](si on update bien pos à chaque move)
class Game:
    def __init__(self, mat):
        self.mat = mat

    def est_dans_plateau(self, x, y):
        return 0 <= x < 5 and 0 <= y < 5

    def afficher(self):
        for ligne in self.mat:
            print(ligne)
        print("Positions :", pos)


def case_libre(x, y):
    return (x, y) not in pos.values()


class Ouvrier:
    def __init__(self, identifiant, x, y, jeu):
        self.id = identifiant
        self.x = x
        self.y = y
        self.jeu = jeu
        pos[self.id] = (x, y)

    def deplacer(self, x, y):
        if not self.jeu.est_dans_plateau(x, y):
            print("Hors plateau")
            return

        if abs(x - self.x) <= 1 and abs(y - self.y) <= 1:
            if case_libre(x, y):
                # règle : montée max de 1
                if self.jeu.mat[x][y] <= self.jeu.mat[self.x][self.y] + 1:
                    self.x = x
                    self.y = y
                    pos[self.id] = (x, y)
                else:
                    print("Trop haut")
            else:
                print("Case occupée")
        else:
            print("Déplacement invalide")

    def construire(self, x, y):
        if not self.jeu.est_dans_plateau(x, y):
            print("Hors plateau")
            return

        if abs(x - self.x) <= 1 and abs(y - self.y) <= 1:
            if case_libre(x, y):
                if self.jeu.mat[x][y] < 4:
                    self.jeu.mat[x][y] += 1
                else:
                    print("Dôme déjà présent")
            else:
                print("Impossible de construire ici")
        else:
            print("Construction invalide")
            
            
jeu = Game(mat)

ouvrier1 = Ouvrier(0, 0, 0, jeu)
ouvrier2 = Ouvrier(1, 4, 4, jeu)

jeu.afficher()

ouvrier1.deplacer(1, 0)
ouvrier1.construire(1, 1)

jeu.afficher()
