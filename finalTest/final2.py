from flask import Flask, render_template
import RPi.GPIO as GPIO
app = Flask(__name__)

import smbus2 as smbus
import time
import threading
import datetime
GPIO.setmode(GPIO.BCM)

led_pin1 = 14
led_pin2 = 15
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)





#TEmp/Humi configuration
bus = smbus.SMBus(1)
addr_temp = 0x40
cmd_temp = 0xf3
cmd_humi = 0xf5
soft_reset = 0xfe

# FND configuration
addr_fnd = 0x20
config_port = 0x06
out_port = 0x02
data_fnd = (0xFC,0x60,0xDA,0xF2,0x66,0xB6,0x3E,0xE0,0xFE,0xF6,0x01)
digit = (0x7F,0xBF,0xDF,0xEF,0xF7,0xFB)
out_disp = 0
ns_new = ""
stop = 0

globalTemp = 0


# 쓰레드 제어를 위한 객체
run_event = threading.Event()
run_event.set()
run_event.clear()


def fnd_disp():
    #Output temp into 7-segment

    while run_event.is_set():
            try:
                if (ns_new != ""):
                    for i in range(0,4,1):
                        # notation of dot(.)
                        out_disp = data_fnd[10] << 8 | digit[1]
                        bus.write_word_data(addr_fnd, out_port, out_disp )
                        time.sleep(0.01)
                        n = int(ns_new[i])
                        #print("%2d " %n)
                        out_disp = data_fnd[n] << 8 | digit[i]
                        bus.write_word_data(addr_fnd, out_port, out_disp )
                        time.sleep(0.01)
                    if (stop == 1):
                        print("\nExit fnd_disp thread")
                        break
            except:
                pass


def temp_humi_read():
    # while run_event.is_set():
    #     try:
    #         temp = 0.0
    #         humi = 0.0
    #         val = 0
    #         data = [0, 0]
    #         bus.write_byte (addr_temp, soft_reset)
    #         time.sleep(0.05)
    #         # temperature
    #         bus.write_byte(addr_temp, cmd_temp)
    #         time.sleep(0.260)
    #         for i in range(0,2,1):
    #             data[i] = bus.read_byte(addr_temp)
    #         val = data[0] << 8 | data[1]
    #         temp = -46.85+175.72/65536*val

    #         for i in range(0,2,1):
    #             data[i] = bus.read_byte(addr_temp)
    #         val = data[0] << 8 | data[1]
    #         humi = -6.0+125.0/65536*val
    #         #print 'temp : %.2f, humi : %.2f' %(temp, humi)
    #         ns = str(temp)
    #         #print("%s : %s " %(ns[0:2],ns[3:5])) # 0~2: integer, 3~5: fractional part
    #         ns_new = ns[0:2]+ns[3:5] 
    #         print("%s " %ns_new)

    #         globalTemp = temp
    #         time.sleep(0.03)
    #         # return ns_new
    #     except:
    #         time.sleep(0.03)

    temp = 0.0
    humi = 0.0
    val = 0
    data = [0, 0]
    bus.write_byte (addr_temp, soft_reset)
    time.sleep(0.05)
    # temperature
    bus.write_byte(addr_temp, cmd_temp)
    time.sleep(0.260)
    for i in range(0,2,1):
        data[i] = bus.read_byte(addr_temp)
    val = data[0] << 8 | data[1]
    temp = -46.85+175.72/65536*val

    for i in range(0,2,1):
        data[i] = bus.read_byte(addr_temp)
    val = data[0] << 8 | data[1]
    humi = -6.0+125.0/65536*val
    #print 'temp : %.2f, humi : %.2f' %(temp, humi)
    ns = str(temp)
    #print("%s : %s " %(ns[0:2],ns[3:5])) # 0~2: integer, 3~5: fractional part
    ns_new = ns[0:2]+ns[3:5] 
    print("%s " %ns_new)

    globalTemp = temp
    return temp

            




# try: # 실제 실행 부분
#     th = threading.Thread(target=fnd_disp)
#     th.start()
#     while True:
#         ns_new = temp_humi_read()
#         time.sleep(0.05)
# except KeyboardInterrupt:
#     stop = 1
# pass



def led():
    for i in range(0, 5):

        GPIO.output(led_pin1, True)
        GPIO.output(led_pin2, True)
        time.sleep(0.5)
        GPIO.output(led_pin1, False)
        GPIO.output(led_pin2, False)
        time.sleep(0.5)



@app.route('/')
def index():

    run_event.clear()
    run_event.set()


    now = datetime.datetime.now()

    # th = threading.Thread(target=temp_humi_read)
    # th.start()

    # th1 = threading.Thread(target=temp_humi_read)
    # th1.start()

    # print(ns_new)
    # temp_float = float(ns_new)
    # print(temp_float)

    mytemp = temp_humi_read()

    globalTempStr = str(globalTemp)
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
    'title' : 'HELLO!',
    'datetime' : timeString,
    'temp' : mytemp
    }

    if mytemp > 32:
        led()


    return render_template('final2.html', **templateData)


@app.route("/<pin>")
def readPin(pin):

    run_event.clear()
    run_event.set()


    now = datetime.datetime.now()

    # th = threading.Thread(target=temp_humi_read)
    # th.start()

    # th1 = threading.Thread(target=temp_humi_read)
    # th1.start()

    # print(ns_new)
    # temp_float = float(ns_new)
    # print(temp_float)

    mytemp = temp_humi_read()

    globalTempStr = str(globalTemp)
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
    'title' : 'HELLO!',
    'datetime' : timeString,
    'temp' : mytemp
    }

    if mytemp > 32:
        led()




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

    return render_template('final2.html', **templateData)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)