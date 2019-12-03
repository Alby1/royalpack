from typing import *
from royalnet.commands import *
from royalnet.serf.discord import *
from royalnet.serf.discord.errors import *
from ..utils import RoyalQueue
import discord


class DiscordSummonEvent(Event):
    name = "discord_summon"

    async def run(self, *,
                  channel_name: str = "",
                  channel_id: Optional[int] = None,
                  guild_id: Optional[int] = None,
                  user_id: Optional[int] = None,
                  **kwargs):
        if not isinstance(self.serf, DiscordSerf):
            raise UnsupportedError()
        # Find the guild
        if guild_id is not None:
            guild: Optional[discord.Guild] = self.serf.client.get_guild(guild_id)
        else:
            guild = None
        # Find the member
        if user_id is not None and guild is not None:
            member: Optional[Union[discord.User, discord.Member]] = guild.get_member(user_id=user_id)
        else:
            member = None
        # From channel id
        if channel_id is not None:
            client: discord.Client = self.serf.client
            channel = client.get_channel(channel_id)
        # Find channel
        elif channel_name != "":
            # Find accessible_to
            accessible_to = [self.serf.client.user]
            if member is not None:
                accessible_to.append(member)
            # Find the channel
            channel: Optional["discord.VoiceChannel"] = self.serf.find_channel(channel_type=discord.VoiceChannel,
                                                                               name=channel_name,
                                                                               guild=guild,
                                                                               accessible_to=accessible_to,
                                                                               required_permissions=["connect", "speak"]
                                                                               )
        elif not (guild_id is None and user_id is None):
            if member.voice is not None:
                channel = member.voice.channel
            else:
                channel = None
        else:
            raise InvalidInputError("Non so a cosa devo connettermi! Specifica il nome di un canale, o entra tu stesso"
                                    " in un canale vocale prima di invocare [c]summon[/c]!")
        if channel is None:
            raise InvalidInputError("Non ho trovato nessun canale in cui connettermi.")
        # Create a new VoicePlayer
        vp = VoicePlayer(loop=self.loop)
        vp.playing = await RoyalQueue.create()
        # Connect to the channel
        try:
            await vp.connect(channel)
        except GuildAlreadyConnectedError:
            raise UserError("Il bot è già connesso in un canale vocale nel Server!\n"
                            "Spostalo manualmente, o disconnettilo e riinvoca [c]summon[/c]!")
        # Add the created VoicePlayer to the list
        self.serf.voice_players.append(vp)
        # Reply to the request
        return {
            "channel": {
                "id": channel.id,
                "name": channel.name,
                "guild": {
                    "name": channel.guild.name,
                },
            }
        }
