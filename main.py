#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import configparser
from datetime import datetime
import pathlib
import logging
from decision_maker import DecisionMaker
from edge_device_regulate.sensors import SensorReader
from edge_device_regulate.edge import Edge


if __name__ == "__main__":

    # parse arguments in command
    parser = argparse.ArgumentParser(description="Process parameters")
    parser.add_argument("mode", choices=["decision", "edge"],
                        help="Set running mode")
    mode = parser.parse_args().mode

    # Configuration
    config = configparser.ConfigParser()
    config.read("config.ini")

    serverUrl = config["MQTT"]["server"]
    topic_sub_entrance = config["MQTT"]["topic_raw_data_entrance"]
    topic_sub_environment = config["MQTT"]["topic_raw_data_environment"]
    topic_pub = config["MQTT"]["topic_plan"]

    # Logging
    log_file_name = datetime.now().strftime("%Y-%m-%d_%H%M_log")
    log_file_path = pathlib.Path(__file__).parent.joinpath("logs", log_file_name)
    log_file_path.parent.mkdir(exist_ok=True)
    log_file_path.touch(exist_ok=True)
    logging.basicConfig(filename=str(log_file_path), level=logging.INFO)

    # Program starts
    if mode == "edge":
        """
        The program as edge device manager, whose job include collecting (publish) data
        from the sensor and execute (subscribe) the plan
        """
        # Sensor reader
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

    else:
        """
        The program as decision maker, who is responsible for collecting data
        from the MQTT broker and then making decisions based on AI planning
        """
        try:

            dm1 = DecisionMaker(client_id="dm1", server_url=serverUrl, content="entrance", configuration=config)
            dm2 = DecisionMaker(client_id="dm2", server_url=serverUrl, content="office", configuration=config)

            dm1.start()
            dm2.start()

            dm1.join()
            dm2.join()

        except (KeyboardInterrupt, SystemExit):

            print("Received keyboard interrupt, quitting ...")
            exit(0)