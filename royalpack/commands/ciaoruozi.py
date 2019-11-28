import telegram
from royalnet.commands import *


class CiaoruoziCommand(Command):
    name: str = "ciaoruozi"

    description: str = "Saluta Ruozi, un leggendario essere che una volta era in User Games."

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        if self.interface.name == "telegram":
            update: telegram.Update = data.update
            user: telegram.User = update.effective_user
            # Se sei Ruozi, salutati da solo!
            if user.id == 112437036:
                await data.reply("👋 Ciao me!")
                return
        await data.reply("👋 Ciao Ruozi!")
