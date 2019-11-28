import re
import datetime
from sqlalchemy import Column, \
                       Integer, \
                       Text, \
                       Boolean, \
                       DateTime, \
                       ForeignKey, \
                       String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr


class Diario:
    __tablename__ = "diario"

    @declared_attr
    def diario_id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def creator_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def quoted_account_id(self):
        return Column(Integer, ForeignKey("users.uid"))

    @declared_attr
    def quoted(self):
        return Column(String)

    @declared_attr
    def text(self):
        return Column(Text)

    @declared_attr
    def context(self):
        return Column(Text)

    @declared_attr
    def timestamp(self) -> datetime.datetime:
        return Column(DateTime, nullable=False)

    @declared_attr
    def media_url(self):
        return Column(String)

    @declared_attr
    def spoiler(self):
        return Column(Boolean, default=False)

    @declared_attr
    def creator(self):
        return relationship("User", foreign_keys=self.creator_id, backref="diario_created")

    @declared_attr
    def quoted_account(self):
        return relationship("User", foreign_keys=self.quoted_account_id, backref="diario_quoted")

    def json(self) -> dict:
        return {
            "diario_id": self.diario_id,
            "creator": self.creator.json() if self.creator else None,
            "quoted_account": self.quoted_account.json() if self.quoted_account else None,
            "quoted": self.quoted,
            "text": self.text,
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
            "media_url": self.media_url,
            "spoiler": self.spoiler
        }

    def __repr__(self):
        return f"<Diario diario_id={self.diario_id}" \
                      f" creator_id={self.creator_id}" \
                      f" quoted_account_id={self.quoted_account_id}" \
                      f" quoted={self.quoted}" \
                      f" text={self.text}" \
                      f" context={self.context}" \
                      f" timestamp={self.timestamp}" \
                      f" media_url={self.media_url}" \
                      f" spoiler={self.spoiler}>"

    def __str__(self):
        text = f"Riga #{self.diario_id} (salvata"
        if self.creator is not None:
            text += f" da {str(self.creator)}"
        text += f" il {self.timestamp.strftime('%Y-%m-%d %H:%M')}):\n"
        if self.media_url is not None:
            text += f"{self.media_url}\n"
        if self.text is not None:
            if self.spoiler:
                hidden = re.sub(r"\w", "█", self.text)
                text += f"\"{hidden}\"\n"
            else:
                text += f"[b]\"{self.text}\"[/b]\n"
        if self.quoted_account is not None:
            text += f" —{str(self.quoted_account)}"
        elif self.quoted is not None:
            text += f" —{self.quoted}"
        else:
            text += f" —Anonimo"
        if self.context:
            text += f", [i]{self.context}[/i]"
        return text
