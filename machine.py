
# -*- coding: utf-8 -*-

import json

class Machine:
    """Cette classe permet de gérer le jumeaux numérique de la machine (json)"""
    data = {}  # Stocke les données du JSON

    @staticmethod
    def load_config():
        """Cette fonction permet de charger le jumeaux numérique de la machine (json)"""
        try:
            with open('machine.json', 'r') as file:
                Machine.data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Erreur : Le jumeau numérique (.json) est introuvable.")



        

    



    
    
