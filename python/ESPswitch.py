#The switch

import machine
import network

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('SuperMassive', 'BlackHole')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

#sending get request
# yeah im lost.
# if pin15 high get url/pin15=on
# if pin15 low get url/pin15=off

#not sure about url, my assumption is this.
url = 192.168.4.1


    def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
