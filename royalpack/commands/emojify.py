import random
from royalnet.commands import *


class EmojifyCommand(Command):
    name: str = "emojify"

    description: str = "Converti un messaggio in emoji."

    syntax = "{messaggio}"

    _emojis = {
        "abcd": ["🔡", "🔠"],
        "back": ["🔙"],
        "cool": ["🆒"],
        "free": ["🆓"],
        "abc": ["🔤"],
        "atm": ["🏧"],
        "new": ["🆕"],
        "sos": ["🆘"],
        "top": ["🔝"],
        "zzz": ["💤"],
        "end": ["🔚"],
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
        
        "1234":["🔢"],
        "777":["🎰"],
        "100":["💯"],
        "69":["♋️"],
        "24":["🏪"],
        "18":["🔞"],
        "10":["🙌", "🔟", "🤲"],
        #9 manca
        "8":["🎱"],
        #7 manca
        #6 manca
        "5":["✋", "🤚","👋"],
        #4 manca
        "3":["🥉"],
        "2":["✌️", "🤘", "🥈"],
        "1":["👆", "☝️", "🖕", "🥇"],
        "0":["⭕️", "🅾️", "📯", "🌝", "🌚", "🌕", "🥯", "🙆‍♀", "🙆‍♂"],
        
        "+":["🏥"],
        "/":["🏒", "🧪", "🧹"],
        "\":["🍢", "🍡", "🥄", "🌂"],
        "*":["✳️"]
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
