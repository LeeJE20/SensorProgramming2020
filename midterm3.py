from bluetooth import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# led
led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

GPIO.output(led_pin1, False)
GPIO.output(led_pin2, False)


#  motor
GPIO_RP = 4
GPIO_RN = 25
GPIO_EN = 12

GPIO.setup(GPIO_RP, GPIO.OUT)
GPIO.setup(GPIO_RN, GPIO.OUT)
GPIO.setup(GPIO_EN, GPIO.OUT)




# Ultra sonic
#set GPIO Pins
GPIO_TRIGGER = 0
GPIO_ECHO = 1

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime= time.time()
    StopTime= time.time()

    #save StartTime
    while GPIO.input(GPIO_ECHO) == 1:
        StartTime= time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 0:
        StopTime= time.time()

    # time difference between start and arrival
    TimeElapsed= StopTime-StartTime

    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed* 34300) / 2
    return distance



# piezo
gpio_piezo = 13

scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]

wholeNote = 1.5
halfNote = wholeNote/2
quarterNote = wholeNote/4

stopTime = 0.04

GPIO.setup(gpio_piezo, GPIO.OUT)

p_peizo = GPIO.PWM(gpio_piezo, 100)
def sound(frequency, note):
    p_peizo.start(60)
    p_peizo.ChangeDutyCycle(50)
    p_peizo.ChangeFrequency(scale[frequency])

    GPIO.output(led_pin1, True)
    GPIO.output(led_pin2, True)
    time.sleep(note-stopTime)
    
    GPIO.output(led_pin1, False)
    GPIO.output(led_pin2, False)
    p_peizo.stop()
    time.sleep(stopTime)




# send string on both server and client
def send(msg):
    print(msg)
    msg = msg+"\n"
    client.send(msg.encode())    

# receive a message form the client
def recv():
    byte_data = client.recv(1024)
    data = byte_data.decode().strip()
    print("recv: ", data, "(", len(data), ")")
    return data


server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(1)
print("start server...")
try:
    client, info = server.accept()
    print("client mac:", info[0], ", port:", info[1])

    # user come
    send("hello")
    for i in range(0, 2):
        GPIO.output(led_pin1, True)
        GPIO.output(led_pin2, True)
        time.sleep(0.3)
        GPIO.output(led_pin1, False)
        GPIO.output(led_pin2, False)
        time.sleep(0.3)
except KeyboardInterrupt:
    print("abort")
    server.close()
    exit()





try:
    while True:
        send("\noption:  1, 2, 3, quit")
        byte_data = client.recv(1024)
        data = byte_data.decode().strip()
        print("recv: ", data, "(", len(data), ")")

        if data == "on":
            GPIO.output(led_pin1, True)
            GPIO.output(led_pin2, True)
        if "off" in data:
            GPIO.output(led_pin1, False)
            GPIO.output(led_pin2, False)
        if "2" in data:
            send("LED fading effect!")
            sleepTime = 0.05

            send("please input iteration: ")
            iter = int(recv())

            for i in range (0, iter):
                p = GPIO.PWM(led_pin1, 90) # create an object p for PWM on port 14 at 50 Hertz
                p2 = GPIO.PWM(led_pin2, 90)

                p.start(0)
                p2.start(90)


                for dc in range(0, 91, 5):
                    p.ChangeDutyCycle(dc) # change the duty cycle to dc%
                    p2.ChangeDutyCycle(90-dc)
                    time.sleep(sleepTime)


                for dc in range(90, -1, -5):
                    p.ChangeDutyCycle(dc)
                    p2.ChangeDutyCycle(90-dc)
                    time.sleep(sleepTime)

                p.stop()
                p2.stop()

        if "1"in data:
            send("DC motor is working!")
            send("please input iteration: ")
            iter = int(recv())


            for i in range (0, iter):
                p = GPIO.PWM(GPIO_RP, 50)
                p.start(0)
                p.ChangeDutyCycle(0)

                p2 = GPIO.PWM(GPIO_RN, 50)
                p2.start(0)
                p2.ChangeDutyCycle(0)

                p.ChangeDutyCycle(50)
                p2.ChangeDutyCycle(0)
                GPIO.output(GPIO_RP, True)
                GPIO.output(GPIO_RN, False)
                GPIO.output(GPIO_EN, True)
                time.sleep(4)
                # send("stop")
                GPIO.output(GPIO_EN, False)
                time.sleep(0.5)
                # send("backword")

                p.ChangeDutyCycle(0)
                p2.ChangeDutyCycle(50)
                GPIO.output(GPIO_RP, False)
                GPIO.output(GPIO_RN, True)
                GPIO.output(GPIO_EN, True)
                time.sleep(4)
                # send("stop")
                GPIO.output(GPIO_EN, False)
                time.sleep(0.5)      
                p.stop()
                p2.stop()

        if "3"in data:
            send("keep measuring distance until distance < 10")
            send("please input time:")
            iter = int(recv())
            iter = iter * 10000
            for i in range(0, iter):
                dist= distance()
                if dist < 10:
                    sound(4, quarterNote)
                    sound(4, quarterNote)
                    sound(2, halfNote)
                    send("Intruders!")
                else:
                    send("Now in safe!!")

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
        client.send(data.encode())
except KeyboardInterrupt:
    print("terminate")
except:
    print(E)

GPIO.cleanup()
client.close()
server.close()