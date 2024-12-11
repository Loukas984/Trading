# strategy.py
from utils.message_bus import MessageBus
import random
import logging

class Strategy:
    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.message_bus.subscribe("price_data", self.on_price_data)
        self.thresholds = {"buy": 20000, "sell": 30000}

    def on_price_data(self, price):
        self.logger.info("Received price data")
        signal = self.generate_signal(price)
        self.logger.info(f"Generated signal: {signal}")
        print(f"Signal généré : {signal}")
        self.message_bus.publish("trade_signal", signal)

    def generate_signal(self, price):
        if price > self.thresholds["sell"]:
            self.logger.info(f"Price is above {self.thresholds['sell']}, generating SELL signal")
            return "SELL"
        elif price < self.thresholds["buy"]:
            self.logger.info(f"Price is below {self.thresholds['buy']}, generating BUY signal")
            return "BUY"
        else:
            self.logger.info(f"Price is between {self.thresholds['buy']} and {self.thresholds['sell']}, generating HOLD signal")
            return "HOLD"

    def execute(self):
        self.logger.info("Executing strategy...")
        print("Exécution de la stratégie...")            