import os.path
import tornado.web
import tornado.ioloop
from tornado.options import define
import pika


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
    def get(self):
        self.render('base.html')


class GetRequestHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name")
        surname = self.get_argument("surname")
        phone = self.get_argument("phone")
        appeal = self.get_argument("appeal")

        # подклбчаемся к очереди и отправляем name
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='rpc_queue')
        channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            body=name
        )
        connection.close()

        self.render('message.html', name=name, surname=surname, phone=phone, appeal=appeal)


if __name__ == '__main__':
    app = Applications()
    app.listen(8888)
    print('im listening port 8888')
    tornado.ioloop.IOLoop.current().start()
