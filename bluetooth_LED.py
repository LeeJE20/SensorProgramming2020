from bluetooth import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

GPIO.output(led_pin1, False)
GPIO.output(led_pin2, False)

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

def send(msg):
    print(msg)
    msg = msg+"\n"
    client.send(msg.encode())    

def recv():
    byte_data = client.recv(1024)
    data = byte_data.decode().strip()
    print("recv: ", data, "(", len(data), ")")
    return data

try:
    while True:
        send("\noption:  on, off, fading, pwm, quit")
        byte_data = client.recv(1024)
        data = byte_data.decode().strip()
        print("recv: ", data, "(", len(data), ")")
        if data == "on":
            GPIO.output(led_pin1, True)
            GPIO.output(led_pin2, True)
        if "off" in data:
            GPIO.output(led_pin1, False)
            GPIO.output(led_pin2, False)
        if "fading" in data:
            sleepTime = 0.05

            p = GPIO.PWM(led_pin1, 50) # create an object p for PWM on port 14 at 50 Hertz
            p2 = GPIO.PWM(led_pin2, 50)

            p.start(0)
            p2.start(100)


            for dc in range(0, 101, 5):
                p.ChangeDutyCycle(dc) # change the duty cycle to dc%
                p2.ChangeDutyCycle(100-dc)
                time.sleep(sleepTime)


            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                p2.ChangeDutyCycle(100-dc)
                time.sleep(sleepTime)

            p.stop()
            p2.stop()
        if ("pwm" in data) or ("PWM" in data):
            msg = "waiting sleep time.."
            send(msg)

            data = recv()
            send("recv sleep time: %s" %data)
            
            send("PWM Dual Fading LED program is started..!!!")





            sleepTime = float(data)

            p = GPIO.PWM(led_pin1, 50) # create an object p for PWM on port 14 at 50 Hertz
            p2 = GPIO.PWM(led_pin2, 50)

            p.start(0)
            p2.start(100)


            for dc in range(0, 101, 5):
                p.ChangeDutyCycle(dc) # change the duty cycle to dc%
                p2.ChangeDutyCycle(100-dc)
                time.sleep(sleepTime)


            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                p2.ChangeDutyCycle(100-dc)
                time.sleep(sleepTime)

            p.stop()
            p2.stop()

            send("PWM end")
        if "quit" in data:
            print("good-bye")
            for i in range(0, 2):
                GPIO.output(led_pin1, False)
                GPIO.output(led_pin2, False)
                time.sleep(0.5)
                GPIO.output(led_pin1, True)
                GPIO.output(led_pin2, True)
                time.sleep(0.5)
            break
        client.send(data.encode())
except KeyboardInterrupt:
    print("terminate")


GPIO.cleanup()
client.close()
server.close()