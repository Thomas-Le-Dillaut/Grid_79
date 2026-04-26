mat=[[0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]
pos={}#en gros ca stoque les endroits ou tu peux pas move et pour les ouvriers tu peux choper leurs coord avec pos[l'id de l'ouvrier](si on update bien pos à chaque move)
class Game():
     def __init__(self,mat):
          self.mat=mat

<<<<<<< HEAD
def someone_here(x,y):
     if (x,y) in pos.values():
          return False
     return True
=======
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
>>>>>>> a93fa59 (chat gpt a du mettre positions mais enft le dictionnaire s'appelait pos)

class ouvrier():
     def __init__(self,id):
          self.id=id
          self.posx=0
          self.posy=0
          self.height=0
          pos[self.id]=(self.posx,self.posy)
     def move(self,x,y):
          if abs(x-self.posx) <= 1 and abs(y-self.posy) <= 1 and someone_here(x,y):
               self.posx=x
               self.posy=y
               self.height=game.mat[x][y]
               pos[self.id]=(self.posx,self.posy)#empeche de move sur un joueur
          else:
               assert "error_cant_move_here"
     def constr(self,x,y,game):
          if abs(x-self.posx) <= 1 and abs(y-self.posy) <= 1 and someone_here(x,y) :
               if game.mat[x][y] == 3:#empeche de move sur une case avec un dome
                    game.mat[x][y]+=1
                    pos[(x,y)]=(x,y)
               elif game.mat[x][y] < 4:
                    game.mat[x][y]+=1
               else:
                    assert"error_constr_sur_dome"
          else:
               assert"error_cant_contr_here"
game=Game(mat)
ouv1=ouvrier(0)
ouv2=ouvrier(1)
