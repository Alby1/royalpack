import discord
from typing import *
from royalnet.serf.discord.discordserf import DiscordSerf
from royalnet.commands import *


class DiscordCvEvent(Event):
    name = "discord_cv"

    def run(self, guild_id: int, **kwargs):
        if not self.interface.name == "discord":
            raise UnsupportedError()
        serf: DiscordSerf = self.interface.serf
        client: discord.Client = serf.client
        guild: discord.Guild = client.get_guild(guild_id)
        members: List[discord.Member] = guild.members
        ...
