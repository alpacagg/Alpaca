class UserException(Exception):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"Exception: {self.message}"

class UserAlreadyExistsError(UserException):
    """Raised when attempting to create a user that already exists"""
    pass

class UserNotFoundError(UserException):
    """Raised when a user cannot be found"""
    pass