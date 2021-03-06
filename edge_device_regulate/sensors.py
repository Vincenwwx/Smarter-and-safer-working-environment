import pathlib
import RPi.GPIO as GPIO
import os
import glob
import time
import board    #for DHT
import adafruit_dht   #for DHT #required CircuitPython lib installation
import configparser

config = configparser.ConfigParser()
config.read(pathlib.Path(__file__).parents[1].joinpath("config.ini"))


class SensorReader:
    def __init__(self):
        self.LDR = int(config["Sensors"]["LDR_pin"])
        self.IR1 = int(config["Sensors"]["IR1_pin"])     # For movement at the entrance
        self.IR2 = int(config["Sensors"]["IR2_pin"])     # For presence at the gate
        self.IR3 = int(config["Sensors"]["IR3_pin"])     # For office
        self.IR4 = int(config["Sensors"]["IR4_pin"])     # For office
        DHT = config["Sensors"]["DHT_pin"]
        self.dhtDevice = adafruit_dht.DHT11(eval(DHT))
        self.device_file = ""

        GPIO.setup(self.LDR, GPIO.IN)
        GPIO.setup(self.IR1, GPIO.IN)
        GPIO.setup(self.IR2, GPIO.IN)
        GPIO.setup(self.IR3, GPIO.IN)
        GPIO.setup(self.IR4, GPIO.IN)

        self.setupW1()

    def setupW1(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'

        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def read_temp_raw(self):  # Read raw temperature. For use in get_body_temperature()
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def get_body_temperature(self):
        """
        Get body temperature by using normal temperature sensor
        :return: temperature    temperature of body
        Reference: https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
        """
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            print("\t [Temperature sensor] Body temperature: " + str(temp_c) + " C")
            return temp_c

    def get_environment_temperature_and_humidity(self):
        """
        Get environment temperature and humidity by using DHT sensor
        :return: [temperature, humidity]
        Reference: https://github.com/adafruit/Adafruit_CircuitPython_DHT/blob/main/examples/dht_simpletest.py
        """
        while True:
            try:
                # Print the values to the serial port
                temperature = self.dhtDevice.temperature
                humidity = self.dhtDevice.humidity
                print("\t [DHT sensor]")
                print("\t\t Office temperature: " + str(temperature))
                print("\t\t Office humidity: " + str(humidity))
                return temperature, humidity

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
                continue

            except Exception as error:
                self.dhtDevice.exit()
                raise error

    def get_environment_brightness(self):
        """
        Get environment brightness by using LDR sensor
        :return:    1: dark
                    0: bright      brightness of the environment
        """
        if GPIO.input(self.LDR):
            print("\t [LDR sensor] Brightness: dark")
            return 1
        else:
            print("\t [LDR sensor] Brightness: bright")
            return 0

    def detect_movement_entrance(self):
        """
        Detect object movement at the gate entrance by using IR sensor
        !!! Attention:
            when object detected, the GPIO input will be 0, otherwise 1
        :return:    1: object detected
                    0: no object
        """
        if not GPIO.input(self.IR1):
            print("\t [IR sensor] Detected object at the entrance")
            return 1
        else:
            print("\t [IR sensor] Not detected object at the entrance")
            return 0

    def detect_presence_at_gate(self):
        """
        Detect object movement at the gate entrance by using IR sensor
        !!! Attention:
            when object detected, the GPIO input will be 0, otherwise 1
        :return:    1: object detected
                    0: no object
        """
        if not GPIO.input(self.IR2):
            print("\t [IR sensor] Detected object at the gate")
            return 1
        else:
            print("\t [IR sensor] Not detected object at the gate")
            return 0

    def detect_movement_office(self):
        """
        Detect object movement inside the office by using IR sensor
        :return: 1:has object  0:no object
        """
        if GPIO.input(self.IR4) or GPIO.input(self.IR3):
            print("\t [IR sensor] Detected object in the office")
            return 1
        else:
            print("\t [IR sensor] Not detected object at the entrance")
            return 0
