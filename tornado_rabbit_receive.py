import pika
import sys
import os
from pika.adapters.tornado_connection import TornadoConnection
import os.path
import tornado.web
import tornado.ioloop
from tornado.options import define


class AppealForm(tornado.web.RequestHandler):
    async def get(self):
        self.render('base.html')


class GetRequestHandler(tornado.web.RequestHandler):
    async def get(self):
        name = self.get_argument("name")
        surname = self.get_argument("surname")
        phone = self.get_argument("phone")
        self.render('message.html', name=name, surname=surname, phone=phone)


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


def main():
    def callback(body):
        print(" [x] Received %r" % body)

    connection = TornadoConnection(on_open_callback=callback)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        app = Applications()
        app.listen(8888)
        print('im listening port 8888')
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.add_timeout(500, main)
        ioloop.start()


    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
