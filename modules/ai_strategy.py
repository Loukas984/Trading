import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import logging

class AIStrategy:
    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.model = self.create_lstm_model()
        self.message_bus.subscribe("price_data", self.on_price_data)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_lstm_model(self):
        """Créer un modèle LSTM simple."""
        logging.info("Création du modèle LSTM...")
        model = Sequential()
        model.add(Input(shape=(100, 1)))
        model.add(LSTM(50, return_sequences=True, dropout=0.2))
        model.add(LSTM(50, return_sequences=False, dropout=0.2))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        logging.info("Modèle LSTM créé avec succès.")
        return model

    def on_price_data(self, price_data):
        """Faire une prédiction de prix avec LSTM."""
        logging.info("Réception des données de prix...")
        # Assurez-vous que price_data est une séquence de données
        if len(price_data) >= 100:  # Vérifie que tu as assez de données
            price_data = np.array(price_data[-100:]).reshape(-1, 100, 1)  # Formater les données
            logging.info("Prédiction du prix suivant...")
            prediction = self.model.predict(price_data)  # Prédiction du modèle
            logging.info(f"Prédiction du prix suivant : {prediction[0][0]}")
            print(f"Prédiction du prix suivant : {prediction[0][0]}")  # Affiche la prédiction

    def execute(self):
        """Méthode pour démarrer le processus, par exemple, entraîner le modèle."""
        logging.info("Exécution de la stratégie AI...")
        print("Exécution de la stratégie AI...")  # Logique d'exécution ici
        self.train_model()

    def train_model(self):
        """Méthode pour entraîner le modèle."""
        logging.info("Entraînement du modèle...")
        try:
            # Générer des données d'entraînement
            train_data = np.random.rand(1000, 100, 1)
            # Entraîner le modèle
            self.model.fit(train_data, np.random.rand(1000, 1), epochs=10, batch_size=32)
            logging.info("Modèle entraîné avec succès.")
        except KeyboardInterrupt:
            logging.warning("Entraînement interrompu par l'utilisateur.")
        except Exception as e:
            logging.error(f"Erreur lors de l'entraînement du modèle: {e}")
