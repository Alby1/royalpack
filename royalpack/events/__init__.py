# Imports go here!
from .discord_cv import DiscordCvEvent
from .discord_summon import DiscordSummonEvent
from .discord_play import DiscordPlayEvent
from .discord_skip import DiscordSkipEvent

# Enter the commands of your Pack here!
available_events = [
    DiscordCvEvent,
    DiscordSummonEvent,
    DiscordPlayEvent,
    DiscordSkipEvent,
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_events]
