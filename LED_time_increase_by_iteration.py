import RPi.GPIO as GPIO
import time
led_pin1 = 14
led_pin2 = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin1, GPIO.OUT) #GPIO 14 ouput

def blink(Num):
    for i in range(1, Num):
        GPIO.output(led_pin1, GPIO.HIGH) ## on 14
        time.sleep(i/2)
        GPIO.output(led_pin1,  GPIO.LOW) ## off 14
        time.sleep(1)
        
In = int(input("Give times you want: "))
blink(In)
print("Program is finished..!!")
GPIO.cleanup()