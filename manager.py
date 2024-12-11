import importlib
import os
import logging
import sys

class BotManager:
    def __init__(self, modules_path, message_bus):
        self.modules_path = modules_path
        self.modules = {}
        self.message_bus = message_bus
        self.priority_modules = ['order_executor', 'risk_manager', 'monitor']

        # Ajouter dynamiquement le chemin des modules au sys.path si ce n'est pas déjà fait
        if self.modules_path not in sys.path:
            sys.path.append(os.path.join(os.path.dirname(__file__), self.modules_path))
            logging.info(f"Chemin des modules '{self.modules_path}' ajouté au système.")
        else:
            logging.info(f"Chemin des modules '{self.modules_path}' déjà présent dans le système.")

    def load_module(self, module_name):
        """Charger dynamiquement un module ou une classe."""
        try:
            # Importer le module via importlib
            module = importlib.import_module(module_name)
            self.modules[module_name] = module
            logging.info(f"Module '{module_name}' chargé avec succès.")
            return module
        except Exception as e:
            logging.error(f"Erreur lors du chargement du module '{module_name}': {e}")

    def load_modules_from_directory(self):
        """Charger tous les modules depuis un répertoire."""
        # Charger d'abord les subscribers
        for module_name in self.priority_modules:
            if f"{module_name}.py" in os.listdir(self.modules_path):
                module = self.load_module(module_name)
                if module:
                    self.execute_module(module)

        # Charger ensuite les autres modules
        for file in os.listdir(self.modules_path):
            if file.endswith(".py") and file != "__init__.py" and file[:-3] not in self.priority_modules:
                module_name = file[:-3]
                module = self.load_module(module_name)
                if module:
                    self.execute_module(module)

    def execute_module(self, module):
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and hasattr(attr, 'execute'):
                instance = attr(self.message_bus)
                instance.execute()

    def get_module(self, module_name):
        """Récupérer un module déjà chargé."""
        return self.modules.get(module_name)
