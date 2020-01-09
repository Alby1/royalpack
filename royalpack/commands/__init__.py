# Imports go here!
from .ciaoruozi import CiaoruoziCommand
from .color import ColorCommand
from .cv import CvCommand
from .diario import DiarioCommand
from .rage import RageCommand
from .reminder import ReminderCommand
from .ship import ShipCommand
from .smecds import SmecdsCommand
from .videochannel import VideochannelCommand
from .pause import PauseCommand
from .play import PlayCommand
from .queue import QueueCommand
from .skip import SkipCommand
from .summon import SummonCommand
from .youtube import YoutubeCommand
from .soundcloud import SoundcloudCommand
from .emojify import EmojifyCommand
from .leagueoflegends import LeagueoflegendsCommand
from .diarioquote import DiarioquoteCommand
from .peertubeupdates import PeertubeUpdatesCommand
from .googlevideo import GooglevideoCommand
from .yahoovideo import YahoovideoCommand
from .userinfo import UserinfoCommand
from .spell import SpellCommand
from .ahnonlosoio import AhnonlosoioCommand
from .eat import EatCommand
from .pmots import PmotsCommand
from .peertube import PeertubeCommand
from .funkwhale import FunkwhaleCommand
from .eval import EvalCommand
from .exec import ExecCommand
from .markov import MarkovCommand

# Enter the commands of your Pack here!
available_commands = [
    CiaoruoziCommand,
    ColorCommand,
    CvCommand,
    DiarioCommand,
    RageCommand,
    ReminderCommand,
    ShipCommand,
    SmecdsCommand,
    VideochannelCommand,
    PauseCommand,
    PlayCommand,
    QueueCommand,
    SkipCommand,
    SummonCommand,
    YoutubeCommand,
    SoundcloudCommand,
    EmojifyCommand,
    LeagueoflegendsCommand,
    DiarioquoteCommand,
    PeertubeUpdatesCommand,
    GooglevideoCommand,
    YahoovideoCommand,
    UserinfoCommand,
    SpellCommand,
    AhnonlosoioCommand,
    EatCommand,
    PmotsCommand,
    PeertubeCommand,
    EvalCommand,
    ExecCommand,
    FunkwhaleCommand,
    MarkovCommand
]

# Don't change this, it should automatically generate __all__
__all__ = [command.__name__ for command in available_commands]
