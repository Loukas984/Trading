from utils.message_bus import MessageBus
import logging
from binance.client import Client
from dotenv import load_dotenv
from utils.message_bus import MessageBus
import logging
import os
import json

class OrderExecutor:
    def __init__(self, message_bus):
        load_dotenv()
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        self.trading_config = config['trading']
        self.quantity = self.trading_config['quantity']
        self.symbol = self.trading_config['symbol']
        
        self.message_bus = message_bus
        self.message_bus.subscribe("trade_signal", self.on_trade_signal)
        
        self.client = Client(
            os.getenv('API_KEY'),
            os.getenv('API_SECRET')
        )
        self.logger = logging.getLogger(__name__)

    def on_trade_signal(self, signal):
        try:
            if signal == "BUY":
                order = self.client.create_order(
                    symbol=self.symbol,
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=self.quantity
                )
                self.logger.info(f"Ordre d'achat exécuté: {order}")
                
            elif signal == "SELL":
                order = self.client.create_order(
                    symbol=self.symbol,
                    side=Client.SIDE_SELL, 
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=self.quantity
                )
                self.logger.info(f"Ordre de vente exécuté: {order}")
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de l'ordre : {e}")

    def execute(self):
        """Attendre et traiter les signaux de trading."""
        self.logger.info("OrderExecutor prêt à recevoir des signaux de trading.")        # Si tu souhaites ajouter une logique d'attente ou de traitement, fais-le ici