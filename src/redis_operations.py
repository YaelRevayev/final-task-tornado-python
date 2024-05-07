import redis
import os
import sys

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
config_dir = os.path.join(project_dir, "config")

sys.path.append(project_dir)
sys.path.insert(0, config_dir)
import configs.config as config

redis_client = redis.StrictRedis(
    host=config.REDIS_HOST_IP, port=config.REDIS_HOST_PORT, db=0
)


def save_to_redis(key, value):
    redis_client.set(key, value, ex=config.EXPIRY_SECONDS)
    redis_client.expire(key, config.EXPIRY_SECONDS)


def does_key_exists(full_file_name):
    return redis_client.exists(full_file_name)


def get_value_by_key(full_file_name):
    return redis_client.get(full_file_name).decode("utf-8")
