import royalnet
from royalnet.commands import *
from royalnet.backpack.tables import *


class ExecCommand(Command):
    # oh god if there is a security vulnerability
    name: str = "exec"

    description: str = "Esegui uno script Python... se sei Steffo."

    syntax: str = "{script}"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        user: User = await data.get_author(error_if_none=True)
        if user.role != "Admin":
            raise CommandError("Non sei autorizzato a eseguire codice arbitrario!\n"
                               "(Sarebbe un po' pericoloso se te lo lasciassi eseguire, non trovi?)")
        try:
            exec(args.joined(require_at_least=1))
        except Exception as e:
            raise CommandError(f"Esecuzione fallita: {e}")
        await data.reply(f"✅ Fatto!")
