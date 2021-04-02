from bluetooth import *
import RPi.GPIO as GPIO
import time


server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(1)
print("start server...")





try:
    client, info = server.accept()
    print("client mac:", info[0], ", port:", info[1])

    # user come
    msg = "hello"
    client.send(msg.encode())
except KeyboardInterrupt:
    print("abort")
    server.close()
    exit()




# send string to client
def send(msg):
    print("send to client: "+msg)
    msg = msg+"\n"
    # client.send(msg.encode())
    client.send(bytes(msg, 'UTF-8'))

# receive a message from the client
def recv():
    byte_data = client.recv(1024)
    data = byte_data.decode().strip()
    print("recv: ", data, "(", len(data), ")")
    return data






while True:
    send("\noption:  on, off, quit\n")
    # byte_data = client.recv(1024)
    # data = byte_data.decode().strip()

    data = recv()
    # print("recv: ", data, "(", len(data), ")")

    if data == "on":
        print("hello on")
    if "off" in data:
        print("receive off")

    if "quit" in data:
        send("App is terminated!!")
        # for i in range(0, 2):
        #     GPIO.output(led_pin1, False)
        #     GPIO.output(led_pin2, False)
        #     time.sleep(0.3)
        #     GPIO.output(led_pin1, True)
        #     GPIO.output(led_pin2, True)
        #     time.sleep(0.3)
        break
    
    send(data)
