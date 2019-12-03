import pickle
import base64
import discord
from typing import *
from royalnet.commands import *
from royalnet.utils import *


class QueueCommand(Command):
    name: str = "queue"

    aliases = ["q"]

    description: str = "Visualizza la coda di riproduzione attuale.."

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        if self.interface.name == "discord":
            message: discord.Message = data.message
            guild: discord.Guild = message.guild
            guild_id: Optional[int] = guild.id
        else:
            guild_id = None
        response: Dict[str, Any] = await self.interface.call_herald_event("discord", "discord_queue",
                                                                          guild_id=guild_id)

        queue_type = response["type"]
        if queue_type == "RoyalQueue":
            next_up = response["next_up"]
            now_playing = response["now_playing"]
            await data.reply(f"ℹ️ La coda contiene {len(next_up)} file.\n\n")

            if now_playing is not None:
                reply = f"Attualmente, sta venendo riprodotto:\n"
                if self.interface.name == "discord":
                    await data.reply(reply)
                    embed = pickle.loads(base64.b64decode(bytes(now_playing["stringified_base64_pickled_discord_embed"],
                                                                encoding="ascii")))
                    # noinspection PyUnboundLocalVariable
                    await message.channel.send(embed=embed)
                else:
                    reply += f"▶️ {now_playing['title']}\n\n"
                    await data.reply(reply)
            else:
                await data.reply("⏹ Attualmente, non sta venendo riprodotto nulla.")

            reply = ""
            if len(next_up) >= 1:
                reply += "I prossimi file in coda sono:\n"
                if self.interface.name == "discord":
                    await data.reply(reply)
                    for item in next_up[:5]:
                        embed = pickle.loads(base64.b64decode(bytes(item["stringified_base64_pickled_discord_embed"],
                                                                    encoding="ascii")))
                        # noinspection PyUnboundLocalVariable
                        await message.channel.send(embed=embed)
                else:
                    reply += numberemojiformat([a["title"] for a in next_up[:5]])
                    await data.reply(reply)
            else:
                await data.reply("ℹ️ Non ci sono altri file in coda.")
        else:
            raise CommandError(f"Non so come visualizzare il contenuto di un [c]{queue_type}[/c].")
