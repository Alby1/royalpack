from .play import PlayCommand


class GooglevideoCommand(PlayCommand):
    name: str = "googlevideo"

    aliases = ["gv"]

    description: str = "Cerca un video su Google Video e lo aggiunge alla coda della chat vocale."

    syntax = "{ricerca}"

    _URL_FORMAT = "gvsearch:{url}"

    # Too bad gvsearch: always finds nothing.
