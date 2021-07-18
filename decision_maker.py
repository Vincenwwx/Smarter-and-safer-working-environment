#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pathlib
from datetime import datetime
import paho.mqtt.client as mqtt
from threading import Thread
from ai_planning.handle_pddl import get_plans, update_problem
import configparser
import json
import logging


"""
Decision maker is responsible for subscribing sensor data and then publish
plans achieved by AI planning
[--Thread 1--]
    Dealing with entrance data
[--Thread 2--]
    Dealing with office data
"""


# ------------------ Callback functions ----------------------
# After receiving incoming messages (AI plans)
def on_environment_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(" < {} received message: {}".format(client, payload))

    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                 " received: " + payload)
    payload = json.loads(payload)
    update_problem("office", payload)

    # Get plans and publish
    plans = get_plans("office")
    for act in plans:
        client.publish(topic_pub, str(act["name"]))
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                     + " published plan: " + str(act["name"]))


def on_entrance_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(" < {} received message: {}".format(client, payload))

    logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                 " received: " + payload)
    payload = json.loads(payload)
    update_problem("entrance", payload)

    # Get plans and publish
    plans = get_plans("entrance")
    for act in plans:
        client.publish(topic_pub, str(act["name"]))
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                     + " published plan: " + str(act["name"]))


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

    def __init__(self, client_id, server_url, content, configuration):
        super(DecisionMaker, self).__init__()
        self.client = mqtt.Client(client_id)
        self.client.on_publish = on_publish
        self.client.username_pw_set(username=configuration["MQTT"]["username"],
                                    password=configuration["MQTT"]["password"])
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

    config = configparser.ConfigParser()
    config.read("config.ini")

    serverUrl = config["MQTT"]["server"]
    topic_sub_entrance = config["MQTT"]["topic_raw_data_entrance"]
    topic_sub_environment = config["MQTT"]["topic_raw_data_environment"]
    topic_pub = config["MQTT"]["topic_plan"]

    log_file_name = datetime.now().strftime("%Y-%m-%d_%H%M_log")
    log_file_path = pathlib.Path(__file__).parent.joinpath("logs", log_file_name)
    log_file_path.parent.mkdir(exist_ok=True)
    log_file_path.touch(exist_ok=True)
    logging.basicConfig(filename=str(log_file_path), level=logging.INFO)

    try:

        dm1 = DecisionMaker(client_id="dm1", server_url=serverUrl, content="entrance")
        dm2 = DecisionMaker(client_id="dm2", server_url=serverUrl, content="office")

        dm1.start()
        dm2.start()

        dm1.join()
        dm2.join()

    except (KeyboardInterrupt, SystemExit):

        print("Received keyboard interrupt, quitting ...")
        exit(0)