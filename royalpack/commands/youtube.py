from .play import PlayCommand


class YoutubeCommand(PlayCommand):
    name: str = "youtube"

    aliases = ["yt"]

    description: str = "Cerca un video su YouTube e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    _URL_FORMAT = "ytsearch:{url}"
