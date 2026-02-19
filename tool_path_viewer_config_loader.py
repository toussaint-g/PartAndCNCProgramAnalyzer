
# -*- coding: utf-8 -*-

import json

class ToolPathConfigLoader:
    """Cette classe permet l'appel de la config du viewer 3D (json)"""
    data = {}  # Stocke les données du JSON

    @staticmethod
    def load_config():
        """Cette fonction appelle la config du viewer 3D (json)"""
        try:
            with open('tool_path_viewer_config.json', 'r') as file:
                ToolPathConfigLoader.data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Erreur : Le fichier de config du viewer (.json) est introuvable.")

