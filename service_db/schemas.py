from pydantic import BaseModel


# Create
class Appeal(BaseModel):
    appeal_message: str


class User(BaseModel):
    name: str
    surname: str
    patronymic: str
    phone: int
