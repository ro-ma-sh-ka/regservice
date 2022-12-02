from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.database_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50)),
    surname = Column(String(50))
    patronymic = Column(String(50))
    phone = Column(String(11))
    appeal = relationship('Appeal')

    def __repr__(self):
        return "".format(self.code)
