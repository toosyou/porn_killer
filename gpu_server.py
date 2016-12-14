from __future__ import print_function
import sys
import tornado
import tornado.web
from tornado import httpserver

sys.path.append('open_nsfw')
import classify_nsfw
from classify_nsfw import caffe_preprocess_and_compute, init_model

net, tranformer = init_model('./open_nsfw/nsfw_model/deploy.prototxt',
                                './open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel')

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        header_Length = self.request.headers.get('Content-Length')
        image = self.request.body

        print('from:', self.request.remote_ip)
        print('\tLength:', float(header_Length)/1024, 'KB')

        scores = caffe_preprocess_and_compute(image, caffe_transformer=tranformer, caffe_net=net, output_layers=['prob'])
        print('\tScore:', scores[1])

        self.add_header('Score', int(scores[1]*10000) )
        self.set_status(200)
        self.finish()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage:', sys.argv[0], 'port_number')
        sys.exit(-1)
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            ],
        )
    app.listen(int(sys.argv[1]))
    print('start server at port:', sys.argv[1])
    tornado.ioloop.IOLoop.current().start()
