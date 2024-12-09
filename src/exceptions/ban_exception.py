class BanException(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"Exception: {self.message}"


class NoBansFoundError(BanException):
    pass