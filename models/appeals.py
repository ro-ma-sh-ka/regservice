from sqlalchemy import Column, Integer, Text
from models.database_config import Base


class Appeal(Base):
    __tablename__ = 'appeals'

    id = Column(Integer, primary_key=True)
    appeal_message = Column(Text(3000))
    user = Column(Integer, ForeignKey='users.id')

    def __repr__(self):
        return "".format(self.code)
