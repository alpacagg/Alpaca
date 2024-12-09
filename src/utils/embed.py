import discord
import traceback
from typing import Optional


class DiscordEmbedUtils:
    """
    Utility class for creating standardized Discord embeds.
    Provides methods for creating success, error, and informational embeds.
    """

    @staticmethod
    def create_error_embed(
            title: str,
            description: str,
            error: Optional[Exception] = None
    ) -> discord.Embed:
        """
        Create a standardized error embed.

        :param title: Title of the error embed
        :param description: Description of the error
        :param error: Optional exception to include in the trace
        :return: Discord Embed object
        """
        embed = discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=discord.Color.red()
        )

        if error:
            # Include error trace if an exception is provided
            trace = traceback.format_exc()
            if len(trace) > 1000:
                trace = trace[-1000:]  # Truncate very long traces

            embed.add_field(
                name="Error Details",
                value=f"```\n{trace}\n```",
                inline=False
            )

        return embed

    @staticmethod
    def create_success_embed(
            title: str,
            description: str,
            user: Optional[discord.User] = None
    ) -> discord.Embed:
        """
        Create a standardized success embed.

        :param title: Title of the success embed
        :param description: Description of the successful action
        :param user: Optional user to set thumbnail
        :return: Discord Embed object
        """
        embed = discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=discord.Color.green()
        )

        if user:
            embed.set_thumbnail(url=user.display_avatar.url)

        return embed

    @staticmethod
    def create_info_embed(
            title: str,
            description: str,
            color: discord.Color = discord.Color.blue()
    ) -> discord.Embed:
        """
        Create a standardized informational embed.

        :param title: Title of the info embed
        :param description: Description of the information
        :param color: Optional color for the embed (defaults to blue)
        :return: Discord Embed object
        """
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=color
        )

        return embed