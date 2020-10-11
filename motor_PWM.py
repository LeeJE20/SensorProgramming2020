import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_RP = 4
GPIO_RN = 25
GPIO_EN = 12

GPIO.setup(GPIO_RP, GPIO.OUT)
GPIO.setup(GPIO_RN, GPIO.OUT)
GPIO.setup(GPIO_EN, GPIO.OUT)


p = GPIO.PWM(GPIO_RP, 50)
#n = GPIO.PWM(GPIO_RN, 50)

p.start(0)
#n.start(0)
cnt = 0



try:
    while True:
        p.ChangeDutyCycle(15)
        #GPIO.output(GPIO_PN, False)
        GPIO.output(GPIO_RN, False)
        GPIO.output(GPIO_EN, True)
        print("angle: 15")
        time.sleep(3)
        
        p.ChangeDutyCycle(60)
        GPIO.output(GPIO_RN, False)
        GPIO.output(GPIO_EN, True)
        print("angle: 60")
        time.sleep(3)
        
        p.ChangeDutyCycle(90)
        GPIO.output(GPIO_RN, False)
        GPIO.output(GPIO_EN, True)
        print("angle: 90")
        time.sleep(3)
        
        
        print("stop")
        GPIO.output(GPIO_EN, False)
        time.sleep(3)
        
except:
    p.stop()
finally:
    GPIO.cleanup()
