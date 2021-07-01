import gin
import sys

sys.path.insert(0, './edge_device_regulate')
from actuators import *
from sensors import *

import RPi.GPIO as GPIO

def main():
    # Gin-configs
    gin.parse_config_file('./configs/configs.gin')

    myLEDController = LEDs_controller()
    myLEDController.config_led()

    mySensorReader = SensorReader()
    mySensorReader.setupW1()

    abc = mySensorReader.get_body_temperature()
    print(abc)

    mySensorReader.get_environment_temperature_and_humidity()


if __name__ == "__main__":
    main()