import royalnet
from royalnet.commands import *
from royalnet.backpack.tables import *


class EvalCommand(Command):
    # oh god if there is a security vulnerability
    name: str = "eval"

    description: str = "Esegui una espressione Python... se sei Steffo."

    syntax: str = "{espressione}"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        user: User = await data.get_author(error_if_none=True)
        if user.role != "Admin":
            raise CommandError("Non sei autorizzato a eseguire codice arbitrario!\n"
                               "(Sarebbe un po' pericoloso se te lo lasciassi eseguire, non trovi?)")
        try:
            result = eval(args.joined(require_at_least=1))
        except Exception as e:
            raise CommandError(f"Eval fallito: {e}")
        await data.reply(repr(result))
