# cogs/ping.py
from discord.ext import commands
import discord
import time


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="ping", description="Check the bot's latency")
    async def ping_slash(self, interaction: discord.Interaction):
        """
        Slash command to check bot latency.

        Responds with:
        - Websocket latency
        - Bot's message response time
        """
        # Record start time
        start_time = time.time()

        # Defer the response to give time for latency calculation
        await interaction.response.defer(ephemeral=True)

        # Calculate latencies
        websocket_latency = round(self.bot.latency * 1000, 2)
        message_latency = round((time.time() - start_time) * 1000, 2)

        # Send the detailed latency information
        await interaction.followup.send(content=f"""
**🏓 Pong!**
- Websocket Latency: `{websocket_latency}ms`
- Message Latency: `{message_latency}ms`
        """.strip(), ephemeral=True)


async def setup(bot):
    await bot.add_cog(PingCog(bot))