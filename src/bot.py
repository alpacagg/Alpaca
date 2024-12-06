import sys
import discord

from discord import Intents
from typing import Any
from utils.logging import Logger

class AlpacaBot(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any):
        super().__init__(intents=intents, **options)
        self._log = Logger(name='Client')

    async def on_ready(self):
        """Logs bot startup and connection details."""
        self._log.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        self._log.info(f"Connected to {len(self.guilds)} guilds")

    async def on_error(self, event: str, *args, **kwargs):
        """Logs errors with detailed traceback."""
        self._log.error(f"Error in event {event}", exc_info=sys.exc_info())

    async def on_guild_join(self, guild: discord.Guild):
        """Logs when bot joins a new guild."""
        self._log.info(f"Joined new guild: {guild.name} (ID: {guild.id})")

    async def on_guild_remove(self, guild: discord.Guild):
        """Logs when bot is removed from a guild."""
        self._log.info(f"Removed from guild: {guild.name} (ID: {guild.id})")
