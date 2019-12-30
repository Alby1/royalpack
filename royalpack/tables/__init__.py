# Imports go here!
from .diario import Diario
from .aliases import Alias
from .wikipages import WikiPage
from .wikirevisions import WikiRevision
from .bios import Bio
from .reminders import Reminder
from .triviascores import TriviaScore
from .mmevents import MMEvent
from .mmresponse import MMResponse
from .leagueoflegends import LeagueOfLegends
from .fiorygi import Fiorygi

# Enter the tables of your Pack here!
available_tables = [
    Diario,
    Alias,
    WikiPage,
    WikiRevision,
    Bio,
    Reminder,
    TriviaScore,
    MMEvent,
    MMResponse,
    LeagueOfLegends,
    Fiorygi,
]

# Don't change this, it should automatically generate __all__
__all__ = [table.__name__ for table in available_tables]
