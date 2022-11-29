import os.path
import tornado.web
import tornado.ioloop
from tornado.options import define
import pika
import uuid


define('port', default=8888, help='default port is 8888', type=int)


class Applications(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", AppealForm),
            (r"/send", GetRequestHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates')
        )
        super(Applications, self).__init__(handlers, **settings)


class AppealForm(tornado.web.RequestHandler):
    async def get(self):
        self.render('base.html')


class GetRequestHandler(tornado.web.RequestHandler):
    async def get(self):
        name = self.get_argument("name")
        surname = self.get_argument("surname")
        phone = self.get_argument("phone")

        fibonacci_rpc = FibonacciRpcClient()
        fibonacci_rpc.call(name)
        self.render('message.html', name=name, surname=surname, phone=phone)


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
        return self.response


if __name__ == '__main__':
    app = Applications()
    app.listen(8888)
    print('im listening port 8888')
    tornado.ioloop.IOLoop.current().start()
