import gin

CLOSED = 0
OPEN = 1


@gin.configurable
class LEDs_controller:
    """
    To-Do:
        Define the GPIO in configs/configs.gin
    """

    def __init__(self, red_address, green_address, yellow_address):
        self.red_addr = red_address
        self.green_addr = green_address
        self.yellow_addr = yellow_address
        self.red_status = CLOSED
        self.green_status = CLOSED
        self.yellow_status = CLOSED

    def set_led(self, name, status):
        """
        set the LED status
        :param   name:      name of the LED to set,
        :param   status:    0 - OFF, 1 - ON
        :return: boolean    True if successfully set, otherwise False
        :exception:         turn on the LED when it is on,
                            or turn off the LED when it is off
        """
        if name not in ["green", "red", "yellow"]:
            raise ValueError("Please check the LED you want to control")
        if name == "green":
            pass
        elif name == "red":
            pass
        elif name == "yellow":
            pass


class Door_controller:

    def __init__(self):
        self.status = CLOSED

    def set_door(self, status):
        """
        Control the door to be opened or closed at the entrance
        :param status: 0 - OFF, 1 - ON
        :return: True if successfully set, otherwise False
        :exception: open the gate when it is opened,
                    or closed the door when it is close
        """
        pass


class heater_controller:
    def __init__(self):
        self.valve_opening = 0

    def set_valve(self, opening):
        self.valve_opening = opening


@gin.configurable
class buzzer_controller:
    def __init__(self, *sounds_path):
        pass

    def display_sound(self, sound_name):
        pass