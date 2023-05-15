

class RabbitChannel:
    def __init__(self, channel):
        self.channel = channel
        self._closed = False

    def stop_consuming(self):
        self.channel.stop_consuming()

    def close(self):
        if not self._closed:
            self.channel.close()
            self._closed = True
