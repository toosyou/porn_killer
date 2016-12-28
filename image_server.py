import subprocess
import tornado
import tornado.web
from tornado import gen
from tornado import httpserver
from tornado import httpclient
from tornado import ioloop
from image_client import send_image
import requests
import json
import base64
import time

max_gpu_retry = 5
dangerous_value = 0.3
max_amount_file = 1000
index_gpu = 0
gpu_ip = ['http://mip1070.toosyou.nctu.me:8787', 'http://toosyou.nctu.me:8787']
calculated = False

def handle_old_file():
    global calculated
    localtime = time.asctime( time.localtime(time.time() ) )
    print(localtime, ':')
    if calculated == True:
        calculated = False
        subprocess.call("ls ./data/history/* -dt | sed -e '1,"+str(max_amount_file)+"d' | xargs -d '\\n' rm -f", shell=True)
        subprocess.call("ls ./data/dangerous/* -dt | sed -e '1,"+str(max_amount_file)+"d' | xargs -d '\\n' rm -f", shell=True)
        print('\tOLD HISTORY & DANGEROUS FILE REMOVED!')
    print('\tfile checked')
    return

class MainHandler(tornado.web.RequestHandler):

    @gen.coroutine
    def post(self):
        header_MAC = self.request.headers.get('MAC')
        header_Time = self.request.headers.get('Time')
        header_Length = self.request.headers.get('Content-Length')
        image = self.request.body

        if not header_MAC or not header_Time or len(image) != int(header_Length):
            print(len(image), header_Length)
            self.set_status(400)
            self.finish()
            return
        else: # all good
            self.set_status(200)
            self.finish()
            calculated = True

        print('from:', self.request.remote_ip)
        print('\tMAC:', header_MAC, 'Time:', header_Time, 'Length:', float(header_Length)/1024, 'KB')

        # get score from gpu servers
        this_index_gpu = self.get_index()

        # retry max 5 times to success
        requester = tornado.httpclient.AsyncHTTPClient()
        req = tornado.httpclient.HTTPRequest(url=gpu_ip[this_index_gpu], method='POST', body=image)
        for i in range(max_gpu_retry):
            try:
                response = yield gen.Task(requester.fetch, req)

                score = float(response.headers['Score'])/10000.0
                print('\tThrough ', gpu_ip[this_index_gpu], 'Score:', score)

                output_data = {
                    'Time' : int(header_Time),
                    'MAC' : header_MAC,
                    'Score' : score,
                    'Image' : str(base64.b64encode( image ) )
                }
            except:
                if i == max_gpu_retry-1:
                    print('\t', max_gpu_retry, 'ERROR MAX-RETRY EXCEED, DROP!')
                    return
                print('\tERROR OCCURED WITH SCORE, RETRY!', i)
                continue
            break

        # save data and image
        self.output_image_json(output_data, image)

        return

    def get_index(self):
        global index_gpu
        this_index_gpu = index_gpu
        index_gpu = (index_gpu+1)%len(gpu_ip)
        return this_index_gpu

    def output_image_json( self, output_data, image):
        header_Time = str(output_data['Time'])
        header_MAC = output_data['MAC']
        score = output_data['Score']

        current_filename = './data/current'
        with open(current_filename+'.json', 'w') as out_current_json:
            json.dump(output_data, out_current_json)

        with open(current_filename+'.jpg', 'wb') as out_current_image:
            out_current_image.write(image)

        history_filename = './data/history/'+header_Time+'_'+header_MAC
        with open(history_filename+'.json', 'w') as out_history_json:
            json.dump(output_data, out_history_json)

        with open(history_filename+'.jpg', 'wb') as out_history_image:
            out_history_image.write(image)

        if score >= dangerous_value: # nsfw dangerous
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
    ioloop.PeriodicCallback(handle_old_file, 60*1000).start()
    tornado.ioloop.IOLoop.current().start()
