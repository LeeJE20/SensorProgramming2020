# 화재경보기

import RPi.GPIO as GPIO
import smbus2 as smbus
import time
import threading


# bcm 모드 세팅
GPIO.setmode(GPIO.BCM)


# 온습도 세팅
bus = smbus.SMBus(1)
addr = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe
temp = 0.0
humi = 0.0
val = 0
data = [0, 0]

# led 세팅
# led 세팅
led_pin1 = 14
led_pin2 =15
GPIO.setup(led_pin1,GPIO.OUT)
GPIO.setup(led_pin2,GPIO.OUT)
p = GPIO.PWM(led_pin1, 50) 
p2 = GPIO.PWM(led_pin2, 50)

p.start(0)
p2.start(0)


def lightAlarm():
    for dc in range(0, 101, 5):
        p.ChangeDutyCycle(dc) # change the duty cycle to dc%
        p2.ChangeDutyCycle(100-dc)
        time.sleep(0.03)


    for dc in range(100, -1, -5):
        p.ChangeDutyCycle(dc)
        p2.ChangeDutyCycle(100-dc)
        time.sleep(0.03)


try:
    bus.write_byte (addr, soft_reset)
    time.sleep(0.05)
    while True:
        # temperature
        bus.write_byte(addr, cmd_temp)
        time.sleep(0.260)
        for i in range(0,2,1):
            data[i] = bus.read_byte(addr)
            val = data[0] << 8 | data[1]
            temp = -46.85+175.72/65536*val
    
    
        # humidity
        bus.write_byte(addr, cmd_humi)
        time.sleep(0.260)
        for i in range(0,2,1):
            data[i] = bus.read_byte(addr)
        val = data[0] << 8 | data[1]
        humi = -6.0+125.0/65536*val 
        print ('temp : %.2f, humi : %.2f' %(temp, humi))
        time.sleep(1)

        # 화재 발생
        if (temp > 29):
            t = threading.Thread(target=lightAlarm)
            t.start() # 쓰레드 동작 시작
        else:
            dc = 0
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
except KeyboardInterrupt:
    pass
