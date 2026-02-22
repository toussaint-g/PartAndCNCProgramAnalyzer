
# -*- coding: utf-8 -*-

import json

class MachinesConfigLoader:
    """Cette classe permet de gérer la configuration des machines (json)"""
    data = {}
    machines_list = {}

    @staticmethod
    def load_config():
        """Charge le fichier JSON et split application / machines_list"""
        try:
            with open('machines_config.json', 'r', encoding="utf-8") as file:
                MachinesConfigLoader.data = json.load(file)

            MachinesConfigLoader.machines_list = MachinesConfigLoader.data.get("machines_list", {})

        except FileNotFoundError:
            raise FileNotFoundError(
                "Erreur : Le fichier des configurations machines (.json) est introuvable."
            )

    @staticmethod
    def get_machines_names():
        """Retourne la liste des noms de machines (clés du JSON)"""
        return sorted(MachinesConfigLoader.machines_list.keys())

    @staticmethod
    def get_machine(machine_name: str):
        """Retourne le dict de la machine"""
        return MachinesConfigLoader.machines_list.get(machine_name, {})
