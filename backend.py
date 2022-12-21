import time
import threading
"""
Create FastAPI server.
There are two tasks:
1. listen to a rabbitmq queue
2. get an appeal from the queue and save in to database by ORM sqlalchemy
"""
from fastapi import FastAPI
import uvicorn
from rabbitmq import consumer


app = FastAPI()


# class BackgroundTasks(threading.Thread):
#     def run_consuming(self, *args, **kwargs):
#         while True:
#             consumer()
#             print('Im listening')
#             time.sleep(3)


if __name__ == '__main__':
    # t = BackgroundTasks()
    # t.start()
    uvicorn.run(app)
