import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def secure_log_error(error_message, repo_name=None):
    """
    Sicheres Logging von Fehlern ohne sensible Daten.
    """
    if repo_name:
        logger.error(f"Fehler bei Repository '{repo_name}': {error_message}")
    else:
        logger.error(f"Fehler: {error_message}")
