import time

from edge_device_regulate.actuators import LEDs_controller, \
    Ventilator_controller, Door_controller, \
    Heater_controller, Buzzer_controller


leds_control = LEDs_controller()
leds_control.set_led("green", 1)

ventilator_control = Ventilator_controller()
ventilator_control.set_ventilator(1)
time.sleep(2)
ventilator_control.set_ventilator(0)

buzzer = Buzzer_controller()
buzzer.play_sound("sorry_pls_try")