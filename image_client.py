import requests
from uuid import getnode as get_mac
from time import gmtime, strftime, localtime

def send_image(ip, port, image):
    headers = {'MAC': str(get_mac()),
                'Time': strftime('%Y%m%d%H%M%S', localtime())}
    response = requests.post('http://' + ip + ':' + str(port), headers=headers, data=image)
    if response.status_code == 200:
        return 0 # ok
    elif response.status_code == 301:
        return -1 # format error
    return -2 # response not defined

if __name__ == '__main__':
    with open('tiny.jpeg', 'rb') as image_file:
        image = image_file.read()
    print(send_image('140.113.89.75', 9999, image))
