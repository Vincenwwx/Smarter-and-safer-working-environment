#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from threading import Thread
import configparser
import json

"""
Decision maker is responsible for subscribing sensor data and then publish
plans achieved by AI planning
[--Thread 1--]
    Dealing with entrance data
[--Thread 2--]
    Dealing with environment data
"""

config = configparser.ConfigParser()
config.read("config.ini")

serverUrl = config["MQTT"]["server"]
topic_sub_entrance = config["MQTT"]["topic_raw_data_entrance"]
topic_sub_environment = config["MQTT"]["topic_raw_data_environment"]
topic_pub = config["MQTT"]["topic_plan"]


# ------------------ Callback functions ----------------------
# Todo: Implement AI planing
# After receiving incoming messages (AI plans)
def on_environment_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(" < {} received message: {}".format(client, payload))

    payload = json.loads(payload)

    client.publish(topic_pub, "Plan for environment")


def on_entrance_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(" < {} received message: {}".format(client, payload))

    payload = json.loads(payload)


def on_entrance_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe(topic_sub_entrance)


def on_environment_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe(topic_sub_environment)


# display all outgoing messages
def on_publish(client, userdata, mid):
    print(" > {} published message: {}".format(client, mid))


class DecisionMaker(Thread):

    def __init__(self, client_id, server_url, content):
        super(DecisionMaker, self).__init__()
        self.client = mqtt.Client(client_id)
        self.client.on_publish = on_publish
        if content == "entrance":
            self.client.on_message = on_entrance_message
            self.client.on_connect = on_entrance_connect
        else:
            self.client.on_message = on_environment_message
            self.client.on_connect = on_environment_connect

        try:
            self.client.connect(server_url)
        except:
            print("Something went wrong by connecting broker, now exit...")
            exit(0)

        print("Decision maker {} on position".format(client_id))

    def run(self) -> None:
        self.client.loop_forever()


if __name__ == '__main__':

    try:

        dm1 = DecisionMaker(client_id="dm1", server_url=serverUrl, content="entrance")
        dm2 = DecisionMaker(client_id="dm2", server_url=serverUrl, content="environment")

        dm1.start()
        dm2.start()

        dm1.join()
        dm2.join()

    except (KeyboardInterrupt, SystemExit):

        print("Received keyboard interrupt, quitting ...")
        exit(0)