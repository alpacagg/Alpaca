import os
import sys
import discord

from discord import Intents
from discord.ext.commands import Bot
from typing import Any, Optional, List
from utils.logging import Logger

class AlpacaBot(Bot):
    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self._log = Logger(name='Client')
        self.cogs_dir = 'src/cogs'

    async def on_ready(self):
        """Logs bot startup and connection details."""
        self._log.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        self._log.info(f"Connected to {len(self.guilds)} guilds")
        await self.tree.sync()

    async def on_error(self, event: str, *args, **kwargs):
        """Logs errors with detailed traceback."""
        self._log.error(f"Error in event {event}", exc_info=sys.exc_info())

    async def on_guild_join(self, guild: discord.Guild):
        """Logs when bot joins a new guild."""
        self._log.info(f"Joined new guild: {guild.name} (ID: {guild.id})")

    async def on_guild_remove(self, guild: discord.Guild):
        """Logs when bot is removed from a guild."""
        self._log.info(f"Removed from guild: {guild.name} (ID: {guild.id})")

    async def _load_extensions(self, cogs_dir: Optional[str] = None) -> List[str]:
        """
        Dynamically load all cogs from a specified directory, supporting nested folders.

        Args:
            cogs_dir (Optional[str]): Directory containing cog files.
                                      Uses default if not specified.

        Returns:
            List[str]: List of successfully loaded cog names
        """
        cogs_dir = cogs_dir or self.cogs_dir
        loaded_cogs = []
        failed_cogs = []

        # Ensure the cogs directory exists
        if not os.path.exists(cogs_dir):
            self._log.warning(f"Cogs directory '{cogs_dir}' does not exist.")
            return loaded_cogs

        # Walk through all directories and files
        for root, dirs, files in os.walk(cogs_dir):
            for filename in files:
                # Check for Python files, excluding __init__ and hidden files
                if filename.endswith('.py') and not filename.startswith('_'):
                    # Calculate the full path and module path
                    full_path = os.path.join(root, filename)

                    # Create module path, replacing path separators with dots
                    # Remove the base cogs_dir from the path and convert to module notation
                    relative_path = os.path.relpath(full_path, start=cogs_dir)
                    module_path = os.path.splitext(relative_path)[0].replace(os.path.sep, '.')
                    cog_path = f"{cogs_dir.replace('/', '.')}.{module_path}"
                    cog_path = cog_path[4:]

                    try:
                        # Load the extension
                        await self.load_extension(cog_path)
                        loaded_cogs.append(module_path)
                        self._log.info(f"Loaded extension: {module_path}")
                    except Exception as e:
                        failed_cogs.append(module_path)
                        self._log.error(f"Failed to load extension {module_path}: {e}",
                                        exc_info=sys.exc_info())

        # Log summary of cogs loading
        self._log.info(f"Loaded {len(loaded_cogs)}/{len(loaded_cogs) + len(failed_cogs)} cogs")

        return loaded_cogs

    async def setup_hook(self):
        """
        Async setup method called when the bot starts.
        Used for loading extensions and any initial setup.
        """
        # Load all cogs
        await self._load_extensions()
