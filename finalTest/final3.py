from flask import Flask, render_template
import datetime
import RPi.GPIO as GPIO
import threading
import time
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)

led_pins = [15, 14]
led_states = [0, 0]


# 피에조
gpio_pin = 13
GPIO.setup(gpio_pin, GPIO.OUT)

p = GPIO.PWM(gpio_pin, 100)



scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]

wholeNote = 1.5
halfNote = wholeNote/2
quarterNote = wholeNote/4
p.start(60)
p.ChangeDutyCycle(0)
stopTime = 0.05
def sound(frequency, note):
    
    p.ChangeDutyCycle(50)
    p.ChangeFrequency(scale[frequency])


    time.sleep(note-stopTime)
    p.ChangeDutyCycle(0)

    time.sleep(stopTime)
    
    



def music():
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


# 쓰레드 제어를 위한 객체
run_event = threading.Event()
run_event.set()
run_event.clear()

led_pwm_run_event = threading.Event()



@app.route("/")
def hello():
    # now = datetime.datetime.now()
    # timeString = now.strftime("%Y-%m-%d %H:%M")
    # templateData = {
    # 'title' : 'HELLO!',
    # 'time': timeString
    # }
    return render_template('final3.html')

@app.route("/led")
def led():
    return render_template('twoled.html')

def twoled():
    # while run_event.is_set():
    #     GPIO.output(led_pin1, False)
    #     GPIO.output(led_pin2, False)
    #     time.sleep(1)
    #     if run_event.is_set():
    #         GPIO.output(led_pin1, True)
    #         GPIO.output(led_pin2, True)
    #         time.sleep(1)
    while run_event.is_set():
        p_led1.ChangeDutyCycle(100)
        p_led2.ChangeDutyCycle(100)
        time.sleep(1)
        if run_event.is_set():
            p_led1.ChangeDutyCycle(0)
            p_led2.ChangeDutyCycle(0)
            time.sleep(1)

def pwmLed():
    while led_pwm_run_event.is_set():
        for dc in range(0, 101, 5):
            if led_pwm_run_event.is_set():
                p_led1.ChangeDutyCycle(dc) # change the duty cycle to dc%
                time.sleep(0.05)
            else: 
                break
        for dc in range(100, -1, -5):
            if led_pwm_run_event.is_set():
                p_led1.ChangeDutyCycle(dc)
                time.sleep(0.05)
            else: 
                break


def update_leds():
    for i, value in enumerate(led_states):
        GPIO.output(led_pins[i], value)

@app.route("/<pin>")
def ledPin(pin="n"):
    if pin == "0":
        led_num = int(pin)
        led_states[led_num] = not led_states[led_num]
        update_leds()
    if pin == "1":
        led_num = int(pin)
        led_states[led_num] = not led_states[led_num]
        update_leds()
    if pin == "2":
        t1 = threading.Thread(target=music)
        t1.start()




    return render_template('final3.html')
    




@app.route("/readPin/<pin>")
def readPin(pin):
    try:
        GPIO.setup(int(pin), GPIO.IN)
        if GPIO.input(int(pin)) == True:
            response = "Pin number " + pin + " is high!"
        else:
            response = "Pin number " + pin + " is low!"
    except:
        response = "There was an error reading pin " + pin + "."
    templateData = {
    'title' : 'Status of Pin' + pin,
    'response' : response
    }

    return render_template('pin.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)