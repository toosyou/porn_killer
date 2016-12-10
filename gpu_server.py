import tornado
import tornado.web
from tornado import httpserver
from subprocess import Popen
from subprocess import PIPE

classifier = Popen(['python', './classify_nsfw.py', '--model_def nsfw_model/deploy.prototxt',
                        '--pretrained_model nsfw_model/resnet_50_1by2_nsfw.caffemodel'], stdin=PIPE, stdout=PIPE)

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        header_Length = self.request.headers.get('Content-Length')
        image = self.request.body

        print('from:', self.request.remote_ip)
        print('\tLength:', float(header_Length)/1024, 'KB')
        with open('test.jpeg', 'wb') as out_jpg:
            out_jpg.write(image)

        print(classifier.communicate(input=image))

        self.set_status(200)
        self.finish()

if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            ],
        )
    app.listen(8787)
    tornado.ioloop.IOLoop.current().start()
