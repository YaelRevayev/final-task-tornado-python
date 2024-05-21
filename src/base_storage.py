class BaseStorage:
    def save(self, key, value):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError
