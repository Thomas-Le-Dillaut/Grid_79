mat=[[0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]
pos={}#en gros ca stoque les endroits ou tu peux pas move et pour les ouvriers tu peux choper leurs coord avec pos[l'id de l'ouvrier](si on update bien pos à chaque move)
class Game():
     def __init__(self,mat):
          self.mat=mat

def someone_here(x,y):
     if (x,y) in pos.values():
          return False
     return True

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
