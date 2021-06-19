import paho.mqtt.client as mqtt
import time


class MqttTerminal:
    def __init__(self, server, client):
        self.client = mqtt.Client(client)
        self.client.connect(server)

    def publish_data(self, catalogue, data):
        self.client.publish(catalogue, data)
        print("Successfully published " + str(data) + " under catalogue " + catalogue)

    def subscribe_data(self, catalogue):
        self.client.loop_start()
        self.client.subscribe(catalogue)
        self.client.on_message = self.on_message()
        time.sleep(3)
        self.client.loop_stop()


def on_message(userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))