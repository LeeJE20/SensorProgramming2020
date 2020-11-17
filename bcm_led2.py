import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


led_pin1 = 14
led_pin2 =15
GPIO.setup(led_pin1,GPIO.OUT)
GPIO.setup(led_pin2,GPIO.OUT)
p = GPIO.PWM(led_pin1, 50) # create an object p for PWM on port 14 at 50 Hertz
p2 = GPIO.PWM(led_pin2, 50)

print("PWM Dual Fading LED program is started..!!!")


p.start(0)
p2.start(100)
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc) # change the duty cycle to dc%
            p2.ChangeDutyCycle(100-dc)
            time.sleep(0.05)


        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(100-dc)
            time.sleep(0.05)
except KeyboardInterrupt:
    pass
    p.stop()
    p2.stop()
    GPIO.cleanup()
    print("PWM Dual Fading LED program is finished..!!!")