import os
from dataclasses import dataclass


@dataclass
class BotConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BotConfig, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self.owner_id = int(os.getenv('OWNER_ID', 0))
        self.token = os.getenv('DISCORD_BOT_TOKEN', '')


    def validate(self):
        """Validate critical configuration parameters"""
        if not self.token:
            raise ValueError("Discord bot token is not configured")
        if not self.owner_id:
            raise ValueError("Owner ID is not configured")