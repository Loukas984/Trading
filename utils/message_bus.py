import logging

class MessageBus:
    def __init__(self):
        self.subscribers = {}
        self.logger = logging.getLogger(__name__)

    def subscribe(self, topic, callback):
        """Permet à un module de s'abonner à un sujet (topic)."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        if callback not in self.subscribers[topic]:
            self.subscribers[topic].append(callback)
            self.logger.info(f"Module subscribed to topic '{topic}'")

    def publish(self, topic, data):
        """Permet à un module de publier des données sur un sujet."""
        if topic in self.subscribers:
            self.logger.info(f"Publishing data on topic '{topic}'")
            for callback in self.subscribers[topic]:
                try:
                    callback(data)
                except Exception as e:
                    self.logger.error(f"Error publishing data on topic '{topic}': {str(e)}")
        else:
            self.logger.warning(f"No subscribers for topic '{topic}'")

    def unsubscribe(self, topic, callback):
        """Permet à un module de se désabonner d'un sujet."""
        if topic in self.subscribers and callback in self.subscribers[topic]:
            self.subscribers[topic].remove(callback)
            self.logger.info(f"Module unsubscribed from topic '{topic}'")
        elif topic not in self.subscribers:
            self.logger.warning(f"No subscribers for topic '{topic}'")
        else:
            self.logger.warning(f"Callback not found for topic '{topic}'")            