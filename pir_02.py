import RPi.GPIO as GPIO
import time

pir = 24
led_pin1 = 14
led_pin2 = 15

GPIO.setmode(GPIO.BCM)

GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)
GPIO.setup(pir, GPIO.IN)

gpio_pin = 13 # 피에조
GPIO.setup(gpio_pin, GPIO.OUT)
p = GPIO.PWM(gpio_pin, 100)
p.start(100) # start the PWM on 100% duty cycle

#음계
scale = [32.7032, 34.6478, 36.7081, 38.8909, 41.2034, 43.6535, 46.2493, 48.9994, 51.9130, 55.0000, 58.2705, 61.7354]
name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note = dict(zip(name, scale))

#옥타브
octav = 4
# 소리 내기 함수
# string 음이름 (C, C# 등), int 소리 낼 음의 옥타브
def sound(noteName, localOctav = octav):
    GPIO.output(led_pin2, True)
    # 한 옥타브가 올라가면 주파수는 2배가 된다.
    countedOctav = 2**(localOctav-1)
    p.ChangeDutyCycle(50)
    p.ChangeFrequency(note[noteName] * countedOctav)
    time.sleep(0.1)




def loop():
    cnt = 0
    while True:
        if (GPIO.input(pir) == True):
            cnt += 1
            GPIO.output(led_pin1, True)
            sound('C')
            sound('E')
            sound('G')
            sound('C', octav+1)
            GPIO.output(led_pin1, False)
            GPIO.output(led_pin2, False)
            time.sleep(0.3)
            p.ChangeDutyCycle(0)
            #time.sleep(0.5)

try:
    loop()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()