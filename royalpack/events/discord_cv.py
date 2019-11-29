import discord
from typing import *
from royalnet.serf.discord.discordserf import DiscordSerf
from royalnet.commands import *


class DiscordCvEvent(Event):
    name = "discord_cv"

    async def run(self, guild_id: Optional[int] = None, **kwargs) -> dict:
        if not self.interface.name == "discord":
            raise UnsupportedError()

        # noinspection PyTypeChecker
        serf: DiscordSerf = self.interface.serf

        client: discord.Client = serf.client

        if guild_id is None:
            guilds: List[discord.Guild] = client.guilds
            if len(guilds) == 0:
                raise ConfigurationError("Il bot non è in nessun Server.")
            elif len(guilds) > 1:
                raise UserError("Non hai specificato di quale Server vuoi vedere le informazioni!")
            else:
                guild = guilds[0]
        else:
            guild: discord.Guild = client.get_guild(guild_id)

        members: List[Union[discord.User, discord.Member]] = guild.members
        channels: List[discord.VoiceChannel] = guild.voice_channels

        results = []

        for member in members:
            data = {
                "id": member.id,
                "name": member.name,
                "discriminator": member.discriminator,
                "nick": member.nick,
                "bot": member.bot,
                "voice": {
                    "channel": {
                        "id": member.voice.channel.id,
                        "name": member.voice.channel.name,
                        "position": member.voice.channel.position,
                        "category": {
                            "id": member.voice.channel.category_id,
                            "name": member.voice.channel.category.name,
                            "position": member.voice.channel.category.position,
                        } if member.voice.channel.category is not None else {
                            "id": None,
                            "name": None,
                            "position": -1,
                        },
                        "bitrate": member.voice.channel.bitrate,
                        "user_limit": member.voice.channel.user_limit,
                    },
                    "server_mute": member.voice.mute,
                    "server_deaf": member.voice.deaf,
                    "self_mute": member.voice.self_mute,
                    "self_deaf": member.voice.self_deaf,
                    "video": member.voice.self_video,
                    "golive": member.voice.self_stream,
                    "afk": member.voice.afk,
                } if member.voice is not None else None,
                "status": {
                    "main": member.status.value,
                    "desktop": member.desktop_status.value,
                    "mobile": member.mobile_status.value,
                    "web": member.web_status.value,
                },
                "activities": [activity.to_dict() for activity in member.activities if activity is not None],
                "roles": [{
                    "id": role.id,
                    "name": role.name,
                    "hoist": role.hoist,
                    "position": role.position,
                    "managed": role.managed,
                    "mentionable": role.mentionable,
                } for role in member.roles]
            }

            results.append(data)

        return {
            "guild": {
                "id": guild.id,
                "name": guild.name,
                "members": results,
            }
        }
