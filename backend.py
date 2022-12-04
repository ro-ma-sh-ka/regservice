import json
import time
import threading
from fastapi import FastAPI
import uvicorn
import pika
from sqlalchemy.orm import Session
from service_db.database_config import Base, engine
import service_db.models
import service_db.schemas

Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/response")
def hello():
    return {"message": "hello", "x": 'response'}


def write_appeal(appeal: service_db.schemas.Appeal, user_id):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the
    appeal_to_write = service_db.models.Appeal(appeal_message=appeal, user=user_id)

    # add it to the session and commit it
    session.add(appeal_to_write)
    session.commit()

    # close the session
    session.close()


def write_user(name: service_db.schemas.User,
               surname: service_db.schemas.User,
               patronymic: service_db.schemas.User,
               phone: service_db.schemas.User,
               appeal: service_db.schemas.Appeal):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the
    user_to_write = service_db.models.User(name=name, surname=surname, patronymic=patronymic, phone=phone)

    # add it to the session and commit it
    session.add(user_to_write)
    session.commit()
    user_id = user_to_write.id
    write_appeal(appeal, user_id)
    # close the session
    session.close()


def pdf_process_function(msg):
    print(" PDF processing")
    msg_dict = json.loads(msg)
    print(" [x] Received ", msg_dict['appeal'])
    write_user(msg_dict['name'], msg_dict['surname'], msg_dict['patronymic'], msg_dict['phone'], msg_dict['appeal'])

    print(" PDF processing finished")


class BackgroundTasks(threading.Thread):
    def run(self, *args, **kwargs):
        while True:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()  # start a channel
            channel.queue_declare(queue='appeals')

            def callback(ch, method, properties, body):
                pdf_process_function(body)

            channel.basic_consume('appeals', callback, auto_ack=True)
            channel.start_consuming()
            connection.close()

            time.sleep(3)


if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()
    uvicorn.run(app)
