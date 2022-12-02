from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship
# from models.appeals import Appeal
# from models.users import User


DATABASE_URL = 'sqlite:///appeals_registration.db'
Base = declarative_base()
engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)


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
    phone = Column(String(11))
    appeal = relationship('Appeal')

    def __repr__(self):
        return "".format(self.code)


def main():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
