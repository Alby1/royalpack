from .play import PlayCommand


class YahoovideoCommand(PlayCommand):
    name: str = "yahoovideo"

    aliases = ["yv"]

    description: str = "Cerca un video su Yahoo Video e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    _URL_FORMAT = "yvsearch:{url}"
