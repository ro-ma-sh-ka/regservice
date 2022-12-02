# https://python.plainenglish.io/how-to-run-background-tasks-in-fastapi-python-73980fcf5672

from fastapi import FastAPI
import asyncio
import pika
import uuid
import time
from fastapi import BackgroundTasks
import threading
import uvicorn


class FibonacciRpcClient(object):

    def __init__(self):
        # устанавливаем соединение
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        # устанавливаем канал
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)

        # объявляем эксклюзивную callback_queue для ответов.
        self.callback_queue = result.method.queue

        # подписываемся на callback_queue, чтобы получать ответы RPC.
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    # Обратный вызов on_response, который выполняется при каждом ответе,
    # выполняет очень простую работу: для каждого ответного сообщения он проверяет,
    # является ли Correlation_id тем, который мы ищем.
    # Если это так, он сохраняет ответ в self.response и прерывает цикл потребления.
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    # Затем мы определяем наш основной метод call — он выполняет фактический запрос RPC.
    # В методе call мы генерируем уникальный номер correlation_id и сохраняем его —
    # функция обратного вызова on_response будет использовать это значение для получения соответствующего ответа.
    # Также в методе call мы публикуем сообщение запроса с двумя свойствами: reply_to и correlation_id.
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return self.response


app = FastAPI()
# x = [1]           # a global variable x
fibonacci_rpc = FibonacciRpcClient()
# response = fibonacci_rpc.call(30)
response = None


@app.get("/response")
def hello():
    return {"message": "hello", "x": response}


def pdf_process_function(msg):
    print(" PDF processing")
    print(" [x] Received " + str(msg))

    # time.sleep(5) # delays for 5 seconds
    print(" PDF processing finished")


# def callback(ch, method, properties, body):
#     pdf_process_function(body)


class BackgroundTasks(threading.Thread):

    def periodic(self):
        while True:
            # code to run periodically starts here
            print(" [x] Requesting fib(30)")

            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()  # start a channel
            channel.queue_declare(queue='pdfprocess')  # Declare a queue

            # create a function which is called on incoming messages
            def callback(ch, method, properties, body):
                pdf_process_function(body)

            # set up subscription on the queue
            channel.basic_consume('pdfprocess', callback, auto_ack=True)

            # start consuming (blocks)
            channel.start_consuming()
            connection.close()

            # response = fibonacci_rpc.call(30)
            # print(" [.] Got %r" % response)
            # code to run periodically ends here
            # sleep for 3 seconds after running above code
            time.sleep(2)

# def periodic():
#     while True:
#         # code to run periodically starts here
#         print(" [x] Requesting fib(30)")
#
#         # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#         #
#         # # устанавливаем канал
#         # channel = connection.channel()
#         # result = channel.queue_declare(queue='', exclusive=True)
#         #
#         # # объявляем эксклюзивную callback_queue для ответов.
#         # callback_queue = result.method.queue
#         #
#         # # подписываемся на callback_queue, чтобы получать ответы RPC.
#         # channel.basic_consume(
#         #     queue=callback_queue,
#         #     on_message_callback=callback,
#         #     auto_ack=True)
#         #
#         # response = None
#         # corr_id = None
#         # connection.close()
#
#         connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#         channel = connection.channel()  # start a channel
#         channel.queue_declare(queue='pdfprocess')  # Declare a queue
#
#         # create a function which is called on incoming messages
#         def callback(ch, method, properties, body):
#             pdf_process_function(body)
#
#         # set up subscription on the queue
#         channel.basic_consume('pdfprocess', callback, auto_ack=True)
#
#         # start consuming (blocks)
#         channel.start_consuming()
#         connection.close()
#
#
#
#
#         # response = fibonacci_rpc.call(30)
#         # print(" [.] Got %r" % response)
#         # code to run periodically ends here
#         # sleep for 3 seconds after running above code
#         await asyncio.sleep(2)


# @app.on_event("startup")
# async def schedule_periodic():
#     loop = asyncio.get_event_loop()
#     loop.create_task(periodic())


# @app.on_event("startup")
# async def consumer(background_tasks: BackgroundTasks):
#    background_tasks.add_task(periodic)

@app.on_event("startup")
async def startup_event():
    t = BackgroundTasks()
    t.start()

if __name__ == "__main__":
    uvicorn.run(app)
