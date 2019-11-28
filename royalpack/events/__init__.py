# Imports go here!
from .discord_cv import DiscordCvEvent

# Enter the commands of your Pack here!
available_events = [
    DiscordCvEvent,
]

# noinspection PyUnreachableCode

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_events]
