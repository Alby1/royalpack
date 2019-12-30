from typing import *
from royalnet.commands import *
from royalnet.utils import *
from royalnet.backpack.tables import User
from sqlalchemy import func


class UserinfoCommand(Command):
    name: str = "userinfo"

    aliases = ["uinfo", "ui", "useri"]

    description: str = "Visualizza informazioni su un utente."

    syntax = "[username]"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        username = args.optional(0)
        if username is None:
            user: User = await data.get_author(error_if_none=True)
        else:
            found: Optional[User] = await asyncify(
                data.session
                    .query(self.alchemy.get(User))
                    .filter(func.lower(self.alchemy.get(User).username) == func.lower(username))
                    .one_or_none
            )
            if not found:
                raise InvalidInputError("Utente non trovato.")
            else:
                user = found

        r = [
            f"ℹ️ [b]{user.username}[/b] (ID: {user.uid})",
            f"{user.role}",
            "",
        ]

        if user.fiorygi:
            r.append(f"{user.fiorygi}")
            r.append("")

        # Bios are a bit too long
        # if user.bio:
        #     r.append(f"{user.bio}")

        for account in user.telegram:
            r.append(f"{account}")

        for account in user.discord:
            r.append(f"{account}")

        for account in user.leagueoflegends:
            r.append(f"{account}")

        r.append("")

        r.append(f"Ha creato [b]{len(user.diario_created)}[/b] righe di diario, e vi compare in"
                 f" [b]{len(user.diario_quoted)}[/b] righe.")

        r.append("")

        if user.trivia_score:
            r.append(f"Trivia: [b]{user.trivia_score.correct_answers}[/b] risposte corrette / "
                     f"{user.trivia_score.total_answers} totali")

        await data.reply("\n".join(r))
