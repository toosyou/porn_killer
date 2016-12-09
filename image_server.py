import tornado
import tornado.web
from tornado import httpserver

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        header_MAC = self.request.headers.get('MAC')
        header_Time = self.request.headers.get('Time')
        header_Length = self.request.headers.get('Content-Length')
        image = self.request.body

        if not header_MAC or not header_Time:
            self.set_status(400)
            self.finish()
            return

        print(header_MAC, header_Time, header_Length)
        with open('test.jpeg', 'wb') as out_jpg:
            out_jpg.write(image)

        self.set_status(200)
        self.finish()


if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            ],
        )
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
