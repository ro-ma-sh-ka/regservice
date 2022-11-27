import threading
import pika
import tornado.ioloop
import tornado.web


class MessageHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write('hello')
        # self.render('evrika.html')
        print('post: ')
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=self.get_argument('message')
                              )
        self.set_status(202)


def consumer_callback(channel, method, properties, body):
    print('message received: "%s"' % body)


def run_pika():
    print('running pika...')
    channel.basic_consume(consumer_callback, queue='hello')
    channel.start_consuming()

    # print('running pika...')
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=8888))
    # channel = connection.channel()
    #
    # channel.queue_declare(queue='test')
    #
    # def callback(ch, method, properties, body):
    #     print(" [x] Received %r" % body)
    #
    # channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)
    #
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()


if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/", MessageHandler)
    ])
    app.listen(8888)
    print('im listening port 8888')
    # tornado.ioloop.IOLoop.current().start()
    # thread = threading.Thread(target=tornado.ioloop.IOLoop.current().start())

    ioloop = tornado.ioloop.IOLoop.instance()
    rabbit = pika.BlockingConnection()
    channel = rabbit.channel()
    channel.queue_declare(queue='hello')

    for target in (run_pika, tornado.ioloop.IOLoop.current().start()):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()

    try:
        while True:
            input()
    except KeyboardInterrupt:
        print('stopping services...')
        ioloop.stop()
        print('tornado server stopped')
        rabbit.close()
        print('rabbitmq connection closed')
        exit(0)









# def run_tornado():
#     app = Applications()
#     app.listen(8888)
#     tornado.ioloop.IOLoop.current().start()
#     print('running tornado...')
#
#
# def consumer_callback(channel, method, properties, body):
#     print('message received: "%s"')
#
#

#
#
# if __name__ == '__main__':

#print('services running, press ctrl+c to stop')


#
#
