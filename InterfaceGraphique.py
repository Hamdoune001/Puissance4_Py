from tkinter import messagebox
import time
import tkinter as tk
from Jeu import Puissance4
from IA import IA


class InterfaceGraphique:
    def __init__(self):
        self.fen = tk.Tk()
        self.cnv = tk.Canvas(self.fen, width=700, height=600, bg="white")
        self.cnv.grid()
        self.taille_carre = 100
        self.jeu = Puissance4()
        self.ia = IA()
        self.ia.charger_donnees()
        self.tour = 1
        self.mode = None
        self.partie_terminee = False

        self.btn_rejouer = tk.Button(self.fen, text="Rejouer", command=self.rejouer_partie)
        self.btn_rejouer.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
        self.btn_rejouer.config(state="disabled")

        self.btn_joueur = tk.Button(self.fen, text="Jouer contre un joueur", command=self.PlayerAgainstPlayer)
        self.btn_joueur.grid(row=0, column=1, padx=10, pady=10)

        self.btn_ia = tk.Button(self.fen, text="Jouer contre l'IA", command=self.PlayerAgainstIA)
        self.btn_ia.grid(row=0, column=2, padx=10, pady=10)

        self.btn_ia_vs_ia = tk.Button(self.fen, text="IA contre IA", command=self.IAvsIA)
        self.btn_ia_vs_ia.grid(row=0, column=3, padx=10, pady=10)

        self.creer_carres()

    def PlayerAgainstPlayer(self):
        print("Jouer contre un joueur")
        self.mode = "joueur"

    def PlayerAgainstIA(self):
        print("Jouer contre l'IA")
        self.mode = "ia"
        self.tour = 1
        self.ia.entrainer_IA()

    def IAvsIA(self):
        print("IA contre IA")
        self.mode = "ia_vs_ia"
        self.tour = 1
        self.ia.entrainer_IA()
        self.IAversusIA()

    def rejouer_partie(self):
        self.jeu = Puissance4()
        self.creer_carres()
        self.tour = 1
        self.btn_rejouer.config(state="normal")

    def creer_carres(self):
        self.cnv.delete("all")
        self.carre_list = []
        for i in range(7):
            row = []
            for j in range(6):
                carre = self.cnv.create_rectangle(i * self.taille_carre, j * self.taille_carre,
                                                  (i + 1) * self.taille_carre, (j + 1) * self.taille_carre,
                                                  fill="white")
                tag = f"carre_{i}_{j}"
                self.cnv.itemconfig(carre, tags=(tag,))
                self.cnv.tag_bind(carre, "<Button-1>", lambda event, col=i: self.jouer_coup(event, col))
                row.append((carre, tag))
            self.carre_list.append(row)

    def trouver_ligne_vide(self, colonne):
        for ligne in range(5, -1, -1):
            if self.jeu.plateau[ligne][colonne] == 0:
                return ligne
        return None

    def jouer_coup(self, event, colonne):
        if self.mode == "joueur":
            ligne_vide = self.trouver_ligne_vide(colonne)
            if ligne_vide is not None:
                if self.tour == 1:
                    self.jeu.jouer(colonne)
                    self.update_plateau(self.jeu.plateau)

                    if self.jeu.check_victoire():
                        messagebox.showinfo("Fin de partie", "Vous avez gagné !")
                        self.rejouer_partie()
                        self.btn_rejouer.config(state="normal")
                        return
                    self.tour = 2
                else:
                    self.jeu.jouer(colonne)
                    self.update_plateau(self.jeu.plateau)
                    if self.jeu.check_victoire():
                        print("Joueur 2 a gagné !")
                        messagebox.showinfo("You Win !", "Player Two Win !")
                        self.rejouer_partie()
                        return
                    self.tour = 1
            else:
                messagebox.showinfo("Colonne pleine", "Veuillez choisir une autre colonne.")
        elif self.mode == "ia":
            ligne_vide = self.trouver_ligne_vide(colonne)
            if ligne_vide is not None:
                if self.tour == 1:
                    self.ia.charger_donnees()
                    self.jeu.jouer(colonne)
                    self.update_plateau(self.jeu.plateau)
                    if self.jeu.check_victoire():
                        messagebox.showinfo("You Win !", "Player 1 Win !")
                        self.rejouer_partie()
                        return
                    self.tour = 2
                    self.ia_joue()
                else:
                    messagebox.showinfo("You Lose !", "IA Win !")
                    self.rejouer_partie()
                    return
        else:
            messagebox.showinfo("Colonne pleine", "Veuillez choisir une autre colonne.")

    def ia_joue(self):
        coup_ia = self.ia.prendre_decision_intelligente(self.jeu.plateau)
        ligne_vide = self.trouver_ligne_vide(colonne=coup_ia)
        if ligne_vide is not None:
            self.jeu.jouer(coup_ia)
            self.update_plateau(self.jeu.plateau)
            if self.jeu.check_victoire():
                print("IA a gagné !")
                return
            self.tour = 1

    def update_plateau(self, plateau):
        for i in range(len(plateau)):
            for j in range(len(plateau[i])):
                if plateau[i][j] == 0:
                    self.cnv.itemconfig(self.carre_list[j][i][0], fill="white")
                elif plateau[i][j] == 1:
                    self.cnv.itemconfig(self.carre_list[j][i][0], fill="red")
                else:
                    self.cnv.itemconfig(self.carre_list[j][i][0], fill="yellow")

    def IAversusIA(self):
        if self.mode == "ia_vs_ia":
            if self.tour == 1:
                self.ia.charger_donnees()
                self.ia_joue()
                self.ia.enregistrer_resultat(self.jeu.plateau)
                self.ia.sauvegarder_donnees()
                self.tour = 2
            else:
                self.ia_joue()
                self.tour = 1
            if self.jeu.check_victoire():
                print("Partie terminée !")
                self.partie_terminee = True
                self.btn_rejouer.config(state="normal")
                return
        if not self.partie_terminee:
            self.fen.after(1000, self.IAversusIA)

    def run(self):
        self.fen.mainloop()
