import discord
from typing import *
from royalnet.commands import *
from royalnet.serf.discord import *


class DiscordSkipEvent(Event):
    name = "discord_skip"

    async def run(self,
                  guild_id: Optional[int] = None,
                  **kwargs) -> dict:
        if not isinstance(self.serf, DiscordSerf):
            raise UnsupportedError()
        client: discord.Client = self.serf.client
        if len(self.serf.voice_players) == 1:
            voice_player: VoicePlayer = self.serf.voice_players[0]
        else:
            if guild_id is None:
                # TODO: trovare un modo per riprodurre canzoni su più server da Telegram
                raise InvalidInputError("Non so in che Server riprodurre questo file...\n"
                                        "Invia il comando su Discord, per favore!")
            guild: discord.Guild = client.get_guild(guild_id)
            if guild is None:
                raise InvalidInputError("Impossibile trovare il Server specificato.")
            voice_player: VoicePlayer = self.serf.find_voice_player(guild)
            if voice_player is None:
                raise UserError("Il bot non è in nessun canale vocale.\n"
                                "Evocalo prima con [c]summon[/c]!")
        # Stop the playback of the current song
        voice_player.voice_client.stop()
        # Done!
        return {}
