import time
from dotenv import load_dotenv
import os
from binance.client import Client
from utils.message_bus import MessageBus
import logging
import pandas as pd
from datetime import datetime
import json

class DataCollector:
    def __init__(self, message_bus):
        load_dotenv()
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        self.trading_config = config['trading']
        # Convertir l'intervalle selon l'unité (m=minutes, s=secondes)
        interval_str = self.trading_config['interval']
        if interval_str.endswith('m'):
            self.interval = int(interval_str.replace('m', '')) * 60
        elif interval_str.endswith('s'):
            self.interval = int(interval_str.replace('s', ''))
        self.max_price_data = self.trading_config['max_price_data']
        self.symbol = self.trading_config['symbol']
        self.message_bus = message_bus
        self.client = Client(
            os.getenv('API_KEY'),
            os.getenv('API_SECRET')
        )
        self.running = True
        self.price_data = []
        self.logger = logging.getLogger(__name__)

        # Appel de la méthode pour charger les données historiques
        self.historical_data = self.load_historical_data(self.symbol, self.interval)
        self.logger.info(f"Chargé {len(self.historical_data)} données historiques.")

    def collect_data(self):
        try:
            price_data = self.client.get_symbol_ticker(symbol="BTCUSDT")
            price = float(price_data['price'])
            self.save_data(price)  # Sauvegarder chaque nouvelle donnée
            self.price_data.append(price)
            self.logger.info(f"Données collectées : {price}")

            if len(self.price_data) >= self.max_price_data:
                self.message_bus.publish("price_data", self.price_data)
                self.price_data = []
        except Exception as e:
            self.logger.error(f"Erreur lors de la collecte des données : {e}")

    def execute(self):
        """Collecter les données en boucle."""
        self.logger.info("Démarrage de la collecte de données...")
        while self.running:
            self.collect_data()
            time.sleep(self.interval)  # Attendre avant de collecter à nouveau

    def stop(self):
        """Méthode pour arrêter la collecte de données."""
        self.running = False
        self.logger.info("Arrêt de la collecte de données.")

    def get_price_data(self):
        """Méthode pour récupérer les données de prix."""
        return self.price_data

    def set_interval(self, interval):
        """Méthode pour définir l'intervalle de collecte de données."""
        self.interval = interval

    def set_max_price_data(self, max_price_data):
        """Méthode pour définir le nombre maximum de données de prix à stocker."""
        self.max_price_data = max_price_data        

    def save_data(self, price_data):
        try:
            df = pd.DataFrame({
                'timestamp': [datetime.now()],
                'price': [price_data]
            })
            df.to_csv('price_history.csv', mode='a', header=False, index=False)
            self.logger.info("Données sauvegardées dans price_history.csv")
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde données : {e}")

    def load_saved_data(self):
        try:
            df = pd.read_csv('price_history.csv')
            return df['price'].tolist()
        except FileNotFoundError:
            return []

    def load_historical_data(self, symbol=None, interval=None, limit=1000):
        """Charger les données historiques depuis Binance."""
        try:
            symbol = symbol or self.symbol
            interval = interval or self.trading_config['interval']
            
            klines = self.client.get_historical_klines(
                symbol, 
                interval,
                "1 day ago UTC",
                limit=limit
            )

            if isinstance(klines, list):
                prices = [float(kline[4]) for kline in klines]  # Prix de clôture
                self.logger.info(f"Chargé {len(prices)} données historiques pour {symbol}.")
                return prices
            else:
                self.logger.error(f"Erreur : la réponse de l'API n'est pas une liste. Type reçu : {type(klines)}")
                return []
        except Exception as e:
            self.logger.error(f"Erreur chargement historique : {e}")
            return []