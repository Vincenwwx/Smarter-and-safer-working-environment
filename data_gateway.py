import paho.mqtt.client as mqtt
import time, threading
import multiprocessing as mp
import configparser
import json
from edge_device_regulate.sensors import get_environment_temperature_and_humidity, \
    get_environment_lightness, detect_movement, get_body_temperature


class DataGateway:

    def __init__(self, client_id, server_url):
        self.client = mqtt.Client(client_id)
        self.client.on_message = self.on_message
        self.client.connect(server_url)

    # ------------------- Callback functions ----------------------
    # After receiving incoming messages (AI plans)
    # Todo: Plan implementation on edge
    @staticmethod
    def on_message(client, userdata, message):
        payload = message.payload.decode("utf-8")
        print(" < received plan " + payload)
        print("Actuators work.....")

    @staticmethod
    def on_entrance_connect(client, userdata, flags, rc):
        print("Connected with result code {0}".format(str(rc)))
        client.subscribe(self.topic_sub)

    def on_environment_connect(client, userdata, flags, rc):
        print("Connected with result code {0}".format(str(rc)))
        client.subscribe(self.topic_sub)
