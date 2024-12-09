import sys

import dotenv
from discord import Intents

from src.bot import AlpacaBot
from src.utils.config import BotConfig


def main():
    """Initialize and run the Discord bot."""
    # Load environment variables
    dotenv.load_dotenv()

    # Get config instance
    config = BotConfig()

    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    # Configure intents
    intents = Intents.default()

    # Initialize and run bot
    try:
        bot = AlpacaBot(intents=intents, command_prefix="a!")
        bot.run(config.token)
    except Exception as e:
        print(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()