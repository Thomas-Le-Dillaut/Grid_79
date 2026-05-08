from test_base_bot import jouer_intelligent
bot_joueur = 1  # Définir le joueur contrôlé par le bot
class Game:
    def __init__(self):
        self.mat = [[0]*5 for _ in range(5)] # on initialise la matrice
        self.positions = {} # ici on stocke les positions des ouvriers (connaître les cases occupées)
        self.ouvriers = [] # contient tous les ouvriers présents dans la partie
        self.joueur_actuel = 0 # indique quel joueur doit jouer son tour

    def est_dans_plateau(self, x, y): #ici on vérifie si la case est bien dans le plateau
        return 0 <= x < 5 and 0 <= y < 5

    def case_libre(self, x, y):
        return (x, y) not in self.positions.values() # vérifie si une case n'est pas occupé par un ouvrier

    def afficher(self):
        print("\nPlateau :")
        for i in range(5):
            for j in range(5):
                print(self.mat[i][j], end=" ") # affiche les positions actuelles des ouvriers
            print()
        print("Positions :", self.positions) # affiche les positions actuelles des ouvriers.
        print("Joueur actuel :", self.joueur_actuel)  # indique quel joueur est en train de jouer.
        print()

    def changer_joueur(self):
        self.joueur_actuel = 1 - self.joueur_actuel # permet d'alterner entre les joueurs

    def peut_bouger(self, ouvrier): #importante pour vérifier la validité d'un input
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = ouvrier.x + dx
                y = ouvrier.y + dy

                if not self.est_dans_plateau(x, y):
                    continue #ignore les cases hors du plateau
                if (x, y) == (ouvrier.x, ouvrier.y):
                    continue # ignore la case actuelle de l’ouvrier
                if not self.case_libre(x, y):
                    continue # ignore les cases occupées.
                if self.mat[x][y] <= self.mat[ouvrier.x][ouvrier.y] + 1:
                    return True # vérifie si un déplacement valide est possible.
        return False # aucun déplacement possible
    def verifier_defaite(self):
        for o in self.ouvriers:
            if o.joueur == self.joueur_actuel:
                if self.peut_bouger(o):
                    return False # le joueur peut encore jouer
        print(f"Le joueur {self.joueur_actuel} ne peut plus jouer. Défaite !")
        return True # le joueur est bloqué


class Ouvrier:
    def __init__(self, identifiant, x, y, joueur, jeu):
        self.id = identifiant  # Identifie chaque ouvrier de manière unique.
        self.x = x  # Position en x de l’ouvrier.
        self.y = y  # Position en y de l’ouvrier.
        self.joueur = joueur  # Indique à quel joueur appartient l’ouvrier.
        self.jeu = jeu  # Référence au jeu principal.

        self.jeu.positions[self.id] = (x, y)  # Enregistre la position initiale de l’ouvrier.
        self.jeu.ouvriers.append(self)  # Ajoute l’ouvrier à la liste des ouvriers du jeu.

    def deplacer(self, x, y):
        if self.joueur != self.jeu.joueur_actuel:
            print("Ce n'est pas ton tour")  # Empêche de jouer hors de son tour.
            return False

        if not self.jeu.est_dans_plateau(x, y):
            print("Hors plateau")  # Vérifie que la case est valide.
            return False

        if (x, y) == (self.x, self.y):
            print("Pas de déplacement")  # Empêche de rester sur place.
            return False

        if abs(x - self.x) <= 1 and abs(y - self.y) <= 1:
            if self.jeu.case_libre(x, y):
                if self.jeu.mat[x][y] <= self.jeu.mat[self.x][self.y] + 1:

                    if self.jeu.mat[x][y] == 3:
                        print(f"🎉 Joueur {self.joueur} gagne !")  # Détecte la victoire.
                        exit()

                    self.x = x
                    self.y = y
                    self.jeu.positions[self.id] = (x, y)  # Met à jour la position.
                    return True
                else:
                    print("Trop haut")  # Déplacement interdit par la hauteur.
            else:
                print("Case occupée")  # Case déjà prise.
        else:
            print("Déplacement invalide")  # Trop loin.
        return False

    def construire(self, x, y):
        if not self.jeu.est_dans_plateau(x, y):
            print("Hors plateau")  # Empêche de construire hors du plateau.
            return False

        if abs(x - self.x) <= 1 and abs(y - self.y) <= 1:
            if self.jeu.case_libre(x, y):
                if self.jeu.mat[x][y] < 4:
                    self.jeu.mat[x][y] += 1  # Augmente le niveau de construction.
                    return True
                else:
                    print("Dôme déjà présent")  # Case déjà terminée.
            else:
                print("Impossible de construire ici")  # Case occupée.
        else:
            print("Construction invalide")  # Trop loin.
        return False


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
    
    if jeu.joueur_actuel == bot_joueur:  # Si c’est le tour du bot, il joue automatiquement.
        jouer_intelligent()  # Si c’est le tour du bot, il joue automatiquement.
        jeu.changer_joueur()  # Passe au joueur suivant.
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
