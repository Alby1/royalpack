import re
import datetime
import telegram
import aiohttp
from typing import *
from royalnet.commands import *
from royalnet.utils import asyncify
from royalnet.backpack.tables import *
from ..tables import *


async def to_imgur(imgur_api_key, photosizes: List[telegram.PhotoSize], caption="") -> str:
    # Select the largest photo
    largest_photo = sorted(photosizes, key=lambda p: p.width * p.height)[-1]
    # Get the photo url
    photo_file: telegram.File = await asyncify(largest_photo.get_file)
    # Forward the url to imgur, as an upload
    async with aiohttp.request("post", "https://api.imgur.com/3/upload", data={
        "image": photo_file.file_path,
        "type": "URL",
        "title": "Diario image",
        "description": caption
    }, headers={
        "Authorization": f"Client-ID {imgur_api_key}"
    }) as request:
        response = await request.json()
        if not response["success"]:
            raise CommandError("Imgur returned an error in the image upload.")
        return response["data"]["link"]


class DiarioCommand(Command):
    name: str = "diario"

    description: str = "Aggiungi una citazione al Diario."

    syntax = "[!] \"{testo}\" --[autore], [contesto]"

    async def run(self, args: CommandArgs, data: CommandData) -> None:
        if self.interface.name == "telegram":
            update: telegram.Update = data.update
            message: telegram.Message = update.message
            reply: telegram.Message = message.reply_to_message
            creator = await data.get_author()
            # noinspection PyUnusedLocal
            quoted: Optional[str]
            # noinspection PyUnusedLocal
            text: Optional[str]
            # noinspection PyUnusedLocal
            context: Optional[str]
            # noinspection PyUnusedLocal
            timestamp: datetime.datetime
            # noinspection PyUnusedLocal
            media_url: Optional[str]
            # noinspection PyUnusedLocal
            spoiler: bool
            if creator is None:
                await data.reply("⚠️ Devi essere registrato a Royalnet per usare questo comando!")
                return
            if reply is not None:
                # Get the message text
                text = reply.text
                # Check if there's an image associated with the reply
                photosizes: Optional[List[telegram.PhotoSize]] = reply.photo
                if photosizes:
                    # Text is a caption
                    text = reply.caption
                    media_url = await to_imgur(self.interface.cfg["Imgur"]["token"],
                                               photosizes, text if text is not None else "")
                else:
                    media_url = None
                # Ensure there is a text or an image
                if not (text or media_url):
                    raise InvalidInputError("Il messaggio a cui hai risposto non contiene testo o immagini.")
                # Find the Royalnet account associated with the sender
                quoted_tg = await asyncify(data.session.query(self.alchemy.get(Telegram))
                                           .filter_by(tg_id=reply.from_user.id)
                                           .one_or_none)
                quoted_account = quoted_tg.royal if quoted_tg is not None else None
                # Find the quoted name to assign
                quoted_user: telegram.User = reply.from_user
                quoted = quoted_user.full_name
                # Get the timestamp
                timestamp = reply.date
                # Set the other properties
                spoiler = False
                context = None
            else:
                # Get the current timestamp
                timestamp = datetime.datetime.now()
                # Get the message text
                raw_text = " ".join(args)
                # Check if there's an image associated with the reply
                photosizes: Optional[List[telegram.PhotoSize]] = message.photo
                if photosizes:
                    media_url = await to_imgur(self.interface.cfg["Imgur"]["token"],
                                               photosizes, raw_text if raw_text is not None else "")
                else:
                    media_url = None
                # Parse the text, if it exists
                if raw_text:
                    # Pass the sentence through the diario regex
                    match = re.match(
                        r'(!)? *["«‘“‛‟❛❝〝＂`]([^"]+)["»’”❜❞〞＂`] *(?:(?:-{1,2}|—) *([^,]+))?(?:, *([^ ].*))?',
                        raw_text)
                    # Find the corresponding matches
                    if match is not None:
                        spoiler = bool(match.group(1))
                        text = match.group(2)
                        quoted = match.group(3)
                        context = match.group(4)
                    # Otherwise, consider everything part of the text
                    else:
                        spoiler = False
                        text = raw_text
                        quoted = None
                        context = None
                    # Ensure there's a quoted
                    if not quoted:
                        quoted = None
                    if not context:
                        context = None
                    # Find if there's a Royalnet account associated with the quoted name
                    if quoted is not None:
                        quoted_alias = await asyncify(
                            data.session.query(self.alchemy.get(Alias))
                                        .filter_by(alias=quoted.lower()).one_or_none
                        )
                    else:
                        quoted_alias = None
                    quoted_account = quoted_alias.royal if quoted_alias is not None else None
                else:
                    text = None
                    quoted = None
                    quoted_account = None
                    spoiler = False
                    context = None
                # Ensure there is a text or an image
                if not (text or media_url):
                    raise InvalidInputError("Manca il testo o l'immagine da inserire nel diario.")
            # Create the diario quote
            diario = self.alchemy.get(Diario)(creator=creator,
                                              quoted_account=quoted_account,
                                              quoted=quoted,
                                              text=text,
                                              context=context,
                                              timestamp=timestamp,
                                              media_url=media_url,
                                              spoiler=spoiler)
            data.session.add(diario)
            await asyncify(data.session.commit)
            await data.reply(f"✅ {str(diario)}")
        else:
            # Find the creator of the quotes
            creator = await data.get_author(error_if_none=True)
            # Recreate the full sentence
            raw_text = " ".join(args)
            # Pass the sentence through the diario regex
            match = re.match(r'(!)? *["«‘“‛‟❛❝〝＂`]([^"]+)["»’”❜❞〞＂`] *(?:(?:-{1,2}|—) *([^,]+))?(?:, *([^ ].*))?',
                             raw_text)
            # Find the corresponding matches
            if match is not None:
                spoiler = bool(match.group(1))
                text = match.group(2)
                quoted = match.group(3)
                context = match.group(4)
            # Otherwise, consider everything part of the text
            else:
                spoiler = False
                text = raw_text
                quoted = None
                context = None
            timestamp = datetime.datetime.now()
            # Ensure there is some text
            if not text:
                raise InvalidInputError("Manca il testo o l'immagine da inserire nel diario.")
            # Or a quoted
            if not quoted:
                quoted = None
            if not context:
                context = None
            # Find if there's a Royalnet account associated with the quoted name
            if quoted is not None:
                quoted_alias = await asyncify(
                    data.session.query(self.alchemy.get(Alias))
                                .filter_by(alias=quoted.lower())
                                .one_or_none
                )
            else:
                quoted_alias = None
            quoted_account = quoted_alias.royal if quoted_alias is not None else None
            if quoted_alias is not None and quoted_account is None:
                raise UserError("Il nome dell'autore è ambiguo, quindi la riga non è stata aggiunta.\n"
                                "Per piacere, ripeti il comando con un nome più specifico!")
            # Create the diario quote
            diario = self.alchemy.Diario(creator=creator,
                                         quoted_account=quoted_account,
                                         quoted=quoted,
                                         text=text,
                                         context=context,
                                         timestamp=timestamp,
                                         media_url=None,
                                         spoiler=spoiler)
            data.session.add(diario)
            await asyncify(data.session.commit)
            await data.reply(f"✅ {str(diario)}")
