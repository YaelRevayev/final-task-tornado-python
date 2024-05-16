import yaml
import os
import sys


def load_config(config_file):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    os.chdir(project_dir)
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


config_file = "configs/config.yaml"
config = load_config(config_file)


HAPROXY_SERVER_IP = config["HAPROXY_SERVER_IP"]
HAPROXY_SERVER_PORT = config["HAPROXY_SERVER_PORT"]
REDIS_HOST_IP = config["REDIS_HOST_IP"]
REDIS_HOST_PORT = config["REDIS_HOST_PORT"]
DIRECTORY_TO_WATCH = config["DIRECTORY_TO_WATCH"]
FILES_FOLDER_NAME = config["FILES_FOLDER_NAME"]
LOGS_FOLDER_NAME = config["LOGS_FOLDER_NAME"]
EXPIRY_SECONDS = config["EXPIRY_SECONDS"]
SCRIPT_PATH = config["SCRIPT_PATH"]
