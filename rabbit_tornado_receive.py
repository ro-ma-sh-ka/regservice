import pika
import os
from pika.adapters.tornado_connection import TornadoConnection
import tornado.ioloop
import tornado.web
import tornado.websocket
import os.path
# from tornado.options import define

# define('port', default=8888, help='default port is 8888', type=int)


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


class PikaClient(object):
    def __init__(self):
        self.connected = False
        self.connection = None
        self.channel = None
        self.messages = list()

    def connect(self):
        self.connection = TornadoConnection(on_open_callback=self.on_connected)

    def on_connected(self, connection):
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        pika.log.info("channel open")
        self.channel = channel


class AppealForm(tornado.web.RequestHandler):
    def get(self):
        self.render('base.html')


class GetRequestHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name")
        surname = self.get_argument("surname")
        phone = self.get_argument("phone")
        self.render('message.html', name=name, surname=surname, phone=phone)


application = Applications()
application.pika = PikaClient()


if __name__ == "__main__":
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_timeout(500, application.pika.connect)
    ioloop.start()
