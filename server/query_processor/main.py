#!/usr/bin/env python3
import signal
import sys
import traceback
from configparser import ConfigParser
from time import sleep

from src.rabbit_initializer import RabbitInitializer
from src.query_processor import QueryProcessor
import logging
import os



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
        pass
        #config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params

def sigterm_handler(signum, frame):
    # Clean up any resources and exit with code 0
    sys.exit(0)

def main():
    signal.signal(signal.SIGTERM, sigterm_handler)
    config_params = initialize_config()
    logging_level = "INFO"#config_params["logging_level"]

    initialize_log(logging_level)

    logging.debug(f"action: config | result: success | "
                  f"logging_level: {logging_level}")

    sleep(10)


    rabbit_initializer = RabbitInitializer()
    channel = rabbit_initializer.get_channel()
    port = 12350
    try:
        process = QueryProcessor(port, channel)
        process.run()
    except Exception as _e:
        logging.info(traceback.format_exc())
    finally:
        channel.close()
        sys.exit(0)

def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='[%(process)d] %(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )


if __name__ == "__main__":
    main()
