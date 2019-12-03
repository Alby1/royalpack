from typing import *
from royalnet.commands import *


class PmotsCommand(Command):
    name: str = "pmots"

    description: str = "Confondi Proto!"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        await data.reply("👣 pmots pmots")
