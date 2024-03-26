import os

import numpy as np
import pandas as pd


class IA:
    def __init__(self):
        self.data_file = 'data.xlsx'
        if os.path.isfile(self.data_file) and os.path.getsize(self.data_file) > 0:
            self.charger_donnees()
        else:
            self.data = pd.DataFrame(columns=['board', 'action', 'victoires'])
        self.victoires = 0

    def incrementer_victoires(self):
        self.victoires += 1
        self.data.at[len(self.data) - 1, 'victoires'] = self.victoires

    def choisir_coup(self, plateau):
        colonnes_disponibles = [col for col in range(len(plateau[0])) if plateau[0][col] == 0]
        return np.random.choice(colonnes_disponibles)

    def enregistrer_resultat(self, plateau):
        flatten_board = [item for sublist in plateau for item in sublist]
        action = self.choisir_coup(plateau)
        victoires = 0
        new_data = {'board': [flatten_board], 'action': [action], 'victoires': [victoires]}
        self.data = pd.concat([self.data, pd.DataFrame(new_data)], ignore_index=True)

    def sauvegarder_donnees(self):
        try:
            self.data.to_excel(self.data_file, index=False)
        except Exception as e:
            print("Erreur lors de la sauvegarde des données :", e)

    def charger_donnees(self):
        try:
            self.data = pd.read_excel(self.data_file, engine='openpyxl')
        except FileNotFoundError:
            print("Le fichier Excel n'existe pas encore.")
            self.data = pd.DataFrame(columns=['board', 'action', 'victoires'])
        except Exception as e:
            print("Erreur lors du chargement des données :", e)
            self.data = pd.DataFrame(columns=['board', 'action', 'victoires'])

    def entrainer_IA(self):
        if len(self.data) == 0:
            print("Aucune donnée disponible pour l'entraînement.")
            return

        self.plateau_actions = {}

        for index, row in self.data.iterrows():
            board_state = tuple(row['board'])
            action = row['action']

            if board_state in self.plateau_actions:
                self.plateau_actions[board_state].append(action)
            else:
                self.plateau_actions[board_state] = [action]

        self.meilleure_action = {}
        for board_state, actions in self.plateau_actions.items():
            self.meilleure_action[board_state] = max(set(actions), key=actions.count)

    def prendre_decision_intelligente(self, plateau):
        flatten_board = tuple([item for sublist in plateau for item in sublist])

        if flatten_board not in self.meilleure_action:
            print("Aucune stratégie n'a été apprise pour cet état de plateau. Utilisation d'une stratégie aléatoire.")
            return self.choisir_coup(plateau)

        return self.meilleure_action[flatten_board]
