#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import time
import multiprocessing as mp
import configparser
import json
import logging
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


class Edge(mp.Process):
    """
    Create a process which is only responsible for sending measurement
    at the entrance or inside the office
    """
    def __init__(self, place, mqtt_client_id, configuration, sensor_readers):
        super(Edge, self).__init__()
        self.client = None
        self.config = configuration
        self.sensor_reader = sensor_readers

        if place == "entrance":
            self.task = self.send_entrance_measurement
            self.mqtt_pub = self.config["MQTT"]["topic_raw_data_entrance"]
            self.delay = 3
        elif place == "office":
            self.task = self.send_env_measurement
            self.mqtt_pub = self.config["MQTT"]["topic_raw_data_environment"]
            self.delay = 10
        else:
            print("Please specify a valid place. Exit...")
            exit(0)

        self.init_mqtt(mqtt_client_id, place)

    def init_mqtt(self, client_id, place):
        self.client = mqtt.Client(client_id)
        self.client.on_publish = self.on_publish
        self.client.connect(self.config["MQTT"]["server"])
        print("MQTT Client {} registered successfully!".format(client_id))

    def run(self) -> None:
        # Start mqtt loop
        self.client.loop_start()

        while True:
            self.task()
            time.sleep(self.delay)

    def _publish(magic):
        """
        This is the definition of the decorator that publish data that the function
        it is decorating to the broker
        """
        def wrapper(self, *args, **kwargs):
            data = magic(self, *args, **kwargs)
            QoS = 2     # set the Qos here
            self.client.publish(self.mqtt_pub, data, QoS)
            return data
        return wrapper

    @_publish
    def send_env_measurement(self):
        print("Sending $ ENVIRONMENT $ measurement...")
        temperature, humidity = self.sensor_reader.get_environment_temperature_and_humidity()
        lightness = self.sensor_reader.get_environment_brightness()
        measurement = json.dumps({
            "temperature": temperature,
            "humidity": humidity,
            "lightness": lightness
        })
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("")
        return measurement

    @_publish
    def send_entrance_measurement(self):
        print("Sending # ENTRANCE # measurement...")
        people_detected = self.sensor_reader.detect_movement_entrance()
        body_temperature = self.sensor_reader.get_body_temperature()
        measurement = json.dumps({
            "people_detected": people_detected,
            "body_temperature": body_temperature
        })
        print("====================================================")
        print("")
        return measurement

    # ------------------- Callback functions ----------------------
    # display all outgoing messages
    @staticmethod
    def on_publish(client, userdata, mid):
        print(" > published message: {}".format(mid))


def on_new_plan(client, userdata, message):

    payload = message.payload.decode("utf-8")
    print(" < received plan " + payload)

    # Office
    if "switchon_humidifier" in payload:
        print("[Actuator] Humidifier is turned on")
    elif "switchoff_humidifier" in payload:
        print("[Actuator] Humidifier is turned off")
    elif "switchon_light" in payload:
        leds_control.set_led("yellow", 1)
    elif "switchoff_light" in payload:
        leds_control.set_led("yellow", 0)
    elif "switchon_fan" in payload:
        ventilator_control.set_ventilator(1)
    elif "switchoff_fan" in payload:
        ventilator_control.set_ventilator(0)
    # Entrance
    elif "switchon_greenled_buzzer" in payload:
        buzzer_control.play_sound("come_in_please")
        leds_control.blink("green")
        door_control.set_door(1)
    elif "switchon_redled_buzzer" in payload:
        buzzer_control.play_sound("sorry_pls_try")
        leds_control.blink("red")
    elif "switchoff_greenled_redled_buzzer" in payload:
        pass
    # Unrecognized plans
    else:
        print("Unrecognized plan, please check!")
        raise


if __name__ == '__main__':

    """
    Parse configuration
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    # --------------------- Init ------------------------
    """
    Sensor reader
    """
    sensor_reader = SensorReader()
    """
    Actuators
    """
    leds_control = LEDs_controller(red_address=config["Actuators"]["LED_red_pin"],
                                   green_address=config["Actuators"]["LED_green_pin"],
                                   yellow_address=config["Actuators"]["LED_yellow_pin"])
    ventilator_control = Ventilator_controller(
        ventilator_pin=config["Actuators"]["ventilator_pin"])
    buzzer_control = Buzzer_controller()
    door_control = Door_controller()

    # ---------------- Data collectors -------------------
    entrance_guard = Edge("entrance", "Safe_Guard", config, sensor_reader)
    comfort_keeper = Edge("office", "Comfort", config, sensor_reader)

    entrance_guard.start()
    entrance_guard.join()

    comfort_keeper.start()
    comfort_keeper.join()

    # ------------------- Executor -----------------------
    """
    Connect the client to MQTT server and register a device
    """
    client = mqtt.Client("Edge executor")
    client.on_message = on_new_plan
    client.connect(config["MQTT"]["server"])
    print("Executor registered successfully!")
    client.subscribe(config["MQTT"]["topic_plan"])

    try:
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):
        leds_control.off()
        ventilator_control.stop()

        print("Received keyboard interrupt, quitting ...")
        exit(0)