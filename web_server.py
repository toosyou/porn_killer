import tornado.ioloop
import tornado.web
import base64
import json
import os, sys

path = "../data_file/dangerous/"
dics = {}


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		MAC = self.get_argument("MAC")
		PERIOD = self.get_argument("PERIOD")
		print(PERIOD)
		if PERIOD=="0":
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
		else:
			
			time_list = []
			dirs = os.listdir( path )
			dirs.sort()
			for file in dirs:
				if(file[-4:] == "json"):
					perameter = file.split("_")
					MACaddr = perameter[1][:-5]
					timestamp = perameter[0]
					if(MACaddr == MAC):
						time_list.append(int(timestamp))
			start_flag = 0
			start = 0
			end = 0
			current = 0
			update = 0
			time_dict = dict()
			period_list = []
			for tt in time_list:
				print(tt)
				if(start_flag ==0):
					start_flag = 1
					start = tt
					current = start	
					update = 1			
				else:
					if tt > current:
						current = current + 100
						update = 1
						if tt > current:
							end = current
							time_dict["start"]=start
							time_dict["end"] = end
							period_list.append(time_dict.copy())
							start = tt
							current = tt
							update = 0
							 
			if update!=0:
				time_dict["start"]=start
				time_dict["end"] = current
				period_list.append(time_dict.copy())
			for item in period_list:
				print(item)			

			total_period = len(time_list)*3/60
			myres = {"total":total_period, "periods":period_list}
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
