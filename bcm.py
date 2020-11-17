import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


led_pin1 = 14
led_pin2 =15
GPIO.setup(led_pin1,GPIO.OUT)
GPIO.setup(led_pin2,GPIO.OUT)
p = GPIO.PWM(led_pin1, 50) # create an object p for PWM on port 14 at 50 Hertz
p.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc) # change the duty cycle to dc% 
            time.sleep(0.1)


        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
    p.stop()
    GPIO.cleanup() 