"""
A simple Python script to send messages to a server over Bluetooth using
Python sockets (with Python 3.3 or above).
"""

import socket

serverMACAddress = 'B8:27:EB:83:3E:F0' #RPi(미니파이)의 Bluetooth MAC Address
port = 2
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))


# send string to server
def send(msg):
    print("send to server: "+msg)
    msg = msg+"\n"
    # client.send(msg.encode())
    s.send(bytes(msg, 'UTF-8'))

# receive a message form the server
def recv():
    byte_data = s.recv(1024)
    data = byte_data.decode().strip()
    # print("recv: ", data, "(", len(data), ")")
    print(data)
    return data


while 1:
    text = input("input please: ")
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
    # data = s.recv(1024)
    # print(recv)
    # data = data.decode().strip()
    # print(data)
    recv()


s.close()