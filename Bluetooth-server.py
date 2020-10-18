from bluetooth import *
server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(1)
print("start server...")
try:
    client, info = server.accept()
    print("client mac:", info[0], ", port:", info[1])
except KeyboardInterrupt:
    print("abort")
    server.close()
    exit()


try:
    while True:
        byte_data = client.recv(1024)
        data = byte_data.decode().strip()
        print("recv: ", data, "(", len(data), ")")
        if "quit" in data:
            print("good-bye")
            break
        client.send(data.encode())
except KeyboardInterrupt:
    print("terminate")
client.close()
server.close()