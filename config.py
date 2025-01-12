import os
import json

class Config:
    # Lädt die Konfiguration aus der Umgebungsvariable
    GITHUB_REPO_CONFIG = json.loads(os.getenv("GITHUB_REPO_CONFIG", "{}"))

    @staticmethod
    def get_repo_config(repo_name):
        """
        Gibt die Konfiguration für ein bestimmtes Repository zurück.
        :param repo_name: Der Name des Repositories (z. B. "repo1").
        :return: Ein Wörterbuch mit URL und Token, falls vorhanden.
        """
        return Config.GITHUB_REPO_CONFIG.get(repo_name, None)

    @staticmethod
    def list_repos():
        """
        Gibt eine Liste aller verfügbaren Repository-Namen zurück.
        """
        return list(Config.GITHUB_REPO_CONFIG.keys())
