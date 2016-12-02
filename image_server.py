import sys
import socketserver
from http.server import HTTPServer, CGIHTTPRequestHandler

class threading_http_server(socketserver.ThreadingMixIn, HTTPServer):
    pass

class image_server_handler(CGIHTTPRequestHandler):
    def do_POST(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        with open('test.jpeg', 'wb') as file_test:
            print(data_string)
            file_test.write(data_string)
        self.send_response(200)
        self.end_headers()
        pass
    def do_GET(self):
        pass


if __name__ == '__main__':
    port = 9999
    httpd = threading_http_server(('', port), image_server_handler)
    print("Starting simple_httpd on port: " + str(httpd.server_port))
    httpd.serve_forever()
