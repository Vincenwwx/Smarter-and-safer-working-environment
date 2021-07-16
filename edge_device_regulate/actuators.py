import RPi.GPIO as GPIO
import pathlib
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class LEDs_controller:

    def __init__(self, red_address, green_address, yellow_address):
        # self.red_addr = config["Actuators"]["LED_red_pin"]
        # self.green_addr = config["Actuators"]["LED_green_pin"]
        # self.yellow_addr = config["Actuators"]["LED_yellow_pin"]
        self.red_addr = int(red_address)
        self.green_addr = int(green_address)
        self.yellow_addr = int(yellow_address)

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
        :param   name:      name of the LED to set ("green", "red" and "yellow")
        :param   status:    0 - OFF, 1 - ON
        :return: None
        """
        if name not in ["green", "red", "yellow"]:
            raise ValueError("Please check the LED you want to control")
        if name == "green":
            GPIO.output(self.green_addr, status)
        elif name == "red":
            GPIO.output(self.red_addr, status)
        elif name == "yellow":
            GPIO.output(self.yellow_addr, status)

    def blink(self, name, delay=2):
        self.set_led(name, 1)
        time.sleep(delay)
        self.set_led(name, 0)

    def off(self):
        GPIO.output(self.yellow_addr, 0)
        GPIO.output(self.red_addr, 0)
        GPIO.output(self.green_addr, 0)


class Ventilator_controller:
    def __init__(self, ventilator_pin):
        self.vent_addr = int(ventilator_pin)
        self.status = 0
        GPIO.setup(self.vent_addr, GPIO.OUT)

    def set_ventilator(self, status):
        """
        Control the ventilator to be opened or closed in the office.
        :param status: 0 - OFF, 1 - ON
        :return: True if successfully set, otherwise False
        """
        if status == 0:
            print("[Actuator] Ventilator is closed")
        elif status == 1:
            print("[Actuator] Ventilator is opened")
        GPIO.output(self.vent_addr, status)

    def stop(self):
        GPIO.output(self.vent_addr, 0)


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
            "body_temp_check" : str(pathlib.Path(__file__).parent.joinpath("sounds", "body_temp_checking.mp3")),
            "come_in_please": str(pathlib.Path(__file__).parent.joinpath("sounds", "come_in_pls.mp3")),
            "sorry_pls_try": str(pathlib.Path(__file__).parent.joinpath("sounds", "sorry_pls_try_again.mp3")),
            "sorry_ur_not_allowed": str(pathlib.Path(__file__).parent.joinpath("sounds", "sry_ur_not_allowed.mp3")),
            "warning": str(pathlib.Path(__file__).parent.joinpath("sounds", "warning.mp3")),
        }
        assert os.path.exists(self.sound_path["sorry_pls_try"]) == True

    def play_sound(self, sound_name):
        """
        play sound of choice
        :param sound_name: str, "body_temp_check", "come_in_please" or "sorry_pls_try"
        :return: None
        """
        os.system("omxplayer "+str(self.sound_path[sound_name]) + " >/dev/null 2>&1")
