from typing import *
from royalnet.commands import *


class CvCommand(Command):
    name: str = "cv"

    description: str = "Elenca le persone attualmente connesse alla chat vocale."

    syntax: str = "[guildname] [all]"

    # @staticmethod
    # async def _legacy_cv_handler(bot: DiscordBot, guild_name: typing.Optional[str], everyone: bool):
    #     # Find the matching guild
    #     if guild_name:
    #         guilds: typing.List[discord.Guild] = bot.client.find_guild_by_name(guild_name)
    #     else:
    #         guilds = bot.client.guilds
    #     if len(guilds) == 0:
    #         raise CommandError("No guilds with the specified name found.")
    #     if len(guilds) > 1:
    #         raise CommandError("Multiple guilds with the specified name found.")
    #     guild = list(bot.client.guilds)[0]
    #     # Edit the message, sorted by channel
    #     discord_members = list(guild.members)
    #     channels = {0: None}
    #     members_in_channels = {0: []}
    #     message = ""
    #     # Find all the channels
    #     for member in discord_members:
    #         if member.voice is not None:
    #             channel = members_in_channels.get(member.voice.channel.id)
    #             if channel is None:
    #                 members_in_channels[member.voice.channel.id] = list()
    #                 channel = members_in_channels[member.voice.channel.id]
    #                 channels[member.voice.channel.id] = member.voice.channel
    #             channel.append(member)
    #         else:
    #             members_in_channels[0].append(member)
    #     # Edit the message, sorted by channel
    #     for channel in sorted(channels, key=lambda c: -c):
    #         members_in_channels[channel].sort(key=lambda x: x.nick if x.nick is not None else x.name)
    #         if channel == 0 and len(members_in_channels[0]) > 0:
    #             message += "[b]Non in chat vocale:[/b]\n"
    #         else:
    #             message += f"[b]In #{channels[channel].name}:[/b]\n"
    #         for member in members_in_channels[channel]:
    #             member: typing.Union[discord.User, discord.Member]
    #             # Ignore not-connected non-notable members
    #             if not everyone and channel == 0 and len(member.roles) < 2:
    #                 continue
    #             # Ignore offline members
    #             if member.status == discord.Status.offline and member.voice is None:
    #                 continue
    #             # Online status emoji
    #             if member.bot:
    #                 message += "🤖 "
    #             elif member.status == discord.Status.online:
    #                 message += "🔵 "
    #             elif member.status == discord.Status.idle:
    #                 message += "⚫ "
    #             elif member.status == discord.Status.dnd:
    #                 message += "🔴 "
    #             elif member.status == discord.Status.offline:
    #                 message += "⚪ "
    #             # Voice
    #             if channel != 0:
    #                 # Voice status
    #                 if member.voice.afk:
    #                     message += "💤 "
    #                 elif member.voice.self_deaf or member.voice.deaf:
    #                     message += "🔇 "
    #                 elif member.voice.self_mute or member.voice.mute:
    #                     message += "🔈 "
    #                 elif member.voice.self_video or member.voice.self_stream:
    #                     message += "🖥 "
    #                 else:
    #                     message += "🔊 "
    #             # Nickname
    #             # if member.nick is not None:
    #             #     message += f"[i]{member.nick}[/i]"
    #             # else:
    #             message += member.name
    #             # Game or stream
    #             if member.activity is not None:
    #                 if member.activity.type == discord.ActivityType.playing:
    #                     message += f" | 🎮 {member.activity.name}"
    #                     # Rich presence
    #                     try:
    #                         if member.activity.state is not None:
    #                             message += f" ({member.activity.state}" \
    #                                        f" | {member.activity.details})"
    #                     except AttributeError:
    #                         pass
    #                 elif member.activity.type == discord.ActivityType.streaming:
    #                     message += f" | 📡 {member.activity.url}"
    #                 elif member.activity.type == discord.ActivityType.listening:
    #                     if isinstance(member.activity, discord.Spotify):
    #                         if member.activity.title == member.activity.album:
    #                             message += f" | 🎧 {member.activity.title} ({andformat(member.activity.artists, final=' e ')})"
    #                         else:
    #                             message += f" | 🎧 {member.activity.title} ({member.activity.album} | {andformat(member.activity.artists, final=' e ')})"
    #                     else:
    #                         message += f" | 🎧 {member.activity.name}"
    #                 elif member.activity.type == discord.ActivityType.watching:
    #                     message += f" | 📺 {member.activity.name}"
    #                 else:
    #                     message += f" | ❓ {member.activity.state}"
    #             message += "\n"
    #         message += "\n"
    #     return {"response": message}

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)

    def _render_member(self,
                       member,
                       display_nick: bool,
                       display_discrim: bool):
        member: Dict[str, Any]
        status: str = ""
        if member["bot"]:
            status = "🤖"
        elif member["status"]["main"] == "online":
            status = "🔵"
        elif member["status"]["main"] == "idle":
            status = "⚫️"
        elif member["status"]["main"] == "dnd":
            status = "🔴"
        elif member["status"]["main"] == "offline":
            status = "⚪️"

        mvoice: Dict[str, Any] = member["voice"]
        voice: str = ""
        if mvoice is not None:
            if mvoice["server_mute"] or mvoice["server_deaf"]:
                voice = "🎵"
            elif mvoice["video"]:
                voice = "🖥"
            elif mvoice["afk"]:
                voice = "💤"
            elif mvoice["self_deaf"]:
                voice = "🔇"
            elif mvoice["self_mute"]:
                voice = "🔈"
            else:
                voice = "🔊"

        if display_nick and member["nick"] is not None:
            name = f"[i]{member['nick']}[/i]"
        elif display_discrim:
            name = f"{member['name']}#{member['discriminator']}"
        else:
            name = member['name']

        activity = ""
        if len(member["activities"]) >= 1:
            # TODO: how to render activities now?
            ...

        return f"{status}{voice} {name}{activity}\n"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        response: Dict[str, Any] = await self.interface.call_herald_event("discord", "discord_cv")

        flags = args.optional(0, default="")
        display_nicks = "n" in flags
        display_discrim = "d" in flags
        display_only_role = "a" not in flags
        display_only_online = "o" not in flags

        # Find all categories
        categories = []
        for member in response["guild"]["members"]:
            if member["voice"] is None:
                continue
            category = member["voice"]["channel"]["category"]
            if category not in categories:
                categories.append(category)
        categories.sort(key=lambda c: c["position"])

        # Find all channels, grouped by category id
        channels = {}
        for member in response["guild"]["members"]:
            if member["voice"] is None:
                continue
            category: Optional[int] = member["voice"]["channel"]["category"]["id"]
            if category not in channels:
                channels[category] = []
            channel = member["voice"]["channel"]
            if member["voice"]["channel"] not in channels[category]:
                channels[category].append(channel)
        for l in channels.values():
            l.sort(key=lambda c: c["position"])

        # Find all members, grouped by channel id
        members = {}
        not_connected_members = []
        for member in response["guild"]["members"]:
            if member["voice"] is None:
                not_connected_members.append(member)
                continue
            channel = member["voice"]["channel"]["id"]
            if channel not in members:
                members[channel] = []
            members[channel].append(member)
        for l in members.values():
            l.sort(key=lambda m: m["name"])

        # Construct the chat message
        message = f"ℹ️ Membri di [i]{response['guild']['name']}[/i]:\n\n"

        for category in categories:
            category: Dict[str, Any]
            if category['id'] is None:
                message += f"[b][Nessuna categoria][/b]\n"
            else:
                message += f"[b][{category['name']}][/b]\n"

            for channel in channels[category["id"]]:
                channel: Dict[str, Any]
                message += f"[b]#{channel['name']}[/b]\n"

                for member in members[channel["id"]]:
                    message += self._render_member(member, display_nicks, display_discrim)

                message += "\n"

        if len(not_connected_members) >= 0:
            message += "[b][Non in chat vocale][/b]\n"
            for member in not_connected_members:

                draw = True

                for role in member["roles"]:
                    if role["id"] == self.interface.cfg["Cv"]["displayed_role_id"]:
                        break
                else:
                    if display_only_role:
                        draw = False

                if display_only_online and member["status"]["main"] == "offline":
                    draw = False

                if draw:
                    message += self._render_member(member, display_nicks, display_discrim)

        await data.reply(message)
