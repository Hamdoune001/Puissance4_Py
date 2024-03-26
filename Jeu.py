import numpy as np


class Puissance4:
    def __init__(self):
        self.plateau = np.zeros((6, 7))
        self.joueur = 1

    def jouer_coup(self, colonne):
        for i in reversed(range(len(self.plateau))):
            if self.plateau[i][colonne] == 0:
                self.plateau[i][colonne] = self.joueur
                break

    def check_victoire(self):
        return (self.check_horizontal() or self.check_vertical() or
                self.check_diagonal_desc() or self.check_diagonal_asc())

    def check_horizontal(self):
        for i in range(len(self.plateau)):
            for j in range(len(self.plateau[i]) - 3):
                if all(self.plateau[i][j + k] == self.joueur for k in range(4)):
                    return True
        return False

    def check_vertical(self):
        for i in range(len(self.plateau) - 3):
            for j in range(len(self.plateau[i])):
                if all(self.plateau[i + k][j] == self.joueur for k in range(4)):
                    return True
        return False

    def check_diagonal_desc(self):
        for i in range(len(self.plateau) - 3):
            for j in range(len(self.plateau[i]) - 3):
                if all(self.plateau[i + k][j + k] == self.joueur for k in range(4)):
                    return True
        return False

    def check_diagonal_asc(self):
        for i in range(3, len(self.plateau)):
            for j in range(len(self.plateau[i]) - 3):
                if all(self.plateau[i - k][j + k] == self.joueur for k in range(4)):
                    return True
        return False

    def jouer(self, colonne):

        if colonne < 0 or colonne > 6:
            print("Choisissez une colonne entre 1 et 7.")
            return

        self.jouer_coup(colonne)
        print(self.plateau)

        if self.check_victoire():
            print("Joueur " + str(self.joueur) + " a gagné !")
        else:
            self.joueur = 3 - self.joueur
