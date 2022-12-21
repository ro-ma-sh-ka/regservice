from sqlalchemy import create_engine, Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import service_db.schemas


DATABASE_URL = 'sqlite:///service_db/appeals_registration.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Appeal(Base):
    """
    Class to define a table where we save messages and match with User class which define users table
    """
    __tablename__ = 'appeals'
    id = Column(Integer, primary_key=True)
    appeal_message = Column(Text(3000))
    user = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "".format(self.code)


class User(Base):
    """"
    class to define a table where we save users
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    patronymic = Column(String(50))
    phone = Column(Integer)
    appeal = relationship('Appeal')

    def __repr__(self):
        return "".format(self.code)


def write_user(name: service_db.schemas.User,
               surname: service_db.schemas.User,
               patronymic: service_db.schemas.User,
               phone: service_db.schemas.User,
               appeal: service_db.schemas.Appeal):
    """
    The method get a data and check if it corrects thanks to pydantic
    """
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance
    user_to_write = User(name=name, surname=surname, patronymic=patronymic, phone=phone)

    # add it to the session and commit it
    session.add(user_to_write)
    session.commit()
    # get a user id to write a message to appeals table
    user_id = user_to_write.id
    # call this method to write a message with user id
    write_appeal(appeal, user_id)
    # close the session
    session.close()


def write_appeal(appeal: service_db.schemas.Appeal, user_id):
    """
     The method get a data and check if it corrects thanks to pydantic
     """
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance
    appeal_to_write = Appeal(appeal_message=appeal, user=user_id)

    # add it to the session and commit it
    session.add(appeal_to_write)
    session.commit()

    # close the session
    session.close()


Base.metadata.create_all(engine)
