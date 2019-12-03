import discord
import pickle
import base64
from typing import *
from royalnet.commands import *
from royalnet.serf.discord import *
from ..utils import RoyalQueue


class DiscordQueueEvent(Event):
    name = "discord_queue"

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
        if isinstance(voice_player.playing, RoyalQueue):
            now_playing = voice_player.playing.now_playing
            return {
                "type": f"{voice_player.playing.__class__.__qualname__}",
                "now_playing": {
                    "title": now_playing.info.title,
                    "stringified_base64_pickled_discord_embed": str(base64.b64encode(pickle.dumps(now_playing.embed())),
                                                                    encoding="ascii")
                } if now_playing is not None else None,
                "next_up": [{
                    "title": ytd.info.title,
                    "stringified_base64_pickled_discord_embed": str(base64.b64encode(pickle.dumps(ytd.embed())),
                                                                    encoding="ascii")
                } for ytd in voice_player.playing.contents]
            }
        else:
            raise CommandError(f"Non so come visualizzare il contenuto di un "
                               f"[c]{voice_player.playing.__class__.__qualname__}[/c].")
