import paho.mqtt.client as mqtt
import time


def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

mqttBroker = "test.mosquitto.org"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker)

#client.loop_start()

client.subscribe("TEMPERATURE_wwx")
client.on_message=on_message

print("test")
#time.sleep(30)
print("after")
#client.loop_stop()