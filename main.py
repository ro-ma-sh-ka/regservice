import os.path
import tornado.web
import tornado.ioloop
from tornado.options import define


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
        self.render('message.html', name=name, surname=surname, phone=phone)


if __name__ == '__main__':
    app = Applications()

    app.listen(8888)
    print('im listening port 8888')
    tornado.ioloop.IOLoop.current().start()
