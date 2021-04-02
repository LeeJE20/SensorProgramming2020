# chatBot

import socket
import threading
import sys
import time

# 서버의 맥어드레스 설정
serverMACAddress = 'B8:27:EB:83:3E:F0' #RPi(미니파이)의 Bluetooth MAC Address
# serverMACAddress = 'B8:27:EB:83:3E:F0' #원래 보드의 Bluetooth MAC Address

# 블루투스 연결
port = 2
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))

# 서버가 보낸 data를 받고 실행시킬 동작
def service(data):
    quitThread = False
    # 프로세스 종료
    if data == "App is terminated!!":
        quitThread = True # 쓰레드 생성 못하게 막기
        sys.exit()

    # 새로운 리스닝 쓰레드 생성
    if quitThread == False:
        th = threading.Thread(target=recv)
        th.start()

    # 클라이언트가 보낸 데이터에 따라 각기 다른 동작
    if data == "time is up":
        print("~~~~~~~~~~~~~~~~~~~~~~server receieved off!!!!!!!")

    # 여기에 내가 원하는 다른 동작 작성

# send string to server
def send(msg):
    print("send to server: "+msg)
    msg = msg+"\n"
    # client.send(msg.encode())
    s.send(bytes(msg, 'UTF-8'))

# 리스닝 함수
# receive a message form the server
def recv():
    try:
        # 서버로부터 받은 메시지 출력
        byte_data = s.recv(1024)
        data = byte_data.decode().strip()
        print(data)

        # 워커 쓰레드 생성
        worker= threading.Thread(target=service, args = [data])
        worker.start()

        return data
    except:
        print("terminate")
        sys.exit()

recv()



while 1:
    # 입력한 메시지를 서버에 전송
    text = input("input please. ")
    send(text)


    if text == "quit":
        break

s.close()