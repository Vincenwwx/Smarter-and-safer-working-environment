import paho.mqtt.client as mqtt
from mqtt_communicate.mqtt_terminal import MqttTerminal


def on_message(client, userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))

mqttBroker = "127.0.0.1"
mqtt = MqttTerminal(mqttBroker, "mobile")

while True:
    mqtt.subscribe_data("sensor_data")