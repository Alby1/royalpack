from .play import PlayCommand


class YoutubeCommand(PlayCommand):
    name: str = "youtube"

    aliases = ["yt"]

    description: str = "Cerca un video su YouTube e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_url(self, args):
        return f"ytsearch:{args.joined()}"
