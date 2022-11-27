# https://gist.github.com/vgoklani/5951694
# https://pika.readthedocs.io/en/stable/modules/adapters/tornado.html

import tornado.web
import tornado.ioloop
import pika
from pika.adapters.tornado_connection import TornadoConnection
import logging
import logging.config

TORNADO_PORT = 8889

RMQ_USER = 'user'
RMQ_PWD = 'password'
RMQ_HOST = 'localhost'
RMQ_PORT = 5762

IOLOOP_TIMEOUT = 500

# configure my logger
# logging.config.fileConfig('log.conf')

# holds channel objects
channel = None


class PikaClient(object):
    # all the following functions precede in order starting with connect
    def connect(self):
        try:
            # logging.getLogger('rmq_tornado')
            credentials = pika.PlainCredentials(RMQ_USER, RMQ_PWD)
            param = pika.ConnectionParameters(host=RMQ_HOST, port=RMQ_PORT, credentials=credentials)
            self.connection = TornadoConnection(param, on_open_callback=self.on_connected)
        except Exception as e:
            print('Something went wrong...', e)

    def on_connected(self, connection):
        """When we are completely connected to rabbitmq this is called"""

        print('Succesfully connected to rabbitmq')

        # open a channel
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, new_channel):
        """When the channel is open this is called"""
        print('Opening channel to rabbitmq')

        global channel
        channel = new_channel


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]

        tornado.web.Application.__init__(self, handlers)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Tornado web server.  Post a message to it using 'message' as a parameter. \
        Message will then be published to a rabbitmq queue.")

    def post(self):
        try:
            rcv_message = self.get_argument('message', 'The received message had no content.')

            print('About to send received message to rabbitmq exchange %s', rcv_message)

            channel.basic_publish(exchange='', routing_key='my_queue_name',
                                  properties=pika.BasicProperties(content_type='application/text'), body=rcv_message)
        except Exception as e:
            print('Something went wrong... %s', e)


application = Application()

if __name__ == "__main__":
    application.pika = PikaClient()
    application.listen(TORNADO_PORT)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_timeout(IOLOOP_TIMEOUT, application.pika.connect)
    ioloop.start()
