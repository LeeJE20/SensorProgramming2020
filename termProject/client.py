"""
A simple Python script to send messages to a server over Bluetooth using
Python sockets (with Python 3.3 or above).
"""

import socket

serverMACAddress = 'B8:27:EB:83:3E:F0' #RPi(미니파이)의 Bluetooth MAC Address
port = 2
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    print("input please")
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()