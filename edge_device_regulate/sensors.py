import gin
import RPi.GPIO as GPIO
import os
import glob
import time

False = 0
True = 1

GPIO.setmode(GPIO.BOARD)

@gin.configurable
def config_sensors():   # Required in initialization
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
 
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'


    GPIO.setup(DHT_data, GPIO.IN)
    GPIO.setup(Light_data, GPIO.IN)
    GPIO.setup(IR1, GPIO.IN)
    GPIO.setup(IR2, GPIO.IN)
    GPIO.setup(IR3, GPIO.IN)
    GPIO.setup(Temperature_data, GPIO.IN)
    pass

def read_temp_raw():    # Read raw temperature. For use in get_body_temperature()
    fdir = open(device_file, 'r')
    rawlines = fdir.readlines()
    fdir.close()
    return rawlines

def get_body_temperature():
    """
    Get body temperature by using normal temperature sensor
    :return: temperature    temperature of body
    """
    rawlines = read_temp_raw()
    while rawlines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        rawlines = read_temp_raw()
    equals_pos = rawlines[1].find('t=')
    if equals_pos != -1:
        temp_string = rawlines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def get_environment_temperature_and_humidity():
    """
    Get environment temperature and humidity by using DHT sensor
    :return: [temperature, humidity]
    """
    pass


def get_weather_report(place):
    """
    Get local climate information from the weather report
    :param place: the place where you want to gather climate information
    :return: temperature of target place
    :exception: if the place not exists
    """
    pass


def get_environment_brightness():
    """
    Get environment brightness by using LDR sensor
    :return: 1:dark  0:bright      brightness of the environment
    """
    return GPIO.input(Light_data)
    pass


def detect_movement_entrance():
    """
    Detect object movement at the gate entrace by using IR sensor
    :return: 1:has object  0:no object
    """
    return GPIO.input(IR1)
    pass


def detect_movement_office():
    """
    Detect object movement inside the office by using IR sensor
    :return: 1:has object  0:no object
    """
    return GPIO.input(IR2), GPIO.input(IR3)
    pass