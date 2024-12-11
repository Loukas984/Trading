import time
import logging

class Monitor:
    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.message_bus.subscribe("trade_signal", self.on_trade_signal)
        self.message_bus.subscribe("price_data", self.on_price_data)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.FileHandler('monitor.log')
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.handler)
        self.trade_signals = []
        self.price_data = []

    def on_trade_signal(self, signal):
        """Surveiller les signaux de trading générés."""
        self.logger.info(f"Surveillance du signal : {signal}")
        print(f"Surveillance du signal : {signal}")
        self.trade_signals.append(signal)
        self.check_signals()

    def on_price_data(self, price):
        """Surveiller les données de prix."""
        self.logger.info(f"Surveillance du prix : {price}")
        print(f"Surveillance du prix : {price}")
        self.price_data.append(price)
        self.check_prices()

    def check_signals(self):
        # Logique de surveillance des signaux
        if len(self.trade_signals) > 5:
            self.logger.warning("Nombre de signaux de trading élevé")
            print("Nombre de signaux de trading élevé")

    def check_prices(self):
        # Logique de surveillance des prix (alertes, logs, etc.)
        if len(self.price_data) > 10:
            self.logger.warning("Nombre de données de prix élevé")
            print("Nombre de données de prix élevé")

    def execute(self):
        """Vérification continue de l'état."""
        while True:
            # Logique de monitoring en continu
            self.logger.info("Surveillance en cours...")
            print("Surveillance en cours...")
            time.sleep(5)            