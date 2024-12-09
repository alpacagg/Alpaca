from datetime import date

from src.database.models import Ban, TemporaryBan


class BanRepository:
    """Repository for Ban-related database operations."""

    @staticmethod
    async def create_ban(user_id: int, reason: str):
        """
        Create a ban for a user.

        :param user_id: ID of the user.
        :param reason: Reason for the ban.
        :return: The created Ban object.
        """
        ban = await Ban.create(user_id=user_id, created_at=date.today(), reason=reason)
        return ban  # Return the Ban instance

    @staticmethod
    async def create_temporary_ban(ban_id: int, end_date: date):
        """
        Create a temporary ban for a user.

        :param ban_id: ID of the ban.
        :param end_date: End date of the temporary ban.
        :return: The created TemporaryBan object.
        """
        temp_ban = await TemporaryBan.create(id_temporary_ban=ban_id, end_date=end_date)
        return temp_ban  # Return the TemporaryBan instance

    @staticmethod
    async def get_bans_by_user(user_id: int):
        """
        Fetch all bans associated with a user.

        :param user_id: ID of the user.
        :return: A list of Ban objects.
        """
        return await Ban.filter(user_id=user_id).all()

    @staticmethod
    async def delete_ban(ban_id: int):
        """
        Delete a ban by its ID.

        :param ban_id: ID of the ban to delete.
        """
        await Ban.filter(id_ban=ban_id).delete()
