from royalnet.commands import *


class AhnonlosoioCommand(Command):
    name: str = "ahnonlosoio"

    description: str = "Ah, non lo so io!"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        await data.reply(r"🤷 Ah, non lo so io! ¯\_(ツ)_/¯")