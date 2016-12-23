#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab
import time
from image_client import send_image
from datetime import datetime
import base64

while(1):
	#filename = "./screenshot/"
	file_name = "current_img.jpeg"
	current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	print(current_time)
	#im=ImageGrab.grab().save(file_name,'JPEG')
	#im = ImageGrab.grab().tobytes()
	with open("current_img.jpeg", 'rb') as image_file:
		image = image_file.read()
	ret = send_image('mip1070.toosyou.nctu.me','9999',image)
	if(ret != 0):
		print("error")
	else:
		print("data sent")

	time.sleep(10)





