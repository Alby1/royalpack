from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr


class Fiorygi:
    __tablename__ = "fiorygi"

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey("users.uid"), primary_key=True)

    @declared_attr
    def user(self):
        return relationship("User", backref=backref("fiorygi", uselist=False))

    @declared_attr
    def fiorygi(self):
        return Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Fiorygi di {self.royal}: {self.fiorygi}>"

    def __str__(self):
        return f"{self.fiorygi} fioryg" + ("i" if self.fiorygi != 1 else "")
