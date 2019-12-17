from .play import PlayCommand


class YahoovideoCommand(PlayCommand):
    name: str = "yahoovideo"

    aliases = ["yv"]

    description: str = "Cerca un video su Yahoo Video e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_url(self, args):
        return f"yvsearch:{args.joined()}"

    # Too bad yvsearch: always finds nothing.
