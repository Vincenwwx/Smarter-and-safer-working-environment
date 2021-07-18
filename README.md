# Smart Cities and Internet of Things
Practicals  2021
## Subject

_Smarter and Safer Working Environment_

## Group members:
- Wenxin Wang
- Aswathi Rajendran
- Minh Huy Le

## Usage
### Data gateway
Run the following command on the raspberry Pi that is used for data collection and publishment: 

_python3 main.py --mode="edge"_

Before running, please configure the mqtt broker server in _config.ini_

### Decision maker
Run the following command on the raspberry Pi that is used for data subscription and AI planning:

_python3 main.py --mode="decision"_

Before running, please configure the mqtt broker server in _config.ini_

### MQTT Broker
In this project we build our broker using [mosquitto mqtt server](https://mosquitto.org/download/)

Attention: After installation, the mqtt server should be configured to allow **remote access** and
the **authentication** method should also be specified.
