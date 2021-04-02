# degital thermometer
import smbus2 as smbus
import time
import threading

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

def fnd_disp():
    #Output temp into 7-segment
    while (ns_new == ""):
        time.sleep(0.01)
        bus.write_word_data(addr_fnd, config_port, 0x0000)
        while True:
            try:
                if (ns_new != ""):
                    for i in range(0,4,1):
                        # notation of dot(.)
                        out_disp = data_fnd[10] << 8 | digit[1]
                        bus.write_word_data(addr_fnd, out_port, out_disp )
                        print(ns_new[i])
                        n = int(ns_new[i])
                        #print("%2d " %n)
                        out_disp = data_fnd[n] << 8 | digit[i]
                        bus.write_word_data(addr_fnd, out_port, out_disp )
                        time.sleep(0.001)
                    if (stop == 1):
                        print("\nExit fnd_disp thread")
                        break
            except:
                pass


def temp_humi_read():
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
    return ns[0:2]+ns[3:5]


try: # 실제 실행 부분
    th = threading.Thread(target=fnd_disp)
    th.start()
    while True:
        ns_new = temp_humi_read()
        time.sleep(0.05)
except KeyboardInterrupt:
    stop = 1
# pass