import logging

class Backtester:
    def __init__(self, message_bus): # Initialiser le backtester
        self.message_bus = message_bus # Initialiser le bus de messages
        self.message_bus.subscribe("price_data", self.on_price_data) # S'abonner aux données de prix
        self.historical_data = [] # Initialiser les données historiques
        self.logger = logging.getLogger(__name__) # Initialiser le logger
        self.logger.setLevel(logging.INFO) # Définir le niveau de log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # Définir le format du log
        handler = logging.FileHandler('backtester.log') # Définir le fichier de log
        handler.setFormatter(formatter) # Appliquer le format du log
        self.logger.addHandler(handler) # Ajouter le handler au logger
        self.strategy_params = { # Définir les paramètres de la stratégie
            'buy_threshold': 20000, # Seuil d'achat
            'sell_threshold': 30000 # Seuil de vente
        }

    def on_price_data(self, price_data): # Méthode pour recevoir les données de prix
        self.logger.info(f"Test de la stratégie avec les données historiques : {price_data}") # Afficher les données de prix reçues
        self.historical_data.extend(price_data) if isinstance(price_data, list) else self.historical_data.append(price_data)  # Ajouter les données de prix à l'historique 
        signal = self.generate_signal(price_data) # Générer un signal de trading
        self.logger.info(f"Signal généré : {signal}") # Afficher le signal généré
        self.message_bus.publish("trade_signal", signal) # Publier le signal de trading

    def generate_signal(self, price_data):
        current_price = price_data[-1] if isinstance(price_data, list) else price_data
        if current_price > self.strategy_params['sell_threshold']: # Signal de vente
            self.logger.info("Prix supérieur à {}, signal de vente généré".format(self.strategy_params['sell_threshold']))
            return "SELL"
        elif current_price < self.strategy_params['buy_threshold']:  # Signal d'achat
            self.logger.info("Prix inférieur à {}, signal d'achat généré".format(self.strategy_params['buy_threshold']))
            return "BUY"
        else: # Signal de maintien
            self.logger.info("Prix compris entre {} et {}, signal de maintien généré".format(self.strategy_params['buy_threshold'], self.strategy_params['sell_threshold']))
            return "HOLD"

    def execute(self): # Méthode pour lancer le backtester
        self.logger.info("Lancement du backtest...")
        for price in self.historical_data: # Parcourir les données historiques pour générer les signaux
            signal = self.generate_signal(price) # Générer un signal pour chaque prix
            self.logger.info(f"Prix : {price}, Signal : {signal}") # Afficher le signal généré
        self.evaluate_performance() # Évaluer la performance de la stratégie
        self.logger.info("Backtest terminé") # Afficher un message pour indiquer que le backtest est terminé

    def evaluate_performance(self): # Méthode pour évaluer la performance de la stratégie
        self.logger.info("Évaluation de la performance de la stratégie...")
        # Exemple de calcul de la performance
        num_sell_signals = len([price for price in self.historical_data if price > self.strategy_params['sell_threshold']])
        if len(self.historical_data) > 0:
            performance = num_sell_signals / len(self.historical_data)
            self.logger.info("Performance de la stratégie : {:.2f}%".format(performance * 100))
        else:
            self.logger.info("Aucune donnée historique disponible pour évaluer la performance.")