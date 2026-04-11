mat=[[0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0],
     [0,0,0,0,0]]

class Game():
     def __init__(self,mat):
          self.mat=mat
          
class ouvriers():
     def __init__(self,id):
          self.id=id
          self.posx=0
          self.posy=0
          self.height=0
     def move(self,x,y):
          if abs(x-self.posx) <= 1 and abs(y-self.posy) <= 1 and (x,y) != (self.posx,self.posy):
               self.posx=x
               self.posy=y
          else:
               return "error_cant_move_here"
     def constr(self,x,y,game):
          if abs(x-self.posx) <= 1 and abs(y-self.posy) <= 1 and (x,y) != (self.posx,self.posy):
               if game.mat[x,y] < 4:
                    game.mat[x,y]+=1
               else:
                    return "error_constr_sur_dome"
          return "error_cant_contr_here"