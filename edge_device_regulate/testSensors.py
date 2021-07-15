from sensors import SensorReader

sr = SensorReader()

print("# ----- Test body temperature sensor -------")
print(str(sr.get_body_temperature()))

print("# --- Test env temperature and humidity ----")
sr.get_environment_temperature_and_humidity()

print("# ------- Test env brightness sensor -------")
sr.get_environment_brightness()

print("# ------ Test movement detect sensor -------")
sr.detect_movement_entrance()