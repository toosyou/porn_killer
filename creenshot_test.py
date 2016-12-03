#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab
import time
from image_client import send_image
from datetime import datetime
import base64

while(1):
	#filename = "./screenshot/"
	current_time = "test.jpeg"
	#current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".jpeg"
	print(current_time)
	im=ImageGrab.grab().save(current_time,'JPEG')
	#im = ImageGrab.grab().tobytes()
	with open("test.jpeg", 'rb') as image_file:
		image = image_file.read()
	print(send_image('140.113.89.75','9999',image))

	time.sleep(10)





