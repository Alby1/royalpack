import typing
import dateparser
import datetime
import pickle
import telegram
import discord
from sqlalchemy import and_
from royalnet.commands import *
from royalnet.utils import *
from royalnet.serf.telegram import escape as telegram_escape
from royalnet.serf.discord import escape as discord_escape
from ..tables import Reminder


class ReminderCommand(Command):
    name: str = "reminder"

    aliases = ["calendar"]

    description: str = "Ti ricorda di fare qualcosa dopo un po' di tempo."

    syntax: str = "[ {data} ] {messaggio}"

    def __init__(self, interface: CommandInterface):
        super().__init__(interface)
        session = interface.alchemy.Session()
        reminders = (
            session.query(interface.alchemy.get(Reminder))
                   .filter(and_(
                       interface.alchemy.get(Reminder).datetime >= datetime.datetime.now(),
                       interface.alchemy.get(Reminder).interface_name == interface.name))
                   .all()
        )
        for reminder in reminders:
            interface.loop.create_task(self._remind(reminder))

    async def _remind(self, reminder):
        await sleep_until(reminder.datetime)
        if self.interface.name == "telegram":
            chat_id: int = pickle.loads(reminder.raw_interface_data)
            client: telegram.Bot = self.serf.client
            await self.serf.api_call(client.send_message,
                                     chat_id=chat_id,
                                     text=telegram_escape(f"❗️ {reminder.message}"),
                                     parse_mode="HTML",
                                     disable_web_page_preview=True)
        elif self.interface.name == "discord":
            channel_id: int = pickle.loads(reminder.raw_interface_data)
            client: discord.Client = self.serf.client
            channel = client.get_channel(channel_id)
            await channel.send(discord_escape(f"❗️ {reminder.message}"))

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        try:
            date_str, reminder_text = args.match(r"\[\s*([^]]+)\s*]\s*([^\n]+)\s*")
        except InvalidInputError:
            date_str, reminder_text = args.match(r"\s*(.+?)\s*\n\s*([^\n]+)\s*")

        try:
            date: typing.Optional[datetime.datetime] = dateparser.parse(date_str, settings={
                "PREFER_DATES_FROM": "future"
            })
        except OverflowError:
            date = None
        if date is None:
            await data.reply("⚠️ La data che hai inserito non è valida.")
            return
        if date <= datetime.datetime.now():
            await data.reply("⚠️ La data che hai specificato è nel passato.")
            return
        await data.reply(f"✅ Promemoria impostato per [b]{date.strftime('%Y-%m-%d %H:%M:%S')}[/b]")
        if self.interface.name == "telegram":
            interface_data = pickle.dumps(data.update.effective_chat.id)
        elif self.interface.name == "discord":
            interface_data = pickle.dumps(data.message.channel.id)
        else:
            raise UnsupportedError("This command does not support the current interface.")
        creator = await data.get_author()
        reminder = self.interface.alchemy.get(Reminder)(creator=creator,
                                                        interface_name=self.interface.name,
                                                        interface_data=interface_data,
                                                        datetime=date,
                                                        message=reminder_text)
        self.interface.loop.create_task(self._remind(reminder))
        data.session.add(reminder)
        await asyncify(data.session.commit)
