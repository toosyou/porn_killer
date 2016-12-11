import sys
import requests
from uuid import getnode as get_mac
from time import gmtime, strftime

def send_image(ip, port, image):
    headers = {'MAC': str(get_mac()),
                'Time': strftime('%Y%m%d%H%M%S', gmtime())}
    response = requests.post('http://' + ip + ':' + str(port), headers=headers, data=image)
    if response.status_code == 200:
        return 0 # ok
    elif response.status_code == 400:
        return -1 # format error
    return -2 # response not defined

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage:', sys.argv[0], 'file_name.jpg')
        sys.exit(-1)

    with open(sys.argv[1], 'rb') as image_file:
        image = image_file.read()

    print(send_image('140.113.207.182', 9999, image))
