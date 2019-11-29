from typing import *
from royalnet.commands import *


class CvCommand(Command):
    name: str = "cv"

    description: str = "Elenca le persone attualmente connesse alla chat vocale."

    syntax: str = "[a][o][n][d][h]"

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
        for mact in member["activities"]:
            # Spotify
            if "type" not in mact:
                activity += f" | 🎧 {mact['details']} ({mact['state']})"
            # Playing
            elif mact["type"] == 0:
                activity += f" | 🎮 {mact['name']}"
                if "state" in mact and "details" in mact:
                    activity += f" ({mact['state']} | {mact['details']})"
                elif "state" in mact:
                    activity += f" ({mact['state']})"
                elif "details" in mact:
                    activity += f" ({mact['details']})"
            # Streaming
            elif mact["type"] == 1:
                activity += f" | 🎥 {mact['name']}"
            # Listening
            elif mact["type"] == 2:
                activity += f" | 🎧 {mact['name']}"
            # Watching
            elif mact["type"] == 3:
                activity += f" | 📺 {mact['name']}"
            # Custom Status
            elif mact["type"] == 4:
                activity += f" | ❓ {mact['state']}"
            else:
                raise ExternalError(f"Unknown Discord activity type: {mact['type']}")

        return f"{status}{voice} {name}{activity}\n"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        response: Dict[str, Any] = await self.interface.call_herald_event("discord", "discord_cv")

        flags = args.optional(0, default="")
        display_nicks = "n" in flags
        display_discrim = "d" in flags
        display_only_role = "a" not in flags
        display_only_online = "o" not in flags
        display_not_connected = "h" not in flags

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

        if display_not_connected and len(not_connected_members) >= 0:
            message += "[b][Non in chat vocale][/b]\n"
            for member in not_connected_members:

                draw = True

                for role in member["roles"]:
                    if role["id"] == self.interface.config["Cv"]["displayed_role_id"]:
                        break
                else:
                    if display_only_role:
                        draw = False

                if display_only_online and member["status"]["main"] == "offline":
                    draw = False

                if draw:
                    message += self._render_member(member, display_nicks, display_discrim)

        await data.reply(message)
