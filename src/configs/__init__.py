import yaml
import os


def load_config(config_file):
    print(os.getcwd())
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


config_file = "./src/configs/config.yaml"
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
