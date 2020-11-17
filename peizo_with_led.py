import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

gpio_pin = 13

scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]

wholeNote = 1.5
halfNote = wholeNote/2
quarterNote = wholeNote/4

stopTime = 0.04


led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

GPIO.output(led_pin1, False)
GPIO.output(led_pin2, False)






def sound(frequency, note):
    p.start(60)
    p.ChangeDutyCycle(50)
    p.ChangeFrequency(scale[frequency]-stopTime)

    GPIO.output(led_pin1, True)
    GPIO.output(led_pin2, True)
    time.sleep(note)
    
    GPIO.output(led_pin1, False)
    GPIO.output(led_pin2, False)
    p.stop()
    time.sleep(stopTime)
    
GPIO.setup(gpio_pin, GPIO.OUT)

p = GPIO.PWM(gpio_pin, 100)
try:
    #p = GPIO.PWM(gpio_pin, 100)
    #p.start(100) # start the PWM on 100% duty cycle
    #p.ChangeDutyCycle(90) # change the duty cycle to 90%
    while True:
        sound(4, quarterNote)
        sound(4, quarterNote)
        sound(5, quarterNote)
        sound(5, quarterNote)
        
        sound(4, quarterNote)
        sound(4, quarterNote)
        sound(2, halfNote)

        sound(4, quarterNote)
        sound(4, quarterNote)
        sound(2, quarterNote)
        sound(2, quarterNote)
        
        sound(1, wholeNote)
        
        
        sound(4, quarterNote)
        sound(4, quarterNote)
        sound(5, quarterNote)
        sound(5, quarterNote)
        
        sound(4, quarterNote)
        sound(4, quarterNote)
        sound(2, halfNote)

        sound(4, quarterNote)
        sound(2, quarterNote)
        sound(1, quarterNote)
        sound(2, quarterNote)
        
        sound(0, wholeNote)
#        p.ChangeFrequency(1)
 #       time.sleep(wholeNote)
        
 #       p.ChangeFrequency(0)
  #      time.sleep(0.01)
  #  p.stop() # stop the PWM output
finally:
    GPIO.cleanup()

