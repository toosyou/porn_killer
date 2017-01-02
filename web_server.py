import tornado.ioloop
import tornado.web
import base64
import json
import os, sys
import datetime

path = "../data_file/dangerous/"
dics = {}


class MainHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
        	#print "setting headers!!!"
        	self.set_header("Access-Control-Allow-Origin", "*")
        	self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        	self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

	def get(self):
		MAC = self.get_argument("MAC")
		PERIOD = self.get_argument("PERIOD")
		now = datetime.datetime.now()
		current_time =  now.strftime("%Y%m%d%H%M%S")
		past_time = now - datetime.timedelta(days=1)
		last_24 = past_time.strftime("%Y%m%d%H%M%S")
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
					if(MACaddr == MAC and (int(timestamp) <= int(current_time)) and (int(timestamp) > int(last_24)) ):
						time_list.append(int(timestamp))
			start_flag = 0
			start = 0
			end = 0
			current = 0
			update = 0
			#time_dict = dict()
			period_list = []
			for tt in time_list:
				if(start_flag ==0):
					start_flag = 1
					start = tt
					current = start	
					update = 1			
				else:
					if tt > current:
						if tt-current>300:
							#print("tt: "+str(tt)+" current: "+str(current))
							time_dict = dict()
							time_dict["start"]=start
							time_dict["end"] = current
							file_name = "../data_file/dangerous/" + str(start) + "_" + str(MAC)+".jpg"
							with open(file_name, "rb") as f:
								img = base64.b64encode(f.read())
							time_dict["photo"] = str(img)
							period_list.append(time_dict.copy())
							start = tt
							current = tt
							update = 0
						else:
							current = tt
							update = 1
							 
			if update!=0:
				time_dict = dict()
				time_dict["start"]=start
				time_dict["end"] = current
				file_name = "../data_file/dangerous/" + str(start) + "_" + str(MAC)+".jpg"
				with open(file_name, "rb") as f:
					img = base64.b64encode(f.read())
				time_dict["photo"] = str(img)
				period_list.append(time_dict.copy())
			#for item in period_list:
				#print(item)			

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

		#print(dics)
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
