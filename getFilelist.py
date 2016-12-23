import os, sys
import json
import requests

# Open a file
path = "../data_file/history/"
dirs = os.listdir( path )

dict = {}

# This would print all the files and directories
for file in reversed(dirs):
	if(file[-4:] == "json"):
		MACaddr = file[-20:-5]
		time = file[0:14]
		if(MACaddr in dict):
			if(dict[MACaddr] < time):
				dict[MACaddr] = time
		else:
			dict[MACaddr] = time

data = json.dumps(dict)
r = requests.post('http://0.0.0.0:7777',data)


