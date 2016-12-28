import os, sys
import json
import requests
import time

# Open a file
path = "../data_file/history/"

dict = {}

# This would print all the files and directories

while(1):
	
	dirs = os.listdir( path )
	print("running")
	for file in reversed(dirs):
		if(file[-4:] == "json"):
			perameter = file.split("_")
			MACaddr = perameter[0]
			timestamp = perameter[1][:-5]
			if(MACaddr in dict):
				if(dict[MACaddr] < timestamp):
					dict[MACaddr] = timestamp
					print(timestamp)
			else:
				dict[MACaddr] = timestamp

	data = json.dumps(dict)
	r = requests.post('http://0.0.0.0:8888',data)
	time.sleep(3)

