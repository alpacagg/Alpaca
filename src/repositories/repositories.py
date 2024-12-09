from threading import Lock
from src.repositories.config_repository import ConfigRepository

class Repositories:
    _instance = None
    _lock = Lock()  # For thread-safe singleton implementation

    def __init__(self):
        """
        Initialize the singleton instance of the repositories.

        :raises: Exception if the instance already exists.
        """
        if Repositories._instance is not None:
            raise Exception("This class is a singleton! Use 'get_instance()' to access it.")
        self.config_repository = ConfigRepository().get_instance()

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the repositories.

        This method uses double-checked locking to ensure that the instance is
        created only once and is thread-safe.

        :return: The singleton instance of the repositories.
        :rtype: Repositories
        """
        if cls._instance is None:
            with cls._lock:  # Double-checked locking for thread safety
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def get_config_repository(self):
        """
        Retrieve the singleton instance of the ConfigRepository.

        :return: The ConfigRepository instance
        :rtype: ConfigRepository
        """
        return self.config_repository

