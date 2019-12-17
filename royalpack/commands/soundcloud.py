from .play import PlayCommand


class SoundcloudCommand(PlayCommand):
    name: str = "soundcloud"

    aliases = ["sc"]

    description: str = "Cerca un video su SoundCloud e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    async def get_url(self, args):
        return f"scsearch:{args.joined()}"
