import os.path
import tornado.web
import tornado.ioloop
import tornado.options
import pika
import json


#define('port', default=80, help='default port is 8888', type=int)


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
        appeal = dict(name=self.get_argument("name"),
                      surname=self.get_argument("surname"),
                      patronymic=self.get_argument("patronymic"),
                      phone=self.get_argument("phone"),
                      appeal=self.get_argument("appeal")
                      )
        payload = json.dumps(appeal)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))  # Connect to CloudAMQP
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue='appeals')  # Declare a queue
        # send a message
        channel.basic_publish(exchange='', routing_key='appeals', body=payload)
        print("[x] Message sent to consumer")
        connection.close()

        self.render('message.html',
                    name=appeal['name'],
                    surname=appeal['surname'],
                    patronymic=appeal['patronymic'],
                    phone=appeal['phone'],
                    appeal=appeal['appeal'])


if __name__ == '__main__':
    app = Applications()
    port = 8888
    app.listen(port)
    print(f'im listening port {port}')
    tornado.ioloop.IOLoop.current().start()
