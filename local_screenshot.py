#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab
import time
from image_client import send_image
from datetime import datetime
import base64

re_num = 0

while(1):
	#filename = "./screenshot/"
	file_name = "current_img.jpeg"
	current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	print(current_time)
	im=ImageGrab.grab().save(file_name,'JPEG')
	#im = ImageGrab.grab().tobytes()
	with open("current_img.jpeg", 'rb') as image_file:
		image = image_file.read()
	try:
		ret = send_image('mip1070.toosyou.nctu.me','9999',image)
		if(ret != 0):
			print("error")

		else:
			print("screenshot sent")

		time.sleep(3)
	
	except:
		
		
		re_num = re_num + 1
		print("send fail, retry no."+str(re_num))
		time.sleep(3)	
		continue





