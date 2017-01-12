from __future__ import print_function
import sys
import tornado
import tornado.web
from tornado import httpserver
import time

sys.path.append('open_nsfw')
import classify_nsfw
from classify_nsfw import caffe_preprocess_and_compute, init_model

net, tranformer = init_model('./open_nsfw/nsfw_model/deploy.prototxt',
                                './open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel')

port_listened = 0

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        header_Length = self.request.headers.get('Content-Length')
        image = self.request.body

        print('from:', self.request.remote_ip, 'to', port_listened)
        print('\tLength:', float(header_Length)/1024, 'KB')

        try:
            calculate_start_time = time.time()
            scores = caffe_preprocess_and_compute(image, caffe_transformer=tranformer, caffe_net=net, output_layers=['prob'])
            calculate_end_time = time.time()
        except:
            print('\tERROR OCCURED!')
            self.set_status(500)
            self.finish()
            return

        print('\tScore:', scores[1])
        print('\tTime:', float(calculate_end_time - calculate_start_time), 's')

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
    port_listened = int(sys.argv[1])
    app.listen( port_listened )
    print('start server at port:', sys.argv[1])
    tornado.ioloop.IOLoop.current().start()
