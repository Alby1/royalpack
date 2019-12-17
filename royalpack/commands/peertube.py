from .play import PlayCommand
from royalnet.commands import *
import aiohttp
import urllib.parse


class PeertubeCommand(PlayCommand):
    name: str = "peertube"

    aliases = ["pt", "royaltube", "rt"]

    description: str = "Cerca un video su RoyalTube e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_url(self, args):
        search = urllib.parse.quote(args.joined(require_at_least=1))
        async with aiohttp.ClientSession() as session:
            async with session.get(self.config["Peertube"]["instance_url"] +
                                   f"/api/v1/search/videos?search={search}") as response:
                j = await response.json()
        if j["total"] < 1:
            raise InvalidInputError("Nessun video trovato.")
        return f'{self.config["Peertube"]["instance_url"]}/videos/watch/{j["data"][0]["uuid"]}'
