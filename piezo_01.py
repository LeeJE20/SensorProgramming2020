import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

gpio_pin = 13
scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]
GPIO.setup(gpio_pin, GPIO.OUT)
try:
    p = GPIO.PWM(gpio_pin, 100)
    p.start(100) # start the PWM on 100% duty cycle
    p.ChangeDutyCycle(90) # change the duty cycle to 90%
    for i in range(8):
        print (i+1)
        p.ChangeFrequency(scale[i])
        time.sleep(0.5)
    p.stop() # stop the PWM output
finally:
    GPIO.cleanup()