import tornado
import tornado.web
from tornado import gen
from tornado import httpserver
from tornado import httpclient
from image_client import send_image
import requests
import json

index_gpu = 0
gpu_ip = ['http://mip1070.toosyou.nctu.me:8787', 'http://toosyou.nctu.me:8787']

class MainHandler(tornado.web.RequestHandler):
    requester = tornado.httpclient.AsyncHTTPClient()

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

        self.set_status(200)
        self.finish()

        global index_gpu
        this_index_gpu = index_gpu
        index_gpu = (index_gpu+1)%len(gpu_ip)

        req = tornado.httpclient.HTTPRequest(url=gpu_ip[this_index_gpu], method='POST', body=image)
        response = yield gen.Task(self.requester.fetch, req)

        score = float(response.headers['Score'])/1000.0
        print('\tThrough ', gpu_ip[this_index_gpu], 'Score:', score)

        with open('./data/'+header_Time+'_'+header_MAC+'.jpg', 'wb') as out_image:
            out_image.write(image)

        output_data = {
                'Time' : int(header_Time),
                'MAC' : header_MAC,
                'Score' : score
                }
        with open('./data/'+header_Time+'_'+header_MAC+'.json', 'w') as out_json:
            json.dump(output_data, out_json)
        return


if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            ],
        )
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
