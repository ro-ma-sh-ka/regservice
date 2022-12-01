# https://python.plainenglish.io/how-to-run-background-tasks-in-fastapi-python-73980fcf5672

from fastapi import FastAPI
import asyncio
import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

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
        return int(self.response)


app = FastAPI()
# x = [1]           # a global variable x
fibonacci_rpc = FibonacciRpcClient()
response = None


@app.get("/response")
def hello():
    return {"message": "hello", "x": response}


async def periodic():
    while True:
        # code to run periodically starts here
        print(" [x] Requesting fib(30)")
        response = fibonacci_rpc.call(30)
        print(" [.] Got %r" % response)
        # code to run periodically ends here
        # sleep for 3 seconds after running above code
        await asyncio.sleep(2)


@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(periodic())
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
