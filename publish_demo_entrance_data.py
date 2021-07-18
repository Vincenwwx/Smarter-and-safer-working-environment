#!/usr/bin/env python
# coding: utf-8

import sys
import configparser
import time

import paho.mqtt.client as mqtt
import json


def on_publish(client, userdata, mid):
    print(" > published message: {}".format(mid))

config = configparser.ConfigParser()
config.read("config.ini")

client = mqtt.Client("Mocker_entrance")
client.on_publish = on_publish
client.username_pw_set(username="sciot", password="sciot_g6")
client.connect(config["MQTT"]["server"])
client.loop_start()

times = 1
for i in range(times):
    mock_data = json.dumps({
        "people_enter": 1,
        "body_temperature": 38.1,
        "people_at_gate": 1,
    })
    client.publish(config["MQTT"]["topic_raw_data_entrance"], mock_data, 2)
    time.sleep(1)