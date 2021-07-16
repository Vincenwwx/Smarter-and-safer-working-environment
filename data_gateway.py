#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
from edge_device_regulate.sensors import SensorReader
from edge_device_regulate.edge import Edge

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


if __name__ == '__main__':

    """
    Parse configuration
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    """
    Sensor reader
    """
    sensor_reader = SensorReader()

    try:

        entrance_guard = Edge("entrance", "Safe_Guard", config, sensor_reader)
        comfort_keeper = Edge("office", "Comfort", config, sensor_reader)
        executor = Edge("executor", "Executor", config, sensor_reader)

        entrance_guard.start()
        comfort_keeper.start()
        executor.start()

        comfort_keeper.join()
        entrance_guard.join()
        executor.join()

    except (KeyboardInterrupt, SystemExit):

        print("Received keyboard interrupt, quitting ...")
        exit(0)