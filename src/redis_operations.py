import redis
from configs import config
from base_storage import AbstractBaseStorage


class RedisStorage(AbstractBaseStorage):
    def __init__(self):
        self.client = redis.StrictRedis(
            host=config.REDIS_HOST_IP,
            port=config.REDIS_HOST_PORT,
            db=0,
            socket_keepalive=True,
            retry_on_timeout=True,
        )

    def save(self, key: str, value: str) -> bool:
        result = self.client.set(key, value, nx=True, ex=config.REDIS_KEY_EXPIRATION)
        return result

    def exists(self, key: str):
        return self.client.exists(key)

    def get(self, key: str):
        return self.client.get(key).decode("utf-8")
