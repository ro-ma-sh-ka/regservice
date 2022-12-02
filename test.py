import time
import threading
from fastapi import FastAPI
import uvicorn
import pika

app = FastAPI()


@app.get("/response")
def hello():
    return {"message": "hello", "x": 'response'}


def pdf_process_function(msg):
    print(" PDF processing")
    print(" [x] Received " + str(msg))
    print(" PDF processing finished")


class BackgroundTasks(threading.Thread):
    def run(self, *args, **kwargs):
        while True:
            print(" [x] Requesting fib(30)")

            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()  # start a channel
            channel.queue_declare(queue='pdfprocess')

            def callback(ch, method, properties, body):
                pdf_process_function(body)

            channel.basic_consume('pdfprocess', callback, auto_ack=True)
            channel.start_consuming()
            connection.close()

            time.sleep(3)


if __name__ == '__main__':
    t = BackgroundTasks()
    t.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)