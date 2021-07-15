import time
import configparser
from edge_device_regulate.actuators import LEDs_controller, \
    Ventilator_controller, Buzzer_controller


config = configparser.ConfigParser()
config.read("config.ini")

leds_control = LEDs_controller(red_address=config["Actuators"]["LED_red_pin"],
                               green_address=config["Actuators"]["LED_green_pin"],
                               yellow_address=config["Actuators"]["LED_yellow_pin"])
leds_control.set_led("green", 0)
leds_control.set_led("red", 1)


ventilator_control = Ventilator_controller(
    ventilator_pin=config["Actuators"]["ventilator_pin"])
ventilator_control.set_ventilator(0)

buzzer = Buzzer_controller()
buzzer.play_sound("sorry_pls_try")
