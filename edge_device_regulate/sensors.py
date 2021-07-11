from random import uniform


def get_body_temperature():
    """
    Get body temperature by using normal temperature sensor
    :return: temperature    temperature of body
    """
    pass


def get_environment_temperature_and_humidity():
    """
    Get environment temperature and humidity by using DHT sensor
    :return: [temperature, humidity]
    """
    return [uniform(24, 26), uniform(20, 30)]


def get_weather_report(place):
    """
    Get local climate information from the weather report
    :param place: the place where you want to gather climate information
    :return: temperature of target place
    :exception: if the place not exists
    """
    pass


def get_environment_lightness():
    """
    Get environment lightness by using LDR sensor
    :return: lightness      lightness of the environment
    """
    return uniform(30, 40)


def detect_movement():
    """
    Detect object movement by using IR sensor
    :return: False/True
    """
    return True

