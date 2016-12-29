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
from termcolor import colored

max_gpu_retry = 5
dangerous_value = 0.3
max_amount_file = 2000
index_gpu = 0
gpu_ip = ['http://mip1070.toosyou.nctu.me:8787', 'http://toosyou.nctu.me:8787']
gpu_error_count = [0, 0]
max_gpu_error_count = 5
gpu_recover_time = 5 #min
calculated = False

def recover_gpu():
    global gpu_error_count
    localtime = time.asctime( time.localtime(time.time() ) )
    print(localtime, ':')
    for index, error_count in enumerate(gpu_error_count):
        if error_count == max_gpu_error_count:
            gpu_error_count[index] = 0
            print(colored('\t\t\t\tRETRY GPU '+str(index)+' !', 'green'))
    print('\t\t\t\tGPU SERVER RECOVERED!')
    return

def handle_old_file():
    global calculated
    localtime = time.asctime( time.localtime(time.time() ) )
    print(localtime, ':\t', end='')
    if calculated == True:
        calculated = False
        subprocess.call("ls ./data/history/* -dt | sed -e '1,"+str(max_amount_file)+"d' | xargs -d '\\n' rm -f", shell=True)
        subprocess.call("ls ./data/dangerous/* -dt | sed -e '1,"+str(max_amount_file)+"d' | xargs -d '\\n' rm -f", shell=True)
        print(colored('OLD HISTORY & DANGEROUS FILE REMOVED!', 'red', attrs=['bold']))
    else:
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

        print('from:', self.request.remote_ip )
        print('\tMAC:', colored(header_MAC, 'green'), 'Time:', header_Time, 'Length:', float(header_Length)/1024, 'KB')

        # get score from gpu servers
        this_index_gpu = self.get_index()
        if this_index_gpu == -1: # no gpu server avaliable
            print(colored('\tNO GPU SERVER AVALIABLE! DROP!', 'red', attrs=['bold']))
            return

        # retry max 5 times to success
        requester = tornado.httpclient.AsyncHTTPClient()
        req = tornado.httpclient.HTTPRequest(url=gpu_ip[this_index_gpu], method='POST', body=image)
        for i in range(max_gpu_retry):
            try:
                response = yield gen.Task(requester.fetch, req)

                score = float(response.headers['Score'])/10000.0
                colored_score = colored('\tScore: '+str(score), 'red', attrs=['underline', 'bold']) if score >= dangerous_value else colored('\tScore: '+str(score), 'blue')
                print('\tThrough\t', gpu_ip[this_index_gpu] )
                print(colored_score)

                output_data = {
                    'Time' : int(header_Time),
                    'MAC' : header_MAC,
                    'Score' : score,
                    'Image' : str(base64.b64encode( image ) )
                }
            except:
                print(colored('\tERROR OCCURED WITH SCORE, RETRY! ' + str(i), 'yellow') )
                if i == max_gpu_retry-1:
                    print(colored('\t'+str(max_gpu_retry)+' ERROR MAX-RETRY EXCEED, DROP!', 'red', attrs=['bold']))
                    error_rtn = self.gpu_error(this_index_gpu)
                    if error_rtn == -1: # gpu dead
                        print(colored('\tGPU SERVER '+str(this_index_gpu)+' DOWN! RETRY '+str(gpu_recover_time)+' MIN LATER!', 'red', attrs=['bold']))
                    else: # failed once
                        print(colored('\tGPU SERVER '+str(this_index_gpu)+' FAILED '+str(error_rtn), 'yellow', attrs=['bold']))
                    return
                continue
            break

        # gpu server succeed
        self.gpu_succeed(this_index_gpu)

        # save data and image
        self.output_image_json(output_data, image)
        return

    def gpu_succeed(self, this_index_gpu):
        global gpu_error_count
        gpu_error_count[this_index_gpu] = 0
        return

    def gpu_error(self, this_index_gpu):
        global gpu_error_count
        error_count = gpu_error_count[this_index_gpu]
        gpu_error_count[this_index_gpu] = error_count+1 if error_count < max_gpu_error_count else error_count
        return gpu_error_count[this_index_gpu] if gpu_error_count[this_index_gpu] < max_gpu_error_count else -1

    def get_index(self):
        global index_gpu
        global gpu_error_count

        for i in range(len(gpu_ip)):
            this_index_gpu = index_gpu
            index_gpu = (index_gpu+1)%len(gpu_ip)
            if gpu_error_count[this_index_gpu] == max_gpu_error_count:
                continue
            return this_index_gpu
        return -1

    def output_image_json( self, output_data, image):
        global calculated
        calculated = True
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
    ioloop.PeriodicCallback(recover_gpu, gpu_recover_time*60*1000).start()
    tornado.ioloop.IOLoop.current().start()
