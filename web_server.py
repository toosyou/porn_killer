import tornado.ioloop
import tornado.web
import base64
import json

dics = {}

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		MAC = self.get_argument("MAC")
		if(MAC in dics):
			
			"""
			message = "Yooooo!"
			with open("test.jpeg", "rb") as f:
				img = base64.b64encode(f.read())
				myres = {"photo":str(img),"msg":message}
				myres = json.dumps(myres)
				self.write(myres)
			"""
			
			timestamp = dics[MAC]
			fileName = timestamp+"_"+MAC
			with open('../data_file/history/'+fileName+'.json') as data_file:    
				data = json.load(data_file)
				myres = {"photo":data["Image"],"msg":data["Score"]}
				myres = json.dumps(myres)
				self.write(myres)

		else:
			myres = {"photo":"","msg":"Unknown MAC"}
			myres = json.dumps(myres)
			self.write(myres)

	def post(self):
		data_json = tornado.escape.json_decode(self.request.body)
		MACs = data_json.keys()
		for key in MACs:
			if(key in dics):
				if(data_json[key] > dics[key]):
					dics[key] = data_json[key]
			else:
				dics[key] = data_json[key]

		print(dics)
		self.write("ok")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
	app = make_app()
	app.listen(8888) 
	print('server running: 0.0.0.0:8888')
	tornado.ioloop.IOLoop.current().start()
