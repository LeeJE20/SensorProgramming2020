import smbus2 as smbus
import RPi.GPIO as GPIO
import time


# light sensor setting 
bus = smbus.SMBus(1)
addr = 0x23
reset = 0x07
con_hr_mode = 0x10
data1 = 0
data2 = 0
val = 0
light_val = 0


# bcm 모드 세팅
GPIO.setmode(GPIO.BCM)

# led 세팅
led_pin1 = 14
led_pin2 =15
GPIO.setup(led_pin1,GPIO.OUT)
GPIO.setup(led_pin2,GPIO.OUT)
p = GPIO.PWM(led_pin1, 50) 
p2 = GPIO.PWM(led_pin2, 50)

p.start(100)
p2.start(100)

try:
    bus.write_byte(addr, reset)
    time.sleep(0.05)
    bus.write_byte(addr, con_hr_mode)
    time.sleep(0.2)
    while True:
        #bus.write_byte(addr, con_hr_mode)
        #time.sleep(0.2)
        data1 = bus.read_byte(addr)
        data2 = bus.read_byte(addr)
        val = (data1 << 8) | data2
        light_val = val / 1.2
        print ('light_val = %.2f' % light_val)
        time.sleep(1)

        if (light_val  < 300):
            dc = 100
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
        elif (light_val  < 500):
            dc = 90
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
        elif (light_val  < 1000):
            dc = 80
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)    
        elif (light_val  < 1500):
            dc = 70
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
        elif (light_val  < 2000):
            dc = 50
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
        elif (light_val  < 3000):
            dc = 30
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
        elif (light_val  < 4000):
            dc = 10
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)
        else:
            dc = 0
            p.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(dc)

except KeyboardInterrupt:
    # do not anything
    pass
finally:
    pass