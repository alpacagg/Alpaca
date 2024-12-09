from datetime import date
from typing_extensions import Optional
from src.database.repositories.ban_repository import BanRepository
from src.exceptions.bans_exception import NoBansFoundError


class BanService:
    @staticmethod
    async def get_bans_by_user(user_id: int):
        return await BanRepository.get_bans_by_user(user_id)

    @staticmethod
    async def ban_user(user_id: int, reason: Optional[str]):
        return await BanRepository.create_ban(user_id, reason)

    @staticmethod
    async def temporary_ban_user(user_id: int, reason: Optional[str], end_date: date):
        ban = await BanRepository.create_ban(user_id, reason)
        return await BanRepository.create_temporary_ban(ban.ban_id, end_date)

    @staticmethod
    async def unban_user(user_id: int):
        bans = await BanService.get_bans_by_user(user_id)
        if not bans:
            raise NoBansFoundError("No bans found for the user", 404)
        for ban in bans:
            await BanRepository.delete_ban(ban.id_ban)
