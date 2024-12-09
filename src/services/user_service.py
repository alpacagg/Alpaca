from src.database.repositories.user_repository import UserRepository
from src.exceptions.user_exception import UserAlreadyExistsError, UserNotFoundError
from typing import Optional


class UserService:
    @staticmethod
    async def create_user(user_id: int) -> dict:
        """
        Create a new user in the database.

        :param user_id: Discord user ID
        :return: Created user details
        :raises UserAlreadyExistsError: If user already exists
        """
        # Check if user already exists
        if await UserRepository.user_exists(user_id):
            raise UserAlreadyExistsError(f"User with ID {user_id} already exists")

        # Create user
        new_user = await UserRepository.create_user(user_id)
        return {
            "id_user": new_user.id_user,
            "created_at": new_user.created_at
        }

    @staticmethod
    async def get_user(user_id: int):
        """
        Retrieve a user by their ID.

        :param user_id: Discord user ID
        :return: User details
        :raises UserNotFoundError: If user is not found
        """
        try:
            return await UserRepository.get_user(user_id)
        except Exception:
            raise UserNotFoundError(f"User with ID {user_id} not found")

    @staticmethod
    async def user_exists(user_id: int) -> bool:
        """
        Check if a user exists in the database.

        :param user_id: Discord user ID
        :return: Boolean indicating user existence
        """
        return await UserRepository.user_exists(user_id)