import random
from royalnet.commands import *


class EmojifyCommand(Command):
    name: str = "emojify"

    description: str = "Converti un messaggio in emoji."

    syntax = "{messaggio}"

    # noinspection InvisibleCharacter
    _emojis = {
        "abcd": ["🔡", "🔠"],
        "back": ["🔙"],
        "cool": ["🆒"],
        "free": ["🆓"],
        "1234": ["🔢"],
        "abc": ["🔤"],
        "atm": ["🏧"],
        "new": ["🆕"],
        "sos": ["🆘"],
        "top": ["🔝"],
        "zzz": ["💤"],
        "end": ["🔚"],
        "777": ["🎰"],
        "100": ["💯"],
        "ab": ["🆎"],
        "cl": ["🆑"],
        "id": ["🆔"],
        "ng": ["🆖"],
        "no": ["♑️"],
        "ok": ["🆗"],
        "on": ["🔛"],
        "sy": ["💱"],
        "tm": ["™️"],
        "wc": ["🚾"],
        "up": ["🆙"],
        "!!": ["‼️"],
        "!?": ["⁉️"],
        "69": ["♋️"],
        "24": ["🏪"],
        "18": ["🔞"],
        "10": ["🙌", "🔟", "🤲"],
        "a": ["🅰️"],
        "b": ["🅱️"],
        "c": ["☪️", "©", "🥐"],
        "d": ["🇩"],
        "e": ["📧", "💶"],
        "f": ["🎏"],
        "g": ["🇬"],
        "h": ["🏨", "🏩", "🏋‍♀", "🏋‍♂"],
        "i": ["ℹ️", "♊️", "🕕"],
        "j": ["⤴️"],
        "k": ["🎋", "🦅", "💃"],
        "l": ["🛴", "🕒"],
        "m": ["♏️", "Ⓜ️", "〽️"],
        "n": ["📈"],
        "o": ["⭕️", "🅾️", "📯", "🌝", "🌚", "🌕", "🥯", "🙆‍♀", "🙆‍♂"],
        "p": ["🅿️"],
        "q": ["🔍", "🍀", "🍭"],
        "r": ["®"],
        "s": ["💰", "💵", "💸", "💲"],
        "t": ["✝️", "⬆️", "☦️"],
        "u": ["⛎", "⚓️", "🍉", "🌙", "🐋"],
        "v": ["✅", "🔽", "☑️", "✔️"],
        "w": ["🤷‍♀", "🤷‍♂", "🤾‍♀", "🤾‍♂", "🤽‍♀", "🤽‍♂"],
        "x": ["🙅‍♀", "🙅‍♂", "❌", "❎"],
        "y": ["💴"],
        "z": ["⚡️"],
        "*": ["*️⃣"],
        "!": ["❗️", "❕", "⚠️"],
        "?": ["❓", "❔"],
        "9": ["9️⃣"],
        "8": ["🎱", "8️⃣"],
        "7": ["7️⃣"],
        "6": ["6️⃣"],
        "5": ["✋", "🤚", "👋", "5️⃣"],
        "4": ["4️⃣"],
        "3": ["🥉", "3️⃣"],
        "2": ["✌️", "🤘", "🥈", "2️⃣"],
        "1": ["👆", "☝️", "🖕", "🥇", "1️⃣"],
        "0": ["⭕️", "🅾️", "📯", "🌝", "🌚", "🌕", "🥯", "🙆‍♀", "🙆‍♂", "0️⃣"],
        "+": ["🏥"],
        "/": ["🏒", "🧪", "🧹"],
        "\\": ["🍢", "🍡", "🥄", "🌂"],
    }

    @classmethod
    def _emojify(cls, string: str):
        new_string = string.lower()
        for key in cls._emojis:
            selected_emoji = random.sample(cls._emojis[key], 1)[0]
            new_string = new_string.replace(key, selected_emoji)
        return new_string

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        string = args.joined(require_at_least=1)
        await data.reply(self._emojify(string))
