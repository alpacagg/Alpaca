from src.database.models import User


class UserRepository:
    """Repository for User-related database operations."""

    @staticmethod
    async def create_user(user_id: int):
        """
        Add a user to the User table.

        :param user_id: ID of the user.
        :return: The created User object.
        """
        user = await User.create(id_user=user_id)
        return user

    @staticmethod
    async def get_user(user_id: int) -> User:
        """
        Fetch a user by their ID.

        :param user_id: ID of the user.
        :return: The User object.
        """
        return await User.get(id_user=user_id)

    @staticmethod
    async def user_exists(user_id: int) -> bool:
        """
        Check if a user exists in the User table.

        :param user_id: ID of the user.
        :return: True if the user exists, False otherwise
        """
        return await User.filter(id_user=user_id).exists()