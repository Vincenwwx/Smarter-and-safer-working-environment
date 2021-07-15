from playsound import playsound
import RPI.GPIO as GPIO
import pathlib
import configparser


config = configparser.ConfigParser
config.read(pathlib.Path(__file__).parents[1].joinpath("config.ini"))


class LEDs_controller:
    """
    Todo:
        Define the GPIO in configs/configs.gin
    """

    def __init__(self, red_address, green_address, yellow_address):
        self.red_addr = config["Actuators"]["LED_red_pin"]
        self.green_addr = config["Actuators"]["LED_green_pin"]
        self.yellow_addr = config["Actuators"]["LED_yellow_pin"]
        self.red_status = 0
        self.green_status = 0
        self.yellow_status = 0

        # Config pins as output
        GPIO.setup(self.red_addr, GPIO.OUT)
        GPIO.setup(self.green_addr, GPIO.OUT)
        GPIO.setup(self.yellow_addr, GPIO.OUT)

    def set_led(self, name, status):
        """
        Set the LED status
        :param   name:      name of the LED to set,
        :param   status:    0 - OFF, 1 - ON
        :return: boolean    True if successfully set, otherwise False
        :exception:         turn on the LED when it is on,
                            or turn off the LED when it is off
        """
        if name not in ["green", "red", "yellow"]:
            raise ValueError("Please check the LED you want to control")
        if name == "green":
            GPIO.output(self.green_addr, status)
            print("Set green LED " + str(status))
        elif name == "red":
            GPIO.output(self.red_addr, status)
            print("Set red LED " + str(status))
        elif name == "yellow":
            GPIO.output(self.yellow_addr, status)
            print("Set yellow LED " + str(status))


class Ventilator_controller:
    def __init__(self):
        self.vent_addr = config["Actuators"]["ventilator_pin"]
        self.status = 0
        GPIO.setup(self.vent_addr, GPIO.OUT)

    def set_ventilator(self, status):
        """
        Control the ventilator to be opened or closed in the office.
        :param status: 0 - OFF, 1 - ON
        :return: True if successfully set, otherwise False
        """
        if status == 0 and self.status == 1:
            GPIO.output(self.vent_addr, status)
            print("[Actuator] Ventilator is closed")
            return True
        elif status == 1 and self.status == 0:
            GPIO.output(self.vent_addr, status)
            print("[Actuator] Ventilator is opened")
            return True
        else:
            return False


class Door_controller:

    def __init__(self):
        self.status = False

    def set_door(self, status):
        """
        Control the door to be opened or closed at the entrance
        :param status: 0 - OFF, 1 - ON
        :return: True if successfully set, otherwise False
        :exception: open the gate when it is opened,
                    or closed the door when it is close
        """
        if status:
            self.status = True
            print("[Actuator] Door is opened")
        else:
            self.status = False
            print("[Actuator] Door is closed")


class Heater_controller:
    def __init__(self):
        self.valve_opening = False

    def set_valve(self, status):
        if status:
            print("[Actuator] Heater is opened.")
            self.valve_opening = True
        else:
            print("[Actuator] Heater is closed.")
            self.valve_opening = False


class Buzzer_controller:

    def __init__(self):
        """
        hard-code the path of sounds:
            1. sound track: "body_temperature checking"
            2. sound track: "come in please"
            3. sound track: "Sorry, please try again
        """
        self.sound_path = {
            "body_temp_check" : pathlib.Path(__file__).parent.joinpath("sounds", "body_temp_checking.mp3").as_uri(),
            "come_in_please": pathlib.Path(__file__).parent.joinpath("sounds", "come_in_pls.mp3").as_uri(),
            "sorry_pls_try": pathlib.Path(__file__).parent.joinpath("sounds", "sorry_pls_try_again.mp3").as_uri()
        }

    def play_sound(self, sound_name):
        """
        play sound of choice
        :param sound_name: String
        :return: None
        """
        playsound(self.sound_path[sound_name])