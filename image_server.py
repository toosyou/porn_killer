import tornado
import tornado.web
from tornado import gen
from tornado import httpserver
from image_client import send_image

index_gpu = 0
gpu_ip = ['http://mip1070.toosyou.nctu.me']
gpu_port = [9999]

class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        header_MAC = self.request.headers.get('MAC')
        header_Time = self.request.headers.get('Time')
        header_Length = self.request.headers.get('Content-Length')
        image = self.request.body

        if not header_MAC or not header_Time:
            self.set_status(400)
            self.finish()
            return

        print('from:', self.request.remote_ip)
        print('\tMAC:', header_MAC, 'Time:', header_Time, 'Length:', float(header_Length)/1024, 'KB')
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
