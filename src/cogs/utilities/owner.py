import discord
from discord.ext import commands
from datetime import timedelta, date

from src.exceptions.ban_exception import NoBansFoundError
from src.exceptions.user_exception import UserAlreadyExistsError
from src.services.user_service import UserService
from src.utils.config import BotConfig
from src.utils.embed import DiscordEmbedUtils
from src.services.ban_service import BanService


def is_me():
    def predicate(ctx):
        return ctx.author.id == BotConfig().owner_id

    return commands.check(predicate)


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ban", description="Ban a user permanently or temporarily")
    @is_me()
    async def ban(
            self,
            interaction: discord.Interaction,
            user: discord.User,
            reason: str = "No reason provided",
            duration: int = 0,
    ):
        """
        Ban a user.

        :param interaction: The interaction object.
        :param user: The user to ban.
        :param reason: The reason for the ban.
        :param duration: Duration in days for a temporary ban (0 for permanent ban).
        """
        try:
            if duration > 0:
                # Temporary ban
                end_date = date.today() + timedelta(days=duration)
                ban = await BanService.temporary_ban_user(user_id=user.id, reason=reason, end_date=end_date)

                embed = DiscordEmbedUtils.create_success_embed(
                    "User Temporarily Banned",
                    f"🚫 **User:** {user.mention}\n"
                    f"**Reason:** {reason}\n"
                    f"**Duration:** {duration} days\n"
                    f"**Ends:** {end_date.strftime('%Y-%m-%d')}",
                    user=user
                )
                await interaction.response.send_message(embed=embed)
            else:
                # Permanent ban
                ban = await BanService.ban_user(user_id=user.id, reason=reason)

                embed = DiscordEmbedUtils.create_success_embed(
                    "User Permanently Banned",
                    f"🚫 **User:** {user.mention}\n"
                    f"**Reason:** {reason}\n"
                    f"**Type:** Permanent Ban",
                    user=user
                )
                await interaction.response.send_message(embed=embed)

        except Exception as e:
            error_embed = DiscordEmbedUtils.create_error_embed(
                "Ban Error",
                f"Failed to ban user: {str(e)}",
                error=e
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @discord.app_commands.command(name="unban", description="Unban a user")
    @is_me()
    async def unban(self, interaction: discord.Interaction, user: discord.User):
        """
        Unban a user by deleting their ban records.

        :param interaction: The interaction object.
        :param user: The user to unban.
        """
        try:
            unban = await BanService.unban_user(user_id=user.id)

            success_embed = DiscordEmbedUtils.create_success_embed(
                "User Unbanned",
                f"User {user.mention} has been successfully unbanned.",
                user=user
            )
            await interaction.response.send_message(embed=success_embed)

        except NoBansFoundError as e:
            error_embed = DiscordEmbedUtils.create_error_embed(
                "Unban Failed",
                f"User {user.mention} is not currently banned."
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except Exception as e:
            error_embed = DiscordEmbedUtils.create_error_embed(
                "Unban Error",
                f"Failed to unban user: {str(e)}",
                error=e
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @discord.app_commands.command(name="register_user", description="Register a user in the database")
    @is_me()
    async def register_user(self, interaction: discord.Interaction, user: discord.User):
        """
        Register a user in the database.

        :param interaction: The interaction object.
        :param user: The user to register.
        """
        try:
            new_user = await UserService.create_user(user.id)

            success_embed = DiscordEmbedUtils.create_success_embed(
                "User Registered",
                f"User {user.mention} has been successfully registered.\n"
                f"**Database ID:** `{new_user['id_user']}`",
                user=user
            )
            await interaction.response.send_message(embed=success_embed)

        except UserAlreadyExistsError:
            error_embed = DiscordEmbedUtils.create_error_embed(
                "Registration Failed",
                f"User {user.mention} is already registered in the database."
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except Exception as e:
            error_embed = DiscordEmbedUtils.create_error_embed(
                "Registration Error",
                f"Failed to register user: {str(e)}",
                error=e
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
