# main.py
from manager import BotManager
from utils.message_bus import MessageBus
import logging
import logging.config

if __name__ == "__main__":
    try:
        # Configurer le logging via un fichier de configuration
        logging.config.fileConfig('logging.conf')

        # Créer une instance de MessageBus
        message_bus = MessageBus()

        # Instancier BotManager avec le chemin vers les modules et le message_bus
        module_manager = BotManager(modules_path="modules", message_bus=message_bus)

        # Charger tous les modules présents dans le répertoire 'modules'
        module_manager.load_modules_from_directory()

        # Exemple d'utilisation d'un module chargé dynamiquement (par exemple, strategy.py)
        module_manager.execute_module_function("strategy", "execute", message_bus)
    except Exception as e:
        logging.error(f"Erreur lors de l'exécution du module : {e}", exc_info=True)
