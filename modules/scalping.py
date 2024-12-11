import logging

class Scalping:
    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.message_bus.subscribe("price_data", self.on_price_data)
        self.scalping_threshold = 0.01  # threshold for scalping
        self.last_price = None
        self.logger = logging.getLogger(__name__)

    def on_price_data(self, price):
        # Logique pour le scalping
        self.execute(price)

    def execute(self, price):
        """Exécuter la logique de scalping."""
        if self.last_price is not None and abs(price - self.last_price) > self.scalping_threshold:
            self.logger.info(f"Scalping Price : {price}")
        else:
            self.logger.debug(f"Price update: {price}")
        self.last_price = price