from abc import ABC, abstractmethod


class AbstractBaseStorage(ABC):
    @abstractmethod
    def save(self, key, value):
        """Save the value associated with the given key."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, key):
        """Check if the given key exists in the storage."""
        raise NotImplementedError

    @abstractmethod
    def get(self, key):
        """Retrieve the value associated with the given key."""
        raise NotImplementedError
