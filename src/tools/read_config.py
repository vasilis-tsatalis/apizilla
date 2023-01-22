# Configuration file reader
import yaml
from decouple import config

def read_configuration():

    file_fullanme = f"{config('CONFIG_FILE')}"

    with open(file_fullanme, 'r') as stream:
        config_routes = yaml.safe_load(stream)

    return config_routes
