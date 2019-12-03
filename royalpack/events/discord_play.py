import discord
import pickle
import base64
import datetime
from typing import *
from royalnet.commands import *
from royalnet.serf.discord import *
from royalnet.bard import *
from ..utils import RoyalQueue


class DiscordPlayEvent(Event):
    name = "discord_play"

    async def run(self,
                  url: str,
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
        ytds = await YtdlDiscord.from_url(url)
        added: List[YtdlDiscord] = []
        too_long: List[YtdlDiscord] = []
        if isinstance(voice_player.playing, RoyalQueue):
            for index, ytd in enumerate(ytds):
                if ytd.info.duration >= datetime.timedelta(seconds=self.config["Play"]["max_song_duration"]):
                    too_long.append(ytd)
                    continue
                await ytd.convert_to_pcm()
                added.append(ytd)
                voice_player.playing.contents.append(ytd)
            if not voice_player.voice_client.is_playing():
                await voice_player.start()
        else:
            raise CommandError(f"Non so come aggiungere musica a [c]{voice_player.playing.__class__.__qualname__}[/c]!")
        return {
            "added": [{
                "title": ytd.info.title,
                "stringified_base64_pickled_discord_embed": str(base64.b64encode(pickle.dumps(ytd.embed())),
                                                                encoding="ascii")
            } for ytd in added],
            "too_long": [{
                "title": ytd.info.title,
                "stringified_base64_pickled_discord_embed": str(base64.b64encode(pickle.dumps(ytd.embed())),
                                                                encoding="ascii")
            } for ytd in too_long]
        }
