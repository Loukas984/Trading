import logging

class RiskManager:
    def __init__(self, message_bus, client=None):
        self.message_bus = message_bus
        self.client = client
        self.max_risk = 0.02  # Risque maximal de 2% par trade
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.message_bus.subscribe("trade_signal", self.on_trade_signal)
        self.entry_price = None

    def on_trade_signal(self, signal):
        """Ajuster la taille des positions ou le stop-loss en fonction du signal."""
        self.logger.info(f"Gestion des risques pour le signal : {signal}")
        if signal == "BUY":
            self.entry_price = self.get_current_price()
            stop_loss = self.calculate_stop_loss("BUY")
            self.logger.info(f"Stop-Loss défini à {stop_loss}")
            # Ici, tu pourrais vouloir transmettre le stop-loss à l'OrderExecutor
        elif signal == "SELL":
            self.entry_price = self.get_current_price()
            stop_loss = self.calculate_stop_loss("SELL")
            self.logger.info(f"Stop-Loss défini à {stop_loss}")
            # Ici, tu pourrais vouloir transmettre le stop-loss à l'OrderExecutor

    def calculate_stop_loss(self, signal):
        """Calculer un stop-loss basé sur le risque."""
        if self.entry_price is None:
            self.logger.error("Prix d'entrée non défini")
            return None
        # Logique pour calculer le stop-loss en fonction du prix d'entrée
        risk_amount = self.entry_price * self.max_risk
        if signal == "BUY":
            return self.entry_price - risk_amount
        else:
            return self.entry_price + risk_amount

    def get_current_price(self):
        """Récupérer le prix actuel depuis l'API Binance."""
        try:
            ticker = self.client.get_symbol_ticker(symbol=self.symbol)
            return float(ticker['price'])
        except Exception as e:
            self.logger.error(f"Erreur récupération prix : {e}")
            return None

    def execute(self):
        """Cette méthode peut être utilisée pour un contrôle dynamique."""
        self.logger.info("RiskManager prêt à gérer les risques.")
        # Si tu souhaites ajouter une logique d'attente ou de traitement, fais-le ici        