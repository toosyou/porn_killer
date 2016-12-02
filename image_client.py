import requests
import base64

with open('tiny.jpeg', 'rb') as image_file:
    image = image_file.read()
headers = {'Content-Length': str(len(image) )}

response = requests.post('http://localhost:9999', headers=headers, data=image)
if response.status_code == 200:
    print('ok')
print(response)
