import pickle
import base64
import discord
from typing import *
from royalnet.commands import *
from royalnet.utils import *


class PlayCommand(Command):
    name: str = "play"

    aliases = ["p"]

    description: str = "Aggiunge un url alla coda della chat vocale."

    syntax = "{url}"

    async def get_url(self, args: CommandArgs):
        return args.joined()

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        # if not (url.startswith("http://") or url.startswith("https://")):
        #     raise CommandError(f"Il comando [c]{self.interface.prefix}play[/c] funziona solo per riprodurre file da"
        #                        f" un URL.\n"
        #                        f"Se vuoi cercare un video, come misura temporanea puoi usare "
        #                        f"[c]ytsearch:nomevideo[/c] o [c]scsearch:nomevideo[/c] come url.")
        if self.interface.name == "discord":
            message: discord.Message = data.message
            guild: discord.Guild = message.guild
            if guild is None:
                guild_id = None
            else:
                guild_id: Optional[int] = guild.id
        else:
            guild_id = None
        response: Dict[str, Any] = await self.interface.call_herald_event("discord", "discord_play",
                                                                          url=await self.get_url(args),
                                                                          guild_id=guild_id)

        too_long: List[Dict[str, Any]] = response["too_long"]
        if len(too_long) > 0:
            await data.reply(f"⚠ {len(too_long)} file non {'è' if len(too_long) == 1 else 'sono'}"
                             f" stat{'o' if len(too_long) == 1 else 'i'} scaricat{'o' if len(too_long) == 1 else 'i'}"
                             f" perchè durava{'' if len(too_long) == 1 else 'no'}"
                             f" più di [c]{self.config['Play']['max_song_duration']}[/c] secondi.")

        added: List[Dict[str, Any]] = response["added"]
        if len(added) > 0:
            reply = f"▶️ Aggiunt{'o' if len(added) == 1 else 'i'} {len(added)} file alla coda:\n"
            if self.interface.name == "discord":
                await data.reply(reply)
                for item in added:
                    embed = pickle.loads(base64.b64decode(bytes(item["stringified_base64_pickled_discord_embed"],
                                                                encoding="ascii")))
                    # noinspection PyUnboundLocalVariable
                    await message.channel.send(embed=embed)
            else:
                reply += numberemojiformat([a["title"] for a in added])
                await data.reply(reply)

        if len(added) + len(too_long) == 0:
            raise ExternalError("Nessun video trovato.")
