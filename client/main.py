#!/usr/bin/env python3
import datetime
import sys
from configparser import ConfigParser
from time import sleep

from src.client import Client
import logging
import os


def convert_time_to_seconds(time_str):
    time_str = time_str.strip('"')
    minutes, seconds = time_str.split('m')
    seconds = seconds.rstrip('s')
    return int(minutes) * 60 + int(seconds)


def initialize_config():
    """ Parse env variables or config file to find program config params

    Function that search and parse program configuration parameters in the
    program environment variables first and the in a config file. 
    If at least one of the config parameters is not found a KeyError exception 
    is thrown. If a parameter could not be parsed, a ValueError is thrown. 
    If parsing succeeded, the function returns a ConfigParser object 
    with config parameters
    """

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("config/config.ini")

    config_params = {}
    try:
        config_params["server_address"] = os.getenv('SERVER_ADDRESS', config["DEFAULT"]["SERVER_ADDRESS"])
        config_params["query_address"] = os.getenv('QUERY_ADDRESS', config["DEFAULT"]["QUERY_ADDRESS"])
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params

def main():
    config_params = initialize_config()
    logging_level = config_params["logging_level"]
    server_address = config_params["server_address"]
    query_address = config_params["query_address"]
    initialize_log(logging_level)

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug(f"action: config | result: success | "
                  f"server_address: {server_address} | log_level: {logging_level}")

    sleep(20)

    # Initialize client
    client = Client(server_address, query_address)
    client.run()
    sys.exit(0)

def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )


if __name__ == "__main__":
    main()
