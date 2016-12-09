import tornado.ioloop
import tornado.web
import base64
import json


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		message = "Yooooo!"
		with open("test.jpeg", "rb") as f:
			img = base64.b64encode(f.read())
			myres = {"photo":str(img),"msg":message}
			myres = json.dumps(myres)
			self.write(myres)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888) 
	print('server running: 0.0.0.0:8888')
	tornado.ioloop.IOLoop.current().start()
