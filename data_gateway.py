#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import threading
import multiprocessing as mp
import configparser
import json
from edge_device_regulate.sensors import SensorReader
from edge_device_regulate.actuators import LEDs_controller, Buzzer_controller, \
    Ventilator_controller, Door_controller, Heater_controller


"""
Data gateway is responsible for collect and publish data from edge devices and 
implement the plans on the actuators
[--Thread 1--]
    Collect sensor data at the entrance every 1s              (MQTT publisher)
[--Thread 2--]
    Collect sensor data at the office environment every 10s   (MQTT publisher)
[--Thread 3--]
    Execute plans                                             (MQTT subscriber)
"""


# client, user and device details
config = configparser.ConfigParser()
config.read("config.ini")

serverUrl = config["MQTT"]["server"]
topic_pub_entrance = config["MQTT"]["topic_raw_data_entrance"]
topic_pub_environment = config["MQTT"]["topic_raw_data_environment"]
topic_sub = config["MQTT"]["topic_plan"]

# task queue to overcome issue with paho when using multiple threads:
#   https://github.com/eclipse/paho.mqtt.python/issues/354
task_queue = mp.Queue()
sensor_reader = SensorReader()

leds_control = LEDs_controller(red_address=config["Actuators"]["LED_red_pin"],
                               green_address=config["Actuators"]["LED_green_pin"],
                               yellow_address=config["Actuators"]["LED_yellow_pin"])
ventilator_control = Ventilator_controller(
    ventilator_pin=config["Actuators"]["ventilator_pin"])
buzzer_control = Buzzer_controller()
door_control = Door_controller()
heater_control = Heater_controller()


# ------------------- Callback functions ----------------------
# After receiving incoming messages (AI plans)
def on_new_plan(client, userdata, message):
    payload = message.payload.decode("utf-8")
    # print(" < received plan " + payload)

    if "switchon_heater" in payload:
        heater_control.set_valve(1)
    elif "switchoff_heater" in payload:
        heater_control.set_valve(0)
    elif "switchon_light" in payload:
        leds_control.set_led("yellow", 1)
    elif "switchoff_light" in payload:
        leds_control.set_led("yellow", 0)
    elif "switchon_fan" in payload:
        ventilator_control.set_ventilator(1)
    elif "switchoff_fan" in payload:
        ventilator_control.set_ventilator(0)
    elif "switchon_heater" in payload:
        heater_control.set_valve(1)
    elif "switchoff_heater" in payload:
        heater_control.set_valve(0)
    else:
        print("Unrecognized plan, please check!")
        raise


# display all outgoing messages
def on_publish(client, userdata, mid):
    print(" > published message: {}".format(mid))


# ------------------- Functions to publish data ----------------------
# Send measurement
def send_env_measurement():
    print("Sending $ ENVIRONMENT $ measurement...")
    temperature, humidity = sensor_reader.get_environment_temperature_and_humidity()
    lightness = sensor_reader.get_environment_brightness()
    measurement = json.dumps({
        "temperature": temperature,
        "humidity": humidity,
        "lightness": lightness
    })
    print("============================================")
    print("")
    publish(topic_pub_environment, measurement)


def send_entrance_measurement():
    print("Sending # ENTRANCE # measurement...")
    people_detected = sensor_reader.detect_movement_entrance()
    body_temperature = sensor_reader.get_body_temperature()
    measurement = json.dumps({
        "people_detected": people_detected,
        "body_temperature": body_temperature
    })
    print("============================================")
    print("")
    publish(topic_pub_entrance, measurement)


# publish a message
def publish(topic, message, wait_for_ack=False):
    QoS = 2 if wait_for_ack else 0
    message_info = client.publish(topic, message, QoS)
    if wait_for_ack:
        print(" > awaiting ACK for {}".format(message_info.mid))
        message_info.wait_for_publish()
        print(" < received ACK for {}".format(message_info.mid))


# -------------------- Threads ------------------------
# main device loop
def data_collect_thread(content, interval):
    """
    Function of thread to collect data
    :param content: "entrance" or "environment"
    :param interval:   time interval to recollect and republish data
    :return: None
    """
    if content == "entrance":
        task = send_entrance_measurement
    elif content == "environment":
        task = send_env_measurement
    else:
        print("Please specify a valid task.\n")
        exit(0)

    while True:
        task_queue.put(task)
        time.sleep(interval)


"""
Connect the client to MQTT server and register a device
"""
client = mqtt.Client("EDGE")
client.on_message = on_new_plan
client.on_publish = on_publish
client.connect(serverUrl)
client.loop_start()
print("Device registered successfully!")

client.subscribe(topic_sub)

"""
create two threads for sending environment and entrance data respectively
"""
device_loop_thread = threading.Thread(target=data_collect_thread, args=("environment", 10,))
device_loop_thread.daemon = True
device_loop_thread.start()

device_loop_thread = threading.Thread(target=data_collect_thread, args=("entrance", 1,))
device_loop_thread.daemon = True
device_loop_thread.start()


# process all tasks on queue
try:
    while True:
        task = task_queue.get()
        task()
except (KeyboardInterrupt, SystemExit):
    leds_control.off()
    ventilator_control.stop()

    print("Received keyboard interrupt, quitting ...")
    exit(0)
