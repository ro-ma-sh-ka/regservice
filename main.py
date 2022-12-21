import os.path
import tornado.web
import tornado.ioloop
import tornado.options
import json
from rabbitmq import sender


class Applications(tornado.web.Application):
    """
    Class to match forms and handlers
    ...
    Handlers
    _______
     - class AppealForm - is a class of creating the first page of our application with a user form to upload an appeal
     - class GetRequestHandler - is a class to get an appeal, send it to a rabbitmq queue
     and show to user a message with the result of sending


    """
    def __init__(self):
        """Initialize the class"""
        handlers = [
            (r"/", AppealForm),
            (r"/send", GetRequestHandler),
        ]

        # set a path to templates forms
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates')
        )

        # define the handlers
        super(Applications, self).__init__(handlers, **settings)


class AppealForm(tornado.web.RequestHandler):
    """Create a user form to send appeal"""
    def get(self):
        self.render('base.html')


class GetRequestHandler(tornado.web.RequestHandler):
    """Get a user appeal and user data by GET method, send it to database and show to the user sending status"""
    def get(self):
        # create a dictionary with an appeal and user data
        appeal = dict(name=self.get_argument("name"),
                      surname=self.get_argument("surname"),
                      patronymic=self.get_argument("patronymic"),
                      phone=self.get_argument("phone"),
                      appeal=self.get_argument("appeal")
                      )

        # convert an appeal dictionary to json to send it to a rabbitmq queue
        payload = json.dumps(appeal)

        # method of sending a new appeal to a rabbitmq queue
        sender(payload)

        # render a page for user with the result
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
