import gin
import RPi.GPIO as GPIO
import os
import glob
import time
import board    #for DHT
import adafruit_dht   #for DHT #required CircuitPython lib installation

@gin.configurable
class SensorReader:
    def __init__(self, Light_data, IR1, IR2, IR3, dhtPin):
        self.Light_data = Light_data
        self.IR1 = IR1
        self.IR2 = IR2
        self.IR3 = IR3
        self.dhtDevice = adafruit_dht.DHT11(eval(dhtPin))
        

        GPIO.setup(Light_data, GPIO.IN)
        GPIO.setup(IR1, GPIO.IN)
        GPIO.setup(IR2, GPIO.IN)
        GPIO.setup(IR3, GPIO.IN)

    def setupW1(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
    
        base_dir = '/sys/bus/w1/devices/'

        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def read_temp_raw(self):    # Read raw temperature. For use in get_body_temperature()
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def get_body_temperature(self):
        """
        Get body temperature by using normal temperature sensor
        :return: temperature    temperature of body
        """
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c


    def get_environment_temperature_and_humidity(self):
        """
        Get environment temperature and humidity by using DHT sensor
        :return: [temperature, humidity]
        """
        while True:
            try:
                # Print the values to the serial port
                temperature_c = self.dhtDevice.temperature
                humidity = self.dhtDevice.humidity
                print(
                    "Temp: {:.1f} C    Humidity: {}% ".format(
                        temperature_c, humidity
                    )
                )
                return temperature_c, humidity

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                self.dhtDevice.exit()
                raise error

            time.sleep(2.0)
        pass


    def get_environment_brightness(self):
        """
        Get environment brightness by using LDR sensor
        :return: 1:dark  0:bright      brightness of the environment
        """
        if (GPIO.input(self.Light_data)==1):
            print("Brightness is dark")
        elif (GPIO.input(self.Light_data)==0):
            print("Brightness is bright")
        return GPIO.input(self.Light_data)
        pass


    def detect_movement_entrance(self):
        """
        Detect object movement at the gate entrace by using IR sensor
        :return: 1:has object  0:no object
        """
        if (GPIO.input(self.IR1)==1):
            print("Detected object at the entrance")
        elif (GPIO.input(self.IR1)==0):
            print("Not detected object at the entrance")
        return GPIO.input(self.IR1)
        pass


    def detect_movement_office(self):
        """
        Detect object movement inside the office by using IR sensor
        :return: 1:has object  0:no object
        """
        myDetection = 1
        if (GPIO.input(self.IR2)==1) or (GPIO.input(self.IR3)==1) :
            print("Detected object in the office")
            myDetection = 1
        else:
            print("Not detected object at the entrance")
            myDetection = 0
        return myDetection  
        #return GPIO.input(IR2), GPIO.input(IR3)
        pass