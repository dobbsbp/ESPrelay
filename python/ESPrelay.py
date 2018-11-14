# Begin configuration
TITLE    = "Relay Status"
GPIO_NUM = 16
# End configuration

import network
import machine
import usocket

ap = network.WLAN(network.AP_IF)
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

sta_if.active()
ap_if.active()

ap_if.config(essid='SuperMassive', authmode=network.AUTH_WPA_WPA2_PSK, password="BlackHole")

pin = machine.Pin(GPIO_NUM)
pin.init(pin.OUT)

def ok(socket, query):
    socket.write("HTTP/1.1 OK\r\n\r\n")
    socket.write("<!DOCTYPE html><title>"+TITLE+"</title><body>")
    socket.write(TITLE+" status: ")
    if pin.value():
        socket.write("<span style='color:green'>ON</span>")
    else:
        socket.write("<span style='color:red'>OFF</span>")
    socket.write("<br>")
    if pin.value():
        socket.write("<form method='POST' action='/off?"+query.decode()+"'>"+
                     "<input type='submit' value='turn OFF'>"+
                     "</form>")
    else:
        socket.write("<form method='POST' action='/on?"+query.decode()+"'>"+
                     "<input type='submit' value='turn ON'>"+
                     "</form>")

def err(socket, code, message):
    socket.write("HTTP/1.1 "+code+" "+message+"\r\n\r\n")
    socket.write("<h1>"+message+"</h1>")

def handle(socket):
    (method, url, version) = socket.readline().split(b" ")
    if b"?" in url:
        (path, query) = url.split(b"?", 2)
    else:
        (path, query) = (url, b"")
    while True:
        header = socket.readline()
        if header == b"":
            return
        if header == b"\r\n":
            break

    if version != b"HTTP/1.0\r\n" and version != b"HTTP/1.1\r\n":
        err(socket, "505", "Version Not Supported")
    elif method == b"GET":
        if path == b"/":
            ok(socket, query)
        else:
            err(socket, "404", "Not Found")
    elif method == b"POST":
        if path == b"/on":
            pin.high()
            ok(socket, query)
        elif path == b"/off":
            pin.low()
            ok(socket, query)
        else:
            err(socket, "404", "Not Found")
    else:
        err(socket, "501", "Not Implemented")

server = usocket.socket()
server.bind(('0.0.0.0', 80))
server.listen(1)
while True:
    try:
        (socket, sockaddr) = server.accept()
        handle(socket)
    except:
        socket.write("HTTP/1.1 500 Internal Server Error\r\n\r\n")
        socket.write("<h1>Internal Server Error</h1>")
    socket.close()
