import configparser
import pathlib

config = configparser.ConfigParser()
config.read(pathlib.Path(__file__).parents[1].joinpath("config.ini").as_uri())
print(pathlib.Path(__file__).parents[1].joinpath("config.ini").as_uri())