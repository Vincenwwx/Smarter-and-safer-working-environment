from random import uniform
from mqtt_terminal import MqttTerminal
import time

mqttBroker = "test.mosquitto.org"
mqtt = MqttTerminal(mqttBroker, "vincenTest")

while True:
    randNumber = uniform(20.0, 21.0)
    mqtt.publish_data("TEMPERATURE_wwx", randNumber)
    time.sleep(1)