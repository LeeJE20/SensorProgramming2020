import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led1 = 14
led2 = 15
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

p = GPIO.PWM(led1, 50) # create an object p for PWM on port 14 at 50 Hertz
p.start(0)
dc = 0

gpio = [ 5, 6, 16, 20, 21] # 5up, 6down, 16left, 20right, 21 center
stat = [ 0, 0, 0, 0, 0]

def print_jog_all():
    print("up : %d, down: %d, left: %d, right : %d, cen: %d" %(stat[0], stat[1], stat[2], stat[3], stat[4]))


try:
    for i in range(5):
        GPIO.setup(gpio[i], GPIO.IN)
    
    cur_stat = 0
    
    while True:
        for i in range(5): #현재 상태 출력
            cur_stat = GPIO.input(gpio[i])
            if cur_stat != stat[i]:
                stat[i] = cur_stat
                print_jog_all()
                
        if (stat[0] == 1): #up
            p.ChangeDutyCycle(100)
            time.sleep(1)
            p.ChangeDutyCycle(0)
        elif (stat[1] == 1): #down
            GPIO.output(led2, True)
            time.sleep(1)
            GPIO.output(led2, False)
        elif (stat[3] == 1): #right - fading
            
            for dc in range(0, 101, 5):
                p.ChangeDutyCycle(dc) # change the duty cycle to dc%
                time.sleep(0.05)
            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                time.sleep(0.05)            
            
        elif (stat[2] == 1): #left - blink
            GPIO.output(led2, True)
            time.sleep(0.3)
            GPIO.output(led2, False)
            time.sleep(0.3)
finally:
    print("Cleaning up")
    GPIO.cleanup()
    p.stop()
