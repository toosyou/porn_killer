import requests
import base64
import json

r = requests.get('http://0.0.0.0:8888?MAC=168091489920777').text


myres = json.loads(r)
print(myres["msg"])

g = open("out.jpg", "wb")
photo = base64.b64decode(myres["photo"][1:-1])
g.write(photo)
g.close()

