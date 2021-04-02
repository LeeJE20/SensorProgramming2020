
from bluetooth import *
import RPi.GPIO as GPIO
import time
import threading
import sys



# 블루투스 설정
port = 2
server = BluetoothSocket(RFCOMM)
# server.bind(("", PORT_ANY))
server.bind(("", port))
server.listen(1)
print("start server...")



# 클라이언트 받기
try:
    client, info = server.accept()
    print("client mac:", info[0], ", port:", info[1])

    # user come
    msg = "hello! this is server!"
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



# 클라이언트가 보낸 string을 받고 실행시킬 동작
def service(data):
    quitThread = False
    # 프로세스 종료
    if "quit" in data:
        print("Server is terminated!!")
        send("App is terminated!!")
        quitThread = True # 쓰레드 생성 못하게 막기
        sys.exit()
    
    # 새로운 리스닝 쓰레드 생성
    if quitThread== False:
        th = threading.Thread(target=recv)
        th.start()

    # 클라이언트가 보낸 데이터에 따라 각기 다른 동작
    if data == "on":
        print("~~~~~~~~~~~~~~~~~~~~~~hello on")
    
    if "off" in data:
        send("time is up")
        print("~~~~~~~~~~~~~~~~~~~receive off")

    if "sec" in data:
        send("~~~~~~~~~~~ "+str(data[0])+" seconds later.....")

    # 여기에 내가 원하는 다른 동작 작성


# 리스닝 함수
# receive a message from the client
def recv():
    try:
        # 클라이언트로부터 받은 메시지 출력
        byte_data = client.recv(1024)
        data = byte_data.decode().strip()
        print("recv: ", data, "(", len(data), ")")
        send("\noption:  on, off, quit\n")

        # 워커 쓰레드 생성
        worker = threading.Thread(target=service, args = [data])
        worker.start()
    except:
        print("terminate")
        sys.exit()

# 리스닝 쓰레드 동작
th = threading.Thread(target=recv)
th.start()

