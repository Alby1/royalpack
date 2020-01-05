from .play import PlayCommand
from royalnet.commands import *
import aiohttp
import urllib.parse


class FunkwhaleCommand(PlayCommand):
    name: str = "funkwhale"

    aliases = ["fw", "royalwhale", "rw"]

    description: str = "Cerca un video su RoyalWhale e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_url(self, args):
        search = urllib.parse.quote(args.joined(require_at_least=1))
        async with aiohttp.ClientSession() as session:
            async with session.get(self.config["Funkwhale"]["instance_url"] +
                                   f"/api/v1/search?query={search}") as response:
                j = await response.json()
        if len(j["tracks"]) < 1:
            raise InvalidInputError("Nessun video trovato.")
        return f'{self.config["Funkwhale"]["instance_url"]}{j["tracks"][0]["listen_url"]}'
