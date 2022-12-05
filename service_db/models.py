from sqlalchemy import Column, Integer, Text, String, ForeignKey
from service_db.database import Base
from sqlalchemy.orm import relationship


class Appeal(Base):
    __tablename__ = 'appeals'
    id = Column(Integer, primary_key=True)
    appeal_message = Column(Text(3000))
    user = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "".format(self.code)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    patronymic = Column(String(50))
    phone = Column(Integer)
    appeal = relationship('Appeal')

    def __repr__(self):
        return "".format(self.code)
