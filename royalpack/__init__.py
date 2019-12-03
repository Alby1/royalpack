# This is a template Pack __init__. You can use this without changing anything in other packages too!

from . import commands, tables, stars, events
from .commands import available_commands
from .tables import available_tables
from .stars import available_page_stars, available_exception_stars
from .events import available_events

from .version import semantic as __version__

__all__ = [
    "commands",
    "tables",
    "stars",
    "events",
    "available_commands",
    "available_tables",
    "available_page_stars",
    "available_exception_stars",
    "available_events",
]
