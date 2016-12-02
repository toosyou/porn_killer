#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab
import time
from datetime import datetime


while(1):
	current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
	print(current_time)
	with open(current_time, 'wb') as f:
		im=ImageGrab.grab()
		im.save(f, format='png')
	
	time.sleep(10)

