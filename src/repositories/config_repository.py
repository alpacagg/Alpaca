from threading import Lock


class ConfigRepository:
    _instance = None
    _lock = Lock()

    def __init__(self):
        """
        Initializes the ConfigRepository.

        This class is a singleton! Use 'get_instance()' to access it.

        :raises Exception: If the ConfigRepository has already been initialized.
        """
        if ConfigRepository._instance is not None:
            raise Exception("This class is a singleton! Use 'get_instance()' to access it.")
        self._owner_id = None
        self._owner_id = None

    @classmethod
    def get_instance(cls) -> 'ConfigRepository':
        """
        Gets the single instance of the ConfigRepository.

        This method ensures thread safety via double-checked locking.

        :return: The single instance of the ConfigRepository.
        :rtype: ConfigRepository
        """
        if cls._instance is None:
            with cls._lock:  # Double-checked locking for thread safety
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def get_owner(self) -> int:
        """
        Gets the ID of the bot owner.

        :return: The ID of the bot owner.
        :rtype: int
        """
        return self._owner_id

    def set_owner(self, owner_id: int) -> None:
        """
        Sets the ID of the bot owner.

        :param owner_id: The ID of the bot owner.
        :type owner_id: int
        """
        self._owner_id = owner_id