import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

def Blink(numTimes, speed):
	for i in range(0, numTimes):
		print("iteration" + str(i+1))
		GPIO.output(led_pin1, True)
		time.sleep(speed)
		GPIO.output(led_pin1, False)
		time.sleep(speed)
		print("Done")
	GPIO.cleanup()

iterations = input("블링크 횟수 입력:")
speed = input("속도 입력:")


Blink(int(iterations), float(speed))
