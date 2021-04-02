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

pinStatus = {'14':0, '15':0}

p_led1 = GPIO.PWM(led_pin1, 50) # create an object p for PWM on port 14 at 50 Hertz
p_led2 = GPIO.PWM(led_pin2, 50)
p_led1.start(0)
p_led2.start(0)
p_led1.ChangeDutyCycle(0)
p_led2.ChangeDutyCycle(0)



# 쓰레드 제어를 위한 객체
run_event = threading.Event()
run_event.set()
run_event.clear()

led_pwm_run_event = threading.Event()



@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
    'title' : 'HELLO!',
    'time': timeString
    }
    return render_template('main.html', **templateData)

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

@app.route("/led/<pin>")
def ledPin(pin="n"):
    if pin == "16":
        print("16pin")
        if (run_event.is_set()):
            run_event.clear()
        else:
            run_event.set()
            # t1 = threading.Thread(target=twoled, args = [run_event])
            t1 = threading.Thread(target=twoled)
            t1.start()
    if pin == "14":
        print("hello14")
        pinStatus['14'] = not pinStatus['14']
        print(pinStatus['14'])
        if pinStatus['14']:
            led_pwm_run_event.set()
            t1 = threading.Thread(target=pwmLed)
            t1.start()
        else:
            led_pwm_run_event.clear()


    return render_template('twoled.html')
    




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