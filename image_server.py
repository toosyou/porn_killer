import tornado
import tornado.web
from tornado import gen
from tornado import httpserver
from tornado import httpclient
from image_client import send_image
import requests
import json
import base64

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

        score = float(response.headers['Score'])/10000.0
        print('\tThrough ', gpu_ip[this_index_gpu], 'Score:', score)

        output_data = {
                'Time' : int(header_Time),
                'MAC' : header_MAC,
                'Score' : score,
                'Image' : str(base64.b64encode( image ) )
                }

        history_filename = './data/history/'+header_Time+'_'+header_MAC
        with open(history_filename+'.json', 'w') as out_history_json:
            json.dump(output_data, out_history_json)

        with open(history_filename+'.jpg', 'wb') as out_history_image:
            out_history_image.write(image)

        current_filename = './data/current'
        with open(current_filename+'.json', 'w') as out_current_json:
            json.dump(output_data, out_current_json)

        with open(current_filename+'.jpg', 'wb') as out_current_image:
            out_current_image.write(image)

        if score >= 0.3:
            dangerous_filename = './data/dangerous/'+header_Time+'_'+header_MAC
            with open(dangerous_filename+'.json', 'w') as out_dangerous_json:
                json.dump(output_data, out_dangerous_json)
            with open(dangerous_filename+'.jpg', 'wb') as out_dangerous_image:
                out_dangerous_image.write(image)
        return


if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r'/', MainHandler),
            ],
        )
    app.listen(9999)
    tornado.ioloop.IOLoop.current().start()
