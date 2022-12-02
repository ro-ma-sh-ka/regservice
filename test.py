import json
import time
import threading
from fastapi import FastAPI
import uvicorn
import pika
import models.database_config
import models.schemas
from sqlalchemy.orm import Session
from models.database_config import engine

app = FastAPI()


@app.get("/response")
def hello():
    return {"message": "hello", "x": 'response'}


def write_appeal(appeal: models.schemas.Appeal):

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the
    appeal_to_write = models.database_config.Appeal(appeal_message=appeal)

    # add it to the session and commit it
    session.add(appeal_to_write)
    session.commit()

    # close the session
    session.close()


def write_user(user: models.schemas.User):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the
    user_to_write = models.database_config.User(name=user.name)

    # add it to the session and commit it
    session.add(user_to_write)
    session.commit()

    # close the session
    session.close()


def pdf_process_function(msg):
    print(" PDF processing")
    msg_dict = json.loads(msg)
    print(" [x] Received ", msg_dict['name'])
    # write_user()
    write_appeal(msg_dict['appeal'])

    print(" PDF processing finished")


class BackgroundTasks(threading.Thread):
    def run(self, *args, **kwargs):
        while True:
            print(" [x] Requesting fib(30)")

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
