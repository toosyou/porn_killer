import sys
import socketserver
from http.server import HTTPServer, CGIHTTPRequestHandler

class threading_http_server(socketserver.ThreadingMixIn, HTTPServer):
    pass

class image_server_handler(CGIHTTPRequestHandler):
    def do_POST(self):
        # download image and response
        if int(self.headers['Content-Length']) > 10000000: # larger than 100M
            self.send_response(500)
            return
        image = self.download_image()
        MAC = self.get_MAC()
        time = self.get_time()

        # response 301 for format error
        if len(image) == 0 or MAC == None or time == None:
            self.send_response(301)
            self.end_headers()
            return

        # response ok
        self.send_response(200)
        self.end_headers()
        self.process_image(image, MAC, time)
        return

    def do_GET(self):
        pass

    def download_image(self):
        content_length = int(self.headers['Content-Length'] )
        return self.rfile.read(content_length )

    def get_MAC(self):
        return self.headers['MAC']

    def get_time(self):
        return self.headers['Time']

    def process_image(self, image, MAC, time):
        pass

if __name__ == '__main__':
    port = 9999
    httpd = threading_http_server(('', port), image_server_handler)
    print("Starting simple_httpd on port: " + str(httpd.server_port))
    httpd.serve_forever()
