# Imports go here!
from .discord_cv import DiscordCvEvent
from .discord_summon import DiscordSummonEvent

# Enter the commands of your Pack here!
available_events = [
    DiscordCvEvent,
    DiscordSummonEvent,
]

# noinspection PyUnreachableCode

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_events]
