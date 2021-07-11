import argparse
import configparser
import time
from decision_maker import DecisionMaker


if __name__ == "__main__":

    # parse arguments in command
    parser = argparse.ArgumentParser(description="Process parameters")
    parser.add_argument("mode", choices=["edge", "decision"],
                        help="Set running mode")
    mode = parser.parse_args().mode

    # Configuration
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Program starts
    if mode == "edge":
        """
        The program as edge device manager, whose job include collecting data
        from the sensor and control the actuators
        """
    else:
        """
        The program as decision maker, who is responsible for collecting data
        from the MQTT broker and then making decisions based on AI planning
        """
        try:

            dm1 = DecisionMaker(client_id="entrance_dealer", content="entrance",
                                server_url=config["MQTT"]["server"])
            dm2 = DecisionMaker(client_id="office_dealer", content="environment",
                                server_url=config["MQTT"]["server"])

            dm1.start()
            dm2.start()
            dm1.join()
            dm2.join()

        except (KeyboardInterrupt, SystemExit):

            print("Received keyboard interrupt, exit...")
            exit(0)