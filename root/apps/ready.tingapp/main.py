import tingbot
from tingbot import screen
from tingbot.graphics import Image

ip_address = None

@tingbot.every(seconds=10)
def get_ip_address():
    global ip_address
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
    except:
        ip_address = None

screen.fill('black')
no_network_image = Image.load('NetworkNotFound.jpg')
ready_image = Image.load('ReadyScreen.gif')

def loop():
    # drawing code here
    if ip_address:
        screen.image(ready_image)
        screen.text(
            ip_address,
            xy=(10, 230),
            align='bottomleft',
            color='white',
            font_size=10,
        )
    else:
        screen.image(no_network_image)
        
# run the app
tingbot.run(loop)
