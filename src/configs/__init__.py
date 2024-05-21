import os
import yaml
from dataclasses import dataclass


@dataclass
class AppConfig:
    HAPROXY_SERVER_IP: str
    HAPROXY_SERVER_PORT: int
    REDIS_HOST_IP: str
    REDIS_HOST_PORT: int
    DIRECTORY_TO_WATCH: str
    FILES_FOLDER_NAME: str
    LOGS_FOLDER_NAME: str
    EXPIRY_SECONDS: int
    SCRIPT_PATH: str
    STORAGE_TYPE: str


def load_config(config_file):
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    os.chdir(project_dir)
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return AppConfig(
        HAPROXY_SERVER_IP=config["HAPROXY_SERVER_IP"],
        HAPROXY_SERVER_PORT=config["HAPROXY_SERVER_PORT"],
        REDIS_HOST_IP=config["REDIS_HOST_IP"],
        REDIS_HOST_PORT=config["REDIS_HOST_PORT"],
        DIRECTORY_TO_WATCH=config["DIRECTORY_TO_WATCH"],
        FILES_FOLDER_NAME=config["FILES_FOLDER_NAME"],
        LOGS_FOLDER_NAME=config["LOGS_FOLDER_NAME"],
        EXPIRY_SECONDS=config["EXPIRY_SECONDS"],
        SCRIPT_PATH=config["SCRIPT_PATH"],
        STORAGE_TYPE=config["STORAGE_TYPE"],
    )


config_file = "../configs/config.yaml"
config = load_config(config_file)
