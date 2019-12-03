import discord
from royalnet.commands import *


class SummonCommand(Command):
    name: str = "summon"

    aliases = ["cv"]

    description: str = "Evoca il bot in un canale vocale."

    syntax: str = "[nomecanale]"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        channel_name = args.joined()
        if self.interface.name == "discord":
            message: discord.Message = data.message
            guild_id = message.guild.id
            user_id = message.author.id
        else:
            guild_id = None
            user_id = None
        response = await self.interface.call_herald_event("discord", "discord_summon",
                                                          channel_name=channel_name, guild_id=guild_id, user_id=user_id)
        if self.interface.name == "discord":
            await data.reply(f"✅ Mi sono connesso in <#{response['channel']['id']}>!")
        else:
            await data.reply(f"✅ Mi sono connesso in [b]#{response['channel']['name']}[/b]!")
