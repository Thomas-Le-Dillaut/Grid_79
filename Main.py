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
                if coups_possibles(o):
                    return False # le joueur peut encore jouer
        print(f"Le joueur {self.joueur_actuel} ne peut plus jouer. Défaite !")
        return True # le joueur est bloqué


import tkinter as tk
import random

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
                        return True

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


def coups_possibles(ouvrier):
    coups = []
    jeu = ouvrier.jeu
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for bx in (-1, 0, 1):
                for by in (-1, 0, 1):
                    nx = ouvrier.x + dx
                    ny = ouvrier.y + dy
                    bx_abs = nx + bx
                    by_abs = ny + by
                    if jeu.est_dans_plateau(nx, ny) and jeu.est_dans_plateau(bx_abs, by_abs):
                        if jeu.mat[bx_abs][by_abs] < 4:
                            if jeu.case_libre(nx, ny) and jeu.mat[nx][ny] - jeu.mat[ouvrier.x][ouvrier.y] <= 1:
                                if (nx, ny) != (ouvrier.x, ouvrier.y):
                                    if jeu.case_libre(bx_abs, by_abs):
                                        if not (bx == 0 and by == 0):
                                            coups.append((nx, ny, bx_abs, by_abs))
    return coups


def score_coup(ouvrier, dx, dy, bx, by):
    score = 0
    jeu = ouvrier.jeu

    hauteur_actuelle = jeu.mat[ouvrier.x][ouvrier.y]
    hauteur_nouvelle = jeu.mat[dx][dy]

    if hauteur_nouvelle == 3:
        return 1000

    score += (hauteur_nouvelle - hauteur_actuelle) * 10
    score += jeu.mat[bx][by]

    adversaires = [o for o in jeu.ouvriers if o.joueur != ouvrier.joueur]
    for adv in adversaires:
        if abs(adv.x - bx) <= 1 and abs(adv.y - by) <= 1:
            score -= 5

    return score


def jouer_intelligent(jeu):
    meilleurs_coups = []
    meilleur_score = -float("inf")
    meilleur_ouvrier = None

    for ouvrier in jeu.ouvriers:
        if ouvrier.joueur == jeu.joueur_actuel:
            coups = coups_possibles(ouvrier)
            for coup in coups:
                dx, dy, bx, by = coup
                s = score_coup(ouvrier, dx, dy, bx, by)
                if s > meilleur_score:
                    meilleur_score = s
                    meilleurs_coups = [coup]
                    meilleur_ouvrier = ouvrier
                elif s == meilleur_score:
                    meilleurs_coups.append(coup)

    if not meilleurs_coups or meilleur_ouvrier is None:
        return False

    dx, dy, bx, by = random.choice(meilleurs_coups)
    if meilleur_ouvrier.deplacer(dx, dy):
        meilleur_ouvrier.construire(bx, by)
        return True
    return False


class Grid3DView:
    def __init__(self, jeu, bot_joueur=1):
        self.jeu = jeu
        self.bot_joueur = bot_joueur
        self.tile = 90
        self.grid_x = 20
        self.grid_y = 20
        self.grid_size = self.tile * 5
        self.selected_worker = None
        self.move_target = None
        self.build_target = None
        self.step = "select_worker"
        self.height_colors = ["#e0e0e0", "#a0a0a0", "#707070", "#404040", "#101010"]
        self.root = tk.Tk()
        self.root.title("Grid 79 - Vue top-down")
        self.canvas = tk.Canvas(self.root, width=self.grid_x * 2 + self.grid_size, height=self.grid_y * 2 + self.grid_size, bg="#202020")
        self.canvas.pack(side="left", fill="both", expand=True)
        side = tk.Frame(self.root, bg="#232323", width=260)
        side.pack(side="right", fill="y")
        self.status = tk.Label(side, text="", fg="#ffffff", bg="#232323", font=("Arial", 12), justify="left")
        self.status.pack(padx=10, pady=(10, 0), anchor="n")
        self.hint = tk.Label(side, text="", fg="#cccccc", bg="#232323", font=("Arial", 10), justify="left", wraplength=240)
        self.hint.pack(padx=10, pady=4, anchor="n")
        legend_title = tk.Label(side, text="Légende des étages", fg="#ffffff", bg="#232323", font=("Arial", 11, "bold"))
        legend_title.pack(padx=10, pady=(12, 4), anchor="w")
        for lvl, color in enumerate(self.height_colors):
            frame = tk.Frame(side, bg="#232323")
            frame.pack(fill="x", padx=10, pady=2)
            box = tk.Canvas(frame, width=22, height=22, bg="#232323", highlightthickness=0)
            box.create_rectangle(0, 0, 22, 22, fill=color, outline="#111111")
            box.pack(side="left")
            label = tk.Label(frame, text=f"Étage {lvl}", fg="#ffffff", bg="#232323", font=("Arial", 10))
            label.pack(side="left", padx=8)
        self.reset_btn = tk.Button(side, text="Réinitialiser", command=self.reset_game)
        self.reset_btn.pack(padx=10, pady=10, fill="x")
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw()
        self.root.after(300, self.run_bot_if_needed)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.mainloop()

    def reset_game(self):
        self.root.destroy()
        main_gui()

    def iso(self, x, y, z=0):
        cx = self.offset_x + (x - y) * (self.tile_w / 2)
        cy = self.offset_y + (x + y) * (self.tile_h / 2) - z * self.layer_h
        return cx, cy

    def point_to_cell(self, px, py):
        if px < self.grid_x or py < self.grid_y:
            return None
        rel_x = px - self.grid_x
        rel_y = py - self.grid_y
        if rel_x >= self.grid_size or rel_y >= self.grid_size:
            return None
        cx = int(rel_x // self.tile)
        cy = int(rel_y // self.tile)
        if 0 <= cx < 5 and 0 <= cy < 5:
            return cx, cy
        return None

    def draw_cell(self, x, y, height):
        x0 = self.grid_x + x * self.tile
        y0 = self.grid_y + y * self.tile
        x1 = x0 + self.tile
        y1 = y0 + self.tile
        fill = self.height_colors[min(height, len(self.height_colors) - 1)]
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#222222", width=2)
        self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(height), fill="#ffffff", font=("Arial", 14, "bold"))

    def draw_worker(self, worker):
        x, y = worker.x, worker.y
        x0 = self.grid_x + x * self.tile
        y0 = self.grid_y + y * self.tile
        cx = x0 + self.tile / 2
        cy = y0 + self.tile / 2
        radius = 18
        color = "#ff6b6b" if worker.joueur == 0 else "#4db8ff"
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=color, outline="#111111", width=2)
        self.canvas.create_oval(cx - radius/2, cy - radius/2 - 2, cx + radius/2, cy + radius/2 - 2, fill="#ffffff", outline="")
        if self.selected_worker is worker:
            self.canvas.create_oval(cx - radius - 4, cy - radius - 4, cx + radius + 4, cy + radius + 4, outline="#ffff66", width=3)

    def update_labels(self):
        texte = f"Joueur actuel : {self.jeu.joueur_actuel}\n"
        texte += "Tour du bot\n" if self.jeu.joueur_actuel == self.bot_joueur else "Tour du joueur humain\n"
        if self.step == "select_worker":
            hint = "Cliquez sur un ouvrier de votre joueur."
        elif self.step == "select_move":
            hint = "Choisissez une case voisine valide pour déplacer l’ouvrier."
        else:
            hint = "Choisissez une case adjacente pour construire."
        self.status.config(text=texte)
        self.hint.config(text=hint)

    def draw_highlights(self):
        if self.step == "select_worker":
            return
        if self.step == "select_move" and self.selected_worker:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    tx = self.selected_worker.x + dx
                    ty = self.selected_worker.y + dy
                    if self.jeu.est_dans_plateau(tx, ty) and self.jeu.case_libre(tx, ty) and self.jeu.mat[tx][ty] <= self.jeu.mat[self.selected_worker.x][self.selected_worker.y] + 1:
                        self.highlight_cell(tx, ty, "#ffff66")
        if self.step == "select_build" and self.move_target:
            mx, my = self.move_target
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    bx = mx + dx
                    by = my + dy
                    if self.can_build_cell(self.selected_worker, self.move_target, (bx, by)):
                        self.highlight_cell(bx, by, "#66ff66")

    def highlight_cell(self, x, y, color):
        x0 = self.grid_x + x * self.tile
        y0 = self.grid_y + y * self.tile
        x1 = x0 + self.tile
        y1 = y0 + self.tile
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=4)

    def valid_move(self, worker, cell):
        x, y = cell
        if not self.jeu.est_dans_plateau(x, y) or (x, y) == (worker.x, worker.y):
            return False
        if abs(x - worker.x) > 1 or abs(y - worker.y) > 1:
            return False
        if not self.jeu.case_libre(x, y):
            return False
        if self.jeu.mat[x][y] > self.jeu.mat[worker.x][worker.y] + 1:
            return False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                bx = x + dx
                by = y + dy
                if self.can_build_cell(worker, (x, y), (bx, by)):
                    return True
        return False

    def can_build_cell(self, worker, move_cell, build_cell):
        x, y = build_cell
        mx, my = move_cell
        if not self.jeu.est_dans_plateau(x, y):
            return False
        if abs(x - mx) > 1 or abs(y - my) > 1:
            return False
        if (x, y) == (mx, my):
            return False
        if self.jeu.mat[x][y] >= 4:
            return False
        if (x, y) == (worker.x, worker.y):
            return True
        return self.jeu.case_libre(x, y)

    def valid_build(self, worker, move_cell, build_cell):
        return self.can_build_cell(worker, move_cell, build_cell)

    def on_click(self, event):
        if self.jeu.verifier_defaite():
            return
        cell = self.point_to_cell(event.x, event.y)
        if cell is None:
            return
        if self.jeu.joueur_actuel == self.bot_joueur:
            return
        if self.step == "select_worker":
            worker = self.find_worker(cell)
            if worker and worker.joueur == self.jeu.joueur_actuel:
                self.selected_worker = worker
                self.step = "select_move"
        elif self.step == "select_move":
            if self.selected_worker and self.valid_move(self.selected_worker, cell):
                self.move_target = cell
                self.step = "select_build"
            else:
                worker = self.find_worker(cell)
                if worker and worker.joueur == self.jeu.joueur_actuel:
                    self.selected_worker = worker
                else:
                    self.step = "select_worker"
                    self.selected_worker = None
                    self.move_target = None
        elif self.step == "select_build":
            if self.selected_worker and self.move_target and self.valid_build(self.selected_worker, self.move_target, cell):
                if self.selected_worker.deplacer(*self.move_target):
                    if self.selected_worker.construire(*cell):
                        if self.jeu.mat[self.selected_worker.x][self.selected_worker.y] == 3:
                            self.status.config(text=f"Joueur {self.selected_worker.joueur} a gagné !")
                            self.draw()
                            return
                        self.jeu.changer_joueur()
                        self.step = "select_worker"
                        self.selected_worker = None
                        self.move_target = None
                        self.build_target = None
                        self.draw()
                        self.root.after(300, self.run_bot_if_needed)
                        return
                self.step = "select_worker"
                self.selected_worker = None
                self.move_target = None
        self.draw()

    def find_worker(self, cell):
        for worker in self.jeu.ouvriers:
            if (worker.x, worker.y) == cell:
                return worker
        return None

    def draw(self):
        self.canvas.delete("all")
        order = sorted([(x, y) for x in range(5) for y in range(5)], key=lambda t: t[0] + t[1])
        for x, y in order:
            self.draw_cell(x, y, self.jeu.mat[x][y])
        self.draw_highlights()
        for worker in self.jeu.ouvriers:
            self.draw_worker(worker)
        self.update_labels()

    def run_bot_if_needed(self):
        if self.jeu.joueur_actuel == self.bot_joueur and not self.jeu.verifier_defaite():
            jouer_intelligent(self.jeu)
            self.jeu.changer_joueur()
            self.draw()
            if self.jeu.verifier_defaite():
                self.status.config(text=f"Le joueur {1 - self.bot_joueur} a gagné !")
            else:
                self.root.after(300, self.run_bot_if_needed)


def main_gui():
    jeu = Game()
    Ouvrier(0, 0, 0, 0, jeu)
    Ouvrier(1, 0, 1, 0, jeu)
    Ouvrier(2, 4, 4, 1, jeu)
    Ouvrier(3, 4, 3, 1, jeu)
    Grid3DView(jeu, bot_joueur=1)

if __name__ == "__main__":
    main_gui()
