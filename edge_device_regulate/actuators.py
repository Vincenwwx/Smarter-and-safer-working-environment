import gin
import RPi.GPIO as GPIO

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
        self.red_status = 0
        self.green_status = 0
        self.yellow_status = 0

    
    def config_led(self): # Config pins as output. Required in initialization
        GPIO.setup(self.red_addr, GPIO.OUT)
        GPIO.setup(self.green_addr, GPIO.OUT)
        GPIO.setup(self.yellow_addr, GPIO.OUT)


    def set_led(self, name, status):
        """
        set the LED status
        :param   name:      name of the LED to set,
        :param   status:    0 - False, 1 - True
        :return: boolean    True if successfully set, otherwise False
        :exception:         turn on the LED when it is on,
                            or turn off the LED when it is off
        """
        if name not in ["green", "red", "yellow"]:
            raise ValueError("Please check the LED you want to control")
        if name == "green":
            GPIO.output(self.green_addr,status)
            print("Set green LED " + str(status))
            pass
        elif name == "red":
            GPIO.output(self.red_addr,status)
            print("Set red LED " + str(status))
            pass
        elif name == "yellow":
            GPIO.output(self.yellow_addr,status)
            print("Set yellow LED " + str(status))
            pass

@gin.configurable
class ventilator_controller:

    def __init__(self, vent_address):
        self.vent_addr = vent_address
        self.status = False
    
    def config_ventilator(self): # Config pins as output. Required in initialization
        GPIO.setup(self.vent_addr, GPIO.OUT) #Relay control pin

    def set_ventilator(self, status):
        """
        Control the ventilator to be opened or closed at the entrance. No physical output.
        :param status: 0 - False, 1 - True
        :return: True if successfully set, otherwise False
        """
        GPIO.output(self.vent_addr,status)
        print("Set ventilator " + str(status))
        pass

class door_controller:

    def __init__(self):
        self.status = False

    def set_door(self, status):
        """
        Control the door to be opened or closed at the entrance. No physical output.
        :param status: 0 - False, 1 - True
        :return: True if successfully set, otherwise False
        :exception: open the gate when it is opened,
                    or closed the door when it is close
        """
        if status == False:
            print("Door is closed")
        elif status == True:
            print("Door is opened")
        pass


class heater_controller:
    def __init__(self):
        self.valve_opening = 0

    def set_valve(self, status):
        """
        Control the heater valve to be opened or closed. No physical output.
        :param status: 0 - False, 1 - True
        :return: True if successfully set, otherwise False
        :exception: open the gate when it is opened,
                    or closed the door when it is close
        """
        if status == False:
            print("Valve is closed")
        elif status == True:
            print("Valve is opened")
        pass


@gin.configurable
class buzzer_controller:
    """
    To-Do:
        Define function and path to play buzzer sound
    """
    def __init__(self, sounds_path):
        pass

    def display_sound(self, sound_name):
        pass