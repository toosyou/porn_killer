import os, sys
import json
import requests
import time

path = "../data_file/history/"

dict = {}

while(1):
	
	dirs = os.listdir( path )
	print("running")
	for file in reversed(dirs):
		if(file[-4:] == "json"):
			perameter = file.split("_")
			MACaddr = perameter[1][:-5]
			timestamp = perameter[0]
			if(MACaddr in dict):
				if(dict[MACaddr] < timestamp):
					dict[MACaddr] = timestamp
					print("add "+MACaddr+": "+timestamp)
			else:
				dict[MACaddr] = timestamp

	data = json.dumps(dict)
	r = requests.post('http://0.0.0.0:8888',data)
	time.sleep(3)

