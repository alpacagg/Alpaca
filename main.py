import os
import sys

import dotenv
from discord import Intents

from src.bot import AlpacaBot
from src.repositories.repositories import Repositories


def main():
    """Initialize and run the Discord bot."""
    # Load environment variables
    dotenv.load_dotenv()

    # Get bot token from environment
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("Error: DISCORD_BOT_TOKEN not found in .env file")
        sys.exit(1)

    # Get owner id from environment
    owner_id = os.getenv('OWNER_ID')
    if not owner_id:
        print("Error: OWNER_ID not found in .env file")
        sys.exit(1)

    # Initialize repositories
    Repositories.get_instance().get_config_repository().set_owner(int(owner_id))

    # Configure intents
    intents = Intents.default()

    # Initialize and run bot
    try:
        bot = AlpacaBot(intents=intents, command_prefix="a!")
        bot.run(token)
    except Exception as e:
        print(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()