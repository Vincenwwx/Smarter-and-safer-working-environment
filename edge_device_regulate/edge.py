import multiprocessing as mp
import paho.mqtt.client as mqtt
import time
import json
from actuators import LEDs_controller, Buzzer_controller, \
    Ventilator_controller, Door_controller


class Edge(mp.Process):
    """
    Create a process which is only responsible for sending measurement
    at the entrance or inside the office
    """
    def __init__(self, place, mqtt_client_id, configuration, sensor_readers):
        super(Edge, self).__init__()
        self.client_id = mqtt_client_id
        self.client = None
        self.config = configuration
        self.sensor_reader = sensor_readers
        self.place = place

        if place == "entrance":
            self.task = self.send_entrance_measurement
            self.mqtt_pub = self.config["MQTT"]["topic_raw_data_entrance"]
            self.delay = 3

        elif place == "office":
            self.task = self.send_env_measurement
            self.mqtt_pub = self.config["MQTT"]["topic_raw_data_environment"]
            self.delay = 10

        elif place == "executor":
            """
            Actuators
            """
            self.leds_control = LEDs_controller(red_address=self.config["Actuators"]["LED_red_pin"],
                                                green_address=self.config["Actuators"]["LED_green_pin"],
                                                yellow_address=self.config["Actuators"]["LED_yellow_pin"])
            self.ventilator_control = Ventilator_controller(
                ventilator_pin=self.config["Actuators"]["ventilator_pin"])
            self.buzzer_control = Buzzer_controller()
            self.door_control = Door_controller()

        else:
            print("Please specify a valid place. Exit...")
            exit(0)

        self.init_mqtt()

    def init_mqtt(self):
        self.client = mqtt.Client(self.client_id)
        self.client.on_publish = self.on_publish
        self.client.username_pw_set(username="sciot", password="sciot_g6")
        if self.place == "executor":
            self.client.on_message = self.on_new_plan
        self.client.connect(self.config["MQTT"]["server"])
        print("MQTT Client {} registered successfully!".format(self.client_id))

    def run(self) -> None:
        # Start mqtt loop
        self.client.loop_start()
        if self.place == "executor":
            self.client.subscribe(self.config["MQTT"]["topic_plan"])
        else:
            while True:
                self.task()
                time.sleep(self.delay)

    def _publish(magic):
        """
        This is the definition of the decorator that publish data that the function
        it is decorating to the broker
        """
        def wrapper(self, *args, **kwargs):
            data = magic(self, *args, **kwargs)
            QoS = 2     # set the Qos here
            self.client.publish(self.mqtt_pub, data, QoS)
            return data
        return wrapper

    @_publish
    def send_env_measurement(self):
        print("Sending $ ENVIRONMENT $ measurement...")
        temperature, humidity = self.sensor_reader.get_environment_temperature_and_humidity()
        lightness = self.sensor_reader.get_environment_brightness()
        measurement = json.dumps({
            "temperature": temperature,
            "humidity": humidity,
            "lightness": lightness
        })
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("")
        return measurement

    @_publish
    def send_entrance_measurement(self):
        print("Sending # ENTRANCE # measurement...")
        people_enter = self.sensor_reader.detect_movement_entrance()
        people_at_gate = self.sensor_reader.detect_presence_at_gate()
        body_temperature = self.sensor_reader.get_body_temperature()
        measurement = json.dumps({
            "people_enter": people_enter,
            "people_at_gate": people_at_gate,
            "body_temperature": body_temperature
        })
        print("====================================================")
        print("")
        return measurement

    # ------------------- Callback functions ----------------------
    # display all outgoing messages
    @staticmethod
    def on_publish(client, userdata, mid):
        print(" > published message: {}".format(mid))

    def on_new_plan(self, client, userdata, message):

        payload = message.payload.decode("utf-8")
        print(" < received plan " + payload)

        # Office
        if "switchon_humidifier" in payload:
            print("[Actuator] Humidifier is turned on")
        elif "switchoff_humidifier" in payload:
            print("[Actuator] Humidifier is turned off")
        elif "switchon_light" in payload:
            self.leds_control.set_led("yellow", 1)
        elif "switchoff_light" in payload:
            self.leds_control.set_led("yellow", 0)
        elif "switchon_fan" in payload:
            self.ventilator_control.set_ventilator(1)
        elif "switchoff_fan" in payload:
            self.ventilator_control.set_ventilator(0)
        # Entrance
        elif "switchon_greenled_buzzer" in payload:
            self.buzzer_control.play_sound("come_in_please")
            self.leds_control.blink("green")
            self.door_control.set_door(1)
        elif "switchon_redled_buzzer" in payload:
            self.buzzer_control.play_sound("sorry_pls_try")
            self.leds_control.blink("red")
        elif "switchoff_greenled_redled_buzzer" in payload:
            pass
        # Unrecognized plans
        else:
            print("Unrecognized plan, please check!")
            raise
