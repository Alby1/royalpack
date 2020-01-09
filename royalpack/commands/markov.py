from typing import *
from royalnet.commands import *
import markovify
import os
import re


class MarkovCommand(Command):
    name: str = "markov"

    description: str = "Genera una frase da una catena di Markov."

    syntax: str = "[modello]"

    _texts: Dict[str, markovify.NewlineText] = {}

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        files: List[str] = tuple(os.walk(self.config["Markov"]["models_directory"]))[0][2]
        for file in files:
            match = re.match("(\S+)\.json", file)
            if match is None:
                continue
            model_name = match.group(1)
            with open(os.path.join(self.config["Markov"]["models_directory"], file)) as f:
                self._texts[model_name] = markovify.NewlineText.from_json(f.read())

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        model_name = args.optional(0, self.config["Markov"]["default_model"])
        try:
            sentence = self._texts[model_name].make_sentence()
        except KeyError:
            raise InvalidInputError("Il modello richiesto non esiste.")
        if sentence is None or sentence == "":
            await data.reply(f"💭 Il bot ([c]{model_name}[/c])... non dice niente. Riprova!")
        else:
            await data.reply(f'💬 Il bot ([c]{model_name}[/c]) dice:\n{sentence}')
