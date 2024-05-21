import redis
import configs as config
from base_storage import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self):
        self.client = redis.StrictRedis(
            host=config.REDIS_HOST_IP,
            port=config.REDIS_HOST_PORT,
            db=0,
            socket_keepalive=True,
            retry_on_timeout=True,
        )

    def save(self, key: str, value: str):
        self.client.set(key, value, ex=config.EXPIRY_SECONDS)

    def exists(self, key: str):
        return self.client.exists(key)

    def get(self, key: str):
        return self.client.get(key).decode("utf-8")
